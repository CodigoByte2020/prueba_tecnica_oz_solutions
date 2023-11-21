from datetime import datetime

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    invoice_due_ids = fields.Many2many(comodel_name='account.move', string='Facturas de clientes vencidas')

    def overdue_customer_invoices(self):
        today = datetime.date(datetime.today())
        overdue_bills = self.env['account.move'].sudo().search([
            ('partner_id', '=', self.id),
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('invoice_date_due', '<', today)
        ])
        view_id = self.env.ref('prueba_tecnica_oz_solutions.res_partner_view_tree').id
        return {
            'name': 'Facturas de clientes vencidas',
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_mode': 'form',
            'view_id': view_id,
            'views': [(view_id, 'form')],
            'target': 'current',
            'context': {
                'default_invoice_due_ids': [(6, 0, overdue_bills.ids)]
            }
        }
