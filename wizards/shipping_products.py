import re

from odoo import api, fields, models
from odoo.exceptions import ValidationError

email_re = re.compile(r"""([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,63})""")


class ShippingProducts(models.TransientModel):
    _name = 'shipping.products'

    informative_note = fields.Text(string='Nota informativa')
    document_file = fields.Binary(string='Documento', required=True, attachment=True)
    document_filename = fields.Char(string='Documento Filename')
    stock_picking_id = fields.Many2one('stock.picking')

    @api.onchange('document_filename')
    def _onchange_document_filename(self):
        if self.document_filename:
            self._validate_attachment_type()

    def _validate_attachment_type(self):
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf']
        if not any(self.document_filename.lower().endswith(ext) for ext in allowed_extensions):
            raise ValidationError('Solo se admiten archivos de tipo imagen y PDF.')

    def send_mail(self):
        '''ASEGURESE DE CONFIGURAR CORRECTAMENTE LOS SERVIDORES DE CORREO.'''
        self._validate_mail()
        template_id = self.env.ref('prueba_tecnica_oz_solutions.notification_shipping_products').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    def _validate_mail(self):
        email_partner = self.stock_picking_id.partner_id.email
        if email_partner and not email_re.match(email_partner):
            raise ValidationError(
                'El email del contacto no cumple con el formato de una dirección de correo estándar. !!!')
        if not email_partner:
            raise ValidationError('El email del contacto no ha sido definido. !!!')
