# -*- coding: utf-8 -*-
{
    'name': "bds",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'downloadwizard','website','website_sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/data.xml',
        'views/viewbds.xml',
        'views/cron.xml',
        'views/fetch.xml',
        'views/import_quan.xml',
        'views/bds_search.xml',
        'views/bds_form.xml',
        'views/bds_list.xml',
        
        'views/poster.xml',
        'views/downloadbds.xml',
        'views/quan.xml',
        'views/error.xml',
        'views/templatebds.xml',
        'views/tproduct_item.xml',
        'views/tproduct_detail.xml',
        'views/tproducts.xml',
        'views/url.xml',
#         'views/garbage/respartner.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}