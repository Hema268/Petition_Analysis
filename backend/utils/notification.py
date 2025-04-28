from twilio.rest import Client
from config.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_notification(message, recipient_number):
    """
    Send an SMS notification using Twilio.

    Args:
        message (str): The message to send.
        recipient_number (str): The recipient's phone number.
    """
    try:
        # Send the SMS
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=recipient_number
        )
        print(f"✅ Notification sent successfully to {recipient_number}!")
    except Exception as e:
        print(f"❌ Error sending notification: {e}")
