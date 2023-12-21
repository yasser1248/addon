# Copyright (c) 2023, magdyabouelatta and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    if not filters:
        return None, None
    columns, data = [], []
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data


def get_columns(filters: dict) -> list[dict]:
    columns = [
        {
            "label": _("Project"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Project",
        },
        {
            "label": _("Project Category"),
            "fieldname": "project_category",
            "fieldtype": "Data",
        },
        {
            "label": _("Start Date"),
            "fieldname": "start_date",
            "fieldtype": "Date",
        },
        {
            "label": _("End Date"),
            "fieldname": "end_date",
            "fieldtype": "Date",
        },
    ]
    return columns


def get_data(filters: dict) -> list[dict]:
    data = []
    project_doctype_data = get_project_doctype_data(filters)
    projects_milestone_data = get_projects_milestone_data(filters)
    projects_risks_data = get_projects_risks_data(filters)
    project_doctype_data.update(
        {
            "from": filters.get("from_date"),
            "to": filters.get("to_date"),
            "projects_milestones": projects_milestone_data,
            "projects_risks": projects_risks_data,
        }
    )
    data.append(project_doctype_data)
    return data


def get_project_doctype_data(filters: dict) -> frappe._dict:
    data = frappe.db.get_list(
        doctype="Project",
        filters={
            "name": filters.get("project"),
            "modified": ["BETWEEN", filters.get("from_date"), filters.get("to_date")],
        },
        fields=[
            "name",
            "project_id",
            "project_name",
            "project_category",
            "project_status",
            "remarks",
            "start_date",
            "end_date",
            "phase",
        ],
    )
    return data[0]


def get_projects_milestone_data(filters: dict) -> list[frappe._dict]:
    report = frappe.get_doc("Report", "Milestone & Tasks")
    _, data, *_ = report.execute_module(filters)

    for milestone in data:
        milestone["status"] = (
            "Done"
            if milestone.get("completion") and milestone.get("completion") == 1.0
            else "Working"
        )

    return data


def get_projects_risks_data(filters: dict) -> list[frappe._dict]:
    report = frappe.get_doc("Report", "Project Details")
    _, data = report.execute_module(filters.update({"doctype": "Projects Risks"}))

    return data


import datetime
[
    {
        "name": "01594-Public Prosecution",
        "project_id": "01594",
        "project_name": "Public Prosecution ",
        "project_category": "Digital Transformation",
        "project_status": None,
        "remarks": None,
        "start_date": datetime.date(2023, 11, 1),
        "end_date": datetime.date(2026, 10, 29),
        "phase": "Phase 1",
        "from": "2023-11-21",
        "to": "2023-12-21",
        "projects_milestones": [
            {
                "project": "01594-Public Prosecution",
                "milestone": "تقرير المقارنات المعيارية و الدراسات المرجعية",
                "sum_total_weight": 15.0,
                "name": "تقرير المقارنات المعيارية و الدراسات المرجعية-00003",
                "creation": datetime.datetime(2023, 12, 18, 14, 48, 28, 142505),
                "tasks": [
                    {
                        "project": "01594-Public Prosecution",
                        "milestone": "تقرير المقارنات المعيارية و الدراسات المرجعية",
                        "task": None,
                        "task_data": "TEST 2",
                        "progress": 100.0,
                        "weight": 5.0,
                        "contribution": 0.33,
                    },
                    {
                        "project": "01594-Public Prosecution",
                        "milestone": "تقرير المقارنات المعيارية و الدراسات المرجعية",
                        "task": None,
                        "task_data": "TEST 1",
                        "progress": 100.0,
                        "weight": 10.0,
                        "contribution": 0.67,
                    },
                ],
                "completion": 1.0,
                "project_contribution": 0.05,
                "status": "Done",
            },
            {
                "project": "01594-Public Prosecution",
                "milestone": "وثيقة استراتيجية التحول الرقمي",
                "sum_total_weight": 66.0,
                "name": "وثيقة استراتيجية التحول الرقمي-00001",
                "creation": datetime.datetime(2023, 12, 13, 13, 44, 36, 917357),
                "tasks": [
                    {
                        "project": "01594-Public Prosecution",
                        "milestone": "وثيقة استراتيجية التحول الرقمي",
                        "task": "TASK--0007",
                        "task_data": "TEST 1",
                        "progress": 100.0,
                        "weight": 10.0,
                        "contribution": 0.15,
                    },
                    {
                        "project": "01594-Public Prosecution",
                        "milestone": "وثيقة استراتيجية التحول الرقمي",
                        "task": None,
                        "task_data": "TEST 4",
                        "progress": 50.0,
                        "weight": 50.0,
                        "contribution": 0.38,
                    },
                    {
                        "project": "01594-Public Prosecution",
                        "milestone": "وثيقة استراتيجية التحول الرقمي",
                        "task": None,
                        "task_data": "TEST 2",
                        "progress": 100.0,
                        "weight": 1.0,
                        "contribution": 0.02,
                    },
                    {
                        "project": "01594-Public Prosecution",
                        "milestone": "وثيقة استراتيجية التحول الرقمي",
                        "task": None,
                        "task_data": "TEST 3",
                        "progress": 100.0,
                        "weight": 5.0,
                        "contribution": 0.08,
                    },
                ],
                "completion": 0.63,
                "project_contribution": 0.03,
                "status": "Working",
            },
            {
                "project": "01594-Public Prosecution",
                "milestone": "وثيقة التصور المستقبلي لمكتب مشاريع التحول الرقمي",
                "sum_total_weight": 15.0,
                "name": "وثيقة التصور المستقبلي لمكتب مشاريع التحول الرقمي-00004",
                "creation": datetime.datetime(2023, 12, 18, 14, 55, 15, 949438),
                "tasks": [
                    {
                        "project": "01594-Public Prosecution",
                        "milestone": "وثيقة التصور المستقبلي لمكتب مشاريع التحول الرقمي",
                        "task": None,
                        "task_data": "TEST 2",
                        "progress": 100.0,
                        "weight": 5.0,
                        "contribution": 0.33,
                    },
                    {
                        "project": "01594-Public Prosecution",
                        "milestone": "وثيقة التصور المستقبلي لمكتب مشاريع التحول الرقمي",
                        "task": None,
                        "task_data": "TEST 1",
                        "progress": 100.0,
                        "weight": 10.0,
                        "contribution": 0.67,
                    },
                ],
                "completion": 1.0,
                "project_contribution": 0.05,
                "status": "Done",
            },
            {
                "project": "01594-Public Prosecution",
                "milestone": "وثيقة خارطة الطريق و خطة التنفيذ",
                "sum_total_weight": 15.0,
                "name": "وثيقة خارطة الطريق و خطة التنفيذ-00005",
                "creation": datetime.datetime(2023, 12, 18, 17, 39, 44, 468645),
                "tasks": [
                    {
                        "project": "01594-Public Prosecution",
                        "milestone": "وثيقة خارطة الطريق و خطة التنفيذ",
                        "task": None,
                        "task_data": "TASK 2",
                        "progress": 100.0,
                        "weight": 10.0,
                        "contribution": 0.67,
                    },
                    {
                        "project": "01594-Public Prosecution",
                        "milestone": "وثيقة خارطة الطريق و خطة التنفيذ",
                        "task": None,
                        "task_data": "TASK 1",
                        "progress": 10.0,
                        "weight": 5.0,
                        "contribution": 0.03,
                    },
                ],
                "completion": 0.7,
                "project_contribution": 0.03,
                "status": "Working",
            },
            {
                "project": "01594-Public Prosecution",
                "milestone": "اخصائي جودة",
                "completion": 0.0,
                "remain": 1.0,
                "status": "Working",
            },
            {
                "project": "01594-Public Prosecution",
                "milestone": "مدير مشاريع بنية تحتية 2",
                "completion": 0.0,
                "remain": 1.0,
                "status": "Working",
            },
            {
                "project": "01594-Public Prosecution",
                "milestone": "مدير مشاريع تطبيقات 1",
                "completion": 0.0,
                "remain": 1.0,
                "status": "Working",
            },
            {
                "project": "01594-Public Prosecution",
                "milestone": "مدير مشروع ادارة البيانات",
                "completion": 0.0,
                "remain": 1.0,
                "status": "Working",
            },
            {
                "project": "01594-Public Prosecution",
                "milestone": "مدير مشروع بنية تحتية 1",
                "completion": 0.0,
                "remain": 1.0,
                "status": "Working",
            },
            {
                "project": "01594-Public Prosecution",
                "milestone": "مدير مشروع تطبيقات 2",
                "completion": 0.0,
                "remain": 1.0,
                "status": "Working",
            },
            {
                "project": "01594-Public Prosecution",
                "milestone": "مدير مشروع سيبر سيكيروتي",
                "completion": 0.0,
                "remain": 1.0,
                "status": "Working",
            },
            {
                "project": "01594-Public Prosecution",
                "milestone": "وثيقة النموذج التشغيلي لمكتب مشاريع التحول الرقمي",
                "completion": 0.0,
                "remain": 1.0,
                "status": "Working",
            },
            {
                "project": "01594-Public Prosecution",
                "milestone": "وثيقة تحديد التوجهات الاستراتيجية و صياغة الاستراتيجية",
                "completion": 0.0,
                "remain": 1.0,
                "status": "Working",
            },
            {
                "project": "01594-Public Prosecution",
                "milestone": "وثيقة تحليل الوضع الراهن للتحول الرقمي",
                "completion": 0.0,
                "remain": 1.0,
                "status": "Working",
            },
            {
                "project": "01594-Public Prosecution",
                "milestone": "وثيقه تحليل الفجوة بين الوضع الحالي والمستقبلي",
                "completion": 0.0,
                "remain": 1.0,
                "status": "Working",
            },
        ],
        "projects_risks": [
            {
                "name": "111e0295dd",
                "creation": datetime.datetime(2023, 12, 21, 11, 58, 40, 658228),
                "modified": datetime.datetime(2023, 12, 21, 11, 58, 40, 658228),
                "modified_by": "Administrator",
                "owner": "Administrator",
                "docstatus": 0,
                "idx": 3,
                "project": "01594-Public Prosecution",
                "project_name": "Public Prosecution ",
                "_user_tags": None,
                "_comments": None,
                "_assign": None,
                "_liked_by": None,
                "risk": "عدم توفر الكوادر البشرية اللازمة لإدارة المشروع من قبل الشركة",
                "phase": None,
                "probability": "Low",
                "impact": "Low",
                "project_link": None,
                "attached": None,
                "action": None,
                "parent": "RISK01594-Public Prosecution",
                "parentfield": "items",
                "parenttype": "Projects Risks",
            },
            {
                "name": "2a63edd634",
                "creation": datetime.datetime(2023, 12, 21, 11, 58, 40, 658228),
                "modified": datetime.datetime(2023, 12, 21, 11, 58, 40, 658228),
                "modified_by": "Administrator",
                "owner": "Administrator",
                "docstatus": 0,
                "idx": 1,
                "project": "01594-Public Prosecution",
                "project_name": "Public Prosecution ",
                "_user_tags": None,
                "_comments": None,
                "_assign": None,
                "_liked_by": None,
                "risk": "جميع افتراضات المشروع في حال عدم توفرها",
                "phase": None,
                "probability": "Low",
                "impact": "Low",
                "project_link": None,
                "attached": None,
                "action": None,
                "parent": "RISK01594-Public Prosecution",
                "parentfield": "items",
                "parenttype": "Projects Risks",
            },
            {
                "name": "4135a43b57",
                "creation": datetime.datetime(2023, 12, 21, 11, 58, 40, 658228),
                "modified": datetime.datetime(2023, 12, 21, 11, 58, 40, 658228),
                "modified_by": "Administrator",
                "owner": "Administrator",
                "docstatus": 0,
                "idx": 6,
                "project": "01594-Public Prosecution",
                "project_name": "Public Prosecution ",
                "_user_tags": None,
                "_comments": None,
                "_assign": None,
                "_liked_by": None,
                "risk": "عدم الالتزام بالاجتماعات المجدولة لتحقيق نطاق المشروع",
                "phase": None,
                "probability": "Low",
                "impact": "Low",
                "project_link": None,
                "attached": None,
                "action": None,
                "parent": "RISK01594-Public Prosecution",
                "parentfield": "items",
                "parenttype": "Projects Risks",
            },
            {
                "name": "6ee5d3621e",
                "creation": datetime.datetime(2023, 12, 21, 11, 58, 40, 658228),
                "modified": datetime.datetime(2023, 12, 21, 11, 58, 40, 658228),
                "modified_by": "Administrator",
                "owner": "Administrator",
                "docstatus": 0,
                "idx": 4,
                "project": "01594-Public Prosecution",
                "project_name": "Public Prosecution ",
                "_user_tags": None,
                "_comments": None,
                "_assign": None,
                "_liked_by": None,
                "risk": "الحروب و الكوارث الطبيعية -لا سمح الله",
                "phase": None,
                "probability": "Low",
                "impact": "Low",
                "project_link": None,
                "attached": None,
                "action": None,
                "parent": "RISK01594-Public Prosecution",
                "parentfield": "items",
                "parenttype": "Projects Risks",
            },
            {
                "name": "c329a5e486",
                "creation": datetime.datetime(2023, 12, 21, 11, 58, 40, 658228),
                "modified": datetime.datetime(2023, 12, 21, 11, 58, 40, 658228),
                "modified_by": "Administrator",
                "owner": "Administrator",
                "docstatus": 0,
                "idx": 5,
                "project": "01594-Public Prosecution",
                "project_name": "Public Prosecution ",
                "_user_tags": None,
                "_comments": None,
                "_assign": None,
                "_liked_by": None,
                "risk": "التأخر في اعتماد المستندات.",
                "phase": None,
                "probability": "Low",
                "impact": "Low",
                "project_link": None,
                "attached": None,
                "action": None,
                "parent": "RISK01594-Public Prosecution",
                "parentfield": "items",
                "parenttype": "Projects Risks",
            },
            {
                "name": "d33fd19ed7",
                "creation": datetime.datetime(2023, 12, 21, 11, 58, 40, 658228),
                "modified": datetime.datetime(2023, 12, 21, 11, 58, 40, 658228),
                "modified_by": "Administrator",
                "owner": "Administrator",
                "docstatus": 0,
                "idx": 2,
                "project": "01594-Public Prosecution",
                "project_name": "Public Prosecution ",
                "_user_tags": None,
                "_comments": None,
                "_assign": None,
                "_liked_by": None,
                "risk": "عدم قدرة الشركة المنفذة على تلبية كافة المتطلبات",
                "phase": None,
                "probability": "Low",
                "impact": "Low",
                "project_link": None,
                "attached": None,
                "action": None,
                "parent": "RISK01594-Public Prosecution",
                "parentfield": "items",
                "parenttype": "Projects Risks",
            },
        ],
    }
]
