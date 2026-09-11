frappe.ui.form.on('Employee Checkin', {
    onload: function (frm) {
        lock_fields(frm);
    },
    refresh: function (frm) {
        lock_fields(frm);
        setTimeout(() => {
            let $btn = frm.get_field('custom_fetch_geolocation')?.$input
                || frm.fields_dict['custom_fetch_geolocation']?.$wrapper.find('button')
                || $(frm.wrapper).find('button:contains("Fetch Geolocation")');

            if ($btn && $btn.length) {
                // Apply light blue background and text color
                $btn.css({
                    'background-color': '#87CEEB',
                    'border-color': '#70C0E8',
                    'color': '#000000',
                    'font-weight': '600'
                });
            }
        }, 100);
    },
    validate(frm) {
        if (!frm.doc.latitude || !frm.doc.longitude) {
            frappe.throw('Please click "Fetch Location" before saving.');
        }
    }
});

function lock_fields(frm) {
    // Once the document is saved (not new), make specific fields read-only
    if (!frm.is_new()) {
        const fields = ['employee', 'time', 'log_type'];
        fields.forEach(field => {
            frm.set_df_property(field, 'read_only', 1);
            frm.toggle_enable(field, false);
        });
    }
}