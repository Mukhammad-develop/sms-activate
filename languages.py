"""
Multi-language support for the bot
Languages: English, Russian, Uzbek
"""

LANGUAGES = {
    'en': {
        'name': 'English 🇬🇧',
        'welcome': """
🎉 *Welcome to SMS-Activate Bot!* 🎉

This bot helps you receive SMS verification codes on virtual numbers.

*Available Commands:*

💰 /balance - Check your balance
💳 /deposit - Request balance top-up
📋 /services - Available services
🌍 /countries - Available countries
💵 /prices - Pricing information
📱 /buy - Purchase a virtual number
📊 /myorders - View your orders
🔍 /check - Check order status
❌ /cancel - Cancel an order
🌐 /language - Change language
📜 /history - Transaction history
❓ /help - Show this help

*Quick Start:*
1. Top up your balance with /deposit
2. Browse services with /services
3. Purchase a number with /buy
4. Check status with /check

📞 *Need Help?*
Contact admin: {admin}
        """,
        'language_select': 'Please select your language:',
        'language_changed': '✅ Language changed to English',
        
        'balance': '💰 *Your Balance*\n\nBalance: `${balance:.2f}` USD',
        'no_balance': '⚠️ Insufficient balance. Please top up your account with /deposit',
        
        'deposit_request': """
💳 *Balance Top-Up*

To top up your balance, please contact the administrator:

👤 Admin: {admin}

📋 Send them your User ID: `{user_id}`

After payment confirmation, your balance will be updated automatically.
        """,
        
        'buy_usage': """
⚠️ *Usage:*
`/buy <service> <country>`

*Example:*
`/buy wa 2` - WhatsApp in Kazakhstan

Use /services and /countries to see codes.
        """,
        
        'buy_processing': '🔄 Processing your order...',
        'buy_success': """
📱 *Number Purchased Successfully!*

📞 *Phone Number:* `+{phone}`

*Order ID:* `{order_id}`
*Service:* `{service}`
*Country:* `{country}`
*Cost:* ${cost:.2f} USD

⏳ *Waiting for SMS...*

Use `/check {order_id}` to check for SMS
Use `/cancel {order_id}` to cancel
        """,
        
        'buy_error': '❌ *Error*\n\n{error}',
        'buy_no_numbers': 'No numbers available for this service/country.',
        'buy_invalid_service': 'Invalid service code. Use /services to see available services.',
        
        'check_usage': '⚠️ *Usage:* `/check <order_id>`\n\n*Example:* `/check 123456`',
        'check_processing': '🔄 Checking status...',
        'check_waiting': '⏳ *Waiting for SMS*\n\nOrder ID: `{order_id}`\nNo SMS received yet.',
        'check_success': """
✅ *SMS Received!*

*Order ID:* `{order_id}`
*Code:* `{code}`
*Text:* {text}
*Time:* {time}
        """,
        'check_cancelled': '❌ This order has been cancelled.',
        'check_not_found': '⚠️ Order not found.',
        
        'cancel_usage': '⚠️ *Usage:* `/cancel <order_id>`\n\n*Example:* `/cancel 123456`',
        'cancel_processing': '🔄 Cancelling order...',
        'cancel_success': '✅ Order cancelled successfully. Balance refunded.',
        'cancel_failed': '❌ Failed to cancel order: {error}',
        'cancel_early': '⚠️ Cannot cancel within first 2 minutes.',
        
        'myorders_empty': '📭 You have no active orders.',
        'myorders_title': '📊 *Your Active Orders*\n\n',
        'myorders_item': '• Order `{order_id}`: {service} - +{phone}\n  Status: {status}\n\n',
        
        'history_empty': '📭 No transaction history.',
        'history_title': '📜 *Transaction History*\n\n',
        'history_item': '• {date}: {type} ${amount:.2f} USD\n  {description}\n\n',
        
        'admin_only': '⚠️ This command is only available to administrators.',
        'stats_title': '📊 *Bot Statistics*\n\n',
        'error_occurred': '❌ An error occurred. Please try again later.',
    },
    
    'ru': {
        'name': 'Русский 🇷🇺',
        'welcome': """
🎉 *Добро пожаловать в SMS-Activate Bot!* 🎉

Этот бот помогает получать SMS-коды на виртуальные номера.

*Доступные команды:*

💰 /balance - Проверить баланс
💳 /deposit - Пополнить баланс
📋 /services - Доступные сервисы
🌍 /countries - Доступные страны
💵 /prices - Информация о ценах
📱 /buy - Купить виртуальный номер
📊 /myorders - Посмотреть заказы
🔍 /check - Проверить статус заказа
❌ /cancel - Отменить заказ
🌐 /language - Сменить язык
📜 /history - История транзакций
❓ /help - Показать эту справку

*Быстрый старт:*
1. Пополните баланс через /deposit
2. Посмотрите сервисы через /services
3. Купите номер через /buy
4. Проверьте статус через /check

📞 *Нужна помощь?*
Свяжитесь с админом: {admin}
        """,
        'language_select': 'Пожалуйста, выберите язык:',
        'language_changed': '✅ Язык изменён на Русский',
        
        'balance': '💰 *Ваш Баланс*\n\nБаланс: `${balance:.2f}` USD',
        'no_balance': '⚠️ Недостаточно средств. Пополните баланс через /deposit',
        
        'deposit_request': """
💳 *Пополнение Баланса*

Для пополнения баланса свяжитесь с администратором:

👤 Админ: {admin}

📋 Отправьте ему ваш User ID: `{user_id}`

После подтверждения оплаты ваш баланс будет обновлён автоматически.
        """,
        
        'buy_usage': """
⚠️ *Использование:*
`/buy <сервис> <страна>`

*Пример:*
`/buy wa 2` - WhatsApp в Казахстане

Используйте /services и /countries для просмотра кодов.
        """,
        
        'buy_processing': '🔄 Обработка вашего заказа...',
        'buy_success': """
📱 *Номер успешно куплен!*

📞 *Телефон:* `+{phone}`

*ID Заказа:* `{order_id}`
*Сервис:* `{service}`
*Страна:* `{country}`
*Стоимость:* ${cost:.2f} USD

⏳ *Ожидание SMS...*

Используйте `/check {order_id}` для проверки SMS
Используйте `/cancel {order_id}` для отмены
        """,
        
        'buy_error': '❌ *Ошибка*\n\n{error}',
        'buy_no_numbers': 'Нет доступных номеров для этого сервиса/страны.',
        'buy_invalid_service': 'Неверный код сервиса. Используйте /services для просмотра.',
        
        'check_usage': '⚠️ *Использование:* `/check <id_заказа>`\n\n*Пример:* `/check 123456`',
        'check_processing': '🔄 Проверка статуса...',
        'check_waiting': '⏳ *Ожидание SMS*\n\nID Заказа: `{order_id}`\nСМС ещё не получено.',
        'check_success': """
✅ *SMS Получено!*

*ID Заказа:* `{order_id}`
*Код:* `{code}`
*Текст:* {text}
*Время:* {time}
        """,
        'check_cancelled': '❌ Этот заказ был отменён.',
        'check_not_found': '⚠️ Заказ не найден.',
        
        'cancel_usage': '⚠️ *Использование:* `/cancel <id_заказа>`\n\n*Пример:* `/cancel 123456`',
        'cancel_processing': '🔄 Отмена заказа...',
        'cancel_success': '✅ Заказ успешно отменён. Баланс возвращён.',
        'cancel_failed': '❌ Не удалось отменить заказ: {error}',
        'cancel_early': '⚠️ Нельзя отменить в первые 2 минуты.',
        
        'myorders_empty': '📭 У вас нет активных заказов.',
        'myorders_title': '📊 *Ваши Активные Заказы*\n\n',
        'myorders_item': '• Заказ `{order_id}`: {service} - +{phone}\n  Статус: {status}\n\n',
        
        'history_empty': '📭 История транзакций пуста.',
        'history_title': '📜 *История Транзакций*\n\n',
        'history_item': '• {date}: {type} ${amount:.2f} USD\n  {description}\n\n',
        
        'admin_only': '⚠️ Эта команда доступна только администраторам.',
        'stats_title': '📊 *Статистика Бота*\n\n',
        'error_occurred': '❌ Произошла ошибка. Попробуйте позже.',
    },
    
    'uz': {
        'name': "O'zbek 🇺🇿",
        'welcome': """
🎉 *SMS-Activate Botiga xush kelibsiz!* 🎉

Bu bot virtual raqamlarga SMS kodlarini olishga yordam beradi.

*Mavjud buyruqlar:*

💰 /balance - Balansni tekshirish
💳 /deposit - Balansni to'ldirish
📋 /services - Mavjud xizmatlar
🌍 /countries - Mavjud davlatlar
💵 /prices - Narxlar haqida ma'lumot
📱 /buy - Virtual raqam sotib olish
📊 /myorders - Buyurtmalaringizni ko'rish
🔍 /check - Buyurtma holatini tekshirish
❌ /cancel - Buyurtmani bekor qilish
🌐 /language - Tilni o'zgartirish
📜 /history - Tranzaksiyalar tarixi
❓ /help - Yordam ko'rsatish

*Tez boshlash:*
1. /deposit orqali balansni to'ldiring
2. /services orqali xizmatlarni ko'ring
3. /buy orqali raqam sotib oling
4. /check orqali holatni tekshiring

📞 *Yordam kerakmi?*
Admin bilan bog'laning: {admin}
        """,
        'language_select': "Iltimos, tilni tanlang:",
        'language_changed': "✅ Til O'zbekchaga o'zgartirildi",
        
        'balance': '💰 *Sizning Balansingiz*\n\nBalans: `${balance:.2f}` USD',
        'no_balance': '⚠️ Mablag yetarli emas. /deposit orqali balansni to\'ldiring',
        
        'deposit_request': """
💳 *Balansni To'ldirish*

Balansni to'ldirish uchun administrator bilan bog'laning:

👤 Admin: {admin}

📋 Unga User ID ni yuboring: `{user_id}`

To'lov tasdiqlanganidan keyin balansingiz avtomatik yangilanadi.
        """,
        
        'buy_usage': """
⚠️ *Foydalanish:*
`/buy <xizmat> <davlat>`

*Misol:*
`/buy wa 2` - Qozog'istonda WhatsApp

Kodlarni ko'rish uchun /services va /countries dan foydalaning.
        """,
        
        'buy_processing': '🔄 Buyurtmangiz qayta ishlanmoqda...',
        'buy_success': """
📱 *Raqam muvaffaqiyatli sotib olindi!*

📞 *Telefon:* `+{phone}`

*Buyurtma ID:* `{order_id}`
*Xizmat:* `{service}`
*Davlat:* `{country}`
*Narx:* ${cost:.2f} USD

⏳ *SMS kutilmoqda...*

SMS tekshirish uchun: `/check {order_id}`
Bekor qilish uchun: `/cancel {order_id}`
        """,
        
        'buy_error': '❌ *Xato*\n\n{error}',
        'buy_no_numbers': 'Bu xizmat/davlat uchun raqamlar mavjud emas.',
        'buy_invalid_service': "Noto'g'ri xizmat kodi. /services dan foydalaning.",
        
        'check_usage': '⚠️ *Foydalanish:* `/check <buyurtma_id>`\n\n*Misol:* `/check 123456`',
        'check_processing': '🔄 Holat tekshirilmoqda...',
        'check_waiting': '⏳ *SMS kutilmoqda*\n\nBuyurtma ID: `{order_id}`\nHali SMS kelmagan.',
        'check_success': """
✅ *SMS Keldi!*

*Buyurtma ID:* `{order_id}`
*Kod:* `{code}`
*Matn:* {text}
*Vaqt:* {time}
        """,
        'check_cancelled': '❌ Bu buyurtma bekor qilingan.',
        'check_not_found': '⚠️ Buyurtma topilmadi.',
        
        'cancel_usage': '⚠️ *Foydalanish:* `/cancel <buyurtma_id>`\n\n*Misol:* `/cancel 123456`',
        'cancel_processing': '🔄 Buyurtma bekor qilinmoqda...',
        'cancel_success': '✅ Buyurtma muvaffaqiyatli bekor qilindi. Balans qaytarildi.',
        'cancel_failed': '❌ Buyurtmani bekor qilib bo\'lmadi: {error}',
        'cancel_early': '⚠️ Dastlabki 2 daqiqada bekor qilib bo\'lmaydi.',
        
        'myorders_empty': '📭 Sizda faol buyurtmalar yo\'q.',
        'myorders_title': '📊 *Sizning Faol Buyurtmalaringiz*\n\n',
        'myorders_item': '• Buyurtma `{order_id}`: {service} - +{phone}\n  Holat: {status}\n\n',
        
        'history_empty': '📭 Tranzaksiyalar tarixi bo\'sh.',
        'history_title': '📜 *Tranzaksiyalar Tarixi*\n\n',
        'history_item': '• {date}: {type} ${amount:.2f} USD\n  {description}\n\n',
        
        'admin_only': '⚠️ Bu buyruq faqat administratorlar uchun.',
        'stats_title': '📊 *Bot Statistikasi*\n\n',
        'error_occurred': '❌ Xatolik yuz berdi. Keyinroq urinib ko\'ring.',
    }
}


def get_text(user_lang: str, key: str, **kwargs) -> str:
    """Get translated text for user language"""
    lang = LANGUAGES.get(user_lang, LANGUAGES['en'])
    text = lang.get(key, LANGUAGES['en'].get(key, key))
    
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    return text


def get_language_keyboard():
    """Get language selection keyboard"""
    from telebot import types
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    for lang_code, lang_data in LANGUAGES.items():
        button = types.InlineKeyboardButton(
            text=lang_data['name'],
            callback_data=f'lang_{lang_code}'
        )
        markup.add(button)
    
    return markup

