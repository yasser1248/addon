// Copyright (c) 2023, magdyabouelatta and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project team asses', {
	setup: function(frm) {
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
	},

	// project: function(frm) {
	// 	if (frm.doc.project) {
	// 		add_child_table_row(frm);
	// 	}
	// },

	// employee: function(frm) {
	// 	if (frm.doc.project) {
	// 		add_child_table_row(frm);
	// 	}
	// }
});


function add_child_table_row(frm) {
	values_promise = frappe.call({
		method: "pp_addon.pp_addon.doctype.project_team_asses.project_team_asses.get_start_end_date",
		args: {"project": frm.doc.project},
	});
	values_promise.then(
		(r) => {
			if (Object.keys(r.message).length > 0) {
				const monthList = generateMonthList(r.message.start_date, r.message.end_date);
				console.log(monthList);
				for (let i=0; i<monthList.length; i++) {
					frm.add_child("items", {"from": monthList[i].firstDay, "to":  monthList[i].lastDay});
				}
				frm.refresh_field("items");
			}
		}
	);
}


function generateMonthList(startDateStr, endDateStr) {
	// Parse start and end dates
	const startDate = new Date(startDateStr);
	const endDate = new Date(endDateStr);

	// Initialize the result array
	const monthList = [];

	// Iterate through months
	let currentDate = new Date(startDate);
	while (currentDate <= endDate) {
		const firstDayOfMonth = currentDate;
		const lastDayOfMonth = frappe.datetime.add_months(currentDate, 1);

		// Push the first and last day of the month to the result array
		monthList.push({
			firstDay: firstDayOfMonth.toISOString().split('T')[0],
			lastDay: lastDayOfMonth
		});

		// Move to the next month
		currentDate = new Date(lastDayOfMonth);
	}

	return monthList;
}
