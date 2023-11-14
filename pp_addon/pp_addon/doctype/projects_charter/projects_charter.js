// Copyright (c) 2023, magdyabouelatta and contributors
// For license information, please see license.txt

frappe.ui.form.on('Projects charter', {
	setup: function(frm) {
		frm.set_query("projects_milestone", () => {
			return {
				filters: {
					project: frm.doc.project,
				}
			}
		});
		frm.set_query("projects_risks", () => {
			return {
				filters: {
					project: frm.doc.project,
				}
			}
		});
		frm.set_query("project_quality", () => {
			return {
				filters: {
					project: frm.doc.project,
				}
			}
		});
	}
});
