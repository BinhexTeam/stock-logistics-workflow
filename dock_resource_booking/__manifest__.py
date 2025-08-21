{
    "name": "Dock Resource Booking",
    "summary": "Manage dock reservations for loading/unloading using OCA resource booking.",
    "version": "16.0.1.0.0",
    "category": "Warehouse",
    "author": "Odoo Community Association (OCA), Binhex",
    "website": "https://github.com/OCA/stock-logistics-workflow",
    "license": "AGPL-3",
    "depends": ["stock", "delivery", "resource_booking", "delivery_dropoff_site"],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_picking_views.xml",
        "views/resource_booking_views.xml",
        "views/menu_views.xml",
    ],
}
