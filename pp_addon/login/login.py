"""
This module contains the login functionality for the application.
"""
import frappe

def after_login():
    frappe.throw("HI")
    # frappe.redirect(
    #     f"{frappe.local.site}/{frappe.scrub('Record Attendance')}/new"
    # )