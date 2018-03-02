# -*- coding: utf-8 -*-

from odoo import api, fields, models
from wdb import set_trace as depurador

class Partner(models.Model):
    _inherit = 'res.partner'

    opportunity_count_lost = fields.Integer("Opportunity lost", compute='_compute_opportunity_lost_count')
    contact_origin = fields.Many2one('res.partner', string='Contact origin')
    send_advertising = fields.Selection([('si','Si'),('no','No'),('no_lopd','No - LOPD')])
    hardware_supplier = fields.Many2one('res.partner', string='Hardware supplier')
    erp_supplier = fields.Many2one('res.partner', string='ERP supplier')
    web_supplier = fields.Many2one('res.partner', string='WEB supplier')
    consultant = fields.Many2one('res.partner', string='Consultant')
    associate = fields.Many2one('res.partner', string='Asociate')
    n_of_employees = fields.Selection([('1',' 1 - 5 '),
                                       ('2',' 6 - 10 '),
                                       ('3',' 11 - 25 '),
                                       ('4',' 26 - 50 '),
                                       ('5',' 51 - 100'),
                                       ('6',' Más de 100 '),],
                                        default='1')
    annual_turnover = fields.Selection([('1',' hasta 100k '),
                                        ('2',' hasta 500k '),
                                        ('3',' hasta 1M '),
                                        ('4',' hasta 3M'),
                                        ('5',' hasta 6M'),
                                        ('6',' más de 6M '),],
                                        default='1')
    company_size = fields.Selection([('1',' autónomo'),
                                     ('2',' pequeña'),
                                     ('3',' mediana '),
                                     ('4',' grande'),
                                     ('5',' multinacional ')],
                                    default='1')
    cnae_code = fields.Char(size=4, string='CNAE code')
    is_hardware_supplier = fields.Boolean(default=False, string='Is hardware supplier')
    is_erp_supplier = fields.Boolean(default=False, string='Is ERP supplier')
    is_web_supplier = fields.Boolean(default=False, string='Is WEB supplier')
    is_consultant = fields.Boolean(default=False, string='Is consultant')
    is_associate = fields.Boolean(default=False, string='Is associate')

    @api.multi
    def _compute_opportunity_lost_count(self):
        for partner in self:
            operator = 'child_of' if partner.is_company else '='  # the opportunity count should counts the opportunities of this company and all its contacts
            partner.opportunity_count_lost = self.env['crm.lead'].search_count(
                [('partner_id', operator, partner.id),
                 ('type', '=', 'opportunity'),
                 ('active', '=', False),
                 ('probability','=','0')])

    @api.multi
    def _compute_meeting_count(self):
        for partner in self:
            partner.meeting_count = len(partner.meeting_ids)
            if partner.is_company:
                workers = self.env['res.partner'].search([('parent_id', '=', partner.id)])
                for w in workers:
                    partner.meeting_count += len(w.meeting_ids)
