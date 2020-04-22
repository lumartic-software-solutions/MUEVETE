# -*- coding: utf-8 -*-

from odoo import models , fields , api , _

class EventEvent(models.Model):
    _inherit = 'event.event'

    counter = fields.Integer(
        string='Counter',
        default=0,
    )
    template_id = fields.Integer(
        string='Template ID',
    )
    depth = fields.Integer(
        string='Depth',
        default=1,
    )
#     product_id = fields.Many2one(
#         'product.template',
#         string='Product',
#     )
    is_template = fields.Boolean(
        string='Template'
    )
    recurrency = fields.Boolean(
        string='Recurrent',
        help="Recurrent Meeting"
    )
    interval = fields.Integer(
        string='Repeat Every',
        default=1,
        help="Repeat every (Days/Week/Month/Year)"
    )
    end_type = fields.Selection([
            ('count', 'Number of repetitions'),
            ('end_date', 'End date')],
        string='Recurrence Termination',
        default='count'
    )
    rrule_type = fields.Selection([
        ('daily', 'Day(s)'),
        ('weekly', 'Week(s)'),
        ('monthly', 'Month(s)'),
        ('yearly', 'Year(s)')],
        string='Recurrency',
        help="Let the event automatically repeat at that interval"
    )
    count = fields.Integer(
        string='Repeat',
        help="Repeat x times",
        default=1
    )
    final_date = fields.Date(
        'Repeat Until'
    )
    mo = fields.Boolean('Mon')
    tu = fields.Boolean('Tue')
    we = fields.Boolean('Wed')
    th = fields.Boolean('Thu')
    fr = fields.Boolean('Fri')
    sa = fields.Boolean('Sat')
    su = fields.Boolean('Sun')
    month_by = fields.Selection([
        ('date', 'Date of month'),
        ('day', 'Day of month')
    ], string='Option', default='date', oldname='select1')
    day = fields.Integer('Date of month', default=1)
    week_list = fields.Selection([
        ('MO', 'Monday'),
        ('TU', 'Tuesday'),
        ('WE', 'Wednesday'),
        ('TH', 'Thursday'),
        ('FR', 'Friday'),
        ('SA', 'Saturday'),
        ('SU', 'Sunday')
    ], string='Weekday')
    byday = fields.Selection([
        ('1', 'First'),
        ('2', 'Second'),
        ('3', 'Third'),
        ('4', 'Fourth'),
        ('5', 'Fifth'),
        ('-1', 'Last')
    ], string='By day')
