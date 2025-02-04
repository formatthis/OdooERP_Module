# customer_health/models/res_partner.py
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_health_ids = fields.One2many(
        'customer.health',    # โมเดลที่เชื่อมโยง
        'company_id',         # ฟิลด์ Many2one ใน customer.health ที่เชื่อมกับ res.partner
        string='Customer Health Records'
    )
