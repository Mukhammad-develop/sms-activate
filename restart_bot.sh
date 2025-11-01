#!/bin/bash

echo "🔄 Restarting SMS-Activate Bot..."

# Kill all Python bot processes
killall -9 python3 2>/dev/null

# Wait for processes to terminate and Telegram to release
echo "⏳ Waiting for cleanup..."
sleep 5

# Start bot
cd /Users/abdurakhmon/Desktop/sms-activate
source venv/bin/activate
nohup python3 bot.py > bot.log 2>&1 &

# Wait and check if started
sleep 3

if ps aux | grep -v grep | grep "python3 bot.py" > /dev/null; then
    echo "✅ Bot started successfully!"
    tail -5 bot.log
else
    echo "❌ Bot failed to start. Check bot.log for errors"
    tail -10 bot.log
fi

