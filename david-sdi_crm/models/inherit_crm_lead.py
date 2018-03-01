# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import except_orm, UserError, ValidationError, RedirectWarning, Warning


class Lead(models.Model):
    _inherit = 'crm.lead'

    # editable =
    activity_ids = fields.One2many(
        'mail.activity', 'res_id', 'Activities',
        auto_join=True,
        groups="base.group_user",
        domain=lambda self: [('res_model', '=', self._name), ('done','=', False)])

    previous_stage_id = fields.Many2one('crm.stage', string='Previous Stage', track_visibility='onchange',
        domain="['|', ('team_id', '=', False), ('team_id', '=', team_id)]",
        group_expand='_read_group_stage_ids', default=None)

    @api.multi
    @api.onchange('stage_id')
    def _onchange_stage_id_b(self):
        """
        comprueba que la oportunidad puede cambiar de etapa en función de si tiene datos
        el campo date_deadline.
        values = self._onchange_stage_id_values(self.stage_id.id)
        self.update(values)
        :return:
        """
        self.ensure_one()
        if not self.date_deadline or self.planned_revenue <= 0:
            values = {"stage_id": 1}
            self.update(values)
            err_msg = _("""
                No se puede cambiar de estado si la oportunidad carece de:
                - fecha de cierre
                - cantidad mayor a 0
                """)
            '''
            err_msg = _('You must define at least one product category in order to be able to create products.')
            redir_msg = _('Go to Internal Categories')
            raise RedirectWarning(err_msg, self.env.ref('product.product_category_action_form').id, redir_msg)
            '''
            action_id = self.env.ref('crm.crm_lead_opportunities_tree_view').id
            raise RedirectWarning(
                err_msg, action_id, _('Back'))

        if self.stage_id.sequence == 3 and not self.previous_stage_id.sequence ==   2:
            values = {"stage_id": self.previous_stage_id}
            self.update(values)
            err_msg = _("""
                            No se puede cambiar una oportunidad a estado ganada
                            si no procede del estado anterior (validada).
                            """)
            warning_mess = {
                'type': 'ir.actions.client',
                'tag': 'action_warn',
                'name':'Warning',
                'params':{
                    'title': _('Secuencia de oportunidad no completada!'),
                    'text': _("""
                            No se puede cambiar una oportunidad a estado ganada
                            si no procede del estado anterior (validada).
                            """),
                    'sticky':True
                }

            }

            warning_mess2 = {
                'type': 'ir.actions.client',
                #'tag': 'my_reload',
                'title': _('Secuencia de oportunidad no completada!'),
                'message': err_msg,
                'class':'mi_clase'
            }

            return {'warning':warning_mess2}

        return {'type': 'ir.actions.client', 'tag': 'reload'}

    @api.multi
    def reload_page(self):
        return {
            'name': _('AVISO'),
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'view_type': 'form',
            'view_id': 'action_wizard_kanban_popup',
            'views': [[False, 'list'], [False, 'kanban'], [False, 'form']],
        }

    @api.multi
    def write(self, vals):
        # stage change: update date_last_stage_update
        if 'stage_id' in vals:
            vals['date_last_stage_update'] = fields.Datetime.now()
            vals["previous_stage_id"] = self.stage_id.id
        if vals.get('user_id') and 'date_open' not in vals:
            vals['date_open'] = fields.Datetime.now()
        # stage change with new stage: update probability and date_closed
        if vals.get('stage_id') and 'probability' not in vals:
            vals.update(self._onchange_stage_id_values(vals.get('stage_id')))
        if vals.get('probability', 0) >= 100 or not vals.get('active', True):
            vals['date_closed'] = fields.Datetime.now()
        elif 'probability' in vals:
            vals['date_closed'] = False
        return super(Lead, self).write(vals)
