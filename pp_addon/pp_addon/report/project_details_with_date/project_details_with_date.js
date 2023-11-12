// Copyright (c) 2023, magdyabouelatta and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Project Details with Date"] = {
	"filters": [
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project",
			"reqd": 1,
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.get_today(),
		},
		{
			"fieldname": "doctype",
			"label": __("DocType"),
			"fieldtype": "Link",
			"options": "DocType",
			"get_query": function() {
				let doctypes = ["Projects Deliverable", "Projects study", "Projects charter", "Projects Milestone",
				"Projects Risks", "Project quality", "Projects Meeting", "Projects Achievement scene", "Project change",
				"Project team asses", "Project learning lesson", "Transaction", "Project payment", "Project items", "Task", "Project Document"];
				return {
					filters: {"module": 'Pp Addon', "name": ["IN", doctypes]},
				}
			},
			"default": "",
			"reqd": 1,
		},
	]
};
