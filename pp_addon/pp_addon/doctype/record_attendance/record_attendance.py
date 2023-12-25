# Copyright (c) 2023, magdyabouelatta and contributors
# For license information, please see license.txt

from datetime import datetime, date

import frappe
from frappe.model.document import Document

from pp_addon.pp_addon.doctype.day_attendance_details.day_attendance_details import update_day_attendance


class RecordAttendance(Document):
    def validate(self):

        today = frappe.utils.getdate(self.get("attendance_time"))
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())

        if (doc := frappe.db.exists(
            "Record Attendance",
            {
                "name1": self.get("name1"),
                "attendance_time": ["between", (start_of_day, end_of_day)],
                "log_type": self.get("log_type"),
                "name": ["!=", self.name],
            },
        )):
            frappe.throw(
                msg=f"Employee is aleardy present on {today}", title="Already Presen t"
            )

    def before_save(self):
        update_day_attendance(self)
