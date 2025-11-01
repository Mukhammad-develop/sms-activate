# Quick Installation Guide

## Step 1: Get Your User ID (Important!)

Before running the bot, you need to get your Telegram User ID:

1. Open Telegram
2. Search for **@userinfobot**
3. Start a chat and it will send you your User ID
4. Copy that number (e.g., 123456789)

## Step 2: Edit bot.py

Open `bot.py` and find line 31:

```python
SUPERUSER_ID = 0  # Replace with your Telegram user ID
```

Change it to your User ID:

```python
SUPERUSER_ID = 123456789  # Your actual User ID
```

## Step 3: Add Your SMS-Activate API Key

1. Go to https://sms-activate.ae
2. Create an account or login
3. Go to API settings and copy your API key
4. Open the `.env` file
5. Replace `your_sms_activate_api_key_here` with your actual API key

Your `.env` file should look like:
```
TELEGRAM_BOT_TOKEN=7345502778:AAE43KA9WO4sDRdyo8CYL9igkzzuadyQdnc
SMS_ACTIVATE_API_KEY=A8b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

## Step 4: Install Dependencies

Run the setup script:

```bash
chmod +x setup.sh
./setup.sh
```

Or install manually:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 5: Run the Bot

Simply run:

```bash
./run.sh
```

Or manually:

```bash
source venv/bin/activate
python3 bot.py
```

## Step 6: Test the Bot

1. Open Telegram
2. Search for your bot (the name you gave it when creating with @BotFather)
3. Click **Start**
4. Select your language
5. Try `/balance` command

## Default Users Have No Balance

- All new users start with 0 balance
- As superuser, you can add balance to users with:
  ```
  /addbalance <user_id> <amount>
  ```
- Example: `/addbalance 123456789 1000` (adds 1000 RUB)

## Superuser Commands

As the superuser, you have access to:

- `/stats` - View bot statistics
- `/users` - List all registered users
- `/mainbalance` - Check the main API balance
- `/addbalance <user_id> <amount>` - Add balance to a user
- `/deductbalance <user_id> <amount>` - Deduct balance from a user
- `/allhistory` - View all transactions

## Troubleshooting

**Bot won't start?**
- Check if `.env` file has correct API keys
- Make sure you edited SUPERUSER_ID in bot.py
- Check if port 8443 or other ports are available

**"Module not found" error?**
- Make sure virtual environment is activated: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

**Bot not responding in Telegram?**
- Check if bot is running (you should see logs in terminal)
- Verify bot token is correct
- Check your internet connection

## Next Steps

1. Add balance to yourself: `/addbalance YOUR_USER_ID 1000`
2. Try buying a number: `/buy wa 2` (WhatsApp in Kazakhstan)
3. Check the status: `/check <activation_id>`
4. View your transactions: `/history`

**Important:** Keep the terminal window open while the bot is running!

To stop the bot, press `Ctrl+C` in the terminal.

