from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    attachment_ids = fields.Many2many('ir.attachment', string="Attachments")