# -*- coding: utf-8 -*-
{
    'name': "Bliss ERP Solution ",
    'summary': """Custumisation for Kajal.""",
    'description': """
        Custumisation for Kajal
    """,
    'author': "Bliss ERP Solution",
    'website': "https://www.blisserpsolution.com",
    'category': 'Sales',
    'version': '17.0.1.0.0',
    'sequence': 1,
    'depends': ['product', 'sale_management'],
    'data': [
        'report/kpp_bank.xml',
        'report/kps_bank.xml',

        'views/product_views.xml',
        'views/sale_order_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'application': True,
    'installable': True,
    'support': 'contact@blisserpsolution.com',
}
