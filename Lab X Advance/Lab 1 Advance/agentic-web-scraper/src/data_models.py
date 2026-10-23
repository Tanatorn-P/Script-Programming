# agentic-web-scraper/src/data_models.py
from dataclasses import dataclass, asdict

@dataclass
class Product:
    """โครงสร้างข้อมูลสำหรับสินค้าที่ถูกดึงข้อมูลมา"""
    name: str
    price: str
    description: str = None
    url: str = None
    image_url: str = None

    def to_dict(self):
        """แปลง Product dataclass เป็น dictionary"""
        return asdict(self)