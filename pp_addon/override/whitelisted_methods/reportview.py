"""
Override Module for Whitelisted Methods in reportview.py
This module provides overrides for certain whitelisted methods in the `reportview.py` module.
The purpose of these overrides is to customize the behavior of specific methods in the report view functionality.
"""

import frappe
from frappe.model.utils import is_virtual_doctype
from frappe.model.base_document import get_controller
from frappe.model.db_query import DatabaseQuery
from frappe.desk import reportview

@frappe.whitelist()
@frappe.read_only()
def get():
    args = reportview.get_form_params()
    # Task Doctype
    if args.get("doctype") == "Task":
        return _handle_task_doctype(args)
    # If virtual doctype, get data from controller get_list method
    if is_virtual_doctype(args.doctype):
        controller = get_controller(args.doctype)
        data = reportview.compress(controller.get_list(args))
    else:
        data = reportview.compress(reportview.execute(**args), args=args)
    return data


def _handle_task_doctype(kwargs: dict) -> dict:

    # ADD child field to fetch from database
    (kwargs["fields"]).append("`tabDependent task`.task AS depends_on_tasks")

    # Expected End Date to fetch from database
    (kwargs["fields"]).append("`tabTask`.exp_end_date")

    # Handle filters
    conditions = ""
    if kwargs.get("filters"):
        q = DatabaseQuery("Task")
        q.filters = kwargs.get("filters")
        q.or_filters = kwargs.get("or_filters") if kwargs.get("or_filters") else []
        q.build_conditions()
        conditions = " AND ".join(q.conditions)
    return frappe.db.sql(f"""
            SELECT {", ".join(kwargs.get("fields"))}
            FROM `tabTask`
            LEFT JOIN `tabDependent task` ON `tabDependent task`.parent = `tabTask`.name
            {"WHERE " + conditions if conditions else ""}
            GROUP BY `tabTask`.name
            ORDER BY `tabTask`.`exp_start_date` ASC
        """, as_dict=1)
