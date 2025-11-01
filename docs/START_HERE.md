# 🚀 START HERE - Quick Deployment Guide

Your Telegram bot token is already configured! Follow these simple steps:

## ✅ What's Already Done

- ✅ Bot token configured: `7345502778:AAE43KA9WO4sDRdyo8CYL9igkzzuadyQdnc`
- ✅ All code files created
- ✅ Multi-language support (English, Russian, Uzbek)
- ✅ User balance system ready
- ✅ Superuser functionality implemented

## 🔴 What You Need To Do (3 Steps)

### Step 1: Get Your Telegram User ID

1. Open Telegram
2. Search for: **@userinfobot**
3. Send `/start` to the bot
4. Copy the number it sends you (example: 123456789)

### Step 2: Set Your Superuser ID

Open `bot.py` in a text editor and find **line 31**:

```python
SUPERUSER_ID = 0  # Replace with your Telegram user ID
```

Change it to your actual ID:

```python
SUPERUSER_ID = 123456789  # ← Put your ID here
```

Save the file.

### Step 3: Get SMS-Activate API Key

1. Visit: https://sms-activate.ae
2. Register/Login
3. Go to API section in your account
4. Copy your API key
5. Create/edit `.env` file in this directory:

```
TELEGRAM_BOT_TOKEN=7345502778:AAE43KA9WO4sDRdyo8CYL9igkzzuadyQdnc
SMS_ACTIVATE_API_KEY=paste_your_api_key_here
```

## 🎯 Deploy and Run

### Option A: Automated Setup (Recommended)

Run the deployment script:

```bash
./deploy_local.sh
```

Then start the bot:

```bash
./run.sh
```

### Option B: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the bot
python3 bot.py
```

## 📱 Test Your Bot

1. Open Telegram
2. Search for your bot (the name you gave it in @BotFather)
3. Click **Start**
4. Select your language (Uzbek/Russian/English)
5. Try these commands:
   - `/balance` - Check balance (will be 0)
   - `/help` - See all commands

## 💰 Add Balance to Users

As superuser, you can add balance to any user:

```
/addbalance <user_id> <amount>
```

Example:
```
/addbalance 123456789 1000
```

This adds 1000 RUB to user with ID 123456789.

## 🔐 Superuser Commands

You'll have access to these special commands:

- `/stats` - View bot statistics
- `/users` - List all users and their balances
- `/mainbalance` - Check the main API account balance
- `/addbalance <user_id> <amount>` - Add balance to a user
- `/deductbalance <user_id> <amount>` - Remove balance from a user
- `/allhistory` - View all transactions from all users

## 👥 User Commands (Available to Everyone)

Regular users can:

- `/balance` - Check their balance
- `/deposit` - Request balance top-up (sends them to contact you)
- `/services` - View available services
- `/countries` - View available countries
- `/prices` - Check prices
- `/buy <service> <country>` - Buy a virtual number (example: `/buy wa 2`)
- `/myorders` - View their active orders
- `/check <order_id>` - Check SMS status
- `/cancel <order_id>` - Cancel an order (balance refunded)
- `/history` - View their transaction history
- `/language` - Change language

## 🌐 Multi-Language Support

Users can choose from:
- 🇬🇧 English
- 🇷🇺 Russian (Русский)
- 🇺🇿 Uzbek (O'zbek)

## 📊 How It Works

1. **User Registration**: New users start with 0 balance
2. **Balance Top-Up**: Users request deposit, you add balance manually
3. **Purchase**: Users buy numbers, balance is deducted automatically
4. **Refunds**: If order is cancelled, balance is refunded automatically
5. **Tracking**: All transactions are logged and viewable

## ⚙️ System Features

✅ **Separate Balances**: Each user has their own balance
✅ **Main Balance Hidden**: Users can't see the main API balance
✅ **Transaction History**: Every transaction is logged
✅ **Multi-Language**: Uzbek, Russian, English
✅ **Superuser Access**: Full control and statistics
✅ **Auto Refunds**: Cancelled orders refund automatically
✅ **Persistent Storage**: All data saved in `users.json`

## 🐛 Troubleshooting

**Bot won't start?**
```bash
# Check Python version
python3 --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Can't find your User ID?**
- Message @userinfobot on Telegram
- Or use @getidsbot

**API errors?**
- Verify your SMS-Activate API key is correct in `.env`
- Check your SMS-Activate account has balance

**Bot not responding?**
- Make sure bot is running (terminal should show logs)
- Check bot token is correct
- Restart the bot: Press Ctrl+C, then run again

## 📝 Example Usage Flow

```
You (Superuser):
1. /start
2. Select English
3. /addbalance 987654321 500  (add 500 RUB to user)
4. /stats  (view statistics)

Regular User (ID: 987654321):
1. /start
2. Select language
3. /balance  (sees 500 RUB)
4. /buy wa 2  (buy WhatsApp number for Kazakhstan)
5. /check 123456  (check for SMS)
6. /history  (view transactions)
```

## 🎉 You're All Set!

Once you complete the 3 steps above and run the bot, it will be fully operational!

**Keep the terminal open** while the bot is running. To stop it, press `Ctrl+C`.

---

**Need Help?**
- Read `README.md` for detailed documentation
- Check `DEPLOYMENT.md` for advanced deployment options
- Review `SERVICE_CODES.md` for service/country codes

