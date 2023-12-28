// Copyright (c) 2023, magdyabouelatta and contributors
// For license information, please see license.txt

frappe.query_reports["Employees Attendance Details"] = {
	"filters": [
		{
			"label": __("From Date"),
			"fieldname": "from_date",
			"fieldtype": "Date",
			"default": frappe.datetime.month_start(),
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.month_end(),
		},
		{
			"label": __("Employee"),
			"fieldname": "employee",
			"fieldtype": "Link",
			"options": "Employee",
		}
	],
	"formatter": function(value, row, column, data, default_formatter) {

		value = default_formatter(value, row, column, data);

		if (data.status === "On Time" && (column.fieldname === "status")) {
			value = $(`<span>${value}</span>`);
			// var $value = $(value).css("font-weight", "bold");
			var $value = $(value).css("color","#008000");

			value = $value.wrap("<p></p>").parent().html();
		}

		if (data.status === "Late") {
			if (in_list(["status", "late_time"], column.fieldname)) {
				value = $(`<span>${value}</span>`);
				var $value = $(value).css("font-weight", "bold");
				var $value = $(value).css("color","#FF0000");

				value = $value.wrap("<p></p>").parent().html();
			}
		}

		return value;
	},
};
