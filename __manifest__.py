# -*- coding: utf-8 -*-
{
    'name':'DAVID-SDI_CRM',
    'version':'1.0.0.1',
    'category':'',
    'author':['David Juaneda'],
    'website':'https://github.com/Dajuayen/crm-djuaneda.git',
    'license':'GPL-3',
    'depends':['base','crm'],
    'data':[
        'views/crm_sdi_templates.xml',
        'views/inherit_crm_views_leads.xml',
        'views/inherit_crm_views_oppor.xml',
        'views/inherit_res_partner_views.xml',
        'views/inherit_view_res_partner_filters.xml',
        'views/inherit_view_crm_case_opportunities_filter.xml',
        'views/inherit_calendar_views.xml',
        'views/inherit_mail_activity_views.xml',
    ],
    'demo':[ ],
    'installable':True,
}
