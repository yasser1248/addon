// Copyright (c) 2023, magdyabouelatta and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Daily Work All"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 0,
			"default": frappe.datetime.week_start(),
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 0,
			"default": frappe.datetime.week_end(),
		},
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project",
			"reqd": 0,
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
			"reqd": 0,
		},
	],
	// "formatter": function(value, row, column, data, default_formatter) {

	// 	value = default_formatter(value, row, column, data);

	// 	if (!data.parent || data.name === "Milestone") {
	// 		value = $(`<span>${value}</span>`);
	// 		var $value = $(value).css("font-weight", "bold");
	// 		if (data.warn_if_negative && data[column.fieldname] < 0) {
	// 			$value.addClass("text-danger");
	// 		}

	// 		value = $value.wrap("<p></p>").parent().html();
	// 	}

	// 	if (data.indent === 7) {
	// 		if (column.fieldname === "progress") {
	// 			value = $(`<span>${value}</span>`);
	// 			var $value = $(value).css("font-weight", "bold");
	// 			var $value = $(value).css("color","#008000");
	// 			if (data.warn_if_negative && data[column.fieldname] < 0) {
	// 				$value.addClass("text-danger");
	// 			}

	// 			value = $value.wrap("<p></p>").parent().html();
	// 		}
	// 		else if (column.fieldname === "weight") {
	// 			value = $(`<span>${value}</span>`);
	// 			var $value = $(value).css("font-weight", "bold");
	// 			var $value = $(value).css("color","#FF0000");
	// 			if (data.warn_if_negative && data[column.fieldname] < 0) {
	// 				$value.addClass("text-danger");
	// 			}

	// 			value = $value.wrap("<p></p>").parent().html();
	// 		}
	// 		else if (column.fieldname === "days") {
	// 			value = $(`<span>${value}</span>`);
	// 			var $value = $(value).css("font-weight", "bold");
	// 			if (data.warn_if_negative && data[column.fieldname] < 0) {
	// 				$value.addClass("text-danger");
	// 			}

	// 			value = $value.wrap("<p></p>").parent().html();
	// 		}
	// 	}

	// 	return value;
	// },
	"tree": true,
	"name_field": "name",
	"parent_field": "parent",
	"initial_depth": 7,
};
