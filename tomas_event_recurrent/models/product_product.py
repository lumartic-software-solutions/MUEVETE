# -*- coding: utf-8 -*-
from openerp import api, fields, models, _

class product_product(models.Model):
    _inherit = "product.product"
    
    product_type_id = fields.Many2one(
        'event.type',
        string='Product Type',
    )
    times = fields.Integer(
        string='Times'
    )
    times_type = fields.Selection([
        ('weekly', 'Week(s)'),
        ('monthly', 'Month(s)')],
        string='Type',
    )
    
    
class product_template(models.Model):
    _inherit = "product.template"
    
    product_type_id = fields.Many2one(
        'event.type',
        string='Product Type',
    )
    times = fields.Integer(
        string='Times'
    )
    times_type = fields.Selection([
        ('weekly', 'Week(s)'),
        ('monthly', 'Month(s)')],
        string='Type',
    )
    allow_free_drink = fields.Boolean(
        string="Allow Free Drink?",
    )
    no_limit = fields.Boolean(
        string="No Limit?",
    )