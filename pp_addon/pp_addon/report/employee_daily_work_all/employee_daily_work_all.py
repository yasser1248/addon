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
    graph = get_graph(data, filters)
    data = convert_data(filters, data)
    data = convert_data_treeview(filters, data)
    return columns, data, None, graph


def get_columns(filters: dict) -> list[dict]:
    columns = [
        {
            "fieldname": "employee",
            "label": _("Employee"),
            "fieldtype": "Data",
            # "options": "Employee",
            "width": 500,
        },
        {
            "fieldname": "project",
            "label": _("Project"),
            "fieldtype": "Link",
            "options": "Project",
            "width": 200,
        },
        # {
        #     "fieldname": "milestone",
        #     "label": _("Milestone"),
        #     "fieldtype": "Link",
        #     "options": "Milestone",
        #     "width": 200,
        # },
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
    data = frappe.db.sql(
        get_query(filters),
        as_dict=1,
    )
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
        conditions += " AND d.milestone = '{milestone}'".format(
            milestone=filters.get("milestone")
        )
    if filters.get("from_date") and filters.get("to_date"):
        conditions += " AND d.modified BETWEEN '{from_date}' AND '{to_date}'".format(
            from_date=filters.get("from_date"), to_date=filters.get("to_date")
        )
    if filters.get("employee"):
        conditions += " AND dwc.done_by = '{employee}'".format(
            employee=filters.get("employee")
        )
    return conditions


def convert_data_treeview(filters: dict, data: list[dict]) -> list[dict]:
    root = frappe._dict(
        {
            "employee": filters.get("employee"),
            "project": filters.get("project"),
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
    new_data.append(
        {
            "employee": "Milestone",
            "project": "",
            "milestone": "Milestone",
            "task_data": "",
            "progress": 0.0,
            "weight": 0.0,
            "days": 0.0,
            "indent": 1,
            "name": "Milestone",
            "parent": "root",
        }
    )
    milestones = list(set(milestone.get("milestone") for milestone in data))
    if not milestones:
        return
    for milestone in milestones:
        new_data.append(
            frappe._dict(
                {
                    "employee": milestone,
                    "project": "",
                    "milestone": milestone,
                    "task_data": "",
                    "progress": 0.0,
                    "weight": 0.0,
                    "days": 0.0,
                    "indent": 2,
                    "name": milestone,
                    "parent": "Milestone",
                },
            )
        )
        for task in data:
            if task.get("milestone") == milestone:
                task["employee"] = task.get("task_data")
                new_data.append(
                    task.update(
                        {
                            "employee": task.get("task_data"),
                            "project": "",
                            "milestone": "",
                            "progress": task.get("progress"),
                            "weight": task.get("weight"),
                            "days": task.get("days"),
                            "indent": 3,
                            "name": task.get("task_data"),
                            "parent": milestone,
                        }
                    )
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


def convert_data(data: list[dict]) -> list[dict]:
	employees = frappe.db.sql(
		"""
		SELECT dwc.done_by AS employee
		""",
	)
"""
{'employee': '124295---مجدي ابوالعطا',
'project': '01594-Public Prosecution',
'milestone': 'تقرير المقارنات المعيارية و الدراسات المرجعية',
'task_data': 'TEST 2',
'progress': 100.0,
'weight': 5.0,
'days': 5.0}
"""

import datetime

[
    {
        "employee": "124295---مجدي ابوالعطا",
        "project": "01594-Public Prosecution",
        "milestone": "تقرير المقارنات المعيارية و الدراسات المرجعية",
        "task_data": "TEST 2",
        "progress": 100.0,
        "weight": 5.0,
        "days": 5.0,
    },
    {
        "employee": "124295---مجدي ابوالعطا",
        "project": "01594-Public Prosecution",
        "milestone": "تقرير المقارنات المعيارية و الدراسات المرجعية",
        "task_data": "TEST 1",
        "progress": 100.0,
        "weight": 10.0,
        "days": 2.0,
    },
    {
        "employee": "1234.Moath alawaji",
        "project": "01594-Public Prosecution",
        "milestone": "مدير مشروع ادارة البيانات",
        "task_data": "تحليل كراسة مشروع مكتب البيانات",
        "progress": 100.0,
        "weight": 100.0,
        "days": 3.0,
    },
    {
        "employee": "1234.Moath alawaji",
        "project": "01594-Public Prosecution",
        "milestone": "مدير مشروع ادارة البيانات",
        "task_data": "إعداد عرض مشروع مكتب إدارة البيانات \x0b(التحول الرقمي)",
        "progress": 80.0,
        "weight": 100.0,
        "days": 5.0,
    },
    {
        "employee": "1234.Moath alawaji",
        "project": "01594-Public Prosecution",
        "milestone": "مدير مشروع ادارة البيانات",
        "task_data": "حضور ملتقى هيئة الحكومة الرقمية",
        "progress": 100.0,
        "weight": 100.0,
        "days": 1.0,
    },
    {
        "employee": "1234.Moath alawaji",
        "project": "01594-Public Prosecution",
        "milestone": "مدير مشروع ادارة البيانات",
        "task_data": "حضور ورشة العمل الخاصة بـ COBIT",
        "progress": 80.0,
        "weight": 100.0,
        "days": 10.0,
    },
    {
        "employee": "1234.Moath alawaji",
        "project": "01594-Public Prosecution",
        "milestone": "مدير مشروع ادارة البيانات",
        "task_data": "تحليل وثيقة نضج البيانات ",
        "progress": 100.0,
        "weight": 100.0,
        "days": 2.0,
    },
    {
        "employee": "124295---مجدي ابوالعطا",
        "project": "01594-Public Prosecution",
        "milestone": "وثيقة استراتيجية التحول الرقمي",
        "task_data": "TEST 1",
        "progress": 100.0,
        "weight": 10.0,
        "days": 0.0,
    },
    {
        "employee": "124295---مجدي ابوالعطا",
        "project": "01594-Public Prosecution",
        "milestone": "وثيقة استراتيجية التحول الرقمي",
        "task_data": "TEST 4",
        "progress": 50.0,
        "weight": 50.0,
        "days": 0.0,
    },
    {
        "employee": "124295---مجدي ابوالعطا",
        "project": "01594-Public Prosecution",
        "milestone": "وثيقة استراتيجية التحول الرقمي",
        "task_data": "TEST 2",
        "progress": 100.0,
        "weight": 1.0,
        "days": 0.0,
    },
    {
        "employee": "124295---مجدي ابوالعطا",
        "project": "01594-Public Prosecution",
        "milestone": "وثيقة استراتيجية التحول الرقمي",
        "task_data": "TEST 3",
        "progress": 100.0,
        "weight": 5.0,
        "days": 0.0,
    },
    {
        "employee": None,
        "project": "01594-Public Prosecution",
        "milestone": "وثيقة تحليل الوضع الراهن للتحول الرقمي",
        "task_data": "meeting ",
        "progress": 0.0,
        "weight": 0.0,
        "days": 0.0,
    },
    {
        "employee": "1234.Moath alawaji",
        "project": "01594-Public Prosecution",
        "milestone": "وثيقة تحليل الوضع الراهن للتحول الرقمي",
        "task_data": "Cobit 2019 Workshop",
        "progress": 2.0,
        "weight": 10.0,
        "days": 0.0,
    },
    {
        "employee": "124295---مجدي ابوالعطا",
        "project": "01594-Public Prosecution",
        "milestone": "وثيقة التصور المستقبلي لمكتب مشاريع التحول الرقمي",
        "task_data": "TEST 2",
        "progress": 100.0,
        "weight": 5.0,
        "days": 2.0,
    },
    {
        "employee": "124295---مجدي ابوالعطا",
        "project": "01594-Public Prosecution",
        "milestone": "وثيقة التصور المستقبلي لمكتب مشاريع التحول الرقمي",
        "task_data": "TEST 1",
        "progress": 100.0,
        "weight": 10.0,
        "days": 10.0,
    },
    {
        "employee": "124295---مجدي ابوالعطا",
        "project": "01594-Public Prosecution",
        "milestone": "وثيقة خارطة الطريق و خطة التنفيذ",
        "task_data": "TASK 2",
        "progress": 100.0,
        "weight": 10.0,
        "days": 2.0,
    },
    {
        "employee": "124295---مجدي ابوالعطا",
        "project": "01594-Public Prosecution",
        "milestone": "وثيقة خارطة الطريق و خطة التنفيذ",
        "task_data": "TASK 1",
        "progress": 10.0,
        "weight": 5.0,
        "days": 2.0,
    },
]
