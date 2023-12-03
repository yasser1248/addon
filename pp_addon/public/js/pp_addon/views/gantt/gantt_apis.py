# gantt_apis.py
"""This module contains utils used by DHTMLX Gantt view"""

import json

import frappe
from frappe.utils import get_date_str


@frappe.whitelist()
def on_afte_link_add(*args, **kwargs) -> dict:
    """Add new task to depends_on"""
    if not kwargs.get("link"):
        return {}
    link = json.loads(kwargs.get("link"))

    target_doc = frappe.get_doc(kwargs.get("doctype"), link.get("target"))
    child_doc = frappe.new_doc(
        "Dependent task",
        parentfield="depends_on",
        parent_doc=target_doc,
    )
    child_doc.task = link.get("source")
    child_doc.save()
    return child_doc


@frappe.whitelist()
def on_after_task_add(*args, **kwargs) -> dict:
    """Add new task from Gantt View"""
    if not kwargs.get("item"):
        return {}
    item = json.loads(kwargs.get("item"))
    doc = frappe.get_doc(
        {
            "doctype": kwargs.get("doctype"),
            "subject": item.get("text"),
            "parent_task": item.get("parent") if item.get("parent") else None,
            "exp_start_date": get_date_str(item.get("start_date")),
            "exp_end_date": get_date_str(item.get("end_date")),
            "progress": item.get("progress"),
        },
    )
    doc.save()
    return doc


@frappe.whitelist()
def on_after_task_update(*args, **kwargs) -> dict:
    """Update task from gantt view"""
    if not kwargs.get("item"):
        return {}
    item = json.loads(kwargs.get("item"))
    doc = frappe.get_doc(item.get("doctype"), kwargs.get("id"))
    doc.update({
        # "subject": item.get("text"),
        "parent_task": item.get("parent") if item.get("parent") else None,
        "exp_start_date": get_date_str(item.get("start_date")),
        "exp_end_date": get_date_str(item.get("end_date")),
        "progress": item.get("progress"),
    })
    doc.save()
    return doc
