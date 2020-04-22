# -*- coding: utf-8 -*-
import time
from odoo import api, models, _
from datetime import datetime
from dateutil.relativedelta import relativedelta

class ReportAgedPartnerBalance(models.AbstractModel):
    _name = 'report.member_barcode_scanner.print_ticket_report_view'

    @api.model
    def render_html(self, docids, data=None):
        model = 'event.registration'
        if not docids:
            docids = self._context.get('active_ids', [])
        docs = self.env[model].browse(docids)
        docargs = {
            'doc_ids': self.ids,
            'doc_model': model,
            'docs': docs,
            'time': time,
        }
        return self.env['report'].render('member_barcode_scanner.print_ticket_report_view', docargs)
