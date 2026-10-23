# spreadsheet-automator/main.py
import sys
import os

# เพิ่มไดเรกทอรี 'src' เข้าไปใน Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from excel_processor import ExcelProcessor

def main():
    """จุดเริ่มต้นหลักสำหรับแอปพลิเคชันจัดการ Excel อัตโนมัติ"""
    input_file = os.path.join('data', 'input_sales.xlsx')
    output_file = os.path.join('data', 'output_sales_report.xlsx')

    os.makedirs('data', exist_ok=True)

    if not os.path.exists(input_file):
        print(f"ข้อผิดพลาด: ไม่พบไฟล์ขาเข้า '{input_file}'")
        print("กรุณาสร้างไฟล์ 'input_sales.xlsx' ในโฟลเดอร์ 'data' พร้อมข้อมูลตัวอย่าง")
        return

    processor = ExcelProcessor()
    print(f"เริ่มประมวลผลข้อมูลยอดขายจาก '{input_file}'...")
    success = processor.process_sales_data(input_file, output_file)

    if success:
        print(f"สร้างรายงานยอดขายและบันทึกลงใน '{output_file}' สำเร็จแล้ว")
    else:
        print("ล้มเหลวในการสร้างรายงานยอดขาย")

if __name__ == "__main__":
    main()