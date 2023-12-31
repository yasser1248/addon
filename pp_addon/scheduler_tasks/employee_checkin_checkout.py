"""
This module contains two functions: checkin and checkout.

The checkin function checks if an employee has made a check-in. If the employee has not made a check-in, an email is sent to the employee. This function is scheduled to run at 10 AM.

The checkout function performs the same check but for check-out instead of check-in. This function is scheduled to run at 6 PM.
"""

import frappe
from frappe.utils import now_datetime, nowdate


def checkin() -> None:
    employees = frappe.db.get_list("Employee", fields=["name", "employee_name", "email", "user_id"])
    employees_not_make_checkin = get_employees("IN")
    if employees_not_make_checkin:
        send_email_to_employees(employees_not_make_checkin, subject="You Did Not Make Check-in", message="You did not make IN in the system")
        send_employees_to_manager(employees_not_make_checkin, subject="Employees Not Make Check-In in System",)


def checkout() -> None:
    employees_not_make_checkout = get_employees("OUT")
    if employees_not_make_checkout:
        send_email_to_employees(employees_not_make_checkout, subject="You Did Not Make Check-out", message="You did not make OUT in the system")
        send_employees_to_manager(employees_not_make_checkout, subject="Employees Not Make Check-OUT in System",)


def get_employees(log_type: str) -> list[frappe._dict]:
    employees = frappe.db.sql(
        f"""
        SELECT
            emp.name, emp.employee_name, emp.email, emp.user_id
        FROM `tabEmployee` AS emp
        WHERE
            NOT EXISTS (
                SELECT *
                FROM `tabRecord Attendance` AS rec_atten
                WHERE
                    emp.name = rec_atten.name1 AND 
                    rec_atten.log_type = "{log_type}" AND 
                    rec_atten.attendance_time >= "{nowdate() + ' 00:00:00'}" AND 
                    rec_atten.attendance_time <= "{now_datetime()}"
            )
        ;
        """,
        as_dict=1,
        )
    return employees


def send_email_to_employees(employees: list[frappe._dict], subject: str, message: str) -> None:
    employees_emails = []
    if employees:
        for emp in employees:
            if emp.get("email"):
                employees_emails.append(emp.get("email"))
            else:
                if emp.get("user_id"):
                    employees_emails.append(emp.get("user_id"))
    if employees_emails:
        email_args= {
        'recipients': employees_emails,
        'subject': subject,
        'message': message,
        }
        frappe.enqueue(
            method=frappe.sendmail,
            queue="default",
            is_async=True,
            now=True,
            job_name="employees_not_make_checkin",
            **email_args,
        )


def send_employees_to_manager(employees: frappe._dict, subject: str,) -> None:
    email_args= {
        'recipients': "magdy.abouelatta@700apps.net",
        'subject': subject,
        'message': "\n".join([emp.get("employee_name") for emp in employees]),
        }
    frappe.enqueue(
            method=frappe.sendmail,
            queue="default",
            is_async=True,
            now=True,
            job_name="employees_not_make_checkin",
            **email_args,
        )
