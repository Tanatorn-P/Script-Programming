# email-sms-automator/main.py
import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from email_sender import EmailSender
from email_receiver import EmailReceiver
from sms_gateway import SMSGateway
from utils import setup_logging, get_env_variable, ensure_directory_exists

logger = setup_logging(__name__)

def main():
    """จุดเริ่มต้นหลักสำหรับรันระบบ Automation การสื่อสาร"""
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, 'data')
    attachments_dir = os.path.join(data_dir, 'attachments')
    ensure_directory_exists(data_dir)
    ensure_directory_exists(attachments_dir)

    try:
        sender_email = get_env_variable("SENDER_EMAIL")
        sender_app_password = get_env_variable("SENDER_APP_PASSWORD")
        smtp_server = get_env_variable("SMTP_SERVER")
        smtp_port = int(get_env_variable("SMTP_PORT"))
        imap_server = get_env_variable("IMAP_SERVER")
        test_recipient_email = get_env_variable("TEST_RECIPIENT_EMAIL")
        test_sms_phone_number = get_env_variable("TEST_SMS_PHONE_NUMBER")
        test_sms_carrier = get_env_variable("TEST_SMS_CARRIER")
    except ValueError as e:
        logger.critical(f"Configuration error: {e}")
        sys.exit(1)

    email_sender = EmailSender(smtp_server, smtp_port, sender_email, sender_app_password)
    email_receiver = EmailReceiver(imap_server, sender_email, sender_app_password)
    sms_gateway = SMSGateway(email_sender)

    # Task 1: ส่งอีเมลแบบ Text ธรรมดา
    logger.info("\n--- Task 1: Sending a simple plaintext email ---")
    email_sender.send_email(test_recipient_email, "Automated Test Email", "ธนธรณ์ ผาลัง 683380576-2")
    time.sleep(2)

    # Task 2: ส่งอีเมลพร้อมแนบไฟล์ PDF
    logger.info("\n--- Task 2: Sending an email with an attachment ---")
    attachment_path = os.path.join(data_dir, 'dummy_report.pdf')
    if os.path.exists(attachment_path):
        email_sender.send_email(test_recipient_email, "Test Email with Attachment", "Please find the report attached.", attachment_path)
    time.sleep(2)

    # Task 3: ส่ง SMS ผ่าน Email Gateway
    logger.info("\n--- Task 3: Sending an SMS via email gateway ---")
    sms_gateway.send_sms(test_sms_phone_number, "Hello from Python via SMS Gateway!", test_sms_carrier)
    time.sleep(3)

    # Task 4: รับและประมวลผลอีเมล
    logger.info("\n--- Task 4: Receiving and processing emails ---")
    email_sender.send_email(sender_email, "Python Test: Email for Receiving Demo", "Demo email body with attachment.", attachment_path)
    time.sleep(8)

    uids = email_receiver.search_emails(criteria='UNSEEN', from_sender=sender_email, subject_contains="Python Test: Email for Receiving Demo")
    if uids:
        for uid in uids:
            email_details = email_receiver.fetch_email_content(uid=uid, mark_as_read=True, download_attachments_dir=attachments_dir)
            if email_details:
                logger.info(f"Received Subject: {email_details['subject']}")
                logger.info(f"Downloaded Attachments: {email_details['attachments_downloaded']}")

    logger.info("\n--- All tasks completed ---")

if __name__ == "__main__":
    main()