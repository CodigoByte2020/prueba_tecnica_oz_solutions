from odoo import fields, models


class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    user_id = fields.Many2one(comodel_name='res.users', string='Responsable')

    def reverse_moves(self):
        action = super(AccountMoveReversal, self).reverse_moves()
        action['context'].update({
            'default_invoice_user_id': self.user_id.id
        })
        return action
