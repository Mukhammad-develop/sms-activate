# 🐛 Price Display Issue - Debugging Guide

## 🔍 Issue Reported

**Example: Australia + Telegram**
- API shows: 4.5
- Bot shows: $6.00
- Should show: $9.00 (4.5 × 2)

**Current calculation:**
```
Bot showing $6.00 = 3.0 × 2
```

So the bot is reading **3.0** instead of **4.5** from somewhere!

---

## 🔧 Debugging Steps

### Step 1: Check What API Actually Returns

Run the bot and look for Telegram to Australia. The logs will now show:

```
INFO - Price for tg in country 13: API=4.5, User sees=$9.00
```

This will tell us:
1. What the API actually returns
2. What the user sees after calculation

---

### Step 2: Check Bot Logs

After restarting, browse to Australia + Telegram in the bot.

Check terminal output:
```bash
tail -f /Users/abdurakhmon/Desktop/sms-activate/bot.log
```

Look for lines like:
```
Price for tg in country 13: API=X.XX, User sees=$Y.YY
```

---

## 🎯 Possible Causes

### 1. **API Returns Different Value**
- API might return `retail` not `cost`
- Might be returning scaled values (4.5 but showing 3)

### 2. **Currency Already Converted**
- API might return USD already, not RUB
- Currently set: `CURRENCY_MULTIPLIER = 1.0` (no conversion)

### 3. **Wrong Field Name**
- We're reading `service_data.get('cost', 0)`
- Might need `service_data.get('retail', 0)` or another field

---

## 🔧 Configuration File: `bot.py`

### Lines 45-52:
```python
# PROFIT MARGIN (2.0 = 100% markup, 3.0 = 200% markup)
PRICE_MULTIPLIER = 2.0  # You charge users 2x the API price

# CURRENCY CONVERSION
# SMS-Activate API might return prices in different formats
# Set to 1.0 if prices are already in desired currency
# Or set conversion rate if needed (e.g., 0.0106 for RUB to USD)
CURRENCY_MULTIPLIER = 1.0  # Treat API prices as-is
```

---

## ✅ Solutions

### Solution 1: If API Returns RUB (Russian Rubles)

If API returns prices in rubles (4.5 RUB = ~$0.05 USD):

**Change line 52:**
```python
CURRENCY_MULTIPLIER = 0.011  # 1 RUB ≈ $0.011 USD
```

Then restart bot.

---

### Solution 2: If API Returns USD Already

If API returns prices in dollars (4.5 = $4.50):

**Keep line 52 as:**
```python
CURRENCY_MULTIPLIER = 1.0  # No conversion needed
```

This is current setting - prices should work!

---

### Solution 3: If Wrong Field is Being Read

Check the API response structure. We might be reading the wrong field.

**Current code (line 423):**
```python
cost = service_data.get('cost', 0)
```

**Try alternatives:**
```python
# Option A: Try 'retail' field
cost = service_data.get('retail', 0)

# Option B: Try 'price' field
cost = service_data.get('price', 0)

# Option C: Try both, prefer retail
cost = service_data.get('retail') or service_data.get('cost', 0)
```

---

## 📊 Expected Calculation

### For Australia + Telegram = 4.5 (API)

**If API returns in USD:**
```
API: $4.50
Markup: ×2
User sees: $9.00 ✅
```

**If API returns in RUB:**
```
API: 4.5 RUB
Convert to USD: 4.5 × 0.011 = $0.0495
Markup: ×2
User sees: $0.10 ❌ (too low!)
```

So API probably returns USD or USD-equivalent already!

---

## 🔍 Next Steps

### 1. **Restart Bot with Logging:**
```bash
cd /Users/abdurakhmon/Desktop/sms-activate
source venv/bin/activate
python3 bot.py
```

### 2. **Test the Price:**
- Open bot in Telegram
- Go to: Purchase → Buy Number → Choose Service First
- Select "Telegram"
- Look at Australia price

### 3. **Check Logs:**
Look at terminal output for:
```
Price for tg in country X: API=Y.YY, User sees=$Z.ZZ
```

### 4. **Report Back:**
Tell me what the logs show:
- What is `API=?` value
- What is `User sees=$?` value
- What Australia country ID is (the X in "country X")

---

## 🎯 Quick Fix (If API Returns Correct Values)

If the API returns 4.5 and you want bot to show $9.00:

**Just make sure these settings:**

**Line 46:**
```python
PRICE_MULTIPLIER = 2.0  # 2x markup ✅
```

**Line 52:**
```python
CURRENCY_MULTIPLIER = 1.0  # No conversion ✅
```

**Formula:**
```
User Price = API Price × CURRENCY_MULTIPLIER × PRICE_MULTIPLIER
User Price = 4.5 × 1.0 × 2.0 = $9.00 ✅
```

---

## 📝 Current Status

✅ **Logging Added** - Will show API values  
✅ **Currency Multiplier** - Set to 1.0 (no conversion)  
✅ **Profit Multiplier** - Set to 2.0 (double price)  
⚠️ **Need to Test** - Restart bot and check logs  

---

Restart your bot and tell me what you see in the logs when browsing Australia + Telegram!

