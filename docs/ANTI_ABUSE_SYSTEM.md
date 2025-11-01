# Anti-Abuse System

## 🛡️ Purpose

Prevent users from repeatedly attempting purchases with insufficient balance, which:
- Wastes API calls to SMS-Activate
- Costs admin money (orders must be cancelled)
- Creates unnecessary load on the system

---

## ⚙️ How It Works

### 1. **Track Failed Purchases**
Every time a purchase fails due to insufficient balance:
- Amount is tracked for that user
- Timestamp is recorded
- Tracked for 20 minutes rolling window

### 2. **Block Threshold**
When user accumulates **$20+** in failed purchases within 20 minutes:
- User is temporarily blocked from purchasing
- Block lasts 20 minutes from first failed purchase

### 3. **Safety Bypass**
User can bypass block if they have **2x the price** they want to buy:
- Example: Want to buy $4 service
- Need $8 in balance to proceed
- This ensures they can actually afford it

---

## 📊 **Example Scenarios**

### Scenario 1: Normal User
```
User balance: $5.00
Tries to buy $9 service → FAIL
Failed total: $9.00 (< $20 threshold)
Result: ✅ Can try again immediately
```

### Scenario 2: Spammer Gets Blocked
```
User balance: $1.00

Attempt 1: $9 service → FAIL (Total: $9)
Attempt 2: $8 service → FAIL (Total: $17)
Attempt 3: $5 service → FAIL (Total: $22) 

Result: 🚫 BLOCKED for 20 minutes
```

### Scenario 3: Blocked User with Enough Balance
```
User is blocked (failed total: $25)
User balance: $10.00
Wants to buy: $4 service

Check: $10 >= ($4 × 2 = $8)? YES ✅

Result: ✅ Allowed to purchase (has safety margin)
```

### Scenario 4: Blocked User Without Safety Margin
```
User is blocked (failed total: $25)
User balance: $7.00
Wants to buy: $4 service

Check: $7 >= ($4 × 2 = $8)? NO ❌

Result: 🚫 Still blocked, needs $8 total
```

---

## 💬 **User Messages**

### English:
```
🚫 Temporarily Blocked

You have $22.50 in failed purchases in the last 20 minutes.

To continue purchasing, you need:
💰 $8.00 (2x the price)

💳 Your current balance: $5.00
📉 You need $3.00 more

⏰ Block will be lifted automatically in 20 minutes.
```

### Russian:
```
🚫 Временная Блокировка

У вас $22.50 неудачных покупок за последние 20 минут.

Чтобы продолжить, вам нужно:
💰 $8.00 (2x от цены)

💳 Ваш баланс: $5.00
📉 Нужно еще $3.00

⏰ Блокировка снимется автоматически через 20 минут.
```

### Uzbek:
```
🚫 Vaqtincha Bloklangan

Sizda oxirgi 20 daqiqada $22.50 muvaffaqiyatsiz xaridlar.

Davom etish uchun kerak:
💰 $8.00 (narxdan 2x)

💳 Sizning balansingiz: $5.00
📉 Yana $3.00 kerak

⏰ Blok 20 daqiqadan keyin avtomatik ochiladi.
```

---

## 📝 **Channel Logging**

### When User Gets Blocked:
```
🕐 2025-11-01 13:30:00

🚫 User Blocked - Anti-Abuse

💰 Failed Total: $22.50
🔷 Attempted Service: tg
💳 User Balance: $5.00
📉 Required: $8.00

👤 User Info:
• ID: `123456`
• Username: @johndoe
```

### Failed Purchase Logs Show Total:
```
⚠️ Purchase Failed - Insufficient Balance

🆔 Order ID: `4361789135`
📞 Phone: +61468115202
🔷 Service: tg
🌍 Country: 175
💰 Required: $9.00
💳 User Balance: $1.12
📉 Short: $7.88
🚨 Total Failed (20min): $22.50  ← Shows accumulation
```

---

## 🔧 **Configuration**

In `bot.py` lines 66-68:

```python
FAILED_PURCHASE_THRESHOLD = 20.0  # USD - Trigger block at $20
FAILED_PURCHASE_BLOCK_TIME = 1200  # seconds (20 minutes)
SAFETY_BALANCE_MULTIPLIER = 2.0  # Need 2x price to bypass
```

### Adjust Settings:

**More Strict:**
```python
FAILED_PURCHASE_THRESHOLD = 10.0  # Block at $10
FAILED_PURCHASE_BLOCK_TIME = 1800  # 30 minutes
SAFETY_BALANCE_MULTIPLIER = 3.0  # Need 3x price
```

**More Lenient:**
```python
FAILED_PURCHASE_THRESHOLD = 30.0  # Block at $30
FAILED_PURCHASE_BLOCK_TIME = 600  # 10 minutes
SAFETY_BALANCE_MULTIPLIER = 1.5  # Need 1.5x price
```

---

## ⏰ **Auto-Cleanup**

Failed purchase records are automatically cleaned up:
- Every 3 minutes (when cleanup thread runs)
- Records older than 20 minutes are removed
- User's block is automatically lifted after 20 minutes

---

## 🎯 **Benefits**

### ✅ **For Admin:**
- Saves money (fewer wasted API calls)
- Reduces cancelled orders
- Prevents spam/abuse
- Less manual intervention needed

### ✅ **For Legitimate Users:**
- Not affected if they have proper balance
- Clear feedback on what's needed
- Fair 20-minute timeout
- Can bypass with sufficient balance

### ✅ **For Bot:**
- Reduced API load
- Better resource management
- Automatic cleanup
- Thread-safe implementation

---

## 🔍 **How to Monitor**

### Check Channel Logs:
1. Search for "🚫 User Blocked"
2. See who's getting blocked
3. Check if threshold is too strict/lenient

### Adjust Based on Data:
- Too many blocks? Increase threshold
- Too much abuse? Decrease threshold
- Users complaining? Lower multiplier

---

## 💡 **Edge Cases Handled**

### ✅ **User tops up during block:**
- If they add enough to have 2x price
- Block is automatically bypassed
- Can purchase immediately

### ✅ **Trying different services:**
- Block is user-wide, not service-specific
- Prevents switching to cheaper services to spam

### ✅ **Multiple attempts same minute:**
- All tracked and accumulated
- Timestamp prevents bypassing with timing

### ✅ **Thread safety:**
- Uses locks for concurrent access
- No race conditions
- Safe for multiple users simultaneously

---

## 🚨 **Important Notes**

1. **Only tracks insufficient balance failures**
   - Other errors (no numbers, API issues) don't count
   - Only spam attempts waste money

2. **Rolling 20-minute window**
   - Not a fixed 20-minute ban
   - Old records drop off continuously
   - More fair than fixed ban

3. **2x multiplier is client price**
   - User needs 2x what THEY pay
   - Not 2x API price
   - Accounts for your profit margin

4. **Superuser not affected**
   - Admin can always purchase
   - No blocks on superuser_id
   - (You can add this if needed)

---

## 📈 **Statistics**

Monitor these metrics in logs:
- How often users get blocked
- Average failed purchase amounts
- Most common blocked services
- Bypass vs full block ratio

This helps optimize thresholds and multipliers over time.

---

**Your bot now has professional anti-abuse protection!** 🛡️✨

