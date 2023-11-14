# Copyright (c) 2023, magdyabouelatta and contributors
# For license information, please see license.txt


import frappe
from frappe import _


def execute(filters=None):
    if not filters:
        return [], []
    columns, data = [], []
    data = get_data(filters)
    columns = get_columns(filters, data)
    return columns, data


def get_data(filters: dict) -> list[dict]:

    data = frappe.db.sql(get_query(filters), as_dict=1,)
    return data


def get_columns(filters: dict, data: list[dict]) -> list[dict]:
    EXCLUDE_Fields = ["creation", "modified", "modified_by", "owner", "docstatus",
                    "idx", "_user_tags", "_comments", "_assign", "_liked_by", "project_name",
                    "parent", "parentfield", "parenttype", "project_id", "project"]

    columns = _get_columns(filters)
    columns = [record for record in columns if record["fieldname"] not in EXCLUDE_Fields]

    return columns


def get_query(filters: dict) -> str:
    conditions = f" WHERE d.project = '{filters.get('project')}' AND d.modified BETWEEN '{filters.get('from_date')}' AND '{filters.get('to_date')}' ; "
    meta = frappe.get_meta(filters.get("doctype"))
    children_list = [i.options for i in meta.get_table_fields()] \
                    if meta.get_table_fields() \
                    else None
    query = f"SELECT * FROM `tab{filters.get('doctype')}` AS d  "
    if children_list:
        for c in children_list:
            alias = f"cd{children_list.index(c)}"
            query += f"LEFT JOIN `tab{c}` AS {alias} ON {alias}.parent = d.name "
    query += conditions
    return query


def _get_columns(filters: dict) -> list[dict]:
    EXCLUDE_COLUMNS = ["Column Break", "Section Break", "Tab Break", "Table"]
    columns = []
    meta = frappe.get_meta(filters.get("doctype"))
    children_list = [i.options for i in meta.get_table_fields()] \
                    if meta.get_table_fields() \
                    else None
    for field in meta.fields:
        if field.fieldtype in EXCLUDE_COLUMNS:
            continue
        options = field.options if field.options else ""
        columns.append(
            {
                "fieldname": field.fieldname,
                "label": _(field.label),
                "fieldtype": field.fieldtype,
                "options": options,
            }
        )
    if children_list:
        for child in children_list:
            meta_child = frappe.get_meta(child)
            for field in meta_child.fields:
                if field.fieldtype in EXCLUDE_COLUMNS:
                    break
                options = field.options if field.options else ""
                columns.append(
                    {
                        "fieldname": field.fieldname,
                        "label": _(field.label),
                        "fieldtype": field.fieldtype,
                        "options": options,
                    }
                )
    return columns
