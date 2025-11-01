#!/bin/bash

echo "🚀 SMS-Activate Bot Setup Script"
echo "================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Dependencies installed successfully!"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your credentials:"
    echo "    - TELEGRAM_BOT_TOKEN"
    echo "    - SMS_ACTIVATE_API_KEY"
    echo ""
    echo "You can get:"
    echo "  - Telegram Bot Token from: https://t.me/botfather"
    echo "  - SMS-Activate API Key from: https://sms-activate.ae"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To run the bot:"
echo "  1. Edit .env file with your credentials"
echo "  2. Activate virtual environment: source venv/bin/activate"
echo "  3. Run the bot: python bot.py"
echo ""
echo "Or simply run: ./run.sh"

