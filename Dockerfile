FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY bot.py .
COPY config.py .

# Set environment variables (override these when running)
ENV TELEGRAM_BOT_TOKEN=""
ENV SMS_ACTIVATE_API_KEY=""

# Run the bot
CMD ["python", "bot.py"]

