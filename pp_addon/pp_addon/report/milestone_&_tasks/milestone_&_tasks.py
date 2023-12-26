# Copyright (c) 2023, magdyabouelatta and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters)
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
            p.project, p.milestone, SUM(c.weight) AS sum_total_weight, p.name, p.creation,
            projects_milestone_child.plan_start__date, projects_milestone_child.plan_end__date,
            projects_milestone_child.actual_start__date, projects_milestone_child.actual_end__date
        FROM `tabDaily Work` AS p
        LEFT JOIN `tabDaily Work Tasks Child Table` AS c
            ON p.name = c.parent
        LEFT JOIN `tabProjects Milestone child` AS projects_milestone_child
            ON p.milestone = projects_milestone_child.name
        WHERE p.project = "{project}"
        GROUP BY p.name;
        """.format(
            project=filters.get("project")
        ),
        as_dict=1,
    )

    project_total_milestones = frappe.db.sql(
        """SELECT
                p.project,
                SUM(c.weight) AS total_weight, c.plan_start__date, c.plan_end__date,
                c.actual_start__date, c.actual_end__date
            FROM `tabProjects Milestone` AS p
            LEFT JOIN `tabProjects Milestone child` AS c
                ON p.name = c.parent
            WHERE p.project = '{project}';
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
        temp = frappe.db.sql(
            """SELECT
                    c.weight
                FROM `tabProjects Milestone child` AS c
                WHERE c.name = '{milestone}';
            """.format(
                milestone=milestone.get("milestone")
            ),
            as_dict=1,
        )
        milestone["project_contribution"] = flt(
            (milestone["completion"] * temp[0].get("weight"))
            / project_total_milestones[0].get("total_weight") if project_total_milestones[0].get("total_weight")!=0 else 1,
            precision=2,
        )
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
        "title": "Project Status",
        "type": "donut",
        "height": 500,
        "colors": ["#36AE7C", "#E64848"],
        "valuesOverPoints": True,
    }
    labels_list = ["Finished", "Unfinished"]
    # finished = sum(milestone.get("completion") for milestone in milestones) * 100
    finished = flt(
        sum(map(lambda x: x.get("project_contribution", 0), milestones)) * 100, precision=2
    )
    unfinished = flt(100.0 - finished, precision=2)
    datasets = [{"values": [finished, unfinished]}]
    graph["data"] = {"labels": labels_list, "datasets": datasets}
    return graph


def add_remaining_milestones(filters: dict, data: list[dict], graph: dict = {}) -> None:
    milestones = [f"'{milestone.get('milestone')}'" for milestone in data]
    if not milestones:
        return
    remaining_milestones = frappe.db.sql(
        """
            SELECT p.project, c.name AS milestone,
            c.plan_start__date, c.plan_end__date,
            c.actual_start__date, c.actual_end__date
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
