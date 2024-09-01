{
    'name': 'CU - Delivery Filter',
    'summary': '''
        Filter products by delivery address selected on modal form: Province and Municipality
    ''',
    'description': """CU - Delivery Filter""",
    'category': 'Website',
    'version': '17.0.1.0.10',
    'author': 'BarSoft',
    'website': 'https://github.com/Barceloch',
    'license': 'OPL-1',
    'price': 0.00,
    'currency': 'USD',
    'depends': ['base', 'website','product', 'contacts', 'sale', 'website_sale', 'web', 'delivery'],
    'data': [
        'security/ir.model.access.csv',
        'data/cuba_locations.xml',
        'views/delivery_filter_template.xml',
        'views/product_form_template.xml',
        'views/product_template_views.xml',
        'views/delivery_carrier_view.xml',
        'views/res_partner_views.xml',
        'views/address_template.xml',
        'views/product_snippets.xml',
        
    ],
    #'images': ['static/description/banner.jpg'],
    'assets': {
        'web.assets_frontend': [
            "cu_delivery_filter/static/src/js/delivery_filter.js",
            #"cu_delivery_filter/static/src/js/error_handling.js",
            #"cu_delivery_filter/static/src/css/custom.css",
        ],
    },
    #"images": ['static/description/banner.png'],
    'installable': True,
}
