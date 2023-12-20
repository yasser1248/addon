# Copyright (c) 2023, magdyabouelatta and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
    if not filters:
        return None, None
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters)
    if not filters.get("milestone"):
        add_remaining_milestones(
            filters,
            data,
        )
    graph = get_graph(data)
    return columns, data, None, graph


def get_columns() -> list[dict]:
    return [
        {
            "label": _("Project"),
            "fieldname": "project",
            "fieldtype": "Link",
            "options": "Project",
        },
        {
            "label": _("Milestone"),
            "fieldname": "milestone",
            "fieldtype": "Data",
        },
        {
            "label": _("Completion"),
            "fieldname": "completion",
            "fieldtype": "Precent",
        },
        {
            "label": _("Remain"),
            "fieldname": "remain",
            "fieldtype": "Precent",
        },
    ]


def get_data(filters: dict) -> list[dict]:
    conditions = ""
    if filters.get("milestone"):
        conditions += " AND p.milestone = '{milestone}'".format(milestone=filters.get("milestone"))
    tasks = frappe.db.sql(
        """
			SELECT p.project, p.milestone,
				c.task, c.task_data, c.progress, c.weight
			FROM `tabDaily Work` AS p
			LEFT JOIN `tabDaily Work Tasks Child Table` AS c ON p.name = c.parent
			WHERE p.project = "{project}" {conditions};
		""".format(
            project=filters.get("project"),
            conditions=conditions,
        ),
        as_dict=1,
    )
    milestones = frappe.db.sql(
        """SELECT
            p.project, p.milestone, SUM(c.weight) AS sum_total_weight , p.name
        FROM `tabDaily Work` AS p
        LEFT JOIN `tabDaily Work Tasks Child Table` AS c
            ON p.name = c.parent
        WHERE p.project = "{project}" {conditions}
        GROUP BY p.name;
        """.format(
            project=filters.get("project"),
            conditions=conditions,
        ),
        as_dict=1,
    )
    for milestone in milestones:
        milestone["tasks"] = []
    milestone_to_tasks(milestones, tasks)
    [
        calculate_task_contribution(task, milestone.get("sum_total_weight"))
        for milestone in milestones
        for task in milestone.get("tasks")
    ]
    for milestone in milestones:
        milestone["completion"] = calculate_milestone_completion(milestone["tasks"])
        milestone["remain"] = flt(1.0 - milestone.get("completion", 0), precision=2)
    return milestones


def calculate_task_contribution(task: dict, sum_total_weight: float) -> float:
    # Calculate the contribution of a task to its milestone completion
    task["contribution"] = flt(
        ((task["progress"] / 100) * task["weight"]) / sum_total_weight if sum_total_weight != 0 else 1, precision=2
    )
    # return (task['progress'] * task['weight']) / 100.0


def calculate_milestone_completion(milestone_tasks: list[dict]) -> float:
    # Calculate the completion percentage for a milestone
    return flt(sum(task.get("contribution") for task in milestone_tasks), precision=2)


def milestone_to_tasks(milestones: list[dict], tasks: list[dict]) -> None:
    for milestone in milestones:
        for task in tasks:
            if (
                milestone["project"] == task["project"]
                and milestone["milestone"] == task["milestone"]
            ):
                milestone["tasks"].append(task)


def get_graph(milestones: list[dict]) -> dict:
    graph = {
        "title": "Milestone Details",
        "type": "bar",
        "height": 500,
        "colors": ["#36AE7C", "#E64848"],
        "valuesOverPoints": True,
    }
    labels_list = [milestone.get("milestone") for milestone in milestones]
    completion = [
        flt(milestone.get("completion", 0) * 100, precision=2)
        for milestone in milestones
    ]
    remain = [
        flt(milestone.get("remain", 0) * 100, precision=2) for milestone in milestones
    ]
    datasets = [
        {"name": "Completion", "values": completion},
        {"name": "Remain", "values": remain},
    ]
    graph["data"] = {"labels": labels_list, "datasets": datasets}
    return graph


def add_remaining_milestones(filters: dict, data: list[dict], graph: dict = {}) -> None:
    milestones = [f"'{milestone.get('milestone')}'" for milestone in data]
    if not milestones:
        return
    remaining_milestones = frappe.db.sql(
        """
            SELECT p.project, c.name AS milestone
            FROM `tabProjects Milestone` AS p
            LEFT JOIN `tabProjects Milestone child` AS c ON p.name = c.parent
            WHERE p.project = '{project}' AND c.name NOT IN ({milestones})
            """.format(
            project=filters.get("project"), milestones=", ".join(milestones)
        ),
        as_dict=1,
    )
    [
        data.append(milestone.update({"completion": 0.0, "remain": 1.0}))
        for milestone in remaining_milestones
    ]
