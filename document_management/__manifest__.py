{
    'name': 'Document Management',
    'version': '1.0',
    'summary': 'Module for managing documents with versioning and customer tagging',
    'description': 'This module allows you to manage documents with versioning and tag them to customers.',
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'category': 'Uncategorized',
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/document_views.xml',
    ],
    'installable': True,
    'application': True,
}