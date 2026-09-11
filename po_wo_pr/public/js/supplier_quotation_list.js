frappe.listview_settings['Supplier Quotation'] = {
    onload: function (listview) {
        listview.page.add_action_item(__('Force Bulk Delete SQs'), function () {
            let selected_items = listview.get_checked_items();

            if (selected_items.length === 0) {
                frappe.msgprint(__('Please select at least one Supplier Quotation.'));
                return;
            }

            frappe.confirm(
                __('This will cancel and delete selected Supplier Quotations along with breaking link locks. Proceed?'),
                function () {
                    let sq_names = selected_items.map(doc => doc.name);

                    frappe.call({
                        method: 'po_wo_pr.irs.api.force_bulk_delete_sqs',
                        args: {
                            sq_names: sq_names
                        },
                        freeze: true,
                        freeze_message: __('Force deleting Supplier Quotations...'),
                        callback: function (r) {
                            if (r.message) {
                                if (r.message.deleted.length > 0) {
                                    frappe.show_alert({
                                        message: __('Successfully deleted {0} Supplier Quotation(s).', [r.message.deleted.length]),
                                        indicator: 'green'
                                    });
                                }
                                if (r.message.failed.length > 0) {
                                    frappe.msgprint({
                                        title: __('Partial Failure'),
                                        indicator: 'red',
                                        message: __('Could not delete: <br>') + r.message.failed.map(f => f.name + ': ' + f.error).join('<br>')
                                    });
                                }
                                listview.refresh();
                            }
                        }
                    });
                }
            );
        });
    }
};