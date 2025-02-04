# customer_health/__manifest__.py
{
    'name': 'Customer Health Management',
    'version': '1.0',
    'category': 'Customer Relationship',
    'summary': 'Create By. Pongsakorn',
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/customer_health_menu.xml',
        'views/customer_health_views.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': True,
}
