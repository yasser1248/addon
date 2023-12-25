"""
Override Module for Whitelisted Methods in client.py
This module provides overrides for certain whitelisted methods in the `client.py` module.
The purpose of these overrides is to customize the behavior of specific methods in the report view functionality.
"""

import frappe
from frappe import _
from frappe.client import get_value

@frappe.whitelist()
def validate_link(doctype: str, docname: str, fields=None):
    if not isinstance(doctype, str):
        frappe.throw(_("DocType must be a string"))

    if not isinstance(docname, str):
        frappe.throw(_("Document Name must be a string"))

    if doctype != "DocType" and not (
        frappe.has_permission(doctype, "select") or frappe.has_permission(doctype, "read")
    ):
        # ignore validation for Projects Milestone child
        if doctype != "Projects Milestone child":
            frappe.throw(
                _("You do not have Read or Select Permissions for {}").format(frappe.bold(doctype)),
                frappe.PermissionError,
            )

    values = frappe._dict()
    values.name = frappe.db.get_value(doctype, docname, cache=True)

    fields = frappe.parse_json(fields)
    if not values.name or not fields:
        return values

    try:
        values.update(get_value(doctype, fields, docname))
    except frappe.PermissionError:
        frappe.clear_last_message()
        frappe.msgprint(
            _("You need {0} permission to fetch values from {1} {2}").format(
                frappe.bold(_("Read")), frappe.bold(doctype), frappe.bold(docname)
            ),
            title=_("Cannot Fetch Values"),
            indicator="orange",
        )

    return values
