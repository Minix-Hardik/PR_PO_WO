app_name = "po_wo_pr"
app_title = "Po Wo Pr"
app_publisher = "Hybrowlabs"
app_description = "none"
app_email = "hybrowlabs@mail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "po_wo_pr",
# 		"logo": "/assets/po_wo_pr/logo.png",
# 		"title": "Po Wo Pr",
# 		"route": "/po_wo_pr",
# 		"has_permission": "po_wo_pr.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/po_wo_pr/css/po_wo_pr.css"
# app_include_js = "/assets/po_wo_pr/js/attendance_calendar_custom.js"

# include js, css files in header of web template
# web_include_css = "/assets/po_wo_pr/css/po_wo_pr.css"
# web_include_js = "/assets/po_wo_pr/js/po_wo_pr.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "po_wo_pr/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

permission_query_conditions = { 
    "Outward Documents": "po_wo_pr.irs.api.outward_documents_permission",
    "Inward Documents": ["po_wo_pr.irs.api.inward_documents_permission", "po_wo_pr.irs.doctype.inward_document.inward_document.get_permission_query_conditions"],
    "Inward Outward Transit": "po_wo_pr.irs.api.get_transit_permission_conditions",
}

doctype_list_js = {
    "Inward Document": "public/js/inward_list.js",
    "Attendance": "public/js/attendance_list.js",
    "Purchase Order": "public/js/purchase_order_list.js",
    "Supplier Quotation": "public/js/supplier_quotation_list.js",
    "Outward Documents": "public/js/outward_list.js",
    "Inward Outward Transit": "public/js/inward_outward_transit_list.js"
}

# include js in doctype views
doctype_js = {
    "Purchase Order" : ["public/js/purchase_order.js", "public/js/enquiry_ref.js"],
    "Item" : "public/js/item_master.js",
    "Request for Quotation": ["public/js/request_quotation.js", "public/js/enquiry_ref.js"],
    "Employee": "public/js/employee.js",
    "Cost Center":"public/js/cost_center.js",
    "Shift Assignment":"public/js/shift_assignment.js",
    "Material Request":"public/js/material_request.js",
    "Attendance": "public/js/attendance.js",
    "Employee Checkin": "public/js/employee_checkin.js",
    "Supplier Quotation": ["public/js/supplier_quotation.js", "public/js/enquiry_ref.js"],
    "Purchase Receipt": ["public/js/purchase_receipt.js", "public/js/enquiry_ref.js"],
    "Purchase Invoice": ["public/js/purchase_invoice.js", "public/js/enquiry_ref.js"],
    "Payment Entry": "public/js/payment_entry.js",
    "Leave Application": "public/js/leave_application.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"Attendance" : "public/js/attendance_calendar_custom.js"}

naming_series_variables = {
	"MFY": "po_wo_pr.api.setup.parse_short_fiscal_year",
}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "po_wo_pr/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "po_wo_pr.utils.jinja_methods",
# 	"filters": "po_wo_pr.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "po_wo_pr.install.before_install"
# after_install = "po_wo_pr.install.after_install"
after_migrate = "po_wo_pr.api.setup.set_buying_naming_series"

# Uninstallation
# ------------

# before_uninstall = "po_wo_pr.uninstall.before_uninstall"
# after_uninstall = "po_wo_pr.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "po_wo_pr.utils.before_app_install"
# after_app_install = "po_wo_pr.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "po_wo_pr.utils.before_app_uninstall"
# after_app_uninstall = "po_wo_pr.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "po_wo_pr.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Employee": "po_wo_pr.overrides.custom_employee_class.CustomEmployee",
	"Request for Quotation": "po_wo_pr.overrides.request_for_quotation.CustomRequestforQuotation",
     "Leave Application": "po_wo_pr.overrides.leave_application.CustomLeaveApplication"
}

# Document Events
# ---------------
# Document Events
# ---------------

doc_events = {
	"Request for Quotation": {
		"before_print": "po_wo_pr.api.request_for_quotation_data.set_supplier_for_print"
	},
	"Loan": {
		"on_submit": "po_wo_pr.api.setup.update_employee_loan_balance",
		"on_cancel": "po_wo_pr.api.setup.update_employee_loan_balance",
		"on_update_after_submit": "po_wo_pr.api.setup.update_employee_loan_balance"
	},
	"Loan Repayment": {
		"on_submit": "po_wo_pr.api.setup.update_employee_loan_balance",
		"on_cancel": "po_wo_pr.api.setup.update_employee_loan_balance"
	},
	"Attendance": {
		"validate": [
			"po_wo_pr.api.attendance_utils.update_custom_work_hours",
			"po_wo_pr.api.attendance_utils.update_attendance_exact_times"
		]
	},
	"Attendance Request": {
		"on_submit": "po_wo_pr.api.attendance_utils.apply_attendance_request_times",
		"on_update_after_submit": "po_wo_pr.api.attendance_utils.apply_attendance_request_times"
	},
	"Employee Checkin": {
		"before_save": "po_wo_pr.api.attendance_utils.update_custom_exact_time"
	},
	"Purchase Receipt": {
		"after_insert": "po_wo_pr.api.setup.set_purchase_receipt_po_fields",
		"on_submit": "po_wo_pr.api.setup.update_po_received_qty",
		"on_cancel": "po_wo_pr.api.setup.update_po_received_qty",
		"validate": "po_wo_pr.overrides.enquiry_ref.set_ref_enquiry_no"
	},
	"Purchase Order": {
		"autoname": "po_wo_pr.api.setup.set_purchase_order_name",
		"validate": [
			"po_wo_pr.overrides.enquiry_ref.set_ref_enquiry_no",
			"po_wo_pr.overrides.branch_approval.set_default_branch",
			"po_wo_pr.overrides.branch_approval.require_branch_before_approval",
			"po_wo_pr.overrides.branch_approval.guard_branch_approval"
		],
		"on_submit": "po_wo_pr.overrides.branch_approval.sync_approval_assignment",
		"on_update_after_submit": "po_wo_pr.overrides.branch_approval.sync_approval_assignment",
		"on_cancel": "po_wo_pr.overrides.branch_approval.sync_approval_assignment",
        "on_update": "po_wo_pr.overrides.purchase_order.create_mrn_on_po_approval"
	},
	"Supplier Quotation": {
		"validate": [
			"po_wo_pr.overrides.enquiry_ref.set_ref_enquiry_no",
			"po_wo_pr.overrides.branch_approval.set_default_branch",
			"po_wo_pr.overrides.branch_approval.require_branch_before_approval",
			"po_wo_pr.overrides.branch_approval.guard_branch_approval"
		],
		"on_submit": "po_wo_pr.overrides.branch_approval.sync_approval_assignment",
		"on_update_after_submit": "po_wo_pr.overrides.branch_approval.sync_approval_assignment",
		"on_cancel": "po_wo_pr.overrides.branch_approval.sync_approval_assignment"
	},
	"Purchase Invoice": {
		"validate": "po_wo_pr.overrides.enquiry_ref.set_ref_enquiry_no"
	},
	"Request for Quotation": {
		"validate": "po_wo_pr.overrides.enquiry_ref.set_ref_enquiry_no"
	}
}

# Scheduled Tasks
# ---------------
# scheduler_events = {
#     "cron": {
#         "* * * * *": [
#             "po_wo_pr.api.get_biomatric_data_every_minute.import_today_biometric_data"
#         ]
#     }
# }


# scheduler_events = {
# 	"all": [
# 		"po_wo_pr.tasks.all"
# 	],
# 	"daily": [
# 		"po_wo_pr.tasks.daily"
# 	],
# 	"hourly": [
# 		"po_wo_pr.tasks.hourly"
# 	],
# 	"weekly": [
# 		"po_wo_pr.tasks.weekly"
# 	],
# 	"monthly": [
# 		"po_wo_pr.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "po_wo_pr.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"erpnext.buying.doctype.request_for_quotation.request_for_quotation.send_supplier_emails": "po_wo_pr.api.request_for_quotation_email.send_supplier_emails",
	"erpnext.buying.doctype.request_for_quotation.request_for_quotation.get_pdf": "po_wo_pr.api.request_for_quotation_data.get_pdf",
	"erpnext.buying.doctype.request_for_quotation.request_for_quotation.make_supplier_quotation_from_rfq": "po_wo_pr.overrides.request_for_quotation_mapper.make_supplier_quotation_from_rfq",
	"erpnext.stock.doctype.material_request.material_request.make_purchase_order": "po_wo_pr.overrides.material_request.make_purchase_order",
	"erpnext.stock.doctype.material_request.material_request.make_request_for_quotation": "po_wo_pr.overrides.material_request.make_request_for_quotation",
	"erpnext.buying.doctype.supplier_quotation.supplier_quotation.make_purchase_order": "po_wo_pr.overrides.purchase_order.make_purchase_order_from_supplier_quotation",
	"erpnext.buying.doctype.supplier_quotation.supplier_quotation.make_purchase_invoice": "po_wo_pr.overrides.purchase_order.make_purchase_invoice_from_supplier_quotation",
	"erpnext.buying.doctype.purchase_order.purchase_order.make_purchase_receipt": "po_wo_pr.overrides.purchase_order.make_purchase_receipt",
	"erpnext.buying.doctype.purchase_order.purchase_order.make_purchase_invoice": "po_wo_pr.overrides.purchase_order.make_purchase_invoice",
	"erpnext.stock.doctype.purchase_receipt.purchase_receipt.make_purchase_invoice": "po_wo_pr.overrides.purchase_order.make_purchase_invoice_from_receipt",
	"hrms.hr.doctype.leave_application.leave_application.get_leave_details": "po_wo_pr.overrides.leave_application.get_leave_details",
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "po_wo_pr.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["po_wo_pr.utils.before_request"]
# after_request = ["po_wo_pr.utils.after_request"]

# Job Events
# ----------
# before_job = ["po_wo_pr.utils.before_job"]
# after_job = ["po_wo_pr.utils.after_job"]

# User Data Protection
# --------------------
fixtures = [
    {
        "doctype": "Property Setter",
        "filters": {
            "name":["in",[
                # "Employee-custom_shift_issuer-hidden",
            # "Employee-shift_request_approver-hidden","Employee-custom_attendance_exception-hidden",
            # "Employee-custom_allow_mobile_checkin-hidden","Employee-department-hidden","Item-item_code-hidden","Employee-main-field_order",
            # "Employee-micr_code-hidden","Employee-iban-hidden","Employee-ctc-hidden","Employee-custom_esic_number-hidden","Employee Education-main-field_order",
            # "Employee External Work History-main-field_order","Employee-custom_educational_details-hidden","Employee-lft-hidden","Employee-rgt-hidden",
            # "Employee-old_parent-hidden","Employee Internal Work History-department-hidden",
            "Material Request Item-gst_hsn_code-hidden","Material Request Item-conversion_factor-req",
            "Material Request Item-conversion_factor-hidden","Material Request-scan_barcode-hidden","Material Request Item-manufacture_details-hidden","Material Request Item-accounting_details_section-hidden",
            "Material Request Item-accounting_dimensions_section-collapsible", "Material Request Item-rate-hidden","Supplier Quotation-quotation_number-label","Supplier Quotation Item-gst_hsn_code-hidden",
            "Supplier Quotation Item-gst_hsn_code-hidden","Supplier Quotation Item-conversion_factor-reqd","Supplier Quotation Item-conversion_factor-hidden","Supplier Quotation Item-item_weight_details-hidden",
            "Supplier Quotation Item-manufacture_details-hidden","Purchase Order-scan_barcode-hidden","Purchase Order-discount_section-collapsible","Purchase Order-shipping_rule-hidden"
            ,"Purchase Order-incoterm-hidden","Supplier Quotation-ignore_pricing_rule-hidden","Employee External Work History-company_name-label","Employee External Work History-contact-label",
            "Purchase Receipt-incoterm-hidden","Purchase Invoice-incoterm-hidden","Supplier Quotation-incoterm-hidden","Purchase Receipt-shipping_col-hidden","Supplier Quotation-column_break_34-hidden",
            "Purchase Invoice-column_break_58-hidden","Purchase Receipt-scan_barcode-hidden","Purchase Invoice-scan_barcode-hidden","Purchase Receipt-main-field_order","Purchase Receipt-shipping_rule-hidden",
            "Purchase Receipt-raw_material_details-hidden","Purchase Invoice-shipping_rule-hidden","Purchase Invoice-main-field_order","Purchase Invoice-raw_materials_supplied-hidden","Supplier Quotation-shipping_rule-hidden",
            "Quotation-scan_barcode-hidden","Quotation-incoterm-hidden","Item-gst_hsn_code-default","Supplier Quotation-place_of_supply-hidden",
            "Supplier Quotation-accounting_dimensions_section-hidden","Purchase Order-place_of_supply-hidden","Purchase Order-scan_barcode-hidden","Material Request Item-accounting_dimensions_section-hidden",
            "Purchase Order-ignore_pricing_rule-hidden","Material Request Item-actual_qty-hidden","Material Request Item-projected_qty-hidden","Material Request Item-min_order_qty-hidden","Material Request Item-accounting_details_section-hidden",
            "Material Request Item-page_break-hidden","Request for Quotation Item-section_break_24-hidden","Purchase Order Item-manufacture_details-hidden","Supplier Quotation Item-ad_sec_break-hidden","Supplier Quotation Item-section_break_44-hidden",
            "Request for Quotation Item-image_view-hidden","Request for Quotation Item-section_break_23-hidden",
            "Request for Quotation-incoterm-hidden","Supplier Quotation-main-field_order","Supplier Quotation-named_place-hidden","Purchase Order-set_warehouse-default","Purchase Order-main-field_order",
            "Purchase Receipt Item-manufacture_details-hidden","Purchase Receipt-place_of_supply-hidden","Purchase Receipt-apply_putaway_rule-hidden","Purchase Receipt-is_subcontracted-hidden",
            "Purchase Invoice-place_of_supply-hidden","Purchase Order-payment_terms_template-default","Purchase Invoice-payment_terms_template-default",
            "Expense Claim-department-hidden","Expense Claim-main-field_order",
            "Material Request Item-stock_uom-hidden",
            "Material Request Item-stock_uom-reqd",
            "Request for Quotation Item-stock_uom-reqd",
            "Request for Quotation Item-stock_uom-hidden",
            "Supplier Quotation Item-stock_uom-reqd",
            "Supplier Quotation Item-stock_uom-hidden",
            "Purchase Receipt Item-stock_uom-reqd",
            "Purchase Receipt Item-stock_uom-hidden",
            "Supplier Quotation Item-base_amount-hidden",
            "Supplier Quotation Item-base_rate-hidden",
            "Purchase Order Item-stock_uom-hidden",
            "Purchase Order Item-base_rate-hidden",
            "Purchase Order Item-base_amount-hidden",
            "Purchase Receipt Item-base_amount-hidden",
            "Purchase Receipt Item-base_rate-hidden",
            "Leave Application-half_day-hidden",
            "Employee-custom_attach_aadhar-hidden",
            "Employee-main-field_order",
            "Attendance Request-half_day-hidden",
            "Employee-custom_head_quarter_city-hidden",
            "Purchase Order Item-gst_details_section-hidden",
            "Purchase Order Item-references_section-hidden",
            "Material Request Item-item_code-label",
            "Material Request Item-item_name-hidden",
            "Request for Quotation Supplier-send_email-default",
            "Request for Quotation-main-default_print_format",
            "Supplier Quotation-transaction_date-label",
            ]]
        }
    },
    {
        "dt": "Custom Field",
        "filters": [
            ["name", "in", [
                "Request for Quotation-custom_tab_2","Request for Quotation-custom_compare","Attendance-custom_half_day_type",
                "Expense Claim-custom_maa_project","Attendance-custom_work_hours",
                "Employee Checkin-custom_exact_time","Employee Checkin-custom_exact_date","Employee Checkin-custom_branch","Attendance-custom_branch","Attendance-custom_exact_out_time",
                "Attendance-custom_exact_in_time","Asset-custom_custodian_name","Asset-department-hidden","Asset-custom_asset_status","Asset-custom_supplier_name","Asset-custom_asset_id",
                "Asset-custom_note",
            "Contact person-custom_contact_number",
            "Purchase Invoice-custom_gate_pass_id",
            "Purchase Invoice-custom_gate_pass_no",
            "Material Request-custom_contact_numbers",
            "Material Request-custom_section_break_hcx0y",
            "Material Request-custom_contact_person",
            "Purchase Receipt-custom_gate_pass_date",
            "Purchase Receipt-custom_gate_pass_no",
            "Purchase Order-custom_our_enquiry_ref",
            "Request for Quotation-custom_our_enquiry_ref",
            "Bank Account-custom_branch",
            "Supplier Quotation-custom_delivery_terms",
            "Purchase Receipt-custom_lr_amount",
            "Purchase Invoice-custom_lr_amount",
            "Purchase Receipt Item-custom_challan_qty",
            "Purchase Receipt Item-custom_remarks",
            "Purchase Invoice Item-custom_challan_qty",
            "Purchase Invoice Item-custom_remarks",
            "Purchase Order-custom_term_selection",
            "Material Request-custom_term_selection",
            "Request for Quotation-custom_term_selection",
            "Supplier Quotation-custom_term_selection",
            "Purchase Receipt-custom_term_selection",
            "Purchase Invoice-custom_term_selection",
            "Purchase Order Item-custom_no_of_service"

            ]
            ]
        ]
    },


    {
    "dt": "DocType",
    "filters": [
        ["name", "in", [
            "MR Contact Person"
        ]]
    ]
},
   
    {
        "dt": "Translation",
        "filters": [
            ["name", "in", [
                "ova7m68opp"
            ]
            ]
        ]
    },

    {
        "dt": "Workflow",
        "filters": [["name", "in", [
            "Supplier Quotation Approval",
            "Purchase Order Approval",
        ]]]
    },

    # states/actions the purchase workflows depend on (not shipped by Frappe)
    {
        "dt": "Workflow State",
        "filters": [["name", "in", ["Pending Approval"]]]
    },
    {
        "dt": "Workflow Action Master",
        "filters": [["name", "in", ["Send for Approval"]]]
    }

]

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"po_wo_pr.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
