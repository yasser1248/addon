// Copyright (c) 2023, magdyabouelatta and contributors
// For license information, please see license.txt

// $("button.first-page,button.last-page,button.next-page,button.prev-page").on(
//   "click",
//   function () {
// 	console.log("clicked code")
//     cur_frm.doc.items.forEach(function (e) {
//       if (e.assessment_date == cur_frm.doc.from) {
//         console.log("show");
//         $("data-idx='e.assessment_date'").show();
//       } else {
//         console.log("hide");
//         $("data-idx='e.assessment_date'").hide();
//       }
//     });
//   }
// );
	frappe.ui.form.on('Project team asses', {
		setup: function(frm) {
		if (frm.is_new()) {
			// frappe.call({
			// 	method: "pp_addon.pp_addon.doctype.project_team_asses.project_team_asses.get_all_type_of_asses",
			// 	args: {},
			// 	callback: (r) => {
			// 		if (r.message) {
			// 			r.message.forEach((item) => {
			// 				frm.add_child("items", {"item": item.name,"weight": item.weight});
			// 			});
			// 			frm.refresh_field("items");
			// 		}
			// 	},
			// });
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
			// frm.set_value("items", []);
			// frm.refresh_field("items")
			frappe.call({
				method: "pp_addon.pp_addon.doctype.project_team_asses.project_team_asses.get_all_type_of_asses",
				args: {},
				callback: (r) => {
					if (r.message) {
						r.message.forEach((item) => {
							if (frm.doc.items == undefined || frm.doc.items.find((i) => i.item == item.name && i.assessment_date == frm.doc.from) == undefined )
							{
								frm.add_child("items", {"item": item.name,"weight": item.weight,"assessment_date":frm.doc.from});
							}
						});
						frm.refresh_field("items");
						if (frm.doc.items) {
							// frm.doc.items.forEach(function(e){
							// 	if ( e.assessment_date == frm.doc.from){
							// 		$("[data-idx='"+e.idx+"']").show()
							// 	}else{
							// 		$("[data-idx='"+e.idx+"']").hide()
							// 	}
							// 	})
							const parts = cur_frm.doc.from.split("-");
							$("input[data-fieldtype=Date]").val(`${parts[2]}-${parts[1]}-${parts[0]}`).trigger('keyup');
                
						// 	current_date.toLocaleDateString("en-US", {
						// 		day: "2-digit",
						// 		month: "2-digit",
						// 	year: "numeric",
						// })
						// .replace(/\//g, '-')).click()

						// frm.refresh_field("items");
						}
					}
				},
			});
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
