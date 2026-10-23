# web-scraping-intro/src/scraper.py
import requests
from bs4 import BeautifulSoup


class SimpleWebScraper:
    """
    คลาสสำหรับรวมฟังก์ชันการทำ web scraping พื้นฐาน
    ปรับให้ใช้กับเว็บไซต์ Automate the Boring Stuff (3rd Edition)
    """

    def __init__(self, target_url):
        self.target_url = target_url

    def _get_html_content(self):
        """
        ดาวน์โหลดเนื้อหา HTML จาก URL เป้าหมาย
        มีการตรวจสอบข้อผิดพลาดพื้นฐาน
        """
        print(f"กำลังดาวน์โหลดเนื้อหาจาก: {self.target_url}")
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(self.target_url, headers=headers, timeout=30)
            response.raise_for_status()
            print("ดาวน์โหลดเนื้อหาสำเร็จ")
            return response.text
        except requests.exceptions.HTTPError as e:
            print(f"เกิดข้อผิดพลาด HTTP: {e} - Status Code: {e.response.status_code}")
            return None
        except requests.exceptions.ConnectionError as e:
            print(f"เกิดข้อผิดพลาดการเชื่อมต่อ: {e} - ไม่สามารถเชื่อมต่อกับ {self.target_url}")
            return None
        except requests.exceptions.Timeout:
            print("การ request หมดเวลา")
            return None
        except requests.exceptions.RequestException as e:
            print(f"เกิดข้อผิดพลาด request ที่ไม่คาดคิด: {e}")
            return None

    def scrape_main_titles(self):
        """
        ดึงชื่อหนังสือหลักและรายการชื่อบทต่างๆ
        จากหน้าแรกของ Automate the Boring Stuff (3rd Edition)
        """
        html_content = self._get_html_content()
        if not html_content:
            return None

        soup = BeautifulSoup(html_content, 'html.parser')

        # --- ดึงชื่อหนังสือ ---
        # โครงสร้าง: <article> -> <header> -> <h1 itemprop="name headline">
        book_title = "ไม่พบชื่อหนังสือ"
        article_tag = soup.find('article')
        if article_tag:
            header_tag = article_tag.find('header')
            if header_tag:
                h1_tag = header_tag.find('h1')
                if h1_tag:
                    book_title = h1_tag.get_text(strip=True)

        # --- ดึงรายการชื่อบท ---
        # โครงสร้าง: <div class="content-body"> -> <ul> -> <li> -> <a.
        chapter_titles = []
        content_body = soup.find('div', class_='content-body')
        if content_body:
            chapter_links = content_body.select('ul li a')
            for link in chapter_links:
                title = link.get_text(strip=True)
                if title:
                    chapter_titles.append(title)

        return {
            "book_title": book_title,
            "chapter_titles": chapter_titles
        }
