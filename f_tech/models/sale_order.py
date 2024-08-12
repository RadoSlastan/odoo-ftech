from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    attachment_ids = fields.Many2many('ir.attachment', string="Attachments")

    def action_convert_to_purchase(self):
        return {
            'name': 'Convert Sale Order Lines to Purchase Order',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.line.to.purchase.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('f_tech.view_sale_order_line_to_purchase_wizard_form').id,
            'target': 'new',
            'context': {'default_sale_order_id': self.id},
        }