# Service and Country Codes Reference

Quick reference for commonly used service and country codes.

## Popular Service Codes

### Social Media & Messaging

| Service | Code | Description |
|---------|------|-------------|
| WhatsApp | `wa` | WhatsApp Messenger |
| Telegram | `tg` | Telegram Messenger |
| Viber | `vi` | Viber Messenger |
| WeChat | `we` | WeChat |
| Signal | `sg` | Signal Messenger |
| Discord | `ds` | Discord |

### Social Networks

| Service | Code | Description |
|---------|------|-------------|
| Facebook | `fb` | Facebook |
| Instagram | `ig` | Instagram |
| Twitter/X | `tw` | Twitter (X) |
| TikTok | `tk` | TikTok |
| VKontakte | `vk` | VK (VKontakte) |
| LinkedIn | `lf` | LinkedIn |
| Snapchat | `sn` | Snapchat |
| Reddit | `rd` | Reddit |

### Tech & Services

| Service | Code | Description |
|---------|------|-------------|
| Google | `go` | Google Services |
| Microsoft | `mm` | Microsoft Services |
| Apple | `ap` | Apple Services |
| Amazon | `am` | Amazon |
| Yahoo | `mb` | Yahoo |
| PayPal | `pp` | PayPal |

### Ride-Sharing & Delivery

| Service | Code | Description |
|---------|------|-------------|
| Uber | `ub` | Uber |
| Lyft | `ly` | Lyft |
| Bolt | `bo` | Bolt |
| Yandex Taxi | `yt` | Yandex Taxi |
| Delivery Club | `dc` | Delivery services |

### Dating Apps

| Service | Code | Description |
|---------|------|-------------|
| Tinder | `tn` | Tinder |
| Badoo | `bd` | Badoo |

### Crypto & Finance

| Service | Code | Description |
|---------|------|-------------|
| Binance | `bn` | Binance |
| Coinbase | `cb` | Coinbase |
| Blockchain | `bc` | Blockchain |

### Gaming

| Service | Code | Description |
|---------|------|-------------|
| Steam | `st` | Steam |
| Blizzard | `bl` | Blizzard |
| Epic Games | `ep` | Epic Games |

### Other Services

| Service | Code | Description |
|---------|------|-------------|
| Other | `ot` | Other services |
| Any | `any` | Any service |

---

## Popular Country Codes

### Europe

| Country | Code | Description |
|---------|------|-------------|
| Russia | `0` | Russian Federation |
| Ukraine | `1` | Ukraine |
| Kazakhstan | `2` | Kazakhstan |
| Poland | `15` | Poland |
| UK | `16` | United Kingdom |
| Romania | `32` | Romania |
| Netherlands | `48` | Netherlands |
| Germany | `43` | Germany |
| France | `78` | France |
| Spain | `56` | Spain |
| Italy | `86` | Italy |

### Asia

| Country | Code | Description |
|---------|------|-------------|
| China | `3` | China |
| Hong Kong | `14` | Hong Kong |
| Philippines | `4` | Philippines |
| Myanmar | `5` | Myanmar |
| Indonesia | `6` | Indonesia |
| Malaysia | `7` | Malaysia |
| Kenya | `8` | Kenya |
| India | `22` | India |
| Vietnam | `10` | Vietnam |
| Kyrgyzstan | `11` | Kyrgyzstan |
| Cambodia | `24` | Cambodia |
| Laos | `25` | Laos |
| Bangladesh | `60` | Bangladesh |
| Thailand | `52` | Thailand |

### Americas

| Country | Code | Description |
|---------|------|-------------|
| USA | `12` | United States |
| Canada | `36` | Canada |
| Brazil | `73` | Brazil |
| Mexico | `26` | Mexico |
| Argentina | `39` | Argentina |
| Colombia | `33` | Colombia |

### Middle East

| Country | Code | Description |
|---------|------|-------------|
| Israel | `13` | Israel |
| Turkey | `62` | Turkey |
| UAE | `65` | United Arab Emirates |
| Egypt | `21` | Egypt |

### Africa

| Country | Code | Description |
|---------|------|-------------|
| Nigeria | `19` | Nigeria |
| South Africa | `31` | South Africa |

### Oceania

| Country | Code | Description |
|---------|------|-------------|
| Australia | `175` | Australia |
| New Zealand | `67` | New Zealand |

---

## Usage Examples

### Get a WhatsApp number in Kazakhstan
```
/getnumber wa 2
```

### Get a Telegram number in Russia
```
/getnumber tg 0
```

### Get a Google verification in India
```
/getnumber go 22
```

### Get Instagram number in USA
```
/getnumber ig 12
```

### Check prices for WhatsApp in Kazakhstan
```
/prices wa 2
```

---

## How to Find More Codes

### Using the Bot

1. **List all services:**
```
/services
```

2. **List all countries:**
```
/countries
```

3. **Check specific prices:**
```
/prices <service> <country>
```

### Using the API Directly

Check the API documentation in `api-documentation.txt` for complete lists.

---

## Notes

- **Availability varies** by country and service
- **Prices differ** based on demand and country
- Use `/prices` to check current availability
- Some combinations may not be available
- Popular services in popular countries may have limited availability

---

## Getting Help

If a service or country code doesn't work:
1. Check if it's available: `/prices <service> <country>`
2. Try alternative countries
3. Check your balance: `/balance`
4. View active numbers: `/activations`

---

**Pro Tip:** Save frequently used codes for quick access!

Example workflow:
```bash
# Save as aliases in your notes
wa_kz="/getnumber wa 2"      # WhatsApp Kazakhstan
tg_ru="/getnumber tg 0"      # Telegram Russia
ig_us="/getnumber ig 12"     # Instagram USA
```

