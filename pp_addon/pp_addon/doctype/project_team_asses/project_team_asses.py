# Copyright (c) 2023, magdyabouelatta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Projectteamasses(Document):
	pass


@frappe.whitelist()
def get_start_end_date(*args, **kwargs):
    data = frappe.get_all("Project", ["start_date", "end_date",], {"name": kwargs.get("project")})
    if len(data) == 1:
        return data[0]
    else:
        return None


@frappe.whitelist()
def get_all_type_of_asses(*args, **kwargs):
    data = frappe.get_all("Type of asses")
    if len(data) > 0:
        return data
    else:
        return None
