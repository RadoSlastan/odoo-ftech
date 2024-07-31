from odoo import models, fields, api
from odoo.tools.misc import unique


class ProductProduct(models.Model):
    _inherit = 'product.product'

    order_id = fields.Many2one('sale.order', string='Sale Order', compute='_compute_order_id', store=False)
    product_so_qty = fields.Integer('Quantity', compute='_compute_product_so_qty', store=False)
    @api.depends('order_id')
    def _compute_product_so_qty(self):
        for product in self:
            order_lines = product.order_id.order_line.filtered(lambda line: line.product_id.id == product.id)
            product.product_so_qty = sum(line.product_uom_qty for line in order_lines)
            if order_lines:
                product.product_so_qty = sum(line.product_uom_qty for line in order_lines)
            else:
                product.product_so_qty = 0
    @api.depends()
    def _compute_order_id(self):
        for product in self:
            order_id = dict(product.env.context or {}).get('order_id')
            product.order_id = self.env['sale.order'].browse(order_id)

    is_in_sale_order = fields.Boolean(
        string='In Sale Order',
        compute='_compute_is_in_sale_order',
        default=True
    )

    @api.depends('order_id')
    def _compute_is_in_sale_order(self):
        for product in self:
            product.is_in_sale_order = any(line.product_id == product for line in product.order_id.order_line)

    def action_add_to_sale_order(self):
        if not self.order_id:
            return
        product_ids = self.env.context.get('active_ids', [])
        print(product_ids)
        for product_id in product_ids:
            product = self.env['product.product'].browse(product_id)
            self.order_id.order_line.create({
                'order_id': self.order_id.id,
                'product_id': product.id,
                'name': product.name,
                'product_uom_qty': 1,
                'price_unit': product.lst_price,
            })
        return True

    def action_remove_from_sale_order(self):
        product_ids = self.env.context.get('active_ids', [])
        for product_id in product_ids:
            order_line = self.order_id.order_line.filtered(lambda line: line.product_id.id == product_id)
            if order_line:
                order_line.unlink()
        return True

    def action_add_qty(self):
        pass

    def action_sub_qty(self):
        pass

    @api.depends('name', 'default_code', 'product_tmpl_id')
    @api.depends_context('display_default_code', 'seller_id', 'company_id', 'partner_id')
    def _compute_display_name(self):
        # overrided this def to make the discription in the SO without the internal reference
        def get_display_name(name, code):

            return name

        partner_id = self._context.get('partner_id')
        if partner_id:
            partner_ids = [partner_id, self.env['res.partner'].browse(partner_id).commercial_partner_id.id]
        else:
            partner_ids = []
        company_id = self.env.context.get('company_id')

        # all user don't have access to seller and partner
        # check access and use superuser
        self.check_access_rights("read")
        self.check_access_rule("read")

        product_template_ids = self.sudo().product_tmpl_id.ids

        if partner_ids:
            # prefetch the fields used by the `display_name`
            supplier_info = self.env['product.supplierinfo'].sudo().search_fetch(
                [('product_tmpl_id', 'in', product_template_ids), ('partner_id', 'in', partner_ids)],
                ['product_tmpl_id', 'product_id', 'company_id', 'product_name', 'product_code'],
            )
            supplier_info_by_template = {}
            for r in supplier_info:
                supplier_info_by_template.setdefault(r.product_tmpl_id, []).append(r)

        for product in self.sudo():
            variant = product.product_template_attribute_value_ids._get_combination_name()

            name = variant and "%s (%s)" % (product.name, variant) or product.name
            sellers = self.env['product.supplierinfo'].sudo().browse(self.env.context.get('seller_id')) or []
            if not sellers and partner_ids:
                product_supplier_info = supplier_info_by_template.get(product.product_tmpl_id, [])
                sellers = [x for x in product_supplier_info if x.product_id and x.product_id == product]
                if not sellers:
                    sellers = [x for x in product_supplier_info if not x.product_id]
                # Filter out sellers based on the company. This is done afterwards for a better
                # code readability. At this point, only a few sellers should remain, so it should
                # not be a performance issue.
                if company_id:
                    sellers = [x for x in sellers if x.company_id.id in [company_id, False]]
            if sellers:
                temp = []
                for s in sellers:
                    seller_variant = s.product_name and (
                            variant and "%s (%s)" % (s.product_name, variant) or s.product_name
                    ) or False
                    temp.append(get_display_name(seller_variant or name, s.product_code or product.default_code))

                # => Feature drop here, one record can only have one display_name now, instead separate with `,`
                # Remove this comment
                product.display_name = ", ".join(unique(temp))
            else:
                product.display_name = get_display_name(name, product.default_code)
