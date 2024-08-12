from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    attachment_ids = fields.Many2many('ir.attachment', string="Attachments")

    def action_add_from_catalog(self):
        #Add the product's tree view .
        action = super().action_add_from_catalog()
        tree_view_id = self.env.ref('f_tech.product_view_tree_catalog').id
        action['views'][0] = (tree_view_id, 'tree')
        return action