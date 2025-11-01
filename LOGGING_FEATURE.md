# Telegram Channel Logging Feature

## 📊 Overview

All important user actions are automatically logged to a Telegram group/channel for monitoring and troubleshooting.

**Log Channel:** `@dawefsgrdntfghmfnbdrsefasgrdhtfj`

---

## 🔔 What Gets Logged

### ✅ Success Actions

### 1. **✅ Purchase Successful**
```
🕐 2025-11-01 12:30:45

✅ Purchase Successful

📞 Phone: +61468115201
🆔 Order ID: `4361789134`
🔷 Service: ig
🌍 Country: 175
💰 Cost: $0.40 USD

👤 User Info:
• ID: `123456`
• Username: @johndoe
```

### 2. **❌ Order Cancelled**
```
🕐 2025-11-01 12:35:20

❌ Order Cancelled

🆔 Order ID: `4361789134`
📞 Phone: +61468115201
🔷 Service: ig
💰 Refunded: $0.40 USD

👤 User Info:
• ID: `123456`
• Username: @johndoe
```

### 3. **📨 SMS Received**
```
🕐 2025-11-01 12:32:15

📨 SMS Received

🆔 Order ID: `4361789134`
🔢 Code: `123456`
📝 Text: Your verification code is 123456
🕐 Time: 2025-11-01 12:32:10

👤 User Info:
• ID: `123456`
• Username: @johndoe
```

### 4. **🌐 Language Changed**
```
🕐 2025-11-01 12:25:00

🌐 Language Changed

📝 New Language: English 🇬🇧

👤 User Info:
• ID: `123456`
• Username: @johndoe
```

### 5. **➕ Admin Added Balance**
```
🕐 2025-11-01 12:40:00

➕ Admin Added Balance

💰 Amount: +$100.00 USD
👤 Target User ID: `789012`

👤 User Info:
• ID: `7514237434`
• Username: @admin
```

### 6. **➖ Admin Deducted Balance**
```
🕐 2025-11-01 12:45:00

➖ Admin Deducted Balance

💰 Amount: -$50.00 USD
👤 Target User ID: `789012`

👤 User Info:
• ID: `7514237434`
• Username: @admin
```

---

### ⚠️ Failed Purchase Attempts

### 7. **⚠️ Purchase Failed - Insufficient Balance**
```
🕐 2025-11-01 12:50:00

⚠️ Purchase Failed - Insufficient Balance

🆔 Order ID: `4361789135`
📞 Phone: +61468115202
🔷 Service: tg
🌍 Country: 175
💰 Required: $9.00
💳 User Balance: $1.12
📉 Short: $7.88

👤 User Info:
• ID: `123456`
• Username: @johndoe
```

### 8. **⚠️ Purchase Failed - No Numbers Available**
```
🕐 2025-11-01 12:52:00

⚠️ Purchase Failed - No Numbers Available

🔷 Service: wa
🌍 Country: 0
📝 Error: No numbers available

👤 User Info:
• ID: `123456`
• Username: @johndoe
```

### 9. **🚨 Purchase Failed - API Balance Empty**
```
🕐 2025-11-01 12:55:00

🚨 Purchase Failed - API Balance Empty

🔷 Service: ig
🌍 Country: 175
📝 Error: Admin's SMS-Activate account has no balance!

👤 User Info:
• ID: `123456`
• Username: @johndoe
```

### 10. **⚠️ Purchase Failed - Invalid Service**
```
🕐 2025-11-01 12:57:00

⚠️ Purchase Failed - Invalid Service

🔷 Service: xyz
🌍 Country: 175
📝 Error: Bad service code

👤 User Info:
• ID: `123456`
• Username: @johndoe
```

### 11. **❌ Purchase Failed - API Error**
```
🕐 2025-11-01 13:00:00

❌ Purchase Failed - API Error

🔷 Service: tg
🌍 Country: 999
📝 Error: COUNTRY_NOT_SUPPORTED

👤 User Info:
• ID: `123456`
• Username: @johndoe
```

### 12. **❌ Purchase Failed - Exception**
```
🕐 2025-11-01 13:05:00

❌ Purchase Failed - Exception

🔷 Service: ig
🌍 Country: 175
📝 Error: Connection timeout

👤 User Info:
• ID: `123456`
• Username: @johndoe
```

---

## 🎯 Purpose

### ✅ **Real-time Monitoring**
- See all purchases as they happen
- Track user activity
- Monitor bot health

### ✅ **Problem Diagnosis**
- When user reports an issue, check channel history
- See exact details of what happened
- Timestamps for debugging

### ✅ **Business Analytics**
- Track purchase volume
- Monitor cancellation rates
- See popular services/countries

### ✅ **Admin Actions Audit**
- All balance changes logged
- Full accountability
- Prevents disputes

---

## 🔧 Configuration

### Setting Up Log Channel

1. **Create a Telegram Group/Channel**
   - Create a new Telegram group or channel
   - Add your bot as an administrator

2. **Get Channel Username**
   - Set a public username for the channel (e.g., `@yourlogchannel`)

3. **Update Bot Configuration**
   In `bot.py`:
   ```python
   LOG_CHANNEL = "@dawefsgrdntfghmfnbdrsefasgrdhtfj"
   ```

4. **Test**
   - Make a test purchase
   - Check if log appears in channel

---

## 📝 Log Format

### Standard Format:
```
🕐 [TIMESTAMP]

[EMOJI] [ACTION TITLE]

[ACTION DETAILS]

👤 User Info:
• ID: `[USER_ID]`
• Username: @[USERNAME]
```

### Components:
- **🕐 Timestamp:** Exact date and time of action
- **📋 Action Details:** Service-specific information
- **👤 User Info:** Who performed the action

---

## 🔒 Security

### ✅ **Privacy Considerations**
- Logs contain user IDs and usernames
- Keep log channel private
- Only admin should have access

### ✅ **Sensitive Data**
- Phone numbers are logged (for troubleshooting)
- SMS codes are logged (for verification issues)
- Balance amounts are logged (for accounting)

### ⚠️ **Important**
- **Never share log channel publicly**
- **Don't screenshot and share logs**
- **Regularly review who has access**

---

## 💡 Usage Tips

### 1. **Troubleshooting User Issues**
```
User: "I bought a number but didn't receive it"

Admin action:
1. Go to log channel
2. Search for user's ID or username
3. Find their purchase log
4. Check if SMS was received
5. Verify all details match
```

### 2. **Monitoring Bot Activity**
```
- Open log channel
- See real-time purchases
- Track busy hours
- Monitor for unusual patterns
```

### 3. **Auditing Admin Actions**
```
- Search for "Admin Added Balance"
- Review all balance changes
- Verify amounts and targets
- Ensure proper authorization
```

---

## 🚫 What's NOT Logged

The following actions are **NOT** logged (view-only, no state changes):

- ❌ /start command
- ❌ /help command
- ❌ /balance check
- ❌ /services list
- ❌ /countries list
- ❌ /prices check
- ❌ /myorders view
- ❌ /history view
- ❌ /stats view

**Reason:** Only log actions that **change state** (POST operations), not read operations.

---

## 🔍 Searching Logs

### By User ID:
Search for: `` `123456` ``

### By Username:
Search for: `@johndoe`

### By Order ID:
Search for: `` `4361789134` ``

### By Action Type:
- Search: `✅ Purchase`
- Search: `❌ Order Cancelled`
- Search: `📨 SMS Received`
- Search: `➕ Admin Added`
- Search: `➖ Admin Deducted`

---

## 📱 Mobile Access

### Telegram Mobile App:
1. Open log channel
2. Tap search icon
3. Enter user ID / order ID / username
4. View relevant logs instantly

### Desktop:
1. Open log channel
2. Ctrl+F (or Cmd+F on Mac)
3. Search for relevant info

---

## ⚡ Performance

- **Asynchronous:** Logs don't slow down bot
- **Non-blocking:** If logging fails, bot continues
- **Reliable:** Errors are logged to console

### Error Handling:
```python
try:
    self.bot.send_message(LOG_CHANNEL, log_text)
except Exception as e:
    logger.error(f"Failed to log to channel: {e}")
    # Bot continues normally
```

---

## 🎨 Customization

### Adding New Log Types:

```python
# In bot.py, add wherever you want to log:
self.log_to_channel(
    f"🔔 **Your Action Title**\n\n"
    f"📝 **Detail 1:** value1\n"
    f"💰 **Detail 2:** value2",
    user_id=user_id,
    username=username
)
```

### Changing Log Channel:

```python
# In bot.py line 48:
LOG_CHANNEL = "@your_new_channel_username"
```

---

## ✅ Benefits

1. **📊 Full Transparency:** Every action tracked
2. **🔍 Easy Debugging:** Find issues instantly
3. **📈 Analytics:** See patterns over time
4. **🔒 Accountability:** Admin actions logged
5. **⚡ Real-time:** See activity as it happens
6. **📱 Mobile-friendly:** Access from anywhere

---

**Your bot now has professional-grade logging for complete oversight!** 📊✨

