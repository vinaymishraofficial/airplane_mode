# Copyright (c) 2025, Vinay Mishra and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.website.website_generator import WebsiteGenerator


class AirportShop(WebsiteGenerator):
	def autoname(self):
		"""Override route generation to avoid double route prefix."""
		from frappe.utils import slugify
		if not self.route and self.shop_name:
			# Generate route from shop_name only, without parent route prefix
			self.route = slugify(self.shop_name)
	
	def before_save(self):
		# Fix route if it has double prefix
		if self.route and self.route.startswith("airport-shop/airport-shop/"):
			self.route = self.route.replace("airport-shop/airport-shop/", "")
		elif self.route and self.route.startswith("airport-shop/"):
			self.route = self.route.replace("airport-shop/", "")
		
		# Validate that shop type is enabled
		if self.shop_type:
			shop_type = frappe.get_cached_doc("Shop Type", self.shop_type)
			if not shop_type.enabled:
				frappe.throw(f"Shop Type '{self.shop_type}' is disabled. Please select an enabled shop type.")
		
		# Check if the status is being changed to 'Available'
		if self.status == "Available":
			# Clear tenant details and contract expiry fields
			self.tenant_details = None
			self.contract_expiry = None
			
			frappe.msgprint(_("Tenant details and contract expiry have been cleared because the shop is now available."), alert=True)


@frappe.whitelist()
def get_enabled_shop_types():
	"""Return only enabled shop types for link field filter."""
	return {
		"filters": {
			"enabled": 1
		}
	}


def get_list_context(context):
	"""Override default list context to filter by enabled shop types only."""
	context.no_cache = 1
	
	# Add custom get_list method
	original_get_list = context.get("get_list")
	
	def get_filtered_list(doctype, txt, filters, limit_start, limit_page_length=20, order_by=None):
		"""Get only shops with enabled shop types."""
		# Add filter for enabled shop types
		shops = frappe.get_all(
			"Airport Shop",
			filters=[
				["shop_type", "in", frappe.get_all("Shop Type", filters={"enabled": 1}, pluck="name")]
			],
			fields=["name", "shop_name", "shop_type", "airport", "status", "route", "shop_number", "area_sqft"],
			start=limit_start,
			page_length=limit_page_length,
			order_by=order_by or "modified desc"
		)
		return shops
	
	context.get_list = get_filtered_list


def get_permission_query_conditions(user):
	"""Filter list view in desk to show only shops with enabled shop types."""
	if not user:
		user = frappe.session.user
	
	return """
		`tabAirport Shop`.shop_type IN (
			SELECT name FROM `tabShop Type` WHERE enabled = 1
		)
	"""