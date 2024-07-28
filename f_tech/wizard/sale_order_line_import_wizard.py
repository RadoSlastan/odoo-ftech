from odoo import models, fields, api
import base64
import pandas as pd
from io import BytesIO
from odoo.exceptions import UserError


class SaleOrderLineImportWizard(models.TransientModel):
    _name = 'sale.order.line.import.wizard'
    _description = 'Wizard to import sale order lines from an Excel file'

    # file = fields.Binary('Excel File')
    file = fields.Json(string="Attachment")
    filename = fields.Char(string="Filename")
    file_name = fields.Char('File Name', readonly=True)
    import_by = fields.Selection([('code', 'Internal Reference'), ('name', 'Name')],
                                 string='Import Product By', default='code', required=True)

    def import_file(self):
        if not self.file:
            raise UserError("Please upload a file.")
        try:
            file_content = base64.b64decode(self.file)
            data = pd.read_excel(BytesIO(file_content))

            order_id = self.env.context.get('active_id')
            sale_order = self.env['sale.order'].browse(order_id)
            for index, row in data.iterrows():
                product = None
                if self.import_by == 'code':
                    product = self.env['product.product'].search([('default_code', '=', row['Internal reference'])],
                                                                 limit=1)
                elif self.import_by == 'name':
                    product = self.env['product.product'].search([('name', '=', row['Name'])], limit=1)

                if not product:
                    raise UserError(f"Product with {self.import_by} '{row[self.import_by]}' not found.")

                line_vals = {
                    'order_id': sale_order.id,
                    'product_id': product.id,
                    'product_uom_qty': row['Quantity'],
                    'price_unit': row['Unit price'],
                }

                self.env['sale.order.line'].create(line_vals)
        except Exception as e:
            raise UserError(f"An error occurred while processing the file: {str(e)}")

    sample_file = fields.Binary("Sample File", readonly=True)
    sample_file_name = fields.Char("Sample File Name", readonly=True)

    def download_sample_file(self):

        sample_data = {
            'Name': ['Sample Product'],
            'Quantity': [1],
            'Internal reference': ['SAMPLE001'],
            'Unit price': [0.0],
        }
        df = pd.DataFrame(sample_data)

        file_stream = BytesIO()
        with pd.ExcelWriter(file_stream, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')

        file_content = file_stream.getvalue()
        file_name = 'Sample_Sale_Order_Lines.xlsx'

        self.sample_file = base64.b64encode(file_content)
        self.sample_file_name = file_name

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content?model={self._name}&field=sample_file&id={self.id}&filename_field=sample_file_name&download=true',
            'target': 'self',
        }
