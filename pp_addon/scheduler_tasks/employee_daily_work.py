"""
This module contains a scheduler function that send Employee Daily Report to an Email.

The scheduler runs the function every Thursday 2 PM.
"""

import frappe
from frappe.email.doctype.auto_email_report.auto_email_report import send_now

def send_report():
    doc = frappe.get_doc("Auto Email Report", "Employee Daily Work All")
    doc.send()
    # send_now(doc.name)
