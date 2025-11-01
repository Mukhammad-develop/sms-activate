# PythonAnywhere Deployment Guide

## 🚀 Quick Deploy Commands

### Step 1: Open Bash Console on PythonAnywhere

Go to: **Dashboard → Consoles → Bash**

---

### Step 2: Clone Repository

```bash
cd ~
git clone https://github.com/Mukhammad-develop/sms-activate.git
cd sms-activate
```

---

### Step 3: Create Virtual Environment

```bash
python3.10 -m venv venv
source venv/bin/activate
```

---

### Step 4: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Step 5: Create .env File

```bash
cat > .env << 'EOF'
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=7345502778:AAE43KA9WO4sDRdyo8CYL9igkzzuadyQdnc

# SMS-Activate API Configuration
SMS_ACTIVATE_API_KEY=A4351cecA75b3d22f0eb3e2bc351dcc5
EOF
```

---

### Step 6: Test Bot Manually (Optional)

```bash
python bot.py
# Press Ctrl+C to stop after testing
```

---

### Step 7: Create Always-On Task Script

```bash
cat > run_bot.sh << 'EOF'
#!/bin/bash
cd /home/YOUR_USERNAME/sms-activate
source venv/bin/activate
python bot.py
EOF

chmod +x run_bot.sh
```

**⚠️ Replace `YOUR_USERNAME` with your PythonAnywhere username!**

---

### Step 8: Configure Always-On Task

1. Go to: **Dashboard → Tasks → Always-on tasks** (Paid accounts only)
2. Click **"Add a new always-on task"**
3. **Command:** `/home/YOUR_USERNAME/sms-activate/run_bot.sh`
4. Click **"Create"**
5. Click **"Enable"** to start

---

## 🔧 Alternative: Using Screen (Free Account)

If you don't have Always-on tasks, use `screen`:

```bash
cd ~/sms-activate
source venv/bin/activate

# Start screen session
screen -S sms-bot

# Run bot
python bot.py

# Detach: Press Ctrl+A then D
# Bot keeps running in background!

# To reattach later:
screen -r sms-bot
```

**⚠️ Note:** Screen sessions may be terminated on free accounts after 24 hours of inactivity.

---

## 📋 Complete One-Liner (All Steps)

Copy and paste this entire block:

```bash
cd ~ && \
git clone https://github.com/Mukhammad-develop/sms-activate.git && \
cd sms-activate && \
python3.10 -m venv venv && \
source venv/bin/activate && \
pip install --upgrade pip && \
pip install -r requirements.txt && \
cat > .env << 'EOF'
TELEGRAM_BOT_TOKEN=7345502778:AAE43KA9WO4sDRdyo8CYL9igkzzuadyQdnc
SMS_ACTIVATE_API_KEY=A4351cecA75b3d22f0eb3e2bc351dcc5
EOF
echo "✅ Setup complete! Now create Always-on task or use screen."
```

Then create the runner script:

```bash
cat > run_bot.sh << 'EOF'
#!/bin/bash
cd /home/YOUR_USERNAME/sms-activate
source venv/bin/activate
python bot.py
EOF
chmod +x run_bot.sh
sed -i "s/YOUR_USERNAME/$(whoami)/" run_bot.sh
echo "✅ Runner script created: run_bot.sh"
```

---

## 🔍 Monitoring & Management

### Check if Bot is Running

```bash
ps aux | grep bot.py
```

### View Logs

```bash
cd ~/sms-activate
tail -f bot.log
```

### Stop Bot

```bash
pkill -f bot.py
```

### Restart Bot

```bash
pkill -f bot.py
cd ~/sms-activate
source venv/bin/activate
python bot.py &
```

---

## 🔄 Update Bot from GitHub

```bash
cd ~/sms-activate
pkill -f bot.py  # Stop bot
git pull origin main  # Update code
source venv/bin/activate
pip install -r requirements.txt  # Update dependencies
python bot.py &  # Restart bot
```

---

## 📊 Always-On Task Configuration

### Dashboard Settings:
- **Working directory:** `/home/YOUR_USERNAME/sms-activate`
- **Command:** `/home/YOUR_USERNAME/sms-activate/run_bot.sh`
- **Description:** SMS-Activate Telegram Bot
- **Enabled:** ✅ Yes

### If Task Fails:
1. Check logs: `tail -f ~/sms-activate/bot.log`
2. Test manually: `cd ~/sms-activate && source venv/bin/activate && python bot.py`
3. Check .env file: `cat ~/sms-activate/.env`
4. Verify dependencies: `pip list`

---

## ⚠️ Important Notes

### 1. **PythonAnywhere Limitations:**
- Free accounts: No Always-on tasks (use screen)
- Paid accounts: Always-on tasks available
- CPU usage limits apply
- Outbound internet may be restricted on free accounts

### 2. **API Access:**
- SMS-Activate API requires outbound HTTPS
- Add `api.sms-activate.ae` to whitelist (paid accounts)
- Free accounts may have connection issues

### 3. **Database:**
- SQLite database (`users.json`) is local
- Backup regularly: `cp ~/sms-activate/users.json ~/backup/`

### 4. **Bot Token:**
- Keep `.env` file secure
- Don't commit to git (already in .gitignore)
- Regenerate if exposed

---

## 🆘 Troubleshooting

### Bot Won't Start:

```bash
cd ~/sms-activate
source venv/bin/activate
python bot.py  # Check error messages
```

### "Module not found" Error:

```bash
cd ~/sms-activate
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

### "Permission denied" Error:

```bash
chmod +x ~/sms-activate/*.sh
```

### Database Error:

```bash
cd ~/sms-activate
rm users.json  # Recreates on next run
python bot.py
```

---

## 📱 Verify Deployment

1. Open Telegram
2. Find your bot: `@YOUR_BOT_NAME`
3. Send `/start`
4. Should see welcome message in 3 languages
5. Check channel logs: `@dawefsgrdntfghmfnbdrsefasgrdhtfj`

---

## 🎯 Quick Reference

```bash
# Start bot
cd ~/sms-activate && source venv/bin/activate && python bot.py &

# Stop bot
pkill -f bot.py

# View logs
tail -f ~/sms-activate/bot.log

# Check status
ps aux | grep bot.py

# Update bot
cd ~/sms-activate && git pull && pkill -f bot.py && source venv/bin/activate && python bot.py &
```

---

## 💰 Cost Consideration

**Free Account:**
- ✅ Can run bot using screen
- ❌ No Always-on tasks
- ❌ May have API restrictions
- ⚠️ Session timeout after 24h inactivity

**Paid Account ($5/month Hacker plan):**
- ✅ Always-on tasks (bot runs 24/7)
- ✅ Unrestricted API access
- ✅ No session timeouts
- ✅ More CPU/RAM

**Recommended:** Paid account for production bot

---

**Your bot is now deployed on PythonAnywhere!** 🎉

