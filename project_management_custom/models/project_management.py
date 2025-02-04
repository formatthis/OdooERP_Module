# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProjectManagement(models.Model):
    _name = 'project.management'
    _description = 'Project Management'
    _rec_name = 'course_name'

    # อ้างอิงหลักสูตร
    course_id = fields.Many2one(
        comodel_name='customer.health.training',
        string="หลักสูตร",
        required=True,
        ondelete='restrict',
        help="เลือกหลักสูตรด้านสุขภาพจากโมดูล customer_health"
    )

    # แสดงชื่อหลักสูตร
    course_name = fields.Char(
        string="ชื่อหลักสูตร",
        related="course_id.course_id.name",
        store=True
    )

    # วันที่เริ่มและสิ้นสุดโครงการ (อ้างอิงจาก customer.health.training)
    start_date = fields.Date(
        string="วันที่เริ่ม",
        related='course_id.start_date',
        store=True,
        readonly=False
    )
    end_date = fields.Date(
        string="วันที่สิ้นสุด",
        related='course_id.end_date',
        store=True,
        readonly=False
    )

    # ผลประเมิน (อ้างอิงจาก customer.health.training)
    evaluation_result = fields.Text(
        string="ผลประเมิน",
        related='course_id.evaluation_result',
        store=True,
        readonly=False
    )

    # ฟิลด์อื่น ๆ ของโครงการ
    detail = fields.Text(string="รายละเอียดโครงการ")
    cost = fields.Float(string="ต้นทุนโครงการ")

    # พนักงานที่เกี่ยวข้อง
    employee_ids = fields.Many2many(
        'hr.employee',
        string="พนักงานที่เกี่ยวข้อง"
    )

    # วิทยากร
    instructor_ids = fields.Many2many(
        'res.partner',
        string="วิทยากร",
        help="รายชื่อวิทยากรที่บรรยายในหลักสูตร/โครงการนี้"
    )

    # เอกสารประกอบการบรรยาย
    attachment_ids = fields.Many2many(
        'ir.attachment',
        string="เอกสารประกอบการบรรยาย"
    )

    # สถานะโครงการ
    state = fields.Selection([
        ('draft', 'ฉบับร่าง'),
        ('in_progress', 'กำลังดำเนินการ'),
        ('done', 'เสร็จสิ้น'),
        ('cancel', 'ยกเลิก'),
    ], string="สถานะ", default='draft')

    # Transition Logic
    def action_in_progress(self):
        self.state = 'in_progress'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'

    # Validation: ตรวจสอบวันที่
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.end_date < record.start_date:
                raise ValidationError("วันที่สิ้นสุดต้องไม่ก่อนวันที่เริ่มโครงการ")

    # Onchange Logic: แสดงข้อความเตือนเมื่อวันที่ไม่ถูกต้อง
    @api.onchange('start_date', 'end_date')
    def _onchange_dates(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            return {
                'warning': {
                    'title': "วันที่ไม่ถูกต้อง",
                    'message': "วันที่สิ้นสุดต้องไม่ก่อนวันที่เริ่มโครงการ",
                }
            }
