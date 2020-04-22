# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta, MO, SU
from openerp.exceptions import UserError
from odoo import models , fields , api , _
from datetime import datetime, date, timedelta


class EventRegistration(models.Model):
    _inherit = 'event.registration'
    
    membership_product_id = fields.Many2one(
        'product.product',
        string='Membership Product',
    )
    membership_payment_id = fields.Many2one(
        'product.template',
        string="Membership Payment",
    )

#     @api.onchange('partner_id')
#     def onchange_partner(self):
#         for line in self.partner_id.member_lines:
#             if line.membership_id.product_tmpl_id.product_type_id == self.event_id.event_type_id:
#                 self.membership_payment = line.membership_id.name

    @api.model
    @api.constrains('partner_id', 'event_id')
    def _validate_attendee(self):
        today = fields.date.today()
        
        week_start = today + relativedelta(weekday=MO(-1))
        week_end = today + relativedelta(weekday=SU(+1))
        
        month_start = today.replace(day=1)  # month start date
        month_end = str(today + relativedelta(months=+1, day=1, days=-1))[:10]  # month end date
        
        for rec in self:
            member = rec.partner_id
            event = rec.event_id
            event_type = event.event_type_id
            
            attend_in_month = 0
            attend_in_week = 0
            
            if member and event_type:
                self._cr.execute("""
                        SELECT
                            reg.id
                        FROM
                            event_registration reg
                        LEFT JOIN event_event event
                            ON event.id = reg.event_id
                        WHERE
                            reg.partner_id IS NOT NULL AND
                            event.event_type_id=%s AND
                            reg.partner_id=%s AND
                            event.date_begin::date >= '%s' AND
                            event.date_begin::date <= '%s'
                    """ % (event_type.id, member.id, month_start, month_end,))
                month_events = self._cr.dictfetchall()
                attend_in_month = len(month_events)
                
                
                self._cr.execute("""
                        SELECT
                            reg.id
                        FROM
                            event_registration reg
                        LEFT JOIN event_event event
                            ON event.id = reg.event_id
                        WHERE
                            reg.partner_id IS NOT NULL AND
                            event.event_type_id=%s AND
                            reg.partner_id=%s AND
                            event.date_begin::date >= '%s' AND
                            event.date_begin::date <= '%s'
                    """ % (event_type.id, member.id, week_start, week_end,))
                week_events = self._cr.dictfetchall()
                attend_in_week = len(week_events)
                time_week = 0
                time_month = 0
                if self.partner_id.membership_state == "paid":  # check member status
                    for line in self.partner_id.member_lines:
                        if line.membership_id.product_tmpl_id.product_type_id == event_type:
                            
                            member_from = line.membership_id.product_tmpl_id.membership_date_from
                            member_date = line.membership_id.product_tmpl_id.membership_date_to
                            
                            date = datetime.strptime(member_date, "%Y-%m-%d").date()
                            member_time = datetime.strptime('23:59:59', '%H:%M:%S').time()
                            mem = datetime.combine(date, member_time)
                            member_to = mem.strftime('%Y-%m-%d %H:%M:%S')
                            
                            if event.date_begin >= member_from and event.date_begin <= member_to:
                                if line.state == "paid":
                                    if not line.membership_id.product_tmpl_id.no_limit:
                                        if line.membership_id.product_tmpl_id.times_type == 'weekly':
                                            time_week += line.membership_id.product_tmpl_id.times
                                            if attend_in_week <= time_week:
                                                self.membership_payment_id = line.membership_id.product_tmpl_id
                                                break
                                        else:
                                            time_month += line.membership_id.product_tmpl_id.times
                                            if attend_in_month <= time_month:
                                                self.membership_payment_id = line.membership_id.product_tmpl_id
                                                break
                                    else:
                                        self.membership_payment_id = line.membership_id.product_tmpl_id
                                        break
                                    
                if not self.membership_payment_id:
                    raise UserError(
                        _("You have already exceed for this event!")
                    )    
                
        return True
