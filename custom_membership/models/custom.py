from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    
    @api.one
    def _compute_event_reg(self):
        reg_id = self.env['event.registration'].search([('partner_id', '=', self.id)])
        total = 0
        if reg_id:
            for details in reg_id:
                total += 1
            self.event_reg_expected = total
        else:
            self.event_reg_expected = 0
    
    event_reg_expected = fields.Integer(
        string='Number of Expected Attendees',
        readonly=True, compute='_compute_event_reg')
    
	

class EventRegistration(models.Model):
    _inherit = 'event.registration'
    
    
    #  partner onchange for membership is expired or not.
    @api.onchange('partner_id')
    def _onchange_partner(self):
        if self.partner_id:
            contact_id = self.partner_id.address_get().get('contact', False)
            if contact_id:
		if len(self.partner_id.member_lines) == 1:
                    for line in self.partner_id.member_lines:
                        if len(line.account_invoice_line) == 1 :
                            if line.state == 'paid' :
                                if line.account_invoice_line.product_id:
                                    self.membership_payment_id = line.account_invoice_line.product_id.product_tmpl_id.id
                if self.partner_id.membership_start <= self.date_open and  self.date_open <= self.partner_id.membership_stop:
                    contact = self.env['res.partner'].browse(contact_id)
                    self.name = contact.name or self.name
                    self.email = contact.email or self.email
                    self.phone = contact.phone or self.phone
                elif self.partner_id.free_member == True:
                    contact = self.env['res.partner'].browse(contact_id)
                    self.name = contact.name or self.name
                    self.email = contact.email or self.email
                    self.phone = contact.phone or self.phone
                else:
                    raise UserError(_("%s 's membership is expired.") % self.partner_id.name)
     
    #  To check partner's membership is expired or not   .
    @api.model
    def create(self, vals):
        res = super(EventRegistration, self).create(vals)
        if vals.get('partner_id'):
            partner = self.env['res.partner'].search([('id', '=', vals.get('partner_id'))])
            if partner.membership_start <= res.date_open and  res.date_open <= partner.membership_stop:
                return res
            elif partner.free_member == True:
                return res   
            else:
                raise UserError(_("%s 's membership is expired.") % res.partner_id.name)
                
        else:
        	return res
       
            
