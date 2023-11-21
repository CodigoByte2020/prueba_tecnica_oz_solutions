from odoo import api, fields, models, tools


class StockBalanceReport(models.Model):
    _name = 'stock.balance.report'
    _auto = False
    _description = 'Reporte de saldos de stock físico disponible por almacén'

    id = fields.Integer(string='ID')
    location_id = fields.Many2one(comodel_name='stock.location', string='Ubicación')
    product_id = fields.Many2one(comodel_name='product.product')
    product_name = fields.Char(related='product_id.name', string='Producto')
    category_name = fields.Char(string='Categoría de producto')
    uom_name = fields.Char(string='Unidad de medida')
    quantity = fields.Float(string='Stock Físico')

    @api.model
    def get_query(self):
        data = self._get_data()
        query = f"""
            CREATE OR REPLACE VIEW stock_balance_report AS (
                SELECT sq.id AS id, sq.location_id AS location_id, sq.product_id AS product_id, 
                    pc."name" AS category_name, sq.quantity AS quantity, uu."name" AS uom_name 
                FROM stock_quant sq
                INNER JOIN product_product pp ON sq.product_id = pp.id
                INNER JOIN product_template pt ON pp.product_tmpl_id = pt.id
                INNER JOIN uom_uom uu ON pt.uom_id = uu.id
                INNER JOIN product_category pc ON pt.categ_id = pc.id
                WHERE sq.id IN {tuple(data)}
            );
        """
        return query

    def _get_data(self):
        warehouses = self.env['stock.warehouse'].search([])
        data = []
        for warehouse in warehouses:
            quants = self.env['stock.quant'].search([('location_id', 'child_of', warehouse.view_location_id.id)])
            for quant in quants:
                data.append(quant.id)
        return data

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        query = self.get_query()
        self.env.cr.execute(query)
