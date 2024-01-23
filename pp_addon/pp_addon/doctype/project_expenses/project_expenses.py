# Copyright (c) 2024, magdyabouelatta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ProjectExpenses(Document):
	def validate(self):
		if self.get("expenses") and self.get("from") and self.get("to"):
			for row in self.get("expenses"):
				if self.get("from") <= row.get("date") <= self.get("to"):
					pass
				else:
					frappe.throw(f"Date should be between {self.get('from')} and {self.get('to')}")


@frappe.whitelist()
def get_aleardy_month_expenses(*args, **kwargs):
    data = frappe.get_all("Project Expenses", ["from_to", "from", "to"], {"project": kwargs.get("project"),})
    if len(data) > 0:
        return {"from_to": [f"{item.get('from')} : {item.get('to')}" for item in data]}
    else:
        return None
