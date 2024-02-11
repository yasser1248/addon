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

    refresh: function(frm) {
		add_from_to_options(frm);
	},

    from_to: function(frm) {
		if (frm.doc.from_to) {
			const date = frm.doc.from_to.split(":");
			if (date.length === 2) {
				frm.set_value("from", date[0].trim());
				frm.set_value("to", date[1].trim());
				frm.refresh_field("from");
				frm.refresh_field("to");
			}
		}
        frm.doc.tasks.forEach(function(e){
            if ( e.date >= frm.doc.from  && e.date < frm.doc.to){
                $("[data-idx='"+e.idx+"']").show()
            }else{
                $("[data-idx='"+e.idx+"']").hide()
            }
            })

	},
});

function add_from_to_options(frm) {

	values_promise = frappe.call({
		method: "pp_addon.pp_addon.doctype.project_team_asses.project_team_asses.get_start_end_date",
		args: {"project": frm.doc.project},
	});
	values_promise.then(
		async (r) => {
			if (Object.keys(r.message).length > 0) {
				const monthList = await generateMonthList(frm, r.message.start_date, r.message.end_date);
				frm.set_df_property("from_to", "options", monthList);
			}
			frm.refresh_field("from_to");
		}
	);
}

async function generateMonthList(frm, startDateStr, endDateStr) {
	// Parse start and end dates
	const startDate = new Date(startDateStr);
	const endDate = new Date(endDateStr);

	// Initialize the result array
	const monthList = [];

	// Iterate through months
	let currentDate = new Date(startDate);
	await frappe.call({
		method: "pp_addon.pp_addon.doctype.project_team_asses.project_team_asses.get_aleardy_assesed",
		args: {"project": frm.doc.project},
		callback: (r) => {
			while (currentDate <= endDate) {
				const firstDayOfMonth = currentDate;
				const lastDayOfMonth = frappe.datetime.add_months(currentDate, 1);
				const finall_date = `${firstDayOfMonth.toISOString().split('T')[0]} : ${lastDayOfMonth}`
				if (frm.is_new() && r.message && in_list(r.message.from_to, finall_date)) {
					// Move to the next month
					currentDate = new Date(lastDayOfMonth);
					continue;
				}
				// Push the first and last day of the month to the result array
				// monthList.push({
				// 	firstDay: firstDayOfMonth.toISOString().split('T')[0],
				// 	lastDay: lastDayOfMonth
				// });
				monthList.push(finall_date);
				// Move to the next month
				currentDate = new Date(lastDayOfMonth);
			}
		},
	});

	return monthList;
}
