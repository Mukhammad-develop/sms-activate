# Auto-Refund System for Expired Orders

## 🎯 Purpose

Automatically refund users when their orders expire after 20 minutes, ensuring users never lose money even if they forget to cancel manually.

---

## 🚨 **The Problem (Before)**

### What happened:
```
1. User buys number for $9
2. No SMS arrives
3. User forgets to cancel manually
4. 20 minutes pass
5. SMS-Activate API auto-cancels → Refunds YOUR API account ✅
6. User's bot balance: Still -$9 ❌ (NO REFUND!)
```

**Result:** Admin gets money back, user loses $9 forever!

---

## ✅ **The Solution (Now)**

### What happens now:
```
1. User buys number for $9
2. No SMS arrives
3. User forgets to cancel
4. 20 minutes pass
5. SMS-Activate API auto-cancels
6. Bot auto-refund system detects expired order
7. User automatically refunded $9 ✅
8. User gets notification ✅
```

**Result:** Everyone happy! Fair and automatic!

---

## ⚙️ **How It Works**

### 1. **Background Thread**
- Runs every **5 minutes**
- Checks all active orders in database
- Queries SMS-Activate API for status

### 2. **Detection**
```python
For each active order:
    Check API status
    If STATUS_CANCEL (expired):
        → Refund user
        → Update database
        → Log to channel
        → Notify user
```

### 3. **Auto-Refund Process**
```
Order Status: active
    ↓
Background check every 5 min
    ↓
API returns: STATUS_CANCEL
    ↓
Auto-refund triggered:
    ✅ Add money back to user balance
    ✅ Mark order as cancelled in DB
    ✅ Log to channel
    ✅ Send notification to user
```

---

## 📱 **User Notifications**

### English:
```
🔄 Auto-Refund

Order 4361789134 expired after 20 minutes.

💰 Refunded: $9.00
```

### Russian:
```
🔄 Авто-возврат

Заказ 4361789134 истёк через 20 минут.

💰 Возвращено: $9.00
```

### Uzbek:
```
🔄 Avto-qaytarish

Buyurtma 4361789134 20 daqiqadan keyin tugadi.

💰 Qaytarildi: $9.00
```

---

## 📊 **Channel Logging**

```
🕐 2025-11-01 13:15:00

🔄 Auto-Refund - Order Expired

🆔 Order ID: `4361789134`
📞 Phone: +61468115201
🔷 Service: tg
💰 Refunded: $9.00
📝 Reason: Order expired (20 min timeout)

👤 User Info:
• ID: `123456`
• Username: @johndoe
```

---

## 🔧 **Configuration**

In `bot.py` line 72:

```python
AUTO_REFUND_CHECK_INTERVAL = 300  # seconds (5 minutes)
```

### Adjust Check Frequency:

**More Frequent (Faster refunds):**
```python
AUTO_REFUND_CHECK_INTERVAL = 180  # 3 minutes
```

**Less Frequent (Less API load):**
```python
AUTO_REFUND_CHECK_INTERVAL = 600  # 10 minutes
```

**Recommended:** 300 seconds (5 minutes) - Good balance

---

## 🎯 **Coverage**

### What Gets Auto-Refunded:

✅ **Orders expired by timeout (20 min)**
- User bought but no SMS came
- Order automatically cancelled by API
- Full refund to user

✅ **Orders cancelled by system**
- Any STATUS_CANCEL from API
- Regardless of reason
- Full refund guaranteed

### What Doesn't Get Refunded:

❌ **Successfully completed orders**
- User received SMS code
- Order marked as complete
- No refund (user got service)

❌ **Manually cancelled by user**
- User already refunded via cancel button
- No double refund

---

## 📈 **Benefits**

### For Users:
- ✅ Never lose money on expired orders
- ✅ Automatic - no action needed
- ✅ Get notification when refunded
- ✅ Fair and transparent

### For Admin:
- ✅ Better reputation
- ✅ Fewer support tickets
- ✅ Automatic process (no manual work)
- ✅ Complete audit trail in logs

### For Bot:
- ✅ Maintains balance integrity
- ✅ Database stays accurate
- ✅ No orphaned payments
- ✅ Professional operation

---

## 🔄 **Timeline Example**

```
00:00 - User buys number
00:02 - Waiting for SMS
00:05 - Auto-refund check #1 → Order still active ✅
00:10 - Auto-refund check #2 → Order still active ✅
00:15 - Auto-refund check #3 → Order still active ✅
00:20 - SMS-Activate cancels order (timeout)
00:25 - Auto-refund check #4 → Detects STATUS_CANCEL
        → Refunds $9.00 to user ✅
        → Sends notification ✅
        → Logs to channel ✅
```

**Maximum delay:** 5 minutes after expiry

---

## 🛡️ **Safety Features**

### 1. **No Double Refunds**
- Checks order status in database first
- Only refunds orders marked as 'active' or 'pending'
- Once refunded, status changes to 'cancelled'
- Won't refund same order twice

### 2. **Error Handling**
- If API call fails, skips that order
- Tries again in next cycle (5 min)
- Logs all errors
- Doesn't crash on failure

### 3. **Thread Safety**
- Background thread is daemon (stops with bot)
- Independent of main bot operations
- Won't block user interactions
- Safe for concurrent users

### 4. **Rate Limiting**
- Only checks every 5 minutes
- Not spamming API
- Efficient resource usage
- Respectful to API limits

---

## 📊 **Monitoring**

### In Bot Logs:
```bash
tail -f bot.log | grep "Auto-refund"
```

Look for:
```
[INFO] Auto-refunded $9.00 to user 123456 for expired order 4361789134
[INFO] Auto-refunded 3 expired orders
```

### In Channel:
Search for: `🔄 Auto-Refund`

### Statistics:
- Count refunds per day
- Average refund amounts
- Most common expired services
- User retention after auto-refunds

---

## 🔍 **Troubleshooting**

### Issue: User says order expired but no refund

**Check:**
1. Look at channel logs for auto-refund
2. Check database: `status` field for that order
3. Verify order age (must be 20+ min old)
4. Check bot logs for errors

**Fix:**
- If no auto-refund log: Background thread may have failed
- If status still 'active': Database not updated
- Manual refund: `/addbalance <user_id> <amount>`

### Issue: Double refunds

**Check:**
- Should be impossible (status check prevents this)
- If happens, check database transaction history
- Look for race condition in logs

**Fix:**
- Review transaction history in database
- Adjust if necessary with `/deductbalance`

---

## 💡 **Edge Cases Handled**

### ✅ **User cancels manually at same time**
- Manual cancel happens first
- Status changes to 'cancelled'
- Auto-refund skips (status not 'active')
- No double refund

### ✅ **SMS arrives after 19 minutes**
- User gets code
- Status changes to 'completed' or similar
- Auto-refund skips (status not 'active')
- No incorrect refund

### ✅ **Bot restarts during check**
- Thread is daemon (stops cleanly)
- Next startup, thread restarts
- Picks up where left off
- No missed refunds

### ✅ **API is down**
- Error caught and logged
- Order stays in active list
- Tries again next cycle (5 min)
- Eventually refunds when API returns

---

## 📝 **Database States**

### Order Status Flow:
```
active → STATUS_CANCEL detected → cancelled (refunded)
active → STATUS_OK received → completed (no refund)
active → manual cancel → cancelled (refunded)
active → auto-refund → cancelled (refunded)
```

### Transaction History:
```
- Purchase: -$9.00 (Order 4361789134)
- Auto-refund: +$9.00 (Auto-refund for expired order 4361789134)
```

---

## 🚀 **Performance**

### Resource Usage:
- **CPU:** Minimal (runs every 5 min)
- **Memory:** Negligible (processes one user at a time)
- **API Calls:** 1 per active order per 5 min
- **Database:** 1 query per user, 1 update per refund

### Scaling:
- 100 users with 1 active order each = 100 API calls per 5 min
- Well within API limits
- Can handle thousands of users

---

## 🎉 **Result**

**Before:** Users lost money on expired orders
**After:** 100% automatic refunds, zero manual intervention needed!

---

**Your bot now provides 5-star customer service automatically!** 🔄✨

