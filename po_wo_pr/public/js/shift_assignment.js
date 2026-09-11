frappe.ui.form.on("Shift Assignment", {
    refresh(frm) {
        frm.toggle_display("custom_holiday", false);
    }
});

frappe.ui.form.on('Shift Assignment', {
    refresh: function (frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Manage Locations'), function () {
                open_manage_locations_dialog(frm);
            }, __('Actions'));
        }
    }
});

function open_manage_locations_dialog(frm) {
    // Map existing child table rows to the format expected by the dialog
    let existing_locations = (frm.doc.custom_multiple_shift_location || []).map(row => {
        return {
            name: row.name,
            location: row.location,
            is_active: row.is_active
        };
    });

    let dialog = new frappe.ui.Dialog({
        title: __('Manage Shift Locations'),
        size: 'large',
        fields: [
            {
                label: __('Locations'),
                fieldname: 'locations',
                fieldtype: 'Table',
                cannot_add_rows: false,
                in_place_edit: true,
                data: existing_locations, // Load existing data here
                fields: [
                    {
                        fieldtype: 'Data',
                        fieldname: 'name',
                        label: __('Name'),
                        hidden: 1 // Hidden field to track existing child row IDs
                    },
                    {
                        fieldtype: 'Link',
                        fieldname: 'location',
                        label: __('Location'),
                        options: 'Shift Location', // Ensure this matches your exact Location DocType
                        in_list_view: 1,
                        reqd: 1
                    },
                    {
                        fieldtype: 'Check',
                        fieldname: 'is_active',
                        label: __('Is Active'),
                        default: 0,
                        in_list_view: 1
                    }
                ]
            }
        ],
        primary_action_label: __('Update Locations'),
        primary_action: function (values) {
            let locations = values.locations || [];

            frappe.call({
                method: 'po_wo_pr.irs.api.update_shift_locations',
                args: {
                    parent_doc: frm.doc.name,
                    locations: JSON.stringify(locations)
                },
                freeze: true,
                freeze_message: __('Updating Locations...'),
                callback: function (r) {
                    if (r.message) {
                        dialog.hide();
                        frappe.show_alert({
                            message: __('Shift locations updated successfully!'),
                            indicator: 'green'
                        });
                        frm.reload_doc();
                    }
                }
            });
        }
    });

    dialog.show();
}