// Copyright (c) 2023, magdyabouelatta and contributors
// For license information, please see license.txt

frappe.ui.form.on("User Projects", {
	after_save(frm) {
        frappe.call({
            method: "pp_addon.pp_addon.doctype.user_projects.user_projects.set_user_permissions",
            args: {doc: frm.doc},
            callback: (r) => {console.log(r.message);},
        });
	},
});
