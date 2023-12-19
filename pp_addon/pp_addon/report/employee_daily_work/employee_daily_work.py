# Copyright (c) 2023, magdyabouelatta and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
    if not filters:
        return None, None

    columns, data = [], []
    columns = get_columns(filters)
    data = get_data(filters)
    graph = get_graph(data)
    return columns, data, None, graph


def get_columns(filters: dict) -> list[dict]:
    columns = [
        {
            "fieldname": "employee",
            "label": _("Employee"),
            "fieldtype": "Link",
            "options": "Employee",
            "width": 200,
        },
        {
            "fieldname": "project",
            "label": _("Project"),
            "fieldtype": "Link",
            "options": "Project",
            "width": 200,
        },
        {
            "fieldname": "milestone",
            "label": _("Milestone"),
            "fieldtype": "Link",
            "options": "Milestone",
            "width": 200,
        },
        {
            "fieldname": "task_data",
            "label": _("Task"),
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "progress",
            "label": _("Progress"),
            "fieldtype": "Percent",
            "width": 100,
        },
        {
            "fieldname": "weight",
            "label": _("Weight"),
            "fieldtype": "Float",
            "precision": 2,
            "width": 100,
        },
        {
            "fieldname": "days",
            "label": _("Days"),
            "fieldtype": "Float",
            "precision": 2,
            "width": 100,
        },
    ]
    return columns


def get_data(filters: dict) -> list[dict]:
    data = frappe.db.sql(get_query(filters), as_dict=1,)
    return data


def get_query(filters: dict) -> list[dict]:
    conditions = get_conditions(filters)
    query = f"""
        SELECT
            dwc.done_by AS employee, d.project, d.milestone, dwc.task_data, dwc.progress, dwc.weight, dwc.days
        FROM `tabDaily Work` AS d
        LEFT JOIN `tabDaily Work Tasks Child Table` AS dwc
            ON d.name = dwc.parent
        WHERE {conditions}
    """
    return query

def get_conditions(filters: dict) -> str:
    conditions = ""
    if filters.get("project"):
        conditions += "d.project = '{project}'".format(project=filters.get("project"))
    if filters.get("milestone"):
        conditions += " AND d.milestone = '{milestone}'".format(milestone=filters.get("milestone"))
    if filters.get("from_date") and filters.get("to_date"):
        conditions += " AND d.modified BETWEEN '{from_date}' AND '{to_date}'".format(from_date=filters.get("from_date"), to_date=filters.get("to_date"))
    if filters.get("employee"):
        conditions += " AND dwc.done_by = '{employee}'".format(employee=filters.get("employee"))
    return conditions


def get_graph(data: list[dict]) -> dict:
    graph = {
        "title": "Employee Tasks Detals",
        "type": "bar",
        "height": 500,
        "colors": ["#36AE7C", "#E64848"],
        "valuesOverPoints": True,
    }
    labels_list = [task.get("task_data") for task in data]
    completion = [
        flt(task.get("progress", 0), precision=2)
        for task in data
    ]
    remain = [
        flt(100 - task.get("progress", 0), precision=2) for task in data
    ]
    datasets = [
        {"name": "Completion", "values": completion},
        {"name": "Remain", "values": remain},
    ]
    graph["data"] = {"labels": labels_list, "datasets": datasets}
    return graph
