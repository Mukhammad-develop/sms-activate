#!/bin/bash

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║   SMS-Activate Bot - Quick Start                  ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Check if bot.py has SUPERUSER_ID set
if grep -q "SUPERUSER_ID = 0" bot.py; then
    echo "⚠️  SUPERUSER_ID is not configured!"
    echo ""
    echo "📋 Follow these steps:"
    echo ""
    echo "1. Get your Telegram User ID from @userinfobot"
    echo "2. Open bot.py and find line 31"
    echo "3. Change SUPERUSER_ID = 0 to SUPERUSER_ID = YOUR_ID"
    echo ""
    echo "Example: SUPERUSER_ID = 123456789"
    echo ""
    read -p "Press Enter after you've done this..."
fi

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file..."
    cat > .env << 'EOF'
TELEGRAM_BOT_TOKEN=7345502778:AAE43KA9WO4sDRdyo8CYL9igkzzuadyQdnc
SMS_ACTIVATE_API_KEY=your_api_key_here
EOF
    echo "✅ Created .env file"
fi

# Check if API key is set
if grep -q "your_api_key_here" .env 2>/dev/null; then
    echo ""
    echo "⚠️  SMS-Activate API key is not configured!"
    echo ""
    echo "📋 Follow these steps:"
    echo ""
    echo "1. Go to https://sms-activate.ae"
    echo "2. Login and go to API section"
    echo "3. Copy your API key"
    echo "4. Open .env file in this folder"
    echo "5. Replace 'your_api_key_here' with your actual key"
    echo ""
    read -p "Press Enter after you've done this..."
fi

# Setup virtual environment
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate and install
echo ""
echo "📥 Installing dependencies..."
source venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Dependencies installed"

# Run the bot
echo ""
echo "🚀 Starting bot..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python3 bot.py

