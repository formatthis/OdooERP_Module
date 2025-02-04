# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

# ------------------------------------------------------------------------
# Customer Health Model
# ------------------------------------------------------------------------
class CustomerHealth(models.Model):
    _name = 'customer.health'
    _description = 'Customer Health Information'

    # Basic customer information
    name = fields.Char(string='ชื่อ-นามสกุล', required=True)
    phone = fields.Char(string='เบอร์โทรศัพท์')
    email = fields.Char(string='อีเมล')
    address = fields.Text(string='ที่อยู่')

    # Health-related details
    chronic_diseases = fields.Text(string='โรคประจำตัว')
    food_allergies = fields.Text(string='อาหารที่แพ้')
    health_interests = fields.Text(string='ความสนใจด้านสุขภาพ')

    # Body composition measurements
    fat_mass_percent = fields.Float(string="เปอร์เซ็นต์ไขมันในร่างกาย (%)")
    muscle_mass = fields.Float(string="มวลกล้ามเนื้อ (กก.)")
    body_water = fields.Float(string="ปริมาณน้ำในร่างกาย (%)")
    bone_mass = fields.Float(string="มวลกระดูก (กก.)")

    # Fitness measurements
    vital_capacity = fields.Float(string="ความจุปอด (ลิตร)")
    grip_strength = fields.Float(string="แรงบีบมือ (กก.)")
    flexibility = fields.Float(string="ความยืดหยุ่น (ซม.)")
    sit_and_stand = fields.Float(string="ทดสอบนั่ง-ลุก (ครั้ง)")

    # Metabolic measurements
    bmr = fields.Float(string="อัตราการเผาผลาญพื้นฐาน (กิโลแคลอรี)")
    bmi = fields.Float(string="ค่าดัชนีมวลกาย (BMI)")
    bmi_category = fields.Selection([
        ('underweight', 'น้ำหนักน้อยกว่ามาตรฐาน'),
        ('normal', 'น้ำหนักปกติ'),
        ('overweight', 'น้ำหนักเกิน'),
        ('obese', 'โรคอ้วน')
    ], string="หมวดหมู่ BMI")

    # Overall health analysis
    body_analysis_score = fields.Selection([
        ('excellent', 'ยอดเยี่ยม'),
        ('good', 'ดี'),
        ('average', 'ปานกลาง'),
        ('below_average', 'ต่ำกว่าปานกลาง')
    ], string="คะแนนวิเคราะห์ร่างกาย")
    analysis_date = fields.Date(string="วันที่วิเคราะห์", default=fields.Date.context_today)

    # Training history
    training_history_ids = fields.One2many(
        'customer.health.training',
        'customer_id',
        string='ประวัติการเข้าร่วมอบรม'
    )

    # Company information
    company_id = fields.Many2one(
        'res.partner',
        string='ชื่อบริษัท',
        domain=[('is_company', '=', True)],
        required=True,
        help="เลือกชื่อบริษัทจากรายชื่อบริษัทในระบบ"
    )


# ------------------------------------------------------------------------
# Training Course Model
# ------------------------------------------------------------------------
class TrainingCourse(models.Model):
    _name = 'training.course'
    _description = 'Training Course'

    name = fields.Char(string='ชื่อหลักสูตร', required=True)
    description = fields.Text(string='คำอธิบายหลักสูตร')


# ------------------------------------------------------------------------
# Customer Health Training Model
# ------------------------------------------------------------------------
class CustomerHealthTraining(models.Model):
    _name = 'customer.health.training'
    _description = 'Customer Health Training History'
    _rec_name = 'course_id'

    customer_id = fields.Many2one(
        'customer.health',
        string='ลูกค้า',
        ondelete='cascade',
        required=True
    )
    course_id = fields.Many2one(
        'training.course',
        string='ชื่อหลักสูตร',
        required=True,
        help="เลือกหลักสูตรการอบรมที่เคยสร้างไว้แล้ว"
    )
    start_date = fields.Date(string='วันที่เริ่ม', required=True)
    end_date = fields.Date(string='วันที่สิ้นสุด', required=True)
    evaluation_result = fields.Text(string='ผลประเมิน')

    # Related fields for display
    course_name = fields.Char(
        string="ชื่อหลักสูตร",
        related="course_id.name",
        store=True
    )

    customer_name = fields.Char(
        string="ชื่อลูกค้า",
        related="customer_id.name",
        store=True
    )

    # SQL Constraints
    _sql_constraints = [
        ('unique_customer_course',
         'unique(customer_id, course_id, start_date, end_date)',
         'ลูกค้าแต่ละคนสามารถลงทะเบียนในหลักสูตรเดียวได้เพียงครั้งเดียวในช่วงเวลาเดียวกัน!')
    ]

    # Constraints: ตรวจสอบวันที่สิ้นสุดต้องไม่ก่อนวันที่เริ่มต้น
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.end_date < record.start_date:
                raise ValidationError("วันที่สิ้นสุดต้องไม่ก่อนวันที่เริ่มต้น")

    # Constraints: ตรวจสอบไม่ให้มีหลักสูตรซ้ำในช่วงเวลาเดียวกัน
    @api.constrains('customer_id', 'course_id', 'start_date', 'end_date')
    def _check_unique_training(self):
        for record in self:
            overlapping = self.search([
                ('id', '!=', record.id),
                ('customer_id', '=', record.customer_id.id),
                ('course_id', '=', record.course_id.id),
                '|',
                ('start_date', '<=', record.end_date),
                ('end_date', '>=', record.start_date),
            ])
            if overlapping:
                raise ValidationError(
                    f"ลูกค้า '{record.customer_id.name}' มีการอบรมหลักสูตร "
                    f"'{record.course_id.name}' ซ้ำในช่วงเวลาเดียวกัน!"
                )