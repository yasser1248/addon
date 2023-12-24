# Copyright (c) 2023, magdyabouelatta and contributors
# For license information, please see license.txt

import frappe
from frappe import _


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
            "label": _("Employee"),
            "fieldname": "name1",
            "fieldtype": "Link",
            "options": "Employee",
        },
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
    # frappe.throw(str(query))
    data = _get_data(filters, query)
    return data


def get_query(filters: frappe._dict) -> str:
    conditions = get_conditions(filters)
    query = f"""
        SELECT
            name1,
            DATE(rec_atten.attendance_time) AS date,
            (CASE WHEN rec_atten.log_type = 'IN' THEN rec_atten.attendance_time END) AS check_in,
            (CASE WHEN rec_atten.log_type = 'OUT' THEN rec_atten.attendance_time END) AS check_out,
            (SUM(CASE WHEN rec_atten.log_type IN ('IN', 'OUT') THEN TIMESTAMPDIFF(SECOND, '1970-01-01', rec_atten.attendance_time) ELSE 0 END) -
                SUM(CASE WHEN rec_atten.log_type IN ('Exit', 'Enter') THEN TIMESTAMPDIFF(SECOND, '1970-01-01', rec_atten.attendance_time) ELSE 0 END)) / 3600 AS total_working
        FROM `tabRecord Attendance` AS rec_atten
        WHERE {conditions}
        GROUP BY date, name1;
    """
    return query


def get_conditions(filters: frappe._dict) -> str:
    conditions = ""
    if filters.get("from_date") and filters.get("to_date"):
        conditions += " rec_atten.attendance_time BETWEEN '{from_date}' AND '{to_date}'".format(
            from_date=filters.get("from_date"), to_date=filters.get("to_date")
        )
    elif filters.get("from_date"):
        conditions += " rec_atten.attendance_time >= '{from_date}'".format(
            from_date=filters.get("from_date")
        )
    elif filters.get("to_date"):
        conditions += " rec_atten.attendance_time <= '{to_date}'".format(
            from_date=filters.get("to_date")
        )
    if filters.get("employee"):
        conditions += " AND rec_atten.name1 = '{employee}'".format(
            employee=filters.get("employee")
        )
    return conditions


def _get_data(filters: frappe._dict, query: str) -> list[frappe._dict]:
    data = frappe.db.sql(query, as_dict=1)
    return data
