# Copyright (c) 2025, Vinay Mishra and contributors
# For license information, please see license.txt


# filename: airplane_mode/airplane_mode/doctype/airplane_flight/airplane_flight.py
import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils.background_jobs import enqueue

class AirplaneFlight(WebsiteGenerator):
    def on_submit(self):
        self.status = 'Completed'


def on_update(doc, method=None):
    """DocType hook: when gate changes, sync it to all linked tickets."""
    # Skip if the DocType has no gate field defined.
    if not doc.meta.has_field("gate_number"):
        return

    if doc.is_new():
        return

    old_gate = frappe.db.get_value(doc.doctype, doc.name, "gate_number")
    if old_gate == doc.gate_number or not doc.gate_number:
        return

    enqueue(
        update_ticket_gates,
        queue="long",
        job_name=f"Update ticket gates for flight {doc.name}",
        flight_name=doc.name,
        new_gate=doc.gate_number,
    )


def update_ticket_gates(flight_name: str, new_gate: str):
    """Background job: update gate number in all tickets linked to a flight."""
    tickets = frappe.get_all("Airplane Ticket", filters={"flight": flight_name}, pluck="name")
    for ticket in tickets:
        frappe.db.set_value("Airplane Ticket", ticket, "gate_number", new_gate, update_modified=False)
    frappe.db.commit()
