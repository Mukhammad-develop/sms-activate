"""
Configuration file for SMS-Activate Bot
Load settings from environment variables or .env file
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

# SMS-Activate API Configuration
SMS_ACTIVATE_API_KEY = os.getenv('SMS_ACTIVATE_API_KEY', '')

# Bot Settings
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
TIMEOUT = int(os.getenv('TIMEOUT', '10'))

# API Settings
API_BASE_URL = 'https://api.sms-activate.ae/stubs/handler_api.php'

# Validation
def validate_config():
    """Validate that all required configuration is present"""
    errors = []
    
    if not TELEGRAM_BOT_TOKEN:
        errors.append("TELEGRAM_BOT_TOKEN is not set")
    
    if not SMS_ACTIVATE_API_KEY:
        errors.append("SMS_ACTIVATE_API_KEY is not set")
    
    if errors:
        error_msg = "\n".join(f"  - {error}" for error in errors)
        raise ValueError(f"Configuration errors:\n{error_msg}")
    
    return True

if __name__ == '__main__':
    try:
        validate_config()
        print("✅ Configuration is valid!")
        print(f"\nBot Token: {TELEGRAM_BOT_TOKEN[:10]}...")
        print(f"API Key: {SMS_ACTIVATE_API_KEY[:10]}...")
    except ValueError as e:
        print(f"❌ {e}")

