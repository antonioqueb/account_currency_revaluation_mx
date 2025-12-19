from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountRevaluationWizard(models.TransientModel):
    _name = 'account.revaluation.wizard'
    _description = 'Currency Revaluation Wizard'

    date = fields.Date(string='Revaluation Date', required=True, default=fields.Date.context_today)
    journal_id = fields.Many2one('account.journal', string='Journal', required=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)

    def generate_revaluation_entries(self):
        self.ensure_one()
        # Buscar cuentas marcadas para revaluación
        accounts = self.env['account.account'].search([
            ('allow_revaluation', '=', True),
            ('company_id', '=', self.company_id.id)
        ])
        
        if not accounts:
            raise UserError(_("No accounts marked for revaluation."))

        move_lines = []
        
        for account in accounts:
            # Obtener el saldo en moneda extranjera y moneda local a la fecha
            # En Odoo 18/19 usamos el query builder o compute_tables
            self.env.cr.execute("""
                SELECT sum(amount_currency), sum(balance)
                FROM account_move_line
                WHERE account_id = %s AND date <= %s AND parent_state = 'posted'
            """, (account.id, self.date))
            res = self.env.cr.fetchone()
            
            amt_currency = res[0] or 0.0
            current_balance_mxn = res[1] or 0.0
            
            if amt_currency == 0:
                continue

            # Calcular el valor esperado según la tasa de cambio de la fecha elegida
            # Suponiendo que la cuenta tiene una moneda seteada (ej. USD)
            currency = account.currency_id or self.company_id.currency_id
            expected_balance_mxn = currency._convert(
                amt_currency, self.company_id.currency_id, self.company_id, self.date
            )
            
            adjustment = expected_balance_mxn - current_balance_mxn
            
            if adjustment == 0:
                continue

            # Determinar cuenta de contrapartida
            if adjustment > 0:
                counterpart_account = self.company_id.revaluation_gain_account_id
            else:
                counterpart_account = self.company_id.revaluation_loss_account_id

            if not counterpart_account:
                raise UserError(_("Please configure revaluation gain/loss accounts in settings."))

            # Crear líneas de asiento
            move_lines.append((0, 0, {
                'name': _('Revaluation: %s') % account.name,
                'account_id': account.id,
                'debit': adjustment if adjustment > 0 else 0.0,
                'credit': -adjustment if adjustment < 0 else 0.0,
            }))
            
            move_lines.append((0, 0, {
                'name': _('Revaluation: %s') % account.name,
                'account_id': counterpart_account.id,
                'debit': -adjustment if adjustment < 0 else 0.0,
                'credit': adjustment if adjustment > 0 else 0.0,
            }))

        if move_lines:
            move = self.env['account.move'].create({
                'journal_id': self.journal_id.id,
                'date': self.date,
                'ref': _('Currency Revaluation MXN/USD'),
                'line_ids': move_lines,
            })
            return {
                'name': _('Revaluation Entry'),
                'view_mode': 'form',
                'res_model': 'account.move',
                'res_id': move.id,
                'type': 'ir.actions.act_window',
            }
        
        return {'type': 'ir.actions.act_window_close'}
