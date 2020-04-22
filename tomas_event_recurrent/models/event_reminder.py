# -*- coding: utf-8 -*-

from odoo import models , fields , api , _
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU
from datetime import datetime, date, timedelta

class Event_Manager(models.Model):
    _name = 'event.event_manager'
    
    @api.model
    def create_next_event(self):
        current = fields.Date.today()
        current_date = datetime.strptime(current, '%Y-%m-%d')
        current_day = current_date.weekday()
        dpth = 1
        
        event_ids = self.env['event.event'].search([('is_template' , '=', True), ('recurrency', '=', True), ('state', '!=', 'done')])
        for event in event_ids:
            if event.end_type == 'count':
                event.counter += 1
            week_list = []
            while dpth <= event.depth:
                
                if event.mo:
                    event_date = current_date + relativedelta(weekday=MO(dpth))
                    week_list.append(event_date)
                if event.tu:
                    event_date = current_date + relativedelta(weekday=TU(dpth))
                    week_list.append(event_date)
                if event.we:
                    event_date = current_date + relativedelta(weekday=WE(dpth))
                    week_list.append(event_date)
                if event.th:
                    event_date = current_date + relativedelta(weekday=TH(dpth))
                    week_list.append(event_date)
                if event.fr:
                    event_date = current_date + relativedelta(weekday=FR(dpth))
                    week_list.append(event_date)
                if event.sa:
                    event_date = current_date + relativedelta(weekday=SA(dpth))
                    week_list.append(event_date)
                if event.su:
                    event_date = current_date + relativedelta(weekday=SU(dpth))
                    week_list.append(event_date)
                
                event_tmpl_start_date = event.date_begin
                event_tmpl_start_time = datetime.strptime(event_tmpl_start_date, "%Y-%m-%d %H:%M:%S").time()
                
                event_tmpl_end_date = event.date_end
                event_tmpl_end_time = datetime.strptime(event_tmpl_end_date, "%Y-%m-%d %H:%M:%S").time()
                
                dpth += 1
                
                for event_day in week_list:
                    
                    event_start_date = datetime.combine(event_day, event_tmpl_start_time)
                    event_end_date = datetime.combine(event_day, event_tmpl_end_time)
                    
                    date = event_start_date.strftime('%Y-%m-%d %H:%M:%S')
                    final_date = event.final_date
                    day = event_day.strftime('%Y-%m-%d')
                    event_find = self.env['event.event'].search([('template_id' , '=', event.id), ('date_begin', '=', date)])
                    if event.end_type == 'end_date' and day > event.final_date:
                        event.state = 'done'
                        return True
                    elif event.end_type == 'count' and event.counter > event.count:
                        event.state = 'done'
                        return True
                    elif not event_find:
                        new_event_id = event.copy(default={
                                    'is_template':False,
                                    'date_begin': event_start_date,
                                    'date_end': event_end_date,
                                    'recurrency': False,
                                    'template_id':event.id,
                                })