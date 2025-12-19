from odoo import fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    revaluation_loss_account_id = fields.Many2one('account.account', string='Revaluation Loss Account')
    revaluation_gain_account_id = fields.Many2one('account.account', string='Revaluation Gain Account')
    provision_bs_loss_account_id = fields.Many2one('account.account', string='Provision B.S Loss Account')
    provision_pl_loss_account_id = fields.Many2one('account.account', string='Provision P&L Loss Account')
