from odoo import models, fields, api

class Document(models.Model):
    _name = 'document.management'
    _description = 'Document Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Document Name', required=True)
    version = fields.Char(string='Version', required=True)
    document_file = fields.Binary(string='Document File', attachment=True)
    customer_id = fields.Many2one('res.partner', string='Customer', domain=[('customer_rank', '>', 0)])
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user)
    last_updated_by = fields.Many2one('res.users', string='Last Updated By', readonly=True)
    last_updated_on = fields.Datetime(string='Last Updated On', readonly=True)

    @api.model
    def create(self, vals):
        vals['last_updated_by'] = self.env.user.id
        vals['last_updated_on'] = fields.Datetime.now()
        return super(Document, self).create(vals)

    def write(self, vals):
        vals['last_updated_by'] = self.env.user.id
        vals['last_updated_on'] = fields.Datetime.now()
        return super(Document, self).write(vals)