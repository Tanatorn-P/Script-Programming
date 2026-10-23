# agentic-web-scraper/src/scraper_agent.py
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import logging
from driver_manager import DriverManager
from data_models import Product
from utils import wait_for_element, robust_click, save_data_to_json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ScraperAgent:
    """Agentic Web Scraper ที่ทำงานตามคอนฟิกูเรชันที่กำหนด"""
    def __init__(self, config, browser='chrome', headless=True):
        self.config = config
        self.driver_manager = DriverManager(browser_name=browser, headless=headless)
        self.driver = None
        self.scraped_products = []
        self.max_pages = config.get("max_pages", 5)
        logging.info(f"Scraper Agent initialized with config for {config['start_url']}")

    def _get_element_text(self, parent_element, selector, selector_type=By.CSS_SELECTOR):
        try:
            element = parent_element.find_element(selector_type, selector)
            return element.text.strip()
        except NoSuchElementException:
            return None

    def _get_element_attribute(self, parent_element, selector, attribute, selector_type=By.CSS_SELECTOR):
        try:
            element = parent_element.find_element(selector_type, selector)
            return element.get_attribute(attribute).strip()
        except NoSuchElementException:
            return None

    def _parse_product_data(self, item_element):
        """
        Extracts product data from a single product item element based on config selectors.
        """
        selectors = self.config["item_data_selectors"]
        
        # ดึงข้อมูลเฉพาะเมื่อ selector ไม่เป็น None หรือค่าว่าง
        name_sel = selectors.get("name")
        price_sel = selectors.get("price")
        desc_sel = selectors.get("description")
        url_sel = selectors.get("url")
        img_sel = selectors.get("image_url")

        name = self._get_element_text(item_element, name_sel) if name_sel else None
        price = self._get_element_text(item_element, price_sel) if price_sel else None
        description = self._get_element_text(item_element, desc_sel) if desc_sel else None
        url = self._get_element_attribute(item_element, url_sel, "href") if url_sel else None
        image_url = self._get_element_attribute(item_element, img_sel, "src") if img_sel else None

        if name and price: # Basic validation for a valid product
            return Product(name=name, price=price, description=description, url=url, image_url=image_url)
        return None

    def scrape_page(self):
        logging.info(f"Scraping page: {self.driver.current_url}")
        try:
            item_elements = self.driver.find_elements(By.CSS_SELECTOR, self.config["item_container_selector"])
            if not item_elements:
                item_elements = self.driver.find_elements(By.XPATH, self.config["item_container_selector"])

            logging.info(f"Found {len(item_elements)} potential product items.")
            for item_element in item_elements:
                product = self._parse_product_data(item_element)
                if product:
                    self.scraped_products.append(product.to_dict())
        except Exception as e:
            logging.error(f"Error while scraping items: {e}")

    def run(self):
        self.driver = self.driver_manager.get_driver()
        if not self.driver:
            logging.error("Failed to get WebDriver. Exiting.")
            return
        try:
            self.driver.get(self.config["start_url"])
            current_page = 1
            while current_page <= self.max_pages:
                logging.info(f"Processing page {current_page}")
                self.scrape_page()
                time.sleep(self.config.get("delay_between_pages", 2))

                pagination_selector = self.config["pagination_selector"]
                if pagination_selector:
                    try:
                        next_page_button = wait_for_element(self.driver, By.CSS_SELECTOR, pagination_selector, timeout=5)
                        if not next_page_button:
                            next_page_button = wait_for_element(self.driver, By.XPATH, pagination_selector, timeout=5)

                        if next_page_button and next_page_button.is_displayed() and next_page_button.is_enabled():
                            robust_click(self.driver, By.CSS_SELECTOR, pagination_selector)
                            current_page += 1
                        else:
                            break
                    except (NoSuchElementException, TimeoutException):
                        break
                else:
                    break
        finally:
            self.driver_manager.quit_driver()
            logging.info(f"Scraping finished. Total products: {len(self.scraped_products)}")
            save_data_to_json(self.scraped_products, "scraped_products.json")