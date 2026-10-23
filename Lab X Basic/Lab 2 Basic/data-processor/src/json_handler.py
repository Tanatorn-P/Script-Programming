# data-processor/src/json_handler.py
import json
import os
from utils import ensure_directory_exists, setup_logging

logger = setup_logging(__name__)

class JSONHandler:
    """
    จัดการการอ่าน การเขียน และการจัดการพื้นฐานของไฟล์ JSON
    """
    def __init__(self):
        logger.info("JSONHandler ถูก initialized แล้ว")

    def read_json(self, file_path):
        """อ่านไฟล์ JSON และคืนค่าเป็นออบเจกต์ Python"""
        if not os.path.exists(file_path):
            logger.error(f"ไม่พบไฟล์ JSON: {file_path}")
            return None
        
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                data = json.load(file)
                logger.info(f"อ่าน JSON สำเร็จจาก '{file_path}'")
                return data
        except json.JSONDecodeError as e:
            logger.error(f"รูปแบบ JSON ไม่ถูกต้องใน '{file_path}': {e}")
            return None
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการอ่านไฟล์ JSON '{file_path}': {e}")
            return None

    def write_json(self, data, file_path, indent=4):
        """เขียนออบเจกต์ Python ลงในไฟล์ JSON พร้อมจัดรูปแบบสวยงาม (Pretty-printing)"""
        ensure_directory_exists(os.path.dirname(file_path))
        try:
            with open(file_path, mode='w', encoding='utf-8') as file:
                json.dump(data, file, indent=indent, ensure_ascii=False)
                logger.info(f"เขียน JSON สำเร็จไปยัง '{file_path}'")
                return True
        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการเขียนไฟล์ JSON '{file_path}': {e}")
            return False

    def update_inventory(self, inventory_data, product_id, new_stock_level):
        """อัปเดตระดับสต็อกของสินค้าในข้อมูลคลังสินค้าแบบซ้อน (Nested)"""
        updated = False
        if not isinstance(inventory_data, list):
            logger.warning("ข้อมูลคลังสินค้าไม่ใช่ลิสต์ ไม่สามารถอัปเดตได้")
            return False
            
        for product in inventory_data:
            if product.get("id") == product_id:
                product["stock"] = new_stock_level
                logger.info(f"อัปเดตสต็อกสำหรับสินค้า '{product_id}' เป็น {new_stock_level}")
                updated = True
                break
                
        if not updated:
            logger.warning(f"ไม่พบสินค้า '{product_id}' ในคลังสินค้าสำหรับการอัปเดต")
        return updated

    def add_product(self, inventory_data, new_product):
        """เพิ่มพจนานุกรมสินค้าใหม่ลงในลิสต์คลังสินค้า"""
        if not isinstance(inventory_data, list):
            logger.warning("ข้อมูลคลังสินค้าไม่ใช่ลิสต์ ไม่สามารถเพิ่มสินค้าได้")
            return False
        inventory_data.append(new_product)
        logger.info(f"เพิ่มสินค้าใหม่สำเร็จ: {new_product.get('name', 'N/A')}")
        return True