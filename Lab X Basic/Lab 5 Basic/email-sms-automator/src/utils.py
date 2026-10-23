# email-sms-automator/src/utils.py
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_logging(name, level=logging.INFO):
    """ตั้งค่า Logger สำหรับโมดูลเฉพาะ"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

def get_env_variable(var_name):
    """ดึงค่าตัวแปรสภาพแวดล้อม และแจ้งเตือนหากไม่พบ"""
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"Environment variable '{var_name}' not set. Please check your .env file.")
    return value

def ensure_directory_exists(path):
    """ตรวจสอบว่าไดเรกทอรีมีอยู่หรือไม่ หากไม่มีให้สร้างขึ้นใหม่"""
    try:
        os.makedirs(path, exist_ok=True)
        logging.info(f"Directory ensured: {path}")
    except OSError as e:
        logging.error(f"Error creating directory {path}: {e}")
        raise