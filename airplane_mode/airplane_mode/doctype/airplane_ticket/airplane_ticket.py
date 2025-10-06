# Copyright (c) 2025, Vinay Mishra and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document
import random

class AirplaneTicket(Document):

    def validate(self):
        self.remove_duplicate_addons()
        self.calculate_total_amount()

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

    def calculate_total_amount(self):
        """Total Amount = Flight Price + sum of all add-on amounts"""
        child_row_total_amount = sum([row.amount for row in self.add_ons])
        self.total_amount = (self.flight_price or 0) + child_row_total_amount

    def before_insert(self):
        # Generate random seat number
        number = random.randint(1, 99)  # Random number between 1 and 99
        letter = random.choice(['A', 'B', 'C', 'D', 'E'])  # Random letter
        self.seat = f"{number}{letter}"

    def on_submit(self):
        if self.status != "Boarded":
            frappe.throw("Only tickets with status 'Boarded' can be submitted.")
    
