# Copyright (c) 2025, Vinay Mishra and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document
import random

class AirplaneTicket(Document):

    def validate(self):
        self.remove_duplicate_addons()

    def remove_duplicate_addons(self):
        seen = set()                                                        # added a blank set here
        unique_rows = []                                                    # to store unique rows
        for row in self.add_ons:                                            # iterate through child table rows
            if row.item not in seen:                                        # check if item is already in set
                seen.add(row.item)                                          # if not, add to set
                unique_rows.append(row)                                     # and to unique rows list
         # after loop ends, we have only unique rows in unique_rows list
         # replace with only unique rows
        self.set("add_ons", unique_rows)

	# Implement the controller to compute total amount
    def before_save(self):
        add_on_amount = sum(add_on.amount for add_on in self.add_ons)
        self.total_amount = self.flight_price + add_on_amount

    def before_insert(self):
        # Generate random seat number
        number = random.randint(1, 99)  # Random number between 1 and 99
        letter = random.choice(['A', 'B', 'C', 'D', 'E'])  # Random letter
        self.seat = f"{number}{letter}"

        # Perform the validation in airline capacity
        airplane_flight = self.flight
        airplane = frappe.get_doc("Airplane Flight", airplane_flight).airplane
        capacity = frappe.get_doc("Airplane", airplane).capacity
        total_tickets = frappe.db.count('Airplane Ticket', filters={'flight': airplane_flight})
        
        if total_tickets > capacity:
            frappe.throw(f"The number of tickets for {airplane} exceeds the airplane's capacity: {capacity}.")

    def on_submit(self):
        if self.status != "Boarded":
            frappe.throw("Only tickets with status 'Boarded' can be submitted.")

