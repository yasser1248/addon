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

    # DOCTYPES = {
    #     "Projects Deliverable": _get_projects_deliverable_data,
    #     "Projects study": _get_projects_study_data,
    #     "Projects charter": _get_projects_charter_data,
    #     "Projects Milestone": _get_projects_milestone_data,
    #     "Projects Risks": _get_projects_risks_data,
    #     "Project quality": _get_project_quality_data,
    # }
    # data = DOCTYPES.get(filters.get("doctype"))(filters)
    # data = frappe.db.sql(f"""
    #             SELECT * FROM `tab{filters.get("doctype")}` AS d
    #             WHERE d.project = "{filters.get("project")}"
    #         """, as_dict=1)

    data = frappe.db.sql(get_query(filters), as_dict=1,)
    return data


def get_columns(filters: dict, data: list[dict]) -> list[dict]:
    EXCLUDE_Fields = ["creation", "modified", "modified_by", "owner", "docstatus",
                    "idx", "_user_tags", "_comments", "_assign", "_liked_by", "project_name",
                    "parent", "parentfield", "parenttype", "project_id", "project"]

    columns = _get_columns(filters)
    columns = [record for record in columns if record["fieldname"] not in EXCLUDE_Fields]
    # for record in data:
    #     for key, value in record.items():
    #         if key == "name":
    #             columns.append(
    #                 {
    #                     "fieldname": f"{key}",
    #                     "label": _(f"{frappe.unscrub(key)}"),
    #                     "fieldtype": "Link",
    #                     "options": f"{filters.get('doctype')}",
    #                     "width": 300,
    #                 }
    #             )
    #         elif key not in EXCLUDE_Fields:
    #             columns.append(
    #                 {
    #                     "fieldname": f"{key}",
    #                     "label": _(f"{frappe.unscrub(key)}"),
    #                     "fieldtype": "Date" if isinstance(value, datetime.datetime) else "Data",
    #                     "width": 300,
    #                 }
    #             )

    return columns


def get_query(filters: dict) -> str:
    conditions = f" WHERE d.project = '{filters.get('project')}' ;"
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


# #############################################################################
def _get_projects_deliverable_data(filters: dict) -> list[dict]:
    """Return the data if DocType specified is Projects Deliverable"""
    data = frappe.db.sql(f"""
            SELECT d.name, d.project,
                cd.deliver, cd.deliver_date, cd.deliver_state, cd.quality, cd.attach
            FROM `tab{filters.get("doctype")}` AS d
            LEFT JOIN `tabDeliverable child` AS cd ON cd.parent = d.name
            WHERE d.project = "{filters.get("project")}"
        """,
        as_dict=1,
    )
    return data


def _get_projects_study_data(filters: dict) -> list[dict]:
    """Return the data if DocType specified is Projects study"""
    data = frappe.db.sql(f"""
            SELECT d.name, d.project, d.feasibility, d.future_vision_of_the_project,
                d.strategic_link, d.benefits, d.scope, d.assumptions_and_determinants,
                d.components_of_the_projec, d.challenges_and_risks, d.time_frame,
                d.required_resources, d.relevant_people_and_their_determinants,
                d.project_governance
            FROM `tab{filters.get("doctype")}` AS d
            WHERE d.project = "{filters.get("project")}"
        """,
        as_dict=1,
    )
    return data

def _get_projects_charter_data(filters: dict) -> list[dict]:
    """Return the data if DocType specified is Projects charter"""
    data = frappe.db.sql(f"""
            SELECT *
            FROM `tab{filters.get("doctype")}` AS d
            WHERE d.project = "{filters.get("project")}"
        """,
        as_dict=1)
    return data

def _get_projects_milestone_data(filters: dict) -> list[dict]:
    """Return the data if DocType specified is Projects Milestone"""
    data = frappe.db.sql(f"""
            SELECT d.name, d.project,
                cd.milestone_name, cd.milestone_description, cd.status, cd.quality
            FROM `tab{filters.get("doctype")}` AS d
            LEFT JOIN `tabProjects Milestone child` AS cd ON cd.parent = d.name
            WHERE d.project = "{filters.get("project")}"
        """,
        as_dict=1)
    return data

def _get_projects_risks_data(filters: dict) -> list[dict]:
    """Return the data if DocType specified is Projects Risks"""
    data = frappe.db.sql(f"""
            SELECT d.name, d.project,
                cd.risk, cd.phase, cd.probability, cd.impact, cd.attached, cd.action
            FROM `tab{filters.get("doctype")}` AS d
            LEFT JOIN `tabProjects Risks child` AS cd ON cd.parent = d.name
            WHERE d.project = "{filters.get("project")}"
        """,
        as_dict=1)
    return data

def _get_project_quality_data(filters: dict) -> list[dict]:
    """Return the data if DocType specified is Project quality"""
    data = frappe.db.sql(f"""
            SELECT d.name, d,project_name, d.quality_planning_approach, d.quality_assurance_approach, d.quality_control_approach, d.quality_improvement_approach,
                cd.quality_roles, cd.quality_responsibilities,
                cdd.task, cdd.item, cdd.metric, cdd.measurement_method
            FROM `tab{filters.get("doctype")}` AS d
            LEFT JOIN `tabProject quality rules` AS cd ON cd.parent = d.name
            LEFT JOIN `tabProject quality metrices` AS cdd ON cdd.parent = d.name
            WHERE d.project = "{filters.get("project")}"
        """,
        as_dict=1)
    return data
