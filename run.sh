#!/bin/bash

echo "🤖 Starting SMS-Activate Bot..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check configuration
echo "🔍 Checking configuration..."
python3 config.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Configuration check failed. Please check your .env file"
    exit 1
fi

echo ""
echo "✅ Configuration valid!"
echo "🚀 Starting bot..."
echo ""

# Run the bot
python3 bot.py

