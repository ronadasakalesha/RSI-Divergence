
import requests
from logzero import logger
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_alert(message):
    """
    Sends a message to the configured Telegram chat.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("[TELEGRAM] Telegram credentials not configured. Skipping alert.")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            logger.info("[TELEGRAM] Alert sent successfully!")
            return True
        else:
            logger.error(f"[TELEGRAM] Failed to send alert: {response.text}")
            return False
    except Exception as e:
        logger.error(f"[TELEGRAM] Error sending alert: {e}")
        return False
