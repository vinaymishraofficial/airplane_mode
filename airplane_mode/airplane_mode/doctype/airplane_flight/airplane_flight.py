# Copyright (c) 2025, Vinay Mishra and contributors
# For license information, please see license.txt


# filename: airplane_mode/airplane_mode/doctype/airplane_flight/airplane_flight.py
import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils.background_jobs import enqueue

class AirplaneFlight(WebsiteGenerator):
    def on_submit(self):
        self.status = 'Completed'

    def on_update(self):
        """Check if gate number changed and enqueue background update to linked tickets."""
        if self.is_new():
            return

        old_gate = self.get_db_value("gate_number")
        if old_gate != self.gate_number:
            enqueue(
                update_ticket_gates,
                queue="long",
                job_name=f"Update ticket gates for flight {self.name}",
                flight_name=self.name,
                new_gate=self.gate_number,
            )


def update_ticket_gates(flight_name: str, new_gate: str):
    """Background job: update gate number in all tickets linked to a flight."""
    tickets = frappe.get_all("Ticket", filters={"flight": flight_name}, pluck="name")
    for t in tickets:
        frappe.db.set_value("Ticket", t, "gate_number", new_gate, update_modified=False)
    frappe.db.commit()
