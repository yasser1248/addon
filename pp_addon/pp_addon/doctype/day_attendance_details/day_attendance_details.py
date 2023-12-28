# Copyright (c) 2023, magdyabouelatta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime, time_diff_in_hours, nowdate, now_datetime


class DayAttendanceDetails(Document):
    pass


def update_day_attendance(doc):
    day_attendance_details = check_day_attendance_details(doc)
    day_attendance_details_child = check_day_attendance_details_child(
        doc,
        day_attendance_details,
    )


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
        day_attendance_details.day = day.date()
    day_attendance_details.save(ignore_permissions=True)
    return day_attendance_details


def check_day_attendance_details_child(doc: Document, day_attendance_details: Document) -> Document:
    if day_attendance_details_child := frappe.db.exists(
        "Day Attendance Details Child",
        {
            "employee": doc.get("name1"),
            "parent": day_attendance_details.get("name"),
        },
    ):
        day_attendance_details_child = frappe.get_doc(
            "Day Attendance Details Child", day_attendance_details_child
        )
        

    else:
        day_attendance_details_child = day_attendance_details.append("day_details", {"employee": doc.get("name1")})

    day_attendance_details_child = set_fields(doc, day_attendance_details, day_attendance_details_child)
    day_attendance_details_child = update_total_working(doc, day_attendance_details, day_attendance_details_child)
    return day_attendance_details_child


def set_fields(
    doc: Document,
    day_attendance_details: Document,
    day_attendance_details_child: Document,
):
    FIELDS = {
        "IN": "in",
        "OUT": "out",
        "Exit": "exit",
        "Enter": "enter",
    }
    day_attendance_details_child.set(
        FIELDS[doc.get("log_type")], doc.get("attendance_time")
    )
    # set status and late_time fields
    if FIELDS[doc.get("log_type")] == "in":
        late_time = time_diff_in_hours(
            get_datetime(nowdate() + " 08:00:00"),
            doc.get("attendance_time"),
        )
        if late_time == 0:
            day_attendance_details_child.set("status", "On Time")
            day_attendance_details_child.set("late_time", late_time)
        elif late_time < 0:
            day_attendance_details_child.set("status", "Late")
            day_attendance_details_child.set("late_time", abs(late_time))
        else:
            ...

    day_attendance_details_child = day_attendance_details_child.save(ignore_permissions=True)
    return day_attendance_details_child



def update_total_working(
    doc: Document,
    day_attendance_details: Document,
    day_attendance_details_child: Document,
):

    if (
        day_attendance_details_child.get("in")
        and day_attendance_details_child.get("out")
    ):

        total_working = time_diff_in_hours(
            day_attendance_details_child.get("out"),
            day_attendance_details_child.get("in"),
        )
        if day_attendance_details_child.get(
            "exit"
        ) and day_attendance_details_child.get("enter"):
            total_working -= time_diff_in_hours(
                day_attendance_details_child.get("enter"),
                day_attendance_details_child.get("exit"),
            )

        day_attendance_details_child.set("total_working", total_working)

        day_attendance_details_child.save(ignore_permissions=True)
