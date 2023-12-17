// Copyright (c) 2023, magdyabouelatta and contributors
// For license information, please see license.txt

frappe.query_reports["Milestone & Tasks"] = {
	"filters": [
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project",
			"reqd": 1,
		},
		{
			"fieldname": "milestone",
			"label": __("Milestone"),
			"fieldtype": "Link",
			"options": "Projects Milestone child",
			"reqd": 0,
			"hidden": 1,
		},
		{
			"fieldname": "task",
			"label": __("Task"),
			"fieldtype": "Link",
			"options": "Task",
			"hidden": 1,
		},
	]
};
