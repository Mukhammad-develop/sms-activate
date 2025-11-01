# 💰 Profit Margin System

## ✅ 2x Markup Implemented!

Your bot now charges users **2x the API price**, giving you **100% profit margin** on every sale!

---

## 🔧 How It Works

### **API Cost vs User Cost**

```
API Price: $1.00  →  User Pays: $2.00  →  Your Profit: $1.00
API Price: $0.50  →  User Pays: $1.00  →  Your Profit: $0.50
API Price: $2.50  →  User Pays: $5.00  →  Your Profit: $2.50
```

---

## 📊 Example Transaction Flow

### **User Buys a Number**

1. **API returns cost**: `$1.50` (what you pay SMS-Activate)
2. **Bot charges user**: `$3.00` (2x markup)
3. **You keep**: `$1.50` profit!

### **User Cancels Order**

1. **User paid**: `$3.00`
2. **Refund given**: `$3.00` (full refund to user)
3. **You already paid API**: `$1.50` (API may refund depending on timing)

---

## ⚙️ Configuration

### **Change Profit Margin**

Located in `bot.py` line 46:

```python
# PROFIT MARGIN (2.0 = 100% markup, 3.0 = 200% markup)
PRICE_MULTIPLIER = 2.0  # You charge users 2x the API price
```

### **Examples:**

```python
PRICE_MULTIPLIER = 1.5   # 50% profit (API: $1 → User: $1.50)
PRICE_MULTIPLIER = 2.0   # 100% profit (API: $1 → User: $2.00) ← CURRENT
PRICE_MULTIPLIER = 3.0   # 200% profit (API: $1 → User: $3.00)
PRICE_MULTIPLIER = 1.2   # 20% profit (API: $1 → User: $1.20)
```

---

## 📍 Where It's Applied

### ✅ **1. Price Display** (`/prices` command)
Shows 2x prices to users

### ✅ **2. Order Purchase** (Buy flow)
Charges users 2x, pays API 1x

### ✅ **3. Balance Deduction**
Deducts 2x from user balance

### ✅ **4. Transaction History**
Stores and displays user's price (2x)

### ✅ **5. Refunds**
Refunds what user paid (2x)

### ✅ **6. Statistics** (Superuser panel)
Shows user transactions at their prices

---

## 💡 Business Logic

### **What You Pay API:**
- Original SMS-Activate prices
- Only when order is created
- May get refund if cancelled early

### **What Users Pay You:**
- 2x the API price
- Paid upfront from their balance
- Full refund if they cancel (within rules)

### **Your Profit:**
- Difference between user payment and API cost
- Instant on every successful order
- Risk: User cancels after 2min, API doesn't refund (rare)

---

## 📈 Revenue Tracking

### **Check Your Earnings**

All user transactions are in USD. Your earnings = **Total user orders × 50%**

Example:
- Total user orders today: `$100`
- API costs you: `$50`
- **Your profit**: `$50` (100% markup)

---

## 🎯 Real-World Example

### **Scenario: User Orders WhatsApp Number**

```
📱 User Journey:
1. User clicks "Buy WhatsApp"
2. Sees price: "$4.00"
3. Clicks confirm
4. Balance deducted: $4.00
5. Receives number

💰 Your Backend:
1. API call to SMS-Activate
2. API charges: $2.00
3. Your balance: +$2.00 profit
4. User gets number
5. Everyone happy! 🎉
```

---

## 🔐 Superuser View

As superuser, you see:
- **User transactions** at their prices (2x)
- **Total revenue** from all users
- **Individual user spending**

You don't see API costs in the bot (those are handled externally).

---

## ⚠️ Important Notes

1. **Transparent to Users**: Users only see their prices (2x), never API prices
2. **Automatic**: No manual intervention needed
3. **Refunds**: Users get full refund if eligible (you might lose if API doesn't refund)
4. **Flexible**: Change `PRICE_MULTIPLIER` anytime
5. **Restart Required**: If you change multiplier, restart the bot

---

## 🚀 Status

✅ **FULLY IMPLEMENTED AND READY!**

- All purchases use 2x pricing
- All refunds work correctly
- Price display updated
- Transaction history accurate
- Superuser stats show user prices

---

## 📝 To Change Profit Margin:

1. Open `bot.py`
2. Find line 46: `PRICE_MULTIPLIER = 2.0`
3. Change to desired value (e.g., `3.0` for 200% profit)
4. Save file
5. Restart bot: `python3 bot.py`

**Done!** 💰

---

## 💼 Business Formula

```
User Price = API Price × PRICE_MULTIPLIER
Your Profit = User Price - API Price
Profit % = (PRICE_MULTIPLIER - 1) × 100%

Current Settings:
- Multiplier: 2.0
- Profit: 100%
- Every $1 API cost = $1 profit
```

---

**Your bot is now a profitable business! 🚀💰**

