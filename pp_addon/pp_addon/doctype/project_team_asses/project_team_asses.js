// Copyright (c) 2023, magdyabouelatta and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project team asses', {
	setup: function(frm) {
		if (frm.is_new()) {
			frappe.call({
				method: "pp_addon.pp_addon.doctype.project_team_asses.project_team_asses.get_all_type_of_asses",
				args: {},
				callback: (r) => {
					if (r.message) {
						r.message.forEach((item) => {
							frm.add_child("items", {"item": item.name});
						});
						frm.refresh_field("items");
					}
				},
			});
		}
	},

	refresh: function(frm) {
		add_from_to_options(frm);
	},

	// project: function(frm) {
	// 	if (frm.doc.project) {
	// 		add_child_table_row(frm);
	// 	}
	// },

	employee: function(frm) {
		if (frm.doc.project && frm.doc.employee) {
			add_from_to_options(frm);
		}
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
		args: {"project": frm.doc.project, "employee": frm.doc.employee},
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
