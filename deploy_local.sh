#!/bin/bash

echo "🚀 SMS-Activate Bot - Local Deployment"
echo "======================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cat > .env << 'EOF'
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=7345502778:AAE43KA9WO4sDRdyo8CYL9igkzzuadyQdnc

# SMS-Activate API Configuration
# Get your API key from https://sms-activate.ae
SMS_ACTIVATE_API_KEY=your_sms_activate_api_key_here
EOF
    echo -e "${GREEN}✅ .env file created${NC}"
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
fi

echo ""
echo -e "${YELLOW}📝 IMPORTANT SETUP STEPS:${NC}"
echo ""
echo "1️⃣  Get your Telegram User ID:"
echo "   - Open Telegram and message @userinfobot"
echo "   - Copy your User ID"
echo ""
echo "2️⃣  Edit bot.py (line 31):"
echo "   Change: SUPERUSER_ID = 0"
echo "   To:     SUPERUSER_ID = YOUR_USER_ID"
echo ""
echo "3️⃣  Get SMS-Activate API Key:"
echo "   - Visit: https://sms-activate.ae"
echo "   - Go to API settings"
echo "   - Copy your API key"
echo ""
echo "4️⃣  Edit .env file:"
echo "   Replace 'your_sms_activate_api_key_here' with your actual API key"
echo ""
echo -e "${YELLOW}Press Enter when you've completed these steps...${NC}"
read

echo ""
echo "🔧 Setting up environment..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${GREEN}✅ Virtual environment exists${NC}"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo -e "${GREEN}✅ Dependencies installed${NC}"
echo ""

# Verify configuration
echo "🔍 Verifying configuration..."
python3 << 'PYEOF'
import os

# Check bot token
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        content = f.read()
        if 'your_sms_activate_api_key_here' in content:
            print("⚠️  WARNING: SMS-Activate API key is not set in .env file!")
        else:
            print("✅ .env file configured")

# Check superuser ID
with open('bot.py', 'r') as f:
    content = f.read()
    if 'SUPERUSER_ID = 0' in content:
        print("⚠️  WARNING: SUPERUSER_ID is still 0 in bot.py!")
        print("   Please edit bot.py and set your Telegram User ID")
    else:
        print("✅ SUPERUSER_ID is configured")
PYEOF

echo ""
echo -e "${GREEN}🎉 Setup complete!${NC}"
echo ""
echo "To start the bot, run:"
echo -e "${YELLOW}  ./run.sh${NC}"
echo ""
echo "Or manually:"
echo -e "${YELLOW}  source venv/bin/activate${NC}"
echo -e "${YELLOW}  python3 bot.py${NC}"
echo ""

