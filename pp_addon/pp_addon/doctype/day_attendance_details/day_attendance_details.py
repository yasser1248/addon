# Copyright (c) 2023, magdyabouelatta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime, time_diff_in_hours


class DayAttendanceDetails(Document):
    pass


def update_day_attendance(doc):
    day_attendance_details = check_day_attendance_details(doc)
    day_attendance_details_child = check_day_attendance_details_child(
        day_attendance_details
    )
    set_fields(doc, day_attendance_details, day_attendance_details_child)
    update_total_working(doc, day_attendance_details, day_attendance_details_child)

    day_attendance_details.save(ignore_permissions=True)
    frappe.throw(str(day_attendance_details_child.get("employee")))
    # day_attendance_details_child.save(ignore_permissions=True)


def check_day_attendance_details(doc: Document) -> Document:
    day = get_datetime(doc.get("attendance_time"))
    if day_attendance_details := frappe.db.exists(
        "Day Attendance Details", str(day.date())
    ):
        day_attendance_details = frappe.get_doc(
            "Day Attendance Details", day_attendance_details
        )
    else:
        day_attendance_details = frappe.new_doc("Day Attendance Details")
        day_attendance_details.day = str(day.date())
    return day_attendance_details


def check_day_attendance_details_child(day_attendance_details: Document) -> Document:
    if day_attendance_details_child := frappe.db.exists(
        "Day Attendance Details Child",
        {
            "employee": day_attendance_details.get("name1"),
            "parent": day_attendance_details.get("name"),
        },
    ):
        day_attendance_details_child = frappe.get_doc(
            "Day Attendance Details Child", day_attendance_details_child
        )
    else:
        day_attendance_details_child = frappe.new_doc(
            "Day Attendance Details Child",
            parent_doc=day_attendance_details,
            parentfield="day_details",
            employee=day_attendance_details.get("name1"),
        )
    return day_attendance_details_child


def set_fields(
    doc: Document,
    day_attendance_details: Document,
    day_attendance_details_child: Document,
):
    FIELDS = {
        "IN": "check_in",
        "OUT": "check_out",
        "Exit": "exit",
        "Enter": "enter",
    }
    day_attendance_details_child.set(
        FIELDS[doc.get("log_type")], doc.get("attendance_time")
    )


def update_total_working(
    doc: Document,
    day_attendance_details: Document,
    day_attendance_details_child: Document,
):
    if (
        doc.get("log_type") == "OUT"
        and day_attendance_details_child.get("check_in")
        and day_attendance_details_child.get("check_out")
    ):
        total_working = time_diff_in_hours(
            day_attendance_details_child.get("check_out"),
            day_attendance_details_child.get("check_in"),
        )
        if day_attendance_details_child.get(
            "exit"
        ) and day_attendance_details_child.get("enter"):
            total_working -= time_diff_in_hours(
                day_attendance_details_child.get("enter"),
                day_attendance_details_child.get("exit"),
            )

        day_attendance_details_child.set("total_working", total_working)
