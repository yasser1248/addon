// Copyright (c) 2023, magdyabouelatta and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project Sponsors', {
	after_save: function(frm) {
		frm.set_df_property("go_to_web_site", "hidden", !Boolean(frm.doc.sp_website));
	},
	go_to_web_site: function(frm) {
		window.open(frm.doc.sp_website);
	},
	sp_website: function(frm) {
		frm.set_df_property("go_to_web_site", "hidden", !Boolean(frm.doc.sp_website));
	},
});
