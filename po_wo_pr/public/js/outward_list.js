frappe.listview_settings['Outward Documents'] = {
    onload: function (listview) {
        // Adds button to the top toolbar
        listview.page.add_inner_button(__('Send Bulk to Transit'), function () {
            let selected_docs = listview.get_checked_items();

            if (selected_docs.length === 0) {
                frappe.msgprint(__('Please select at least one document.'));
                return;
            }

            open_target_branch_dialog(listview, selected_docs);
        });

        // Adds item inside the 'Actions' dropdown when checkboxes are selected
        listview.page.add_action_item(__('Send to Transit'), function () {
            let selected_docs = listview.get_checked_items();
            open_target_branch_dialog(listview, selected_docs);
        });
    }
};

function open_target_branch_dialog(listview, selected_docs) {
    let d = new frappe.ui.Dialog({
        title: __('Select Target Branch'),
        fields: [
            {
                label: 'Target Branch',
                fieldname: 'target_branch',
                fieldtype: 'Link',
                options: 'Branch',
                reqd: 1
            }
        ],
        primary_action_label: __('Send'),
        primary_action(values) {
            d.hide();
            frappe.call({
                method: "po_wo_pr.irs.api.create_transit_records",
                args: {
                    docs: selected_docs.map(doc => doc.name),
                    target_branch: values.target_branch
                },
                freeze: true,
                freeze_message: __('Creating Transit Records...'),
                callback: function (r) {
                    if (!r.exc) {
                        frappe.show_alert({
                            message: __('Documents sent to Transit successfully.'),
                            indicator: 'green'
                        });
                        listview.refresh();
                    }
                }
            });
        }
    });
    d.show();
}