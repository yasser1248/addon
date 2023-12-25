// Copyright (c) 2023, magdyabouelatta and contributors
// For license information, please see license.txt

frappe.ui.form.on("Daily Work", {
    setup(frm) {
        frm.set_query("milestone", () => {
            return {
                query: "pp_addon.pp_addon.doctype.daily_work.daily_work.get_milestones_for_project",
                filters: {
                    project: frm.doc.project,
                }
            };
        })
    },

    project(frm) {
        if (frm.doc.project) {
            frappe.db.get_value( "Projects Milestone", { project: frm.doc.project }, "name", (r) => {
                frm.set_query("milestone", () => {
                    return {
                        query: "pp_addon.pp_addon.doctype.daily_work.daily_work.get_milestones_for_project",
                        filters: {
                            parent: r.name,
                            project: frm.doc.project,
                        }
                    };
                });
            } );
        }
    },

    milestone(frm) {
        frappe.call({
            method: "set_milestone_days_weight",
            doc: frm.doc,
            callback: (r) => {
                if (Object.keys(r.message).length) {
                    frm.set_value("days", r.message.days);
                    frm.set_value("weight", r.message.weight);
                    frm.refresh_field("days");
                    frm.refresh_field("weight");
                }
            },
        });
    },
});
