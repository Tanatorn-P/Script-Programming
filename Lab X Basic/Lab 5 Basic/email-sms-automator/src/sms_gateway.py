# email-sms-automator/src/sms_gateway.py
from utils import setup_logging
from email_sender import EmailSender

logger = setup_logging(__name__)

class SMSGateway:
    """ส่งข้อความ SMS ผ่าน Email-to-SMS Gateway"""
    def __init__(self, email_sender_instance):
        if not isinstance(email_sender_instance, EmailSender):
            raise TypeError("SMSGateway requires an instance of EmailSender.")
        self.email_sender = email_sender_instance
        self.carrier_gateways = {
            "att": "@txt.att.net",
            "verizon": "@vtext.com",
            "tmobile": "@tmomail.net",
        }
        logger.info("SMSGateway initialized.")

    def send_sms(self, phone_number, message, carrier_name=None):
        """ส่งข้อความสั้นไปยังเบอร์โทรศัพท์ผ่าน Email Gateway"""
        sms_gateway_address = None
        if carrier_name and carrier_name.lower() in self.carrier_gateways:
            sms_gateway_address = f"{phone_number}{self.carrier_gateways[carrier_name.lower()]}"
        elif '@' in phone_number:
            sms_gateway_address = phone_number
        else:
            logger.warning("Invalid carrier or phone number configuration for SMS.")
            return False

        if sms_gateway_address:
            return self.email_sender.send_email(sms_gateway_address, "", message)
        return False