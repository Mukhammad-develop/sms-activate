# Auto-Cancel Feature for Failed Purchases

## 🎯 Purpose

When a user confirms a purchase but doesn't have enough balance, the bot:
1. Purchases from SMS-Activate API (charges admin's account)
2. Realizes user can't pay
3. Needs to cancel to recover money

**Problem:** Sometimes immediate cancel fails (first 2 minutes restriction)

**Solution:** Keep trying to cancel every 3 minutes until successful

---

## ⚙️ How It Works

### 1. Failed Purchase Detection
```
User confirms → API purchases → Check user balance → INSUFFICIENT ❌
```

When this happens, the order is added to `failed_orders` list:
```python
self.failed_orders.append({
    'activation_id': activation_id,
    'timestamp': time.time(),
    'user_id': user_id
})
```

### 2. Background Thread
- Starts automatically when bot starts
- Runs every **3 minutes** (configurable)
- Attempts to cancel all orders in `failed_orders` list

### 3. Cancel Logic
For each failed order:
- Try to cancel: `api.set_status(activation_id, 8)`
- If successful (`ACCESS_CANCEL`): Remove from list ✅
- If failed: Keep in list, try again in 3 minutes 🔄
- After 20 minutes: Give up, remove from list ⏰

---

## 🔧 Configuration

In `bot.py`:
```python
FAILED_ORDERS_CLEANUP_INTERVAL = 180  # seconds (3 minutes)
```

**Adjust if needed:**
- `120` = 2 minutes (faster recovery, more API calls)
- `180` = 3 minutes (balanced) ← Current
- `300` = 5 minutes (slower recovery, fewer API calls)

---

## 📊 Example Timeline

```
00:00 - User confirms purchase, insufficient balance
        → Order added to failed_orders
        → Try immediate cancel → FAILS (too early)

03:00 - Background thread runs
        → Try cancel → FAILS (still too early)

06:00 - Background thread runs
        → Try cancel → SUCCESS! ✅
        → Order removed from list
        → Money recovered
```

---

## 🔍 Monitoring

Logs show cleanup activity:
```
[INFO] Added order 123456789 to failed orders cleanup queue
[INFO] Attempting to cancel 1 failed orders...
[INFO] Successfully cancelled failed order 123456789
[INFO] Cancelled 1 failed orders, 0 remaining
```

---

## 💡 Benefits

✅ **No user overpay** - Users pay exact estimated price, no buffer required
✅ **Auto recovery** - Failed orders automatically cancelled
✅ **Persistent** - Keeps trying until successful (up to 20 min)
✅ **Thread-safe** - Uses locks to prevent race conditions
✅ **Low overhead** - Only runs every 3 minutes

---

## 🛠️ Technical Details

### Thread Safety
```python
self.failed_orders_lock = threading.Lock()

with self.failed_orders_lock:
    self.failed_orders.append(order)
```

### Daemon Thread
- Runs in background
- Automatically stops when bot stops
- Doesn't block main thread

### Retry Limit
- Orders older than 20 minutes are abandoned
- SMS-Activate auto-cancels after 20 min anyway
- Prevents infinite retry loops

---

## ⚠️ Important Notes

1. **First cancel attempt is immediate** - Bot tries to cancel right away, then adds to queue if it fails
2. **Thread-safe** - Multiple purchases can fail simultaneously without issues
3. **Automatic cleanup** - Old orders (20+ min) are automatically removed
4. **Logging** - All cancel attempts are logged for debugging

---

## 🔄 Status Flow

```
Purchase Failed
    ↓
Add to failed_orders
    ↓
Try immediate cancel
    ↓
    ├─ Success? → Done ✅
    └─ Failed? → Wait for background thread
        ↓
    Every 3 minutes:
        Try cancel
        ↓
        ├─ Success? → Remove from list ✅
        ├─ Failed? → Keep trying 🔄
        └─ 20 min passed? → Give up ⏰
```

---

This ensures your admin account is protected while keeping prices fair for users!

