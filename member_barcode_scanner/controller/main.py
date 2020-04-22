# -*- coding: utf-8 -*-
import datetime
from odoo import fields, http, _
from odoo.http import request
from odoo import models , fields , api , SUPERUSER_ID
from odoo.exceptions import UserError
import datetime
import time 
import pytz
from datetime import datetime as dtime

from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as dt

class EventBarcode(http.Controller):

    @api.model
    def _get_next_event(self, member):
#         start_dt = datetime.datetime.now().replace(hour=0, minute=0, second=0)
        start_dt = datetime.datetime.now()
        end_dt = start_dt.replace(hour=23, minute=59, second=59)
        start_dt = start_dt.strftime("%Y-%m-%d")
        
        end_dt = end_dt.strftime("%Y-%m-%d")
        event_domain = [
            ('date_begin', '>=', start_dt),
            ('date_begin', '<=', end_dt),
        ]
        current_event = request.env['event.event'].sudo().search(event_domain, order="date_begin asc")
        return current_event

    @http.route('/member_barcode_scanner/register_attendee', type='json', auth="user")
    def register_attendee(self, barcode, **kw):
        notification_obj = request.env['muk_web_client_notification.send_notifications']
        MemberObj = request.env['res.partner']
        member = MemberObj.search([('barcode_member', '=', barcode)], limit=1)
        employee = request.env['hr.employee'].search([('barcode', '=', barcode)], limit=1)
        admin_id = request.env['res.users'].search(['|',('access_kiosk_mode_notification','=',True),('id','=',SUPERUSER_ID)])
        if admin_id :
            if len(admin_id) == 1 :
                if admin_id.id == SUPERUSER_ID and admin_id.access_kiosk_mode_notification == False :
                    raise UserError(_('Not Found  Kiosk Mode Notification Manager !'))
            if not member and not employee:
                notification_id = notification_obj.create({'title' :'Barcode Notification',
                                               'user_ids' :[(6,0,admin_id.ids)] ,
                                               'type':'warning',
                                               'sticky' :True,
                                               'message' : _('Member or employee not found for this barcode :  %s !') % barcode})
                notification_id.send_notifications()
                return {'employee': _('Member or employee not found for this barcode :  %s !') % barcode}
            elif employee and not member :
                action_msg = employee.attendance_action('hr_attendance.hr_attendance_action_my_attendances')
                action = action_msg['action']['attendance']
                if 'check_out' in action:
                    if action.get('check_out') in [False,None]:
                        notification_id = notification_obj.create({'title' :'Check In Notification',
                                               'user_ids' :[(6,0,admin_id.ids)] ,
                                               'type':'warning',
                                               'sticky' :True,
                                               'message' : _('Welcome %s !') % employee.name})
                        notification_id.send_notifications()
                        return {'employee': _('Welcome %s !') % employee.name}
                    else:
                        notification_id = notification_obj.create({'title' :'Check Out Notification',
                                               'user_ids' :[(6,0,admin_id.ids)] ,
                                               'type':'warning',
                                               'sticky' :True,
                                               'message' : _('Bye %s !') % employee.name})
                        notification_id.send_notifications()
                        return {'employee': _('Bye %s !') % employee.name}
            elif member and not employee :
                event_id = self._get_next_event(member)
                if not event_id:
                    notification_id = notification_obj.create({'title' :_('Notification for %s') % member.name,
                                           'user_ids' :[(6,0,admin_id.ids)] ,
                                           'type':'warning',
                                           'sticky' :True,
                                           'message' : 'Event Not Found for current day !'})
                    notification_id.send_notifications()
                    return {'not_event_day': 'Event Not Found for current day !'}                
    #                 raise UserError(_('Event Not Found for current day!'))
        
                Registration = request.env['event.registration'].sudo()
                attendee = Registration.search([('partner_id', '=', member.id),
                                                ('event_id', 'in', event_id.ids)], limit=1)
                if not attendee:
                    notification_id = notification_obj.create({'title' :_('Notification for %s') % member.name,
                                           'user_ids' :[(6,0,admin_id.ids)] ,
                                           'type':'warning',
                                           'sticky' :True,
                                           'message' : _('Member not registered for current event!')})
                    notification_id.send_notifications()
                    return {'not_member_registered': 'Member not registered for current event !'}
    #                 raise UserError(_('Member not registered for current event!'))
                start_dt = datetime.datetime.now()
                end_dt = start_dt.replace(hour=23, minute=59, second=59)
                event_id = attendee.event_id
                count = Registration.search_count([('state', '=', 'done'),
                                                   ('event_id', '=', event_id.id)])
                attendee_name = attendee.name or _('Attendee')
                if attendee.state == 'cancel':
                    notification_id = notification_obj.create({'title' :_('Warning for %s') % member.name,
                                           'user_ids' :[(6,0,admin_id.ids)] ,
                                           'type':'warning',
                                           'sticky' :True,
                                           'message' : _('Canceled registration')})
                    notification_id.send_notifications()
                    return {'warning': 'Canceled registration', 'count': count}
                elif attendee.state != 'done':
                    attendee.write({'state': 'done', 'date_closed': fields.Datetime.now()})
                    count += 1
                    if attendee.membership_payment_id.allow_free_drink:
                        now = datetime.datetime.now()            
                        current_date = now.strftime(dt)
                        notification_id = notification_obj.create({'title' :_('Notification for %s') % member.name,
                                           'user_ids' :[(6,0,admin_id.ids)] ,
                                           'type':'warning',
                                           'sticky' :True,
                                           'message' :  _('%s is successfully registered,Please collect Ticket.') % attendee_name})
                        notification_id.send_notifications()
                        return {'success': _('%s is successfully registered,Please collect Ticket.') % attendee_name,'current_date': current_date, 'attendee_id': attendee.id, 'partner_id': attendee.partner_id.name, 'event_id': attendee.event_id.name, 'user_id':request.env.user.name}
                    else:
                        notification_id = notification_obj.create({'title' :_('Welcome %s') % member.name,
                                           'user_ids' :[(6,0,admin_id.ids)] ,
                                           'type':'warning',
                                           'sticky' :True,
                                           'message' :  'Thanks for coming'})
                        notification_id.send_notifications()
                        return {'allowEvent': _('%s Successfully Registered.') % attendee_name}
                else:
                    notification_id = notification_obj.create({'title' :_('Warning for %s') % member.name,
                                           'user_ids' :[(6,0,admin_id.ids)] ,
                                           'type':'warning',
                                           'sticky' :True,
                                           'message' : _('%s is already registered') % attendee_name})
                    notification_id.send_notifications()
                    return {'warning': _('%s is already registered') % attendee_name, 'count': count}
            else:
                notification_id = notification_obj.create({'title' :(_('Warning for %s and %s') % member.name,employee.name),
                                           'user_ids' :[(6,0,admin_id.ids)] ,
                                           'type':'warning',
                                           'sticky' :True,
                                           'message' : 'Member and Employee both are same !'})
                notification_id.send_notifications()
                return {'both_same': _('Member and Employee both are same.')}
        
        
        else:
            raise UserError(_('Not Found  Kiosk Mode Notification Manager !'))
