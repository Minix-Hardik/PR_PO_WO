from frappe.desk.form.linked_with import get_linked_docs
from frappe import _
import frappe
import re

@frappe.whitelist()
def bulk_inward_to_outward(docnames,extra_data=None):
    docnames = frappe.parse_json(docnames)
    extra_data = frappe.parse_json(extra_data)
    for docname in docnames:
        doc = frappe.get_doc("Inward Document", docname)
        frappe.new_doc("Outward Documents").update({
            "inward": doc.name,
            "doc_no": extra_data.doc_name,
            "url": extra_data.postal_url,
            "date": extra_data.date,
        }).insert()
    return "ok"

def outward_documents_permission(user):
    if not user:
        user = frappe.session.user
    if user == "Administrator":
        return ""
    employee_branch = frappe.db.get_value("Employee", {"user_id": user}, "branch")
    if not employee_branch:
        return "1 = 0"
    return f"(`tabOutward Documents`.`maa_branch` = '{employee_branch}')"

def inward_documents_permission(user):
    if not user:
        user = frappe.session.user
    if user == "Administrator":
        return ""
    employee_branch = frappe.db.get_value("Employee", {"user_id": user}, "branch")
    if not employee_branch:
        return "1 = 0"
    return f"(`tabInward Document`.`maa_branch` = '{employee_branch}')"

def get_user_ma_prefix_and_branch(user=None):
    """
    Helper function to safely fetch Employee code prefix and branch for a user.
    """
    if not user:
        user = frappe.session.user

    if user == "Administrator":
        return {"employee_name": None, "prefix": "ADMIN", "branch": "Administrator"}

    user_employee = frappe.db.get_value(
        "Employee",
        {"user_id": user, "status": "Active"},
        ["name", "custom_ma_code_prefix", "branch"],
        as_dict=True
    )

    if not user_employee:
        frappe.throw(
            _("No active Employee profile linked to user {0}.").format(user)
        )

    prefix = user_employee.get("custom_ma_code_prefix") or ""
    branch = user_employee.get("branch") or ""

    if not prefix and not branch:
        frappe.throw(
            _("Neither MA Code Prefix nor Branch is configured for employee {0}.").format(user_employee.name)
        )

    return {
        "employee_name": user_employee.name,
        "prefix": prefix,
        "branch": branch
    }


def get_transit_permission_conditions(user):
    """
    Hook to restrict Transit record visibility based on user's branch or prefix.
    """
    if not user:
        user = frappe.session.user

    if user == "Administrator" or "System Manager" in frappe.get_roles(user):
        return ""

    user_employee = frappe.db.get_value(
        "Employee",
        {"user_id": user, "status": "Active"},
        ["custom_ma_code_prefix", "branch"],
        as_dict=True
    )

    if not user_employee:
        return "1=0"

    allowed_values = set()
    if user_employee.get("branch"):
        allowed_values.add(user_employee.branch)
    if user_employee.get("custom_ma_code_prefix"):
        allowed_values.add(user_employee.custom_ma_code_prefix)

    if not allowed_values:
        return "1=0"

    # Properly escape and construct conditions to prevent SQL injection
    escaped_values = ", ".join(frappe.db.escape(v) for v in allowed_values)

    return f"(`tabInward Outward Transit`.`receiver_branch` IN ({escaped_values}) OR `tabInward Outward Transit`.`sender_branch` IN ({escaped_values}))"


@frappe.whitelist()
def create_transit_records(docs, target_branch):
    """
    Creates Transit records for selected Outward Documents.
    """
    if isinstance(docs, str):
        docs = frappe.parse_json(docs)

    if not docs:
        frappe.throw(_("No documents provided for transit creation."))

    emp_info = get_user_ma_prefix_and_branch()
    sender_branch = emp_info.get("branch") or emp_info.get("prefix")

    created_transit_records = []

    for doc_name in docs:
        outward_doc = frappe.get_doc("Outward Documents", doc_name)

        # Check if already in transit
        existing_transit = frappe.db.exists(
            "Inward Outward Transit",
            {
                "outward_reference": outward_doc.name,
                "status": "In Transit"
            }
        )
        if existing_transit:
            frappe.msgprint(_("Outward document {0} is already in transit. Skipping.").format(outward_doc.name))
            continue

        # Create Transit Document
        transit_doc = frappe.get_doc({
            "doctype": "Inward Outward Transit",
            "outward_reference": outward_doc.name,
            "sender_branch": sender_branch or getattr(outward_doc, "maa_branch", ""),
            "receiver_branch": target_branch,
            "status": "In Transit"
        })
        transit_doc.insert(ignore_permissions=True)
        
        # Update original Outward Document status if field exists
        if hasattr(outward_doc, "status"):
            frappe.db.set_value("Outward Documents", outward_doc.name, "status", "In Transit")

        created_transit_records.append(transit_doc.name)

    return created_transit_records


import frappe

@frappe.whitelist()
def receive_transit_to_inward(transit_names):
    """
    Converts 'Inward Outward Transit' records into 'Inward Document' records.
    """
    if isinstance(transit_names, str):
        transit_names = frappe.parse_json(transit_names) if transit_names.startswith("[") else [transit_names]

    if not transit_names:
        frappe.throw(_("No transit records provided to receive."))

    emp_info = get_user_ma_prefix_and_branch()
    created_inwards = []

    for name in transit_names:
        transit_doc = frappe.get_doc("Inward Outward Transit", name)

        if transit_doc.status == "Received":
            frappe.msgprint(_("Transit record {0} is already received. Skipping.").format(name))
            continue

        if not transit_doc.outward_reference:
            frappe.throw(_("Transit record {0} has no linked Outward Document.").format(name))

        outward = frappe.get_doc("Outward Documents", transit_doc.outward_reference)

        # Create Inward Document
        inward_doc = frappe.get_doc({
            "doctype": "Inward Document",
            "received_date": frappe.utils.today(),
            "date": frappe.utils.today(),
            "subject": outward.subject,
            "project": getattr(outward, "project", ""),
            "medium": getattr(outward, "medium", getattr(outward, "meduium", "Courier")),
            "place": getattr(outward, "place", ""),
            "district": getattr(outward, "district", ""),
            "taluka": getattr(outward, "taluka", ""),
            "state": getattr(outward, "state", ""),
            "pincode": getattr(outward, "pincode", ""),
            "sender": outward.to,
            "application_status": "Pending",
            "entry_by": frappe.session.user,
            "maa_branch": emp_info.get("branch") or getattr(outward, "maa_branch", ""),
            "concern_person": emp_info.get("employee_name") or "",
            "remarks": getattr(outward, "remarks", "")
        })
        inward_doc.insert(ignore_permissions=True)

        # Update Transit Record
        transit_doc.inward_reference = inward_doc.name
        transit_doc.status = "Received"
        transit_doc.save(ignore_permissions=True)

        if transit_doc.docstatus == 0:
            transit_doc.submit()

        created_inwards.append(inward_doc.name)

    return created_inwards

@frappe.whitelist()
def force_bulk_delete_pos(po_names):
    if isinstance(po_names, str):
        po_names = frappe.parse_json(po_names)

    deleted = []
    failed = []

    for name in po_names:
        # Sanitize savepoint name to alphanumeric and underscores only
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        savepoint_identifier = f"sp_{safe_name}"

        # Create savepoint safely
        frappe.db.savepoint(savepoint_identifier)
        
        try:
            if not frappe.db.exists("Purchase Order", name):
                continue

            # 1. Clear self-referential amendment links
            frappe.db.sql("""
                UPDATE `tabPurchase Order` 
                SET amended_from = NULL 
                WHERE name = %s OR amended_from = %s
            """, (name, name))

            # 2. Delete linked documents recursively
            delete_all_linked_documents("Purchase Order", name)

            # 3. Cancel and delete original PO
            doc = frappe.get_doc("Purchase Order", name)
            if doc.docstatus == 1:
                doc.cancel()

            frappe.delete_doc("Purchase Order", name, force=True)
            deleted.append(name)

        except Exception as e:
            # Pass the matching sanitized savepoint name on rollback
            frappe.db.rollback(save_point=savepoint_identifier)
            failed.append({"name": name, "error": str(e)})

    frappe.db.commit()
    return {"deleted": deleted, "failed": failed}


def delete_all_linked_documents(doctype, docname):
    linked_docs = get_linked_docs(doctype, docname)

    for linked_dt, records in linked_docs.items():
        if linked_dt == doctype:
            continue

        for rec in records:
            rec_name = rec.get("name")
            if not rec_name or not frappe.db.exists(linked_dt, rec_name):
                continue

            try:
                # Clear amended_from link on child documents if present
                if frappe.get_meta(linked_dt).has_field("amended_from"):
                    frappe.db.sql(f"""
                        UPDATE `tab{linked_dt}` 
                        SET amended_from = NULL 
                        WHERE name = %s OR amended_from = %s
                    """, (rec_name, rec_name))

                # Recursively delete deeper dependencies
                delete_all_linked_documents(linked_dt, rec_name)

                linked_doc = frappe.get_doc(linked_dt, rec_name)
                if linked_doc.docstatus == 1:
                    linked_doc.cancel()

                frappe.delete_doc(linked_dt, rec_name, force=True)

            except Exception as e:
                frappe.log_error(
                    title=f"Failed cascading delete for {linked_dt} {rec_name}",
                    message=frappe.get_traceback()
                )
                raise e


@frappe.whitelist()
def force_bulk_delete_sqs(sq_names):
    if isinstance(sq_names, str):
        sq_names = frappe.parse_json(sq_names)

    deleted = []
    failed = []

    for name in sq_names:
        # Sanitize savepoint name to alphanumeric and underscores only
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        savepoint_identifier = f"sp_{safe_name}"

        # Create savepoint safely
        frappe.db.savepoint(savepoint_identifier)
        
        try:
            if not frappe.db.exists("Supplier Quotation", name):
                continue

            # 1. Clear self-referential amendment links
            frappe.db.sql("""
                UPDATE `tabSupplier Quotation` 
                SET amended_from = NULL 
                WHERE name = %s OR amended_from = %s
            """, (name, name))

            # 2. Delete linked documents recursively
            delete_all_linked_documents("Supplier Quotation", name)

            # 3. Cancel and delete original Supplier Quotation
            doc = frappe.get_doc("Supplier Quotation", name)
            if doc.docstatus == 1:
                doc.cancel()

            frappe.delete_doc("Supplier Quotation", name, force=True)
            deleted.append(name)

        except Exception as e:
            # Pass the matching sanitized savepoint name on rollback
            frappe.db.rollback(save_point=savepoint_identifier)
            failed.append({"name": name, "error": str(e)})

    frappe.db.commit()
    return {"deleted": deleted, "failed": failed}

@frappe.whitelist()
def update_shift_locations(parent_doc, locations):
    if isinstance(locations, str):
        locations = frappe.parse_json(locations)

    doc = frappe.get_doc("Shift Assignment", parent_doc)

    # Clear existing child records in memory
    doc.set("custom_multiple_shift_location", [])

    # Re-build child table entries from dialog payload
    for idx, loc in enumerate(locations, start=1):
        doc.append("custom_multiple_shift_location", {
            "doctype": "Multiple Shift Locations",
            "location": loc.get("location"),
            "is_active": loc.get("is_active", 0),
            "docstatus": 1,
            "idx": idx
        })

    # Force save on submitted document
    doc.flags.ignore_validate_update_after_submit = True
    doc.flags.ignore_permissions = True
    doc.save(ignore_permissions=True)

    frappe.db.commit()
    return True