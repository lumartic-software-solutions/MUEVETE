# -*- coding: utf-8 -*-
from random import randrange
from openerp import api, fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"
    
    barcode_member = fields.Char(
        string="Barcode Membership",
    )
    surname = fields.Char(
        string="Barcode Membership",
    )
    
    @api.model
    def generate_12_random_numbers(self):
        numbers = []
        for x in range(12):
            numbers.append(randrange(10))
        return numbers
    
    @api.model
    def calculate_checksum(self, ean):
        """
        Calculates the checksum for an EAN13
        @param list ean: List of 12 numbers for first part of EAN13
        :returns: The checksum for `ean`.
        :rtype: Integer
        """
        assert len(ean) == 12, "EAN must be a list of 12 numbers"
        sum_ = lambda x, y: int(x) + int(y)
        evensum = reduce(sum_, ean[::2])
        oddsum = reduce(sum_, ean[1::2])
        return (10 - ((evensum + oddsum * 3) % 10)) % 10
    
    @api.model
    def create(self, vals):
        numbers = self.generate_12_random_numbers()
        numbers.append(self.calculate_checksum(numbers))
        barcode = ''.join(map(str, numbers))
        vals.update({'barcode_member': barcode})
        return super(ResPartner, self).create(vals)
