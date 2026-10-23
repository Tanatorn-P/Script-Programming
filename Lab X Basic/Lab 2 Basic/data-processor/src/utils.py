# data-processor/src/utils.py
import logging
import os

# กำหนดค่า Logging พื้นฐาน
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_logging(name, level=logging.INFO):
    """ตั้งค่า Logger สำหรับโมดูลเฉพาะ"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers: # ป้องกันการเพิ่ม handler ซ้ำหากถูกเรียกหลายครั้ง
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

def ensure_directory_exists(path):
    """ตรวจสอบว่ามีไดเรกทอรีอยู่หรือไม่ หากไม่มีให้สร้างขึ้นใหม่"""
    try:
        os.makedirs(path, exist_ok=True)
        logging.info(f"ตรวจสอบ/สร้างไดเรกทอรีเรียบร้อย: {path}")
    except OSError as e:
        logging.error(f"เกิดข้อผิดพลาดในการสร้างไดเรกทอรี {path}: {e}")
        raise