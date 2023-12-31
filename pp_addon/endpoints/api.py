# """
# This module contains the API endpoints for the application.
# """
# import json

# import frappe


# @frappe.whitelist()
# def get_employee_attendance(*args, **kwargs):
#     print(frappe.form_dict)
#     report = frappe.get_doc("Report", "Employees Attendance Details")
#     filters = {"from_date": "01-12-2023", "to_date": "31-12-2023"}
#     _, data =report.execute_module({})
#     return data
