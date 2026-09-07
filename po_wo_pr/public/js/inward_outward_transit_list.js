frappe.listview_settings['Inward Outward Transit'] = {
    onload: function (listview) {
        listview.page.add_action_item(__('Receive Selected'), function () {
            let selected_docs = listview.get_checked_items();
            if (selected_docs.length === 0) {
                frappe.msgprint(__('Please select transit records to receive.'));
                return;
            }

            frappe.confirm(
                __('Are you sure you want to create Inward Documents for {0} selected item(s)?', [selected_docs.length]),
                function () {
                    frappe.call({
                        method: 'po_wo_pr.irs.api.receive_transit_to_inward',
                        args: {
                            transit_names: selected_docs.map(d => d.name)
                        },
                        freeze: true,
                        freeze_message: __('Processing transit items...'),
                        callback: function (r) {
                            if (!r.exc) {
                                frappe.show_alert({
                                    message: __('Inward Document(s) created successfully.'),
                                    indicator: 'green'
                                });
                                listview.refresh();
                            }
                        }
                    });
                }
            );
        });
    }
};