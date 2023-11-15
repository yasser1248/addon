# Copyright (c) 2023, magdyabouelatta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ProjectsMeeting(Document):
    
    @frappe.whitelist()
    def send_summary(self):
        if self.participate:
            names = (item.participate for item in self.participate)
            participates_emails = frappe.db.get_list("Stakholder",
                                                    filters={"name": ["IN", tuple(names)]}, fields=["email"])
            email_kwargs = {
                "recipients": [email for item in participates_emails for _, email in item.items()],
                "message": str(self.get("meeting_summary")),
                "subject": f"Meeting Summary for {self.get('name')}",
            }
            frappe.enqueue(
                method=frappe.sendmail, queue="short", timeout=300, now=True,
                **email_kwargs,
            )

# [{'email': 'oy7104745@gmail.com'}, {'email': 'dev7.itsystematic@gmail.com'}]