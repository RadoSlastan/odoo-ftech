import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SalesOrderLine(models.Model):
    _inherit = "sale.order.line"

    default_code = fields.Char(related='product_id.default_code', readonly=False, string="Code")
    reference = fields.Char(related='product_id.reference', readonly=False, string="Reference")
    hs_code = fields.Char(related='product_id.hs_code', readonly=False, string="HS Code")
    barcode = fields.Char(related='product_id.barcode', readonly=False, string="Barcode")
    origin = fields.Many2one("res.country", related='product_id.origin', readonly=False, string="Origin")
