# -*- coding: utf-8 -*-
{
    'name': "Bliss ERP Solution",
    'summary': """Custumisation for F-tech.""",
    'description': """
        Custumisation for F-tech
    """,
    'author': "Bliss ERP Solution",
    'website': "https://www.blisserpsolution.com",
    'category': '',
    'version': '17.0.1.0.0',
    'sequence': 1,
    'depends': ['base', 'product', 'sale', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_form_view.xml',
        'views/sale_order_view.xml',
        'views/product_view_kanban_catalog.xml',
        'views/product_view.xml',
        'views/product_template_search_view.xml',
        'wizard/view_sale_order_line_to_purchase_wizard_form.xml',
        'wizard/sale_order_line_import_wizard_view.xml'

    ],
    'images': ['static/description/icon.png'],
    'application': True,
    'installable': True,
    'support': 'contact@blisserpsolution.com',
}
