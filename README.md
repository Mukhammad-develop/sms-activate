# SMS-Activate Telegram Bot

A comprehensive Telegram bot for interacting with the SMS-Activate API to receive SMS verification codes on virtual numbers.

## Features

- 💰 **Balance Management** - Check your account balance
- 📋 **Service Browsing** - View all available services
- 🌍 **Country Selection** - Browse available countries
- 💵 **Price Checking** - Get current pricing information
- 📱 **Number Purchasing** - Buy virtual numbers for verification
- 📊 **Activation Management** - View and manage active activations
- 🔍 **Status Checking** - Check SMS status in real-time
- ❌ **Cancellation** - Cancel unwanted activations
- ✅ **Completion** - Mark activations as complete

## Installation

### Prerequisites

- Python 3.7 or higher
- A Telegram Bot Token (get it from [@BotFather](https://t.me/botfather))
- SMS-Activate API Key (get it from [SMS-Activate](https://sms-activate.ae))

### Setup

1. **Clone or download this repository**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**

Create a `.env` file in the project directory:
```bash
cp .env.example .env
```

Edit the `.env` file and add your credentials:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
SMS_ACTIVATE_API_KEY=your_sms_activate_api_key_here
```

Or export them directly:
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export SMS_ACTIVATE_API_KEY="your_api_key_here"
```

4. **Run the bot:**
```bash
python bot.py
```

Or make it executable:
```bash
chmod +x bot.py
./bot.py
```

## Usage

### Available Commands

- `/start` or `/help` - Show welcome message and available commands
- `/balance` - Check your account balance
- `/services` - Get list of available services
- `/countries` - Get list of available countries
- `/prices [service] [country]` - Get pricing information
- `/getnumber <service> <country>` - Purchase a virtual number
- `/activations` - View all active activations
- `/status <activation_id>` - Check status of an activation
- `/cancel <activation_id>` - Cancel an activation
- `/finish <activation_id>` - Mark activation as complete

### Example Workflow

1. **Check your balance:**
```
/balance
```

2. **Browse available services:**
```
/services
```

3. **Purchase a number for WhatsApp in Kazakhstan:**
```
/getnumber wa 2
```
This will return an activation ID and phone number.

4. **Check for SMS:**
```
/status 635468024
```

5. **If you receive the code, finish the activation:**
```
/finish 635468024
```

6. **Or cancel if not needed:**
```
/cancel 635468024
```

### Common Service Codes

- `wa` - WhatsApp
- `tg` - Telegram
- `vi` - Viber
- `go` - Google
- `fb` - Facebook
- `vk` - VKontakte
- `ig` - Instagram
- `tw` - Twitter

### Common Country Codes

- `1` - Ukraine
- `2` - Kazakhstan
- `6` - Russia
- `66` - India
- `187` - Philippines

Use `/services` and `/countries` commands to see full lists.

## API Documentation

This bot uses the SMS-Activate API. For detailed API documentation, refer to:
- `api-documentation.txt` - Comprehensive API reference
- `api-protocol-for-working-with-sms-activate.json` - OpenAPI specification

## Error Handling

The bot provides helpful error messages for common issues:

- **NO_NUMBERS** - No numbers available for the service/country
- **NO_BALANCE** - Insufficient balance
- **BAD_SERVICE** - Invalid service code
- **BAD_KEY** - Invalid API key
- **EARLY_CANCEL_DENIED** - Cannot cancel within first 2 minutes
- **NO_ACTIVATION** - Activation ID not found

## Architecture

### Files Structure

```
sms-activate/
├── bot.py                          # Main bot application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .env                           # Your actual credentials (not in git)
├── README.md                      # This file
├── api-documentation.txt          # API reference
└── api-protocol-for-working-with-sms-activate.json  # OpenAPI spec
```

### Code Structure

- **SMSActivateAPI** - API wrapper class with methods for all API endpoints
- **SMSActivateBot** - Main bot class with command handlers
- Handler methods for each command
- Error handling and user-friendly responses

## Development

### Adding New Features

1. Add new methods to `SMSActivateAPI` class for API calls
2. Add handler methods in `SMSActivateBot` class
3. Register handlers in `_register_handlers` method
4. Update the help text in `handle_start` method

### Logging

The bot uses Python's logging module. Logs include:
- INFO level: General bot operations
- ERROR level: API failures and exceptions

## Security Notes

- **Never commit your `.env` file** to version control
- Keep your API keys secure
- The `.gitignore` should include `.env`
- Use environment variables for sensitive data

## Troubleshooting

### Bot not responding
- Check if the bot token is correct
- Verify the bot is running without errors
- Check your internet connection

### API errors
- Verify your SMS-Activate API key
- Check your account balance
- Ensure the service/country combination is available

### Connection errors
- Check firewall settings
- Verify SMS-Activate API is accessible
- Try restarting the bot

## Support

For issues with:
- **The bot:** Check logs and error messages
- **SMS-Activate API:** Visit [SMS-Activate Support](https://sms-activate.ae)
- **Telegram Bot API:** Check [Telegram Bot Documentation](https://core.telegram.org/bots/api)

## License

This project is provided as-is for educational and personal use.

## Contributing

Feel free to submit issues and enhancement requests!

## Disclaimer

This bot is a third-party tool and is not officially affiliated with SMS-Activate. Use at your own risk and in compliance with SMS-Activate's terms of service.

