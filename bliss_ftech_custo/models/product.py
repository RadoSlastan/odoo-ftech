import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    """Adds last name and first name; name becomes a stored function field."""

    _inherit = "product.template"

    code = fields.Char(string="Code")
    reference = fields.Char(string="Reference")
    hs_code = fields.Char(string="HS Code")
    origin = fields.Many2one("res.country", string="Origin")


class ProductProduct(models.Model):
    _inherit = "product.product"

    def get_product_multiline_description_sale(self):
        self.ensure_one()
        return self.name
