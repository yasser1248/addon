# Copyright (c) 2023, magdyabouelatta and contributors
# For license information, please see license.txt

from datetime import datetime, time

import frappe
from frappe import _
from frappe.utils import time_diff_in_hours, get_datetime


def execute(filters=None):
    if not filters:
        filters = frappe._dict()
    columns, data = [], []
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters: frappe._dict) -> list[dict]:
    columns = [
        {
            "label": _("Day"),
            "fieldname": "day",
            "fieldtype": "Date",
        },
    ]

    if not filters.get("employee"):
        columns.append(
            {
                "label": _("Employee"),
                "fieldname": "name1",
                "fieldtype": "Link",
                "options": "Employee",
            }
        )

    columns += [
        {
            "label": _("Check IN"),
            "fieldname": "check_in",
            "fieldtype": "Datetime",
        },
        {
            "label": _("Check OUT"),
            "fieldname": "check_out",
            "fieldtype": "Datetime",
        },
        {
            "label": _("Total Working"),
            "fiedname": "total_working",
            "fieldtype": "Data",
        },
    ]
    return columns


def get_data(filters: frappe._dict) -> list[dict]:
    query = get_query(filters)
    data = _get_data(filters, query)
    if filters.employee:
        if frappe.db.get_value('Employee', filters.get("employee"), 'custom_employee_signature') and len(data)>0:
            data[0].signature = frappe.db.get_value('Employee', filters.get("employee"), 'custom_employee_signature')
    data = complete_data(data)
    return data


def get_query(filters: frappe._dict) -> str:
    conditions = get_conditions(filters)
    conditions = f"WHERE {conditions}" if conditions else ""
    query = f"""
        SELECT
            day_attendance_details.day AS day,
            day_attendance_details_child.employee AS name1,
            day_attendance_details_child.in AS check_in,
            day_attendance_details_child.out AS check_out,
            day_attendance_details_child.total_working
        FROM `tabDay Attendance Details` AS day_attendance_details
        LEFT JOIN `tabDay Attendance Details Child` AS day_attendance_details_child
            ON day_attendance_details.name = day_attendance_details_child.parent
        {conditions};
    """
    return query


def get_conditions(filters: frappe._dict) -> str:
    conditions = ""
    if filters.get("from_date") and filters.get("to_date"):
        conditions += " day_attendance_details.day BETWEEN '{from_date}' AND '{to_date}'".format(
            from_date=filters.get("from_date"), to_date=filters.get("to_date")
        )
    elif filters.get("from_date"):
        conditions += " day_attendance_details.day >= '{from_date}'".format(
            from_date=filters.get("from_date")
        )
    elif filters.get("to_date"):
        conditions += " day_attendance_details.day <= '{to_date}'".format(
            from_date=filters.get("to_date")
        )
    if filters.get("employee"):
        conditions += " AND day_attendance_details_child.employee = '{employee}'".format(
            employee=filters.get("employee")
        )
    return conditions


def _get_data(filters: frappe._dict, query: str) -> list[frappe._dict]:
    data = frappe.db.sql(query, as_dict=1)
    return data


def complete_data(data: list[frappe._dict]) -> list[frappe._dict]:
    for record in data:

        # if record.get("check_in"):
        #     record["check_in"] = record["check_in"].replace(hour=8, minute=0, second=0, microsecond=0)
        # if record.get("check_out"):
        #     record["check_out"] = record["check_out"].replace(hour=16, minute=0, second=0, microsecond=0)
        # if record.get("check_in") and record.get("check_out"):
        #     record["total_working"] = time_diff_in_hours(record["check_out"], record["check_in"])

        record["check_in"] = get_datetime(str(record["day"]) + " 08:00:00")
        record["check_out"] = get_datetime(str(record["day"]) + " 16:00:00")
        record["total_working"] = time_diff_in_hours(record["check_out"], record["check_in"])

    return data
