"""
This module contains a scheduler function that send Employee Daily Report to an Email.

The scheduler runs the function every Thursday 2 PM.
"""

import frappe

def send_report():
    doc = frappe.get_doc("")