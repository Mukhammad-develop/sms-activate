#!/bin/bash

cd /Users/abdurakhmon/Desktop/sms-activate

echo "🤖 Starting SMS-Activate Bot..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Activate virtual environment
source venv/bin/activate

# Start the bot
python3 bot.py

