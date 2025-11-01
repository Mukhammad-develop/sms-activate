# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Setup

Run the setup script:
```bash
./setup.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Create a `.env` file from template

### Step 2: Configure

Edit the `.env` file and add your credentials:

```bash
nano .env
```

Add:
```
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
SMS_ACTIVATE_API_KEY=your_api_key_from_sms_activate
```

**Where to get these:**
- **Telegram Bot Token**: Message [@BotFather](https://t.me/botfather) on Telegram
  1. Send `/newbot`
  2. Follow the prompts
  3. Copy the token
  
- **SMS-Activate API Key**: 
  1. Visit [sms-activate.ae](https://sms-activate.ae)
  2. Create an account
  3. Go to API settings
  4. Copy your API key

### Step 3: Run

Start the bot:
```bash
./run.sh
```

Or manually:
```bash
source venv/bin/activate
python bot.py
```

## 📱 Using the Bot

1. Open Telegram and search for your bot
2. Start a chat with `/start`
3. Try these commands:
   - `/balance` - Check your balance
   - `/services` - See available services
   - `/getnumber wa 2` - Get a WhatsApp number for Kazakhstan

## 🎯 Quick Example

Get a WhatsApp verification code:

```
1. /balance                    # Check you have funds
2. /getnumber wa 2            # Get number for WhatsApp in Kazakhstan
   → Bot returns: "Activation ID: 123456, Phone: +77001234567"
3. /status 123456             # Check for SMS
   → Bot returns: "Code: 123456"
4. /finish 123456             # Complete activation
```

## ❓ Troubleshooting

**Bot not responding?**
- Check if bot is running (`./run.sh`)
- Verify your bot token is correct
- Make sure bot is not already running

**API errors?**
- Verify your API key
- Check your balance
- Ensure service/country is available

**Need help?**
- Read full `README.md`
- Check `api-documentation.txt`

## 📚 Next Steps

- Read the full [README.md](README.md) for all features
- Check [api-documentation.txt](api-documentation.txt) for API details
- Explore all bot commands with `/help`

## 🔧 Manual Installation (Alternative)

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your credentials
nano .env

# Run the bot
python bot.py
```

---

**Happy SMS receiving! 🎉**

