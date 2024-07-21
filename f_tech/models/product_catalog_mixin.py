from odoo import models


class ProductCatalogMixin(models.AbstractModel):
    _inherit = 'product.catalog.mixin'

    def action_add_from_catalog(self):
        result = super(ProductCatalogMixin, self).action_add_from_catalog()
        tree_view_id = self.env.ref('f_tech.product_view_tree_catalog').id

        result['views'] = [(tree_view_id, 'tree')] + result['views']

        return result