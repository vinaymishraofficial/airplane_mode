// frappe.ready(function() {
// 	const applyShopType = (shop) => {
// 		if (!shop) {
// 			frappe.web_form.set_value("shop_type", "");
// 			return;
// 		}
// 		frappe.db.get_value("Airport Shop", shop, "shop_type")
// 			.then(({ message }) => frappe.web_form.set_value("shop_type", message?.shop_type || ""))
// 			.catch(() => frappe.web_form.set_value("shop_type", ""));
// 	};

// 	const params = new URLSearchParams(window.location.search);
// 	const shopFromQuery = params.get("shop");
// 	if (shopFromQuery) {
// 		frappe.web_form.set_value("shop", shopFromQuery);
// 		applyShopType(shopFromQuery);
// 	}

// 	frappe.web_form.on("shop", (_, value) => applyShopType(value));
// });