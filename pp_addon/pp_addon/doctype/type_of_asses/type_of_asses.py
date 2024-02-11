# Copyright (c) 2023, magdyabouelatta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Typeofasses(Document):
	def before_save(self):
		assessment_list = frappe.get_all("Type of asses",fields=["name","weight"])
		if len(assessment_list) > 0:
			max_weight = 0
			for item in assessment_list:
				max_weight += item.get('weight')
			if max_weight+self.weight > 100:
				frappe.throw("Sum of weights must be less than or equal to 100%")
