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
    # graph = get_graph(data, filters)
    # data = convert_data_treeview(filters, data)
    return columns, data, None  # , graph


def get_columns(filters: dict) -> list[dict]:
    columns = [
        {
            "fieldname": "employee",
            "label": _("Employee"),
            "fieldtype": "Link",
            "options": "Employee",
            "width": 500,
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
            "fieldtype": "Data",
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
            "width": 200,
        },
        {
            "fieldname": "weight",
            "label": _("Weight"),
            "fieldtype": "Float",
            "precision": 2,
            "width": 200,
        },
        {
            "fieldname": "days",
            "label": _("Days"),
            "fieldtype": "Float",
            "precision": 2,
            "width": 200,
        },
    ]
    return columns


def get_data(filters: dict) -> list[dict]:
    data = frappe.db.sql(
        get_query(filters),
        as_dict=1,
    )
    return data


def get_query(filters: dict) -> list[dict]:
    conditions = get_conditions(filters)
    query = f"""
        SELECT
            d.done_by AS employee, d.project, d.milestone, dwc.task_data, dwc.progress, dwc.weight, dwc.days
        FROM `tabDaily Work` AS d
        LEFT JOIN `tabDaily Work Tasks Child Table` AS dwc
            ON d.name = dwc.parent
        WHERE {conditions}
    """
    return query


def get_conditions(filters: dict) -> str:
    conditions = ""
    if filters.get("project"):
        conditions += " d.project = '{project}'".format(project=filters.get("project"))

    if filters.get("milestone"):
        if conditions:
            conditions += " AND "
        conditions += " d.milestone = '{milestone}'".format(
            milestone=filters.get("milestone")
        )

    if filters.get("from_date") and filters.get("to_date"):
        if conditions:
            conditions += " AND "
        conditions += " d.modified BETWEEN '{from_date}' AND '{to_date}'".format(
            from_date=filters.get("from_date"), to_date=filters.get("to_date")
        )
    elif filters.get("from_date"):
        if conditions:
            conditions += " AND "
        conditions += " d.modified >= '{from_date}'".format(
            from_date=filters.get("from_date")
        )
    elif filters.get("to_date"):
        if conditions:
            conditions += " AND "
        conditions += " d.modified <= '{to_date}'".format(
            from_date=filters.get("to_date")
        )

    if filters.get("employee"):
        if conditions:
            conditions += " AND "
        conditions += " d.done_by = '{employee}'".format(
            employee=filters.get("employee")
        )

    return conditions


def convert_data_treeview(filters: dict, data: list[dict]) -> list[dict]:
    root = frappe._dict(
        {
            "employee": "Employees",
            "project": None,
            "milestone": None,
            "task_data": "",
            "progress": 0.0,
            "weight": 0.0,
            "days": 0.0,
            "indent": 0,
            "name": "root",
            "parent": None,
        },
    )

    new_data = [root]
    employees = list(set(map(lambda x: x.get("employee"), data)))

    for emp in employees:
        # Add Employee row
        new_data.append(
            {
                "employee": emp,
                "project": "",
                "milestone": "",
                "task_data": "",
                "progress": 0.0,
                "weight": 0.0,
                "days": 0.0,
                "indent": 1,
                "name": emp,
                "parent": "root",
            },
        )

        # Add Projects under Employee
        projects = list(set(map(lambda x: x.get("project"), filter(lambda x: x.get("employee") == emp, data))))
        new_data.append(
            {
                "employee": "Projects",
                "project": "",
                "milestone": "",
                "task_data": "",
                "progress": 0.0,
                "weight": 0.0,
                "days": 0.0,
                "indent": 2,
                "name": "Projects",
                "parent": emp,
            },
        )
        for proj in projects:
            new_data.append(
                {
                    "employee": proj,
                    "project": "",
                    "milestone": "",
                    "task_data": "",
                    "progress": 0.0,
                    "weight": 0.0,
                    "days": 0.0,
                    "indent": 3,
                    "name": proj,
                    "parent": "Projects",
                },
            )

            # Add Milestones undrer Projects
            milestones = list(set(map(lambda x: x.get("milestone"), filter(lambda x: x.get("project") == proj and x.get("employee") == emp, data))))
            new_data.append(
                    {
                        "employee": "Milestones",
                        "project": "",
                        "milestone": "",
                        "task_data": "",
                        "progress": 0.0,
                        "weight": 0.0,
                        "days": 0.0,
                        "indent": 4,
                        "name": "Milestones",
                        "parent": proj,
                    },
                )
            for ms in milestones:
                new_data.append(
                    {
                        "employee": ms,
                        "project": "",
                        "milestone": "",
                        "task_data": "",
                        "progress": 0.0,
                        "weight": 0.0,
                        "days": 0.0,
                        "indent": 5,
                        "name": ms,
                        "parent": "Milestones",
                    },
                )
                
                # Add Tasks under Milestones
                tasks = filter(lambda x: x.get("milestone") == ms and x.get("project") == proj and x.get("employee") == emp, data)
                new_data.append(
                    {
                        "employee": "Tasks",
                        "project": "",
                        "milestone": "",
                        "task_data": "",
                        "progress": 0.0,
                        "weight": 0.0,
                        "days": 0.0,
                        "indent": 6,
                        "name": "Tasks",
                        "parent": ms,
                    },
                )
                for task in tasks:
                    new_data.append(
                        {
                            "employee": task.get("task_data"),
                            "project": "",
                            "milestone": "",
                            "task_data": "",
                            "progress": task.get("progress"),
                            "weight": task.get("weight"),
                            "days": task.get("days"),
                            "indent": 7,
                            "name": task,
                            "parent": "Tasks",
                        },
                    )

    return new_data


def get_graph(data: list[dict], filters: dict) -> dict:
    report = frappe.get_doc("Report", "Milestone & Tasks")
    _, project_data, _, graph = report.execute_module(filters)
    milestones = list(set(milestone.get("milestone") for milestone in data))
    labels_list = []
    completion = []
    remain = []
    graph = {
        "title": "Employee Tasks Detals",
        "type": "bar",
        "height": 500,
        "colors": ["#36AE7C", "#E64848"],
        "valuesOverPoints": True,
    }
    for milestone in project_data:
        if milestone.get("milestone") in milestones:
            labels_list.append(milestone.get("milestone"))
            completion.append(flt(milestone.get("completion", 0) * 100, precision=2))
            remain.append(flt(100 - milestone.get("completion", 0) * 100, precision=2))

    datasets = [
        {"name": "Completion", "values": completion},
        {"name": "Remain", "values": remain},
    ]
    graph["data"] = {"labels": labels_list, "datasets": datasets}
    return graph
