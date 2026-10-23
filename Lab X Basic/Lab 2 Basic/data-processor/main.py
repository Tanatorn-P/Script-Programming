# data-processor/main.py
import sys
import os

# เพิ่มไดเรกทอรี 'src' เข้าไปใน Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from csv_handler import CSVHandler
from json_handler import JSONHandler
from utils import setup_logging, ensure_directory_exists

logger = setup_logging(__name__)

def main():
    """จุดเริ่มต้นหลักสำหรับโปรแกรมประมวลผลข้อมูล CSV และ JSON"""
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    ensure_directory_exists(data_dir)

    # --- พาธไฟล์ ---
    input_csv_path = os.path.join(data_dir, 'input_sales.csv')
    output_filtered_csv_path = os.path.join(data_dir, 'output_filtered_sales.csv')
    input_json_path = os.path.join(data_dir, 'input_inventory.json')
    output_updated_json_path = os.path.join(data_dir, 'output_updated_inventory.json')

    # --- เริ่มต้น Handlers ---
    csv_proc = CSVHandler()
    json_proc = JSONHandler()

    logger.info("--- เริ่มต้นกระบวนการประมวลผลข้อมูล CSV ---")
    # 1. อ่านข้อมูล CSV
    sales_data = csv_proc.read_csv_as_dicts(input_csv_path)
    if sales_data:
        # 2. ประมวลผลข้อมูลยอดขาย (กรองยอดขาย > $100 และคำนวณสรุป)
        min_amount_for_filter = 100.0
        processed_results = csv_proc.process_sales_data(sales_data, min_sale_amount=min_amount_for_filter)

        filtered_sales = processed_results["filtered_sales"]
        sales_summary = processed_results["summary"]
        logger.info(f"สรุปยอดขายทั้งหมด: {sales_summary}")

        # 3. เตรียมข้อมูลสำหรับเขียน พร้อมเพิ่มแถวสรุป
        if sales_data:
            csv_fieldnames = list(sales_data[0].keys())
        else:
            csv_fieldnames = ['OrderID', 'Product', 'Amount', 'Price', 'Customer']

        summary_row = {
            'OrderID': 'SUMMARY',
            'Product': 'Total/Avg',
            'Amount': sales_summary['Total Sales'],
            'Price': sales_summary['Average Item Price'],
            'Customer': f"Count: {sales_summary['Filtered Sales Count']}"
        }
        filtered_sales_with_summary = filtered_sales + [summary_row]

        # 4. เขียนข้อมูลยอดขายที่กรองแล้วลงไฟล์ CSV ใหม่
        csv_proc.write_dicts_to_csv(filtered_sales_with_summary, output_filtered_csv_path, csv_fieldnames)
    else:
        logger.error("ไม่มีข้อมูลยอดขายจาก CSV ให้ประมวลผล")

    logger.info("--- เริ่มต้นกระบวนการประมวลผลข้อมูล JSON ---")
    # 1. อ่านข้อมูลคลังสินค้า JSON
    inventory_data = json_proc.read_json(input_json_path)
    if inventory_data:
        # 2. อัปเดตสต็อกสินค้าที่มีอยู่
        json_proc.update_inventory(inventory_data, "PROD001", 60)
        json_proc.update_inventory(inventory_data, "PROD003", 75)

        # 3. เพิ่มสินค้าใหม่
        new_product_entry = {
            "id": "PROD004",
            "name": "Gaming Headset",
            "category": "Audio",
            "stock": 90,
            "details": {
                "brand": "SoundBlaster",
                "features": ["Noise Cancelling", "RGB"]
            }
        }
        json_proc.add_product(inventory_data, new_product_entry)

        # 4. เขียนข้อมูล JSON ที่อัปเดตแล้วลงไฟล์ใหม่
        json_proc.write_json(inventory_data, output_updated_json_path, indent=2)
    else:
        logger.error("ไม่มีข้อมูลคลังสินค้าจาก JSON ให้ประมวลผล")

    logger.info("--- กระบวนการประมวลผลข้อมูลเสร็จสิ้นทั้งหมด ---")

if __name__ == "__main__":
    main()