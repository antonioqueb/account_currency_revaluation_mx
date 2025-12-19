from odoo import fields, models

class AccountAccount(models.Model):
    _inherit = 'account.account'

    allow_revaluation = fields.Boolean(
        string='Allow Currency Revaluation',
        help='Check this if you want to include this account in the multicurrency revaluation report.'
    )
