// Copyright (c) 2023, magdyabouelatta and contributors
// For license information, please see license.txt

frappe.query_reports["Employees Attendance Details"] = {
	"filters": [
		{
			"label": __("From Date"),
			"fieldname": "from_date",
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
		},
		{
			"label": __("Employee"),
			"fieldname": "employee",
			"fieldtype": "Link",
			"options": "Employee",
		}
	]
};
