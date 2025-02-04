{
    'name': 'Project Management Custom',
    'version': '1.0.0',
    'category': 'Project',
    'summary': 'โมดูลสำหรับจัดการข้อมูลโครงการ (เชื่อมโยงกับหลักสูตรด้านสุขภาพ)',
    'description': """
    โมดูล Project Management Custom:
    - เชื่อมโยงกับหลักสูตรด้านสุขภาพจากโมดูล customer_health
    - จัดการข้อมูลโครงการ เช่น วันที่เริ่ม-สิ้นสุดโครงการ, วิทยากร, ต้นทุน, ผลประเมิน ฯลฯ
    """,
    'author': 'Your Name',
    'website': 'https://www.yourwebsite.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'contacts',           # ใช้สำหรับการเชื่อมโยงวิทยากร (res.partner)
        'hr',                 # ใช้สำหรับจัดการข้อมูลพนักงานที่เกี่ยวข้องในโครงการ
        'customer_health',    # โมดูลต้นทางที่มี model customer.health.training
    ],
    'data': [
        'security/ir.model.access.csv',  # กำหนดสิทธิ์การเข้าถึงโมเดล
        'views/project_management_views.xml',  # แสดงผล Tree และ Form View
    ],
    'installable': True,  # เปิดให้ติดตั้งโมดูลได้
    'application': True,  # ให้แสดงโมดูลนี้ในหน้าแอปพลิเคชัน
    'auto_install': False,  # ไม่ติดตั้งอัตโนมัติเมื่อมีการติดตั้งโมดูลที่เกี่ยวข้อง
}
