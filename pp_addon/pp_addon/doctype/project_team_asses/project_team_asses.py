# Copyright (c) 2023, magdyabouelatta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Projectteamasses(Document):
    def before_save(self):
        max_periority = 0
        for item in self.items:
            max_periority += item.get('weight')
        if max_periority > 100:
            frappe.throw("Sum of weights must be less than or equal to 100%")


@frappe.whitelist()
def get_start_end_date(*args, **kwargs):
    data = frappe.get_all("Project", ["start_date", "end_date",], {"name": kwargs.get("project")})
    if len(data) == 1:
        return data[0]
    else:
        return None


@frappe.whitelist()
def get_all_type_of_asses(*args, **kwargs):
    data = frappe.get_all("Type of asses",fields=["name","weight"])
    if len(data) > 0:
        return data
    else:
        return None


@frappe.whitelist()
def get_aleardy_assesed(*args, **kwargs):
    data = frappe.get_all("Project team asses", ["from_to", "from", "to"], {"project": kwargs.get("project"), "employee": kwargs.get("employee")})
    if len(data) > 0:
        return {"from_to": [f"{item.get('from')} : {item.get('to')}" for item in data]}
    else:
        return None
