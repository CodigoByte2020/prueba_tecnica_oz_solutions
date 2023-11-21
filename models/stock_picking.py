from odoo import models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def shipping_products(self):
        view_id = self.env.ref('prueba_tecnica_oz_solutions.shipping_products_view_form').id
        return {
            'name': 'Enviar Productos',
            'type': 'ir.actions.act_window',
            'res_model': 'shipping.products',
            'view_mode': 'form',
            'view_id': view_id,
            'views': [(view_id, 'form')],
            'target': 'new',
            'context': {
                'default_stock_picking_id': self.id
            }
        }
