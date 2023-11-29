frappe.views.calendar["Task"] = {
	field_map: {
		"start": "exp_start_date",
		"end": "exp_end_date",
		"id": "name",
		"title": "subject",
		"allDay": "allDay",
		"progress": "progress",
        "color":"color"
	},
	gantt: true,
	filters: [
		{
			"fieldtype": "Link",
			"fieldname": "project",
			"options": "Project",
			"label": __("Project"),
            order_by: 'starts_on',
		}
	],
    style_map: {
        Public: 'success',
        Private: 'info'
    },
	get_events_method: "frappe.desk.calendar.get_events"
}