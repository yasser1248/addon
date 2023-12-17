# Copyright (c) 2023, magdyabouelatta and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters)
    graph = get_graph(data)
    # frappe.msgprint(str(data))
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
    ]


def get_data(filters: dict) -> list[dict]:
    tasks = frappe.db.sql(
        """
			SELECT p.project, p.milestone,
				c.task, c.task_data, c.progress, c.weight
			FROM `tabDaily Work` AS p
			LEFT JOIN `tabDaily Work Tasks Child Table` AS c ON p.name = c.parent
			WHERE p.project = "{project}";
		""".format(
            project=filters.get("project"),
        ),
        as_dict=1,
    )

    milestones = frappe.db.sql(
        """SELECT
            p.project, p.milestone, SUM(c.weight) AS sum_total_weight , p.name
        FROM `tabDaily Work` AS p
        LEFT JOIN `tabDaily Work Tasks Child Table` AS c
            ON p.name = c.parent
        WHERE p.project = "{project}"
        GROUP BY p.name;
        """.format(
            project=filters.get("project")
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
    return milestones


def calculate_task_contribution(task: dict, sum_total_weight: float) -> float:
    # Calculate the contribution of a task to its milestone completion
    task["contribution"] = flt(
        ((task["progress"] / 100) * task["weight"]) / sum_total_weight, precision=2
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
    graph = {"type": "donut", "height": 300}
    labels_list = ["Finished", "Unfinished"]
    # finished = sum(milestone.get("completion") for milestone in milestones) * 100
    finished = flt(sum(map(lambda x: x.get("completion", 0), milestones)) * 100, precision=2)
    unfinished = flt(100.0 - finished, precision=2)
    datasets = [{"values": [finished, unfinished]}]
    graph["data"] = {"labels": labels_list, "datasets": datasets}
    return graph
