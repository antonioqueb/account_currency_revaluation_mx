from odoo import fields, models

class ResConfigSettings(旋.TransientModel):
    _inherit = 'res.config.settings'

    revaluation_loss_account_id = fields.Many2one(
        related='company_id.revaluation_loss_account_id', readonly=False)
    revaluation_gain_account_id = fields.Many2one(
        related='company_id.revaluation_gain_account_id', readonly=False)
    
    provision_bs_loss_account_id = fields.Many2one(
        related='company_id.provision_bs_loss_account_id', readonly=False,
        groups="account_currency_revaluation_mx.group_additional_provisioning")
    provision_pl_loss_account_id = fields.Many2one(
        related='company_id.provision_pl_loss_account_id', readonly=False,
        groups="account_currency_revaluation_mx.group_additional_provisioning")
