# Copyright (c) 2024, magdyabouelatta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EmployeeAssessment(Document):
	pass

@frappe.whitelist()
def get_start_end_date(*args, **kwargs):
    data = frappe.get_all("Project", ["start_date", "end_date",], {"name": kwargs.get("project")})
    if len(data) == 1:
        return data[0]
    else:
        return None

@frappe.whitelist()
def get_aleardy_assesed(*args, **kwargs):
    data = frappe.get_all("Employee Assessment", ["from_to", "from", "to"], {"project": kwargs.get("project"), "employee": kwargs.get("employee")})
    if len(data) > 0:
        return {"from_to": [f"{item.get('from')} : {item.get('to')}" for item in data]}
    else:
        return None