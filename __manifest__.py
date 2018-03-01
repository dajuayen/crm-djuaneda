# -*- coding: utf-8 -*-
{
    'name':'SDI CRM 2',
    'version':'1.0.0.1',
    'category':'',
    'author':['Javier Izco',
            'David Juaneda'],
    #'website':'https://github.com/oscars8a/mymodules.git',
    'license':'GPL-3',
    'depends':['base','crm'],
    'data':[
        'views/crm_sdi_templates.xml',
        #
        'views/inherit_crm_views_leads.xml',
        'views/inherit_crm_views_oppor.xml',
        #
        'views/inherit_res_partner_views.xml',
        #
        'views/inherit_view_res_partner_filters.xml',
        'views/inherit_view_crm_case_opportunities_filter.xml',
        #
        'views/inherit_calendar_views.xml',
        #
        'views/inherit_mail_activity_views.xml',
        #'wizard/throw_popup.xml',
        #'security/ir.model.access.csv',
    ],
    'demo':[ ],
    'installable':True,
}
