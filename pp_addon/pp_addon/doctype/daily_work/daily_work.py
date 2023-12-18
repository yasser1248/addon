# Copyright (c) 2023, magdyabouelatta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DailyWork(Document):
    def validate(self):
        if self.tasks and self.days >= sum(task.days for task in self.tasks):
            pass
        else:
            frappe.throw(
                "Total Days in Tasks ({0}) greater than Milestone Days ({1})".format(
                    sum(task.days for task in self.tasks), self.days
                )
            )

    @frappe.whitelist()
    def set_milestone_days_weight(self):
        data = frappe.db.sql(
            """
                SELECT days, weight
                FROM `tabProjects Milestone child`
                WHERE name = '{0}';
                            """.format(
                self.milestone
            ),
            as_dict=1,
        )
        if data:
            return {
                "days": data[0].get('days'),
                "weight": data[0].get('weight'),
            }
        return {}
