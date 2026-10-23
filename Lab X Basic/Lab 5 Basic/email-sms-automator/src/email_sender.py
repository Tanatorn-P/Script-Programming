# email-sms-automator/src/email_sender.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from utils import setup_logging

logger = setup_logging(__name__)

class EmailSender:
    """จัดการการส่งอีเมลผ่าน SMTP"""
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.server = None
        logger.info(f"EmailSender initialized for {sender_email} via {smtp_server}:{smtp_port}.")

    def _connect(self):
        """เชื่อมต่อและเข้าสู่ระบบ SMTP Server"""
        try:
            self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self.server.starttls()
            self.server.login(self.sender_email, self.sender_password)
            logger.info("Successfully connected and logged into SMTP server.")
            return True
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP authentication failed. Error: {e}")
            self.server = None
            return False
        except Exception as e:
            logger.error(f"An error occurred during SMTP connect/login: {e}")
            self.server = None
            return False

    def _disconnect(self):
        """ตัดการเชื่อมต่อจาก SMTP Server"""
        if self.server:
            try:
                self.server.quit()
                logger.info("Disconnected from SMTP server.")
            except Exception as e:
                logger.warning(f"Error during SMTP disconnection: {e}")
            finally:
                self.server = None

    def send_email(self, recipient_email, subject, body, attachment_path=None, is_html=False):
        """ส่งอีเมล (รองรับข้อความทั่วไป, HTML และการแนบไฟล์)"""
        if not self._connect():
            return False
            
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        if is_html:
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))

        if attachment_path:
            try:
                with open(attachment_path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
                    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
                    msg.attach(part)
                logger.info(f"Attached file: {attachment_path}")
            except Exception as e:
                logger.error(f"Error attaching file {attachment_path}: {e}")

        try:
            self.server.send_message(msg)
            logger.info(f"Email sent successfully to {recipient_email}.")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}. Error: {e}")
            return False
        finally:
            self._disconnect()