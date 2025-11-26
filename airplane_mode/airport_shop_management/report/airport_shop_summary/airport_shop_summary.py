# Copyright (c) 2025, Vinay Mishra and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = [
        {"label": "Airport", "fieldname": "airport", "fieldtype": "Link", "options": "Airport", "width": 180},
        {"label": "Total Shops", "fieldname": "total_shops", "fieldtype": "Int", "width": 120},
        {"label": "Occupied", "fieldname": "occupied", "fieldtype": "Int", "width": 110},
        {"label": "Available", "fieldname": "available", "fieldtype": "Int", "width": 110},
    ]

    data = []
    airports = frappe.get_all("Airport", pluck="name")

    for a in airports:
        total = frappe.db.count("Airport Shop", {"airport": a})
        occupied = frappe.db.count("Airport Shop", {"airport": a, "is_occupied": 1})
        available = total - occupied
        data.append({
            "airport": a,
            "total_shops": total,
            "occupied": occupied,
            "available": available
        })

    return columns, data
