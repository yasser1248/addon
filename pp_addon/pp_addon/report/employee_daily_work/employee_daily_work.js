// Copyright (c) 2023, magdyabouelatta and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Daily Work"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			// "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			// "default": frappe.datetime.get_today(),
		},
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
		},
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
			"reqd": 1,
		},
	],
	"formatter": function(value, row, column, data, default_formatter) {

		value = default_formatter(value, row, column, data);

		if (!data.parent || data.name === "Milestone") {
			value = $(`<span>${value}</span>`);
			var $value = $(value).css("font-weight", "bold");
			if (data.warn_if_negative && data[column.fieldname] < 0) {
				$value.addClass("text-danger");
			}

			value = $value.wrap("<p></p>").parent().html();
		}

		if (data.task_data) {
			if (column.fieldname === "progress") {
				value = $(`<span>${value}</span>`);
				var $value = $(value).css("font-weight", "bold");
				var $value = $(value).css("color","#008000");
				if (data.warn_if_negative && data[column.fieldname] < 0) {
					$value.addClass("text-danger");
				}

				value = $value.wrap("<p></p>").parent().html();
			}
			else if (column.fieldname === "weight") {
				value = $(`<span>${value}</span>`);
				var $value = $(value).css("font-weight", "bold");
				var $value = $(value).css("color","#FF0000");
				if (data.warn_if_negative && data[column.fieldname] < 0) {
					$value.addClass("text-danger");
				}

				value = $value.wrap("<p></p>").parent().html();
			}
			else if (column.fieldname === "days") {
				value = $(`<span>${value}</span>`);
				var $value = $(value).css("font-weight", "bold");
				if (data.warn_if_negative && data[column.fieldname] < 0) {
					$value.addClass("text-danger");
				}

				value = $value.wrap("<p></p>").parent().html();
			}
		}

		return value;
	},
	"tree": true,
	"name_field": "name",
	"parent_field": "parent",
	"initial_depth": 2,
};
