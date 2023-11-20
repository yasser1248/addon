# Copyright (c) 2023, magdyabouelatta and contributors
# For license information, please see license.txt

import json

import frappe
from frappe.utils.nestedset import NestedSet

class Task(NestedSet):
	pass


@frappe.whitelist()
def set_multiple_status(names, status):
	names = json.loads(names)
	for name in names:
		task = frappe.get_doc("Task", name)
		task.status = status
		task.save()


@frappe.whitelist()
def get_children(doctype, parent="", **filters):
	return _get_children(doctype, parent)


def _get_children(doctype, parent="", ignore_permissions=False):
	parent_field = "parent_" + doctype.lower().replace(" ", "_")
	filters = [[f"ifnull(`{parent_field}`,'')", "=", parent], ["docstatus", "<", 2]]

	meta = frappe.get_meta(doctype)

	return frappe.get_list(
		doctype,
		fields=[
			"name as value",
			"{} as title".format(meta.get("title_field") or "name"),
			"status as Status",
			"is_group as expandable",
		],
		filters=filters,
		order_by="name",
		ignore_permissions=ignore_permissions,
	)
