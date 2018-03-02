# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import except_orm, UserError, ValidationError, RedirectWarning, Warning


class Lead(models.Model):
    _inherit = 'crm.lead'

    # modificación para que en el muro no sigan apareciendo las actividades hechas
    activity_ids = fields.One2many(
        'mail.activity', 'res_id', 'Activities',
        auto_join=True,
        groups="base.group_user",
        domain=lambda self: [('res_model', '=', self._name), ('done','!=', True)])

    # activity_dones = fields.Boolean(related='activity_ids.done',
    #     readonly=True,
    #     groups="base.group_user")


    previous_stage_id = fields.Many2one('crm.stage', string='Previous Stage', track_visibility='onchange',
        domain="['|', ('team_id', '=', False), ('team_id', '=', team_id)]",
        group_expand='_read_group_stage_ids', default=None)


    # @api.multi
    @api.onchange('stage_id')
    def _onchange_stage_id(self):
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
            return {'warning': err_msg}

            action_id = self.env.ref('crm.crm_lead_opportunities_tree_view').id
            raise RedirectWarning(
                err_msg, action_id, _('Back'))

        values = self._onchange_stage_id_values(self.stage_id.id)
        self.update(values)
        # return {'type': 'ir.actions.client', 'tag': 'reload'}

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

