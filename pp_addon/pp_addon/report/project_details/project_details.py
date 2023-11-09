# Copyright (c) 2023, magdyabouelatta and contributors
# For license information, please see license.txt

import datetime

import frappe
from frappe import _
from frappe.utils import getdate


def execute(filters=None):
    if not filters:
        return [], []
    columns, data = [], []
    validate_filters(filters)
    data = get_data(filters)
    columns = get_columns(filters, data)
    return columns, data


def validate_filters(filters: dict) -> None:
    from_date = getdate(filters.from_date)
    to_date = getdate(filters.to_date)
    if from_date > to_date:
        frappe.throw(_("From Date cannot be greater than To Date"))


def get_data(filters: dict) -> list[dict]:
    data = frappe.db.sql(f"""
                SELECT * FROM `tab{filters.get("doctype")}` AS d
                WHERE d.project = "{filters.get("project")}" AND d.modified BETWEEN "{filters.get("from_date")}" AND "{filters.get("to_date")}"
            """, as_dict=1)
    return data


def get_columns(filters: dict, data: list[dict]) -> list[dict]:
    EXCLUDE_Fields = ["creation", "modified", "modified_by", "owner", "docstatus", "idx", "_user_tags", "_comments", "_assign", "_liked_by", "project_name"]
    columns = []
    for record in data:
        for key, value in record.items():
            if key == "name":
                columns.append(
                    {
                        "fieldname": f"{key}",
                        "label": _(f"{frappe.unscrub(key)}"),
                        "fieldtype": "Link",
                        "options": f"{filters.get('doctype')}",
                        "width": 300,
                    }
                )
            elif key not in EXCLUDE_Fields:
                columns.append(
                    {
                        "fieldname": f"{key}",
                        "label": _(f"{frappe.unscrub(key)}"),
                        "fieldtype": "Date" if isinstance(value, datetime.datetime) else "Data",
                        "width": 300,
                    }
                )
    return columns
