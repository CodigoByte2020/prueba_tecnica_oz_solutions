{
    'name': 'Prueba tecnica Oz Solutions',
    'summary': 'Módulo de Ventas',
    'description': 'Prueba técnica para desarrollador Odoo.',
    'author': 'Contreras Pumamango Gianmarco - gmcontrpuma@gmail.com',
    'website': 'https://github.com/CodigoByte2020',
    'category': 'Tools',
    'version': '14.0.0.0.1',
    'depends': [
        'stock',
        'account'
    ],
    'data': [
        'data/notification_shipping_products.xml',
        'security/ir.model.access.csv',
        'views/stock_picking_views.xml',
        'views/res_partner_views.xml',
        'views/overdue_customer_invoices.xml',
        'wizards/shipping_products_views.xml',
        'wizards/account_move_reversal_views.xml',
        'reports/stock_balance_report_views.xml'
    ],
    'installable': True,
}
