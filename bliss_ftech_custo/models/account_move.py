from odoo import models,fields

class AccountMove(models.Model):
    _inherit = 'account.move'
    def update_invoice_currencies(self):
        """Update invoice currencies"""
        invoices = self.search([('move_type', '=', 'out_invoice')])
        for invoice in invoices:
            currency_id = invoice.currency_id
            currency_company = invoice.company_id.currency_id
            if currency_id != currency_company:
                state = invoice.state
                if state == 'posted':
                    # set invoice to draft if state is posted
                    invoice.button_draft()

                invoice.with_context(skip_analytic_update=True).write({'currency_id': currency_company.id})
                invoice.with_context(skip_analytic_update=True).write({'currency_id': currency_id.id})

                if state == 'posted':
                    # reset state to 'posted'
                    invoice.action_post()
