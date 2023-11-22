frappe.listview_settings['Projects Meeting'] = {
	add_fields: ["id", "status", "project"],
	filters: [["status", "=", "Before"]],
	onload: function(listview) {
		var method = "pp_addon.pp_addon.doctype.projects_meeting.projects_meeting.set_multiple_status";

		listview.page.add_menu_item(__("Set as Open"), function() {
			listview.call_for_selected_items(method, {"status": "Before"});
		});

		listview.page.add_menu_item(__("Set as Completed"), function() {
			listview.call_for_selected_items(method, {"status": "After"});
		});
	},
	get_indicator: function(doc) {
		var colors = {
			"Before": "orange",
			"Invited": "red",
			"After": "orange",
			"Print": "green",
		}
		return [__(doc.status), colors[doc.status], "status,=," + doc.status];
	},
};
