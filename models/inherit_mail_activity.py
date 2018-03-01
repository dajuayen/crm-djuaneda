# -*- coding: utf-8 -*-
# modify mail.activity, method  action_create_calendar_event.

from odoo import api, models, fields, tools, _

# from wdb import set_trace as depurador

class MailActivity(models.Model):
    _inherit = "mail.activity"

    done = fields.Boolean(default=False)

    @api.multi
    def action_create_calendar_event(self):
        """
        Modified functionality of the method:
        If meeting is created from contact / client, the name of the client +
        name of the contact is automatically put in the subject of the meeting
        :return:
        """
        self.ensure_one()
        print('******************* OVERRIDE action_create_calendar_event MAIL ACTIVITY ****************')
        # depurador()
        action = self.env.ref('calendar.action_calendar_event').read()[0]
        message = self.summary
        attends = []
        try:
            customer = self.env['res.partner'].search([('id', '=', self.env.context.get('default_res_id'))])
            if customer and customer.is_company:
                message = "{} - {}".format(customer.name, message)
            else:
                message = "{}, {} - {}".format(customer.commercial_company_name,
                                               customer.name,
                                               message)
                attends.append(customer)
        except :
            pass


        action['context'] = {
            'default_activity_type_id': self.activity_type_id.id,
            'default_res_id': self.env.context.get('default_res_id'),
            'default_res_model': self.env.context.get('default_res_model'),
            'default_name': message,
            'default_description': self.note and tools.html2plaintext(self.note) or '',
            'default_activity_ids': [(6, 0, self.ids)],
            #'default_partner_ids':attends,
        }
        return action


    def action_feedback(self, feedback=False):
        message = self.env['mail.message']
        if feedback:
            self.write(dict(feedback=feedback))
        for activity in self:
            record = self.env[activity.res_model].browse(activity.res_id)
            activity.done = True
            record.message_post_with_view(
                'mail.message_activity_done',
                values={'activity': activity},
                subtype_id=self.env.ref('mail.mt_activities').id,
                mail_activity_type_id=activity.activity_type_id.id,
            )
            message |= record.message_ids[0]
        return message.ids and message.ids[0] or False

    @api.multi
    def read(self, fields=None, load='_classic_read', *args, **kwargs):
        """ Override to explicitely call check_access_rule, that is not called
            by the ORM. It instead directly fetches ir.rules and apply them. """
        data = super(MailActivity, self).read(fields=fields, load=load)
        result = []
        for row in data:
            activity = self.env['mail.activity'].browse(row['id'])
            if not activity.done:
                result.append(row)
        return result

    # @api.model
    # def default_get(self, fields):
    #     res = super(MailActivity, self).default_get(fields)
    #     if not fields or 'res_model_id' in fields and res.get('res_model'):
    #         res['res_model_id'] = self.env['ir.model']._get(res['res_model']).id
    #     return res

    @api.model
    def create(self, values):
        # depurador()
        # already compute default values to be sure those are computed using the current user
        values_w_defaults = self.default_get(self._fields.keys())
        values_w_defaults.update(values)

        # continue as sudo because activities are somewhat protected
        activity = super(MailActivity, self.sudo()).create(values_w_defaults)
        activity_user = activity.sudo(self.env.user)
        activity_user._check_access('create')
        self.env[activity_user.res_model].browse(activity_user.res_id).message_subscribe(partner_ids=[activity_user.user_id.partner_id.id])
        if activity.date_deadline <= fields.Date.today():
            self.env['bus.bus'].sendone(
                (self._cr.dbname, 'res.partner', activity.user_id.partner_id.id),
                {'type': 'activity_updated', 'activity_created': True})
        return activity_user

    @api.onchange('done')
    def _onchange_done(self):
        if self.done:
            self.state = None
