# Deployment Guide

This guide covers different ways to deploy the SMS-Activate Telegram Bot.

## Table of Contents

1. [Simple Deployment (Local)](#simple-deployment-local)
2. [Docker Deployment](#docker-deployment)
3. [Systemd Service (Linux)](#systemd-service-linux)
4. [Screen/Tmux (Keep Running)](#screentmux-keep-running)
5. [Cloud Deployment](#cloud-deployment)

---

## Simple Deployment (Local)

For development and testing:

```bash
# Setup
./setup.sh

# Configure .env file
nano .env

# Run
./run.sh
```

To keep it running after closing terminal, see Screen/Tmux section below.

---

## Docker Deployment

### Prerequisites
- Docker installed
- Docker Compose (optional but recommended)

### Using Docker Compose (Recommended)

1. **Configure environment:**
```bash
cp .env.example .env
nano .env  # Add your credentials
```

2. **Build and run:**
```bash
docker-compose up -d
```

3. **View logs:**
```bash
docker-compose logs -f
```

4. **Stop:**
```bash
docker-compose down
```

5. **Restart:**
```bash
docker-compose restart
```

### Using Docker directly

1. **Build the image:**
```bash
docker build -t sms-activate-bot .
```

2. **Run the container:**
```bash
docker run -d \
  --name sms-activate-bot \
  --restart unless-stopped \
  -e TELEGRAM_BOT_TOKEN="your_bot_token" \
  -e SMS_ACTIVATE_API_KEY="your_api_key" \
  sms-activate-bot
```

3. **View logs:**
```bash
docker logs -f sms-activate-bot
```

4. **Stop:**
```bash
docker stop sms-activate-bot
docker rm sms-activate-bot
```

---

## Systemd Service (Linux)

Run the bot as a system service on Linux.

### Setup

1. **Edit the service file:**
```bash
nano sms-activate-bot.service
```

Update these fields:
- `User=your_username` → Your Linux username
- `/path/to/sms-activate` → Full path to bot directory (3 places)

2. **Copy service file:**
```bash
sudo cp sms-activate-bot.service /etc/systemd/system/
```

3. **Reload systemd:**
```bash
sudo systemctl daemon-reload
```

4. **Enable and start:**
```bash
sudo systemctl enable sms-activate-bot
sudo systemctl start sms-activate-bot
```

### Managing the Service

**Check status:**
```bash
sudo systemctl status sms-activate-bot
```

**View logs:**
```bash
sudo journalctl -u sms-activate-bot -f
```

**Restart:**
```bash
sudo systemctl restart sms-activate-bot
```

**Stop:**
```bash
sudo systemctl stop sms-activate-bot
```

**Disable autostart:**
```bash
sudo systemctl disable sms-activate-bot
```

---

## Screen/Tmux (Keep Running)

Keep the bot running in the background using screen or tmux.

### Using Screen

1. **Start a screen session:**
```bash
screen -S sms-bot
```

2. **Run the bot:**
```bash
./run.sh
```

3. **Detach from screen:**
- Press `Ctrl+A`, then `D`

4. **Reattach to screen:**
```bash
screen -r sms-bot
```

5. **List all screens:**
```bash
screen -ls
```

### Using Tmux

1. **Start a tmux session:**
```bash
tmux new -s sms-bot
```

2. **Run the bot:**
```bash
./run.sh
```

3. **Detach from tmux:**
- Press `Ctrl+B`, then `D`

4. **Reattach to tmux:**
```bash
tmux attach -t sms-bot
```

5. **List all sessions:**
```bash
tmux ls
```

---

## Cloud Deployment

### VPS (Virtual Private Server)

Popular VPS providers:
- DigitalOcean
- Linode
- Vultr
- AWS EC2
- Google Cloud
- Azure

**Steps:**

1. **Create a VPS instance** (Ubuntu 20.04+ recommended)

2. **Connect via SSH:**
```bash
ssh your_user@your_server_ip
```

3. **Update system:**
```bash
sudo apt update && sudo apt upgrade -y
```

4. **Install Python and git:**
```bash
sudo apt install python3 python3-pip python3-venv git -y
```

5. **Clone or upload your bot:**
```bash
git clone <your-repo-url>
# or upload files using scp/sftp
```

6. **Setup the bot:**
```bash
cd sms-activate
./setup.sh
nano .env  # Add credentials
```

7. **Run using systemd or screen** (see sections above)

### Heroku

**Note:** Heroku free tier has been discontinued. Consider alternatives.

### Railway.app

1. Install Railway CLI
2. Create `railway.toml`
3. Deploy with `railway up`

### Render.com

1. Connect your GitHub repository
2. Set environment variables in dashboard
3. Deploy automatically

---

## Monitoring and Logs

### View Bot Logs

**Local:**
```bash
# Bot outputs to console
./run.sh
```

**Docker:**
```bash
docker-compose logs -f
```

**Systemd:**
```bash
sudo journalctl -u sms-activate-bot -f
```

### Log to File

Modify `bot.py` to add file logging:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
```

---

## Security Best Practices

1. **Never commit .env file** to version control
2. **Use strong API keys** and keep them secure
3. **Keep system updated:**
   ```bash
   sudo apt update && sudo apt upgrade
   ```
4. **Use firewall:**
   ```bash
   sudo ufw enable
   sudo ufw allow ssh
   ```
5. **Run as non-root user**
6. **Regularly backup** your configuration

---

## Troubleshooting

### Bot stops unexpectedly
- Check logs for errors
- Ensure adequate system resources
- Use systemd/docker for auto-restart

### High memory usage
- Monitor with `htop` or `docker stats`
- Consider resource limits

### Connection issues
- Verify internet connectivity
- Check firewall settings
- Ensure API endpoints are accessible

---

## Updating the Bot

### Local/VPS:
```bash
git pull  # or upload new files
source venv/bin/activate
pip install -r requirements.txt --upgrade
sudo systemctl restart sms-activate-bot  # if using systemd
```

### Docker:
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## Support

For deployment issues:
- Check logs first
- Verify all credentials
- Ensure dependencies are installed
- Check server resources (CPU, RAM, disk)

Good luck with your deployment! 🚀

