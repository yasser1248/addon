// Copyright (c) 2023, magdyabouelatta and contributors
// For license information, please see license.txt

frappe.ui.form.on("Daily Work", {
    project(frm) {
        if (frm.doc.project) {
            frappe.db.get_value( "Projects Milestone", { project: frm.doc.project }, "name", (r) => {
                frm.set_query("milestone", () => {
                    return {
                        filters: {
                            parent: r.name
                        }
                    };
                });
            } );
        }
    },
});
