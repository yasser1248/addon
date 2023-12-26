# Copyright (c) 2023, magdyabouelatta and contributors
# For license information, please see license.txt

import json

import frappe
from frappe.model.document import Document


class ProjectsMeeting(Document):
    
    @frappe.whitelist()
    def send_summary(self):
        if self.participate:
            participates_emails = []
            for item in self.participate:
                participates_emails.append(
                    frappe.db.get_value(item.participate_type, item.participate, "email")
                )
            # names = (item.participate for item in self.participate)
            # participates_emails = frappe.db.get_list("Stakholder",
            #                                         filters={"name": ["IN", tuple(names)]}, fields=["email"])
            html = frappe.get_print(self.doctype, self.name,)
            pdf_file = frappe.utils.pdf.get_pdf(html)
            print(type(pdf_file))
            email_kwargs = {
                "recipients": [email for item in participates_emails for _, email in item.items()],
                "message": str(self.get("meeting_summary")),
                "subject": f"Meeting Summary for {self.get('name')}",
                "attachments": [{"fname": self.name, "fcontent": pdf_file}],
            }
            frappe.enqueue(
                method=frappe.sendmail, queue="short", timeout=300, now=True,
                **email_kwargs,
            )


@frappe.whitelist()
def set_multiple_status(names, status):
	names = json.loads(names)
	for name in names:
		task = frappe.get_doc("Projects Meeting", name)
		task.status = status
		task.save()
