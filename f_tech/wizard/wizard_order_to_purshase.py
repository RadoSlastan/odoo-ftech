from odoo import models, fields, api

class SaleOrderLineToPurchaseWizard(models.TransientModel):
    _name = 'sale.order.line.to.purchase.wizard'
    _description = 'Wizard to convert sale order lines to purchase order'

    sale_order_id = fields.Many2one('sale.order', string="Sale Order")
    partner_id = fields.Many2one('res.partner', string="Vendor", required=True)
    line_ids = fields.One2many('sale.order.line.to.purchase.wizard.line', 'wizard_id', string="Sale Order Lines")

    @api.model
    def default_get(self, fields):
        res = super(SaleOrderLineToPurchaseWizard, self).default_get(fields)
        sale_order = self.env['sale.order'].browse(self.env.context.get('active_id'))
        lines = []
        for line in sale_order.order_line:
            lines.append((0, 0, {
                'sale_order_line_id': line.id,
                'product_id': line.product_id.id,
                'name': line.name,
                'product_uom_qty': line.product_uom_qty,
                'unit_price': line.price_unit,
            }))
        res.update({
            'sale_order_id': sale_order.id,
            'line_ids': lines,
        })
        return res

    def action_create_purchase_orders(self):
        PurchaseOrder = self.env['purchase.order']
        for wizard in self:
            purchase_order = PurchaseOrder.create({
                'partner_id': wizard.partner_id.id,
                'order_line': [(0, 0, {
                    'product_id': line.product_id.id,
                    'name': line.name,
                    'product_qty': line.product_uom_qty,
                    'product_uom': line.product_id.uom_po_id.id,
                    'price_unit': line.unit_price,
                    'date_planned': fields.Datetime.now(),
                }) for line in wizard.line_ids if line.selected]
            })
            return {
                'type': 'ir.actions.act_window',
                'name': 'Purchase Order',
                'res_model': 'purchase.order',
                'res_id': purchase_order.id,
                'view_mode': 'form',
                'view_type': 'form',
                'target': 'current',
            }

class SaleOrderLineToPurchaseWizardLine(models.TransientModel):
    _name = 'sale.order.line.to.purchase.wizard.line'
    _description = 'Wizard Sale Order Line'

    wizard_id = fields.Many2one('sale.order.line.to.purchase.wizard', string="Wizard")
    sale_order_line_id = fields.Many2one('sale.order.line', string="Sale Order Line")
    product_id = fields.Many2one('product.product', string="Product")
    name = fields.Char(string="Description")
    product_uom_qty = fields.Float(string="Quantity")
    unit_price = fields.Float(string="Unit Price")
    selected = fields.Boolean(string="Select")
