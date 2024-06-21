{
    'name': "Shipio Customization",
    'author': "Samah Shahla",
    'category': 'Inventory/Inventory',
    'version': '17.0.0.1.0',
    'depends': ['base', 'contacts', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner.xml',
        'views/product_template.xml',
        'views/shipments.xml',
        'views/report_customer_location.xml',
        'views/report_shipments.xml',
        'views/report_all_products.xml',
    ],
    'application': False,
}
