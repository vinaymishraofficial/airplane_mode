# Copyright (c) 2025, Vinay Mishra and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document

class AirplaneFlight(Document):
	pass

	def on_submit(self):
		frappe.db.set_value(self.doctype, self.name, 'status', 'Completed')
