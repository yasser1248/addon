# Copyright (c) 2023, magdyabouelatta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class UserProjects(Document):
    pass


@frappe.whitelist()
def set_user_permissions(*args, **kwargs):
    doc = frappe.utils.json.loads(kwargs.get("doc"))
    if doc.get("projects"):
        for project in doc.get("projects"):
            if frappe.db.exists(
                "User Permission",
                {
                    "user": doc.get("user"),
                    "allow": "Project",
                    "for_value": project.get("project"),
                },
            ):
                continue
            user_permission_doc = frappe.get_doc(
                {
                    "doctype": "User Permission",
                    "user": doc.get("user"),
                    "allow": "Project",
                    "apply_to_all_doctypes": 1,
                    "for_value": project.get("project"),
                }
            )
            user_permission_doc.save()
        handle_remove_projects(doc)


def handle_remove_projects(doc: dict) -> None:
    user_permission_list = frappe.db.get_list(
        "User Permission",
        {
            "user": doc.get("user"),
            "allow": "Project",
            "for_value": ["NOT IN", [p.get("project") for p in doc.get("projects")]],
        },
        ["name", "for_value"],
    )
    if user_permission_list:
        frappe.db.delete("User Permission", user_permission_list)
