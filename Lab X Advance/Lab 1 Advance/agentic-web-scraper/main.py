# agentic-web-scraper/main.py
import sys
import os
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from config_parser import ConfigParser
from scraper_agent import ScraperAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """จุดเริ่มต้นหลักสำหรับรัน Agentic Web Scraper"""
    config_file_path = os.path.join(os.path.dirname(__file__), 'configs', 'example_site_config.json')
    try:
        config_parser = ConfigParser(config_file_path)
        config = config_parser.load_config()

        # กำหนดเบราว์เซอร์และโหมด headless (ตั้งเป็น False หากต้องการดูหน้าจอเบราว์เซอร์ทำงาน)
        scraper_agent = ScraperAgent(config, browser='chrome', headless=True)
        scraper_agent.run()
    except Exception as e:
        logging.critical(f"An unexpected error occurred during execution: {e}")

if __name__ == "__main__":
    main()