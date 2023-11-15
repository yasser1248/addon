# Copyright (c) 2023, magdyabouelatta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Projectscharter(Document):
    def save(self, *args, **kwargs):
        self.set("projects_milestone", frappe.get_value("Projects Milestone", {"project": self.get("project")}, "name"))
        self.set("projects_risks", frappe.get_value("Projects Risks", {"project": self.get("project")}, "name"))
        self.set("project_quality", frappe.get_value("Project quality", {"project": self.get("project")}, "name"))
        return super().save(*args, **kwargs)
