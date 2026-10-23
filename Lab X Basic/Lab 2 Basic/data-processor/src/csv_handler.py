# data-processor/src/csv_handler.py
import csv
import os
from utils import setup_logging, ensure_directory_exists

logger = setup_logging(__name__)

class CSVHandler:
    """
    จัดการการอ่าน การเขียน และการประมวลผลพื้นฐานของไฟล์ CSV
    """
    def __init__(self):
        logger.info("CSVHandler ถูก initialized แล้ว")

    def read_csv_as_dicts(self, file_path):
        """
        อ่านไฟล์ CSV และคืนค่าเป็นลิสต์ของพจนานุกรม (Dictionaries)
        สมมติว่าแถวแรกคือหัวตาราง (Header)
        """
        if not os.path.exists(file_path):
            logger.error(f"ไม่พบไฟล์ CSV: {file_path}")
            return None
        
        data = []
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                data = list(reader)
                logger.info(f"อ่านข้อมูลสำเร็จ {len(data)} แถว จาก '{file_path}'")
                return data
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการอ่านไฟล์ CSV '{file_path}': {e}")
            return None

    def write_dicts_to_csv(self, data, file_path, fieldnames):
        """
        เขียนลิสต์ของพจนานุกรมลงในไฟล์ CSV
        `fieldnames` ต้องเป็นลิสต์ของสตริงที่ตรงกับคีย์ของพจนานุกรมสำหรับเป็นหัวตาราง
        """
        if not data:
            logger.warning("ไม่มีข้อมูลสำหรับเขียนลง CSV")
            return False
        
        ensure_directory_exists(os.path.dirname(file_path))
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
                logger.info(f"เขียนข้อมูลสำเร็จ {len(data)} แถว ลงใน '{file_path}'")
                return True
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการเขียนไฟล์ CSV '{file_path}': {e}")
            return False

    def process_sales_data(self, sales_data, min_sale_amount=0):
        """
        ประมวลผลข้อมูลยอดขาย: คำนวณยอดขายรวม, ราคาเฉลี่ย,
        และกรองยอดขายที่มากกว่าจำนวนที่กำหนด
        """
        if not sales_data:
            logger.warning("ไม่มีข้อมูลยอดขายสำหรับการประมวลผล")
            return {"filtered_sales": [], "summary": {}}
        
        total_sales = 0.0
        total_price = 0.0
        num_items = 0
        filtered_sales = []
        
        for row in sales_data:
            try:
                amount = float(row.get('Amount', 0))
                price = float(row.get('Price', 0))
                total_sales += amount
                num_items += 1
                total_price += price
                if amount >= min_sale_amount:
                    filtered_sales.append(row)
            except ValueError as e:
                logger.warning(f"ข้ามแถวเนื่องจากแปลงข้อมูลผิดพลาด: {row}. ข้อผิดพลาด: {e}")
            except TypeError as e:
                logger.warning(f"ข้ามแถวเนื่องจากคีย์หายไปหรือชนิดข้อมูลไม่ถูกต้อง: {row}. ข้อผิดพลาด: {e}")

        average_price = total_price / num_items if num_items > 0 else 0.0
        summary = {
            "Total Sales": f"{total_sales:.2f}",
            "Average Item Price": f"{average_price:.2f}",
            "Filtered Sales Count": len(filtered_sales)
        }
        logger.info(f"ประมวลผลข้อมูลยอดขายเสร็จสิ้น ยอดขายรวม: {summary['Total Sales']}, จำนวนที่กรองได้: {summary['Filtered Sales Count']}")
        return {"filtered_sales": filtered_sales, "summary": summary}