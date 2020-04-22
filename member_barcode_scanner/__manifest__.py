# -*- coding: utf-8 -*-
{
    'name'          : "Member Barcode Scanner",
    'summary'       : """Member Barcode Scanner""",
    'description'   : """
                    Barcode Scanner
    """,
    'author'        : "Pseudocode",
    'website'       : "www.pseudocode.co",
    'category'      : 'Hidden',
    'version'       : '1.0',
    'depends'       : ['event','tomas_gym_extend','hr_attendance','muk_web_client_notification','itm_material'],
    'data'          : [
        'views/res_company_view.xml',
        'views/member_barcode_view.xml',
        'report/print_ticket_reg.xml',
        'report/print_ticket_view.xml',
        'views/template.xml',
        'views/user_view.xml',
    ],
    'qweb': [
        "static/src/xml/attendance.xml",
    ],
}
