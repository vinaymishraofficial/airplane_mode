import frappe

def execute():
    tickets = frappe.get_all("Airplane Ticket", fields=["name"])
    for ticket in tickets:
        doc = frappe.get_doc("Airplane Ticket", ticket.name)
        if not doc.seat:
            # Generate random seat number
            import random
            number = random.randint(1, 99)  # Random number between 1 and 99
            letter = random.choice(['A', 'B', 'C', 'D', 'E'])  # Random letter
            frappe.db.set_value("Airplane Ticket", doc.name, "seat", f"{number}{letter}")
            print(f"Updated seat for ticket {doc.name} to {f'{number}{letter}'}")
    frappe.db.commit()