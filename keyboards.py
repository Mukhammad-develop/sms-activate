"""
Keyboard layouts for the bot
ReplyKeyboardMarkup and InlineKeyboardMarkup
"""

from telebot import types
from languages import get_text
from service_names import get_service_display_name, get_country_display_name


def get_main_keyboard(lang: str) -> types.ReplyKeyboardMarkup:
    """Get main menu keyboard with main tabs"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    if lang == 'en':
        markup.add(
            types.KeyboardButton("🛒 Purchase"),
            types.KeyboardButton("💰 Balance")
        )
        markup.add(
            types.KeyboardButton("⚙️ Settings"),
            types.KeyboardButton("❓ Help")
        )
    elif lang == 'ru':
        markup.add(
            types.KeyboardButton("🛒 Покупка"),
            types.KeyboardButton("💰 Баланс")
        )
        markup.add(
            types.KeyboardButton("⚙️ Настройки"),
            types.KeyboardButton("❓ Помощь")
        )
    else:  # uz
        markup.add(
            types.KeyboardButton("🛒 Sotib olish"),
            types.KeyboardButton("💰 Balans")
        )
        markup.add(
            types.KeyboardButton("⚙️ Sozlamalar"),
            types.KeyboardButton("❓ Yordam")
        )
    
    return markup


def get_admin_keyboard(lang: str) -> types.ReplyKeyboardMarkup:
    """Get admin keyboard with superuser tab"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    if lang == 'en':
        markup.add(
            types.KeyboardButton("🛒 Purchase"),
            types.KeyboardButton("💰 Balance")
        )
        markup.add(
            types.KeyboardButton("⚙️ Settings"),
            types.KeyboardButton("❓ Help")
        )
        markup.add(
            types.KeyboardButton("🔐 Superuser")
        )
    elif lang == 'ru':
        markup.add(
            types.KeyboardButton("🛒 Покупка"),
            types.KeyboardButton("💰 Баланс")
        )
        markup.add(
            types.KeyboardButton("⚙️ Настройки"),
            types.KeyboardButton("❓ Помощь")
        )
        markup.add(
            types.KeyboardButton("🔐 Суперпользователь")
        )
    else:  # uz
        markup.add(
            types.KeyboardButton("🛒 Sotib olish"),
            types.KeyboardButton("💰 Balans")
        )
        markup.add(
            types.KeyboardButton("⚙️ Sozlamalar"),
            types.KeyboardButton("❓ Yordam")
        )
        markup.add(
            types.KeyboardButton("🔐 Supermenejer")
        )
    
    return markup


def get_purchase_submenu(lang: str) -> types.ReplyKeyboardMarkup:
    """Get purchase submenu - simplified with only Buy and My Orders"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    if lang == 'en':
        markup.add(
            types.KeyboardButton("🛍️ Buy Number"),
            types.KeyboardButton("📊 My Orders")
        )
        markup.add(
            types.KeyboardButton("🔙 Back to Main Menu")
        )
    elif lang == 'ru':
        markup.add(
            types.KeyboardButton("🛍️ Купить номер"),
            types.KeyboardButton("📊 Мои заказы")
        )
        markup.add(
            types.KeyboardButton("🔙 Назад в главное меню")
        )
    else:  # uz
        markup.add(
            types.KeyboardButton("🛍️ Raqam sotib olish"),
            types.KeyboardButton("📊 Buyurtmalarim")
        )
        markup.add(
            types.KeyboardButton("🔙 Asosiy menyu")
        )
    
    return markup


def get_balance_submenu(lang: str) -> types.ReplyKeyboardMarkup:
    """Get balance submenu"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    if lang == 'en':
        markup.add(
            types.KeyboardButton("💳 Check Balance"),
            types.KeyboardButton("➕ Deposit")
        )
        markup.add(
            types.KeyboardButton("📜 Transaction History")
        )
        markup.add(
            types.KeyboardButton("🔙 Back to Main Menu")
        )
    elif lang == 'ru':
        markup.add(
            types.KeyboardButton("💳 Проверить баланс"),
            types.KeyboardButton("➕ Пополнить")
        )
        markup.add(
            types.KeyboardButton("📜 История транзакций")
        )
        markup.add(
            types.KeyboardButton("🔙 Главное меню")
        )
    else:  # uz
        markup.add(
            types.KeyboardButton("💳 Balansni tekshirish"),
            types.KeyboardButton("➕ To'ldirish")
        )
        markup.add(
            types.KeyboardButton("📜 Tranzaksiyalar tarixi")
        )
        markup.add(
            types.KeyboardButton("🔙 Asosiy menyu")
        )
    
    return markup


def get_settings_submenu(lang: str) -> types.ReplyKeyboardMarkup:
    """Get settings submenu"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    if lang == 'en':
        markup.add(
            types.KeyboardButton("🌐 Change Language")
        )
        markup.add(
            types.KeyboardButton("🔙 Back to Main Menu")
        )
    elif lang == 'ru':
        markup.add(
            types.KeyboardButton("🌐 Изменить язык")
        )
        markup.add(
            types.KeyboardButton("🔙 Главное меню")
        )
    else:  # uz
        markup.add(
            types.KeyboardButton("🌐 Tilni o'zgartirish")
        )
        markup.add(
            types.KeyboardButton("🔙 Asosiy menyu")
        )
    
    return markup


def get_superuser_submenu(lang: str) -> types.ReplyKeyboardMarkup:
    """Get superuser submenu"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    if lang == 'en':
        markup.add(
            types.KeyboardButton("📊 Statistics"),
            types.KeyboardButton("👥 Users List")
        )
        markup.add(
            types.KeyboardButton("💎 API Balance"),
            types.KeyboardButton("📈 All Transactions")
        )
        markup.add(
            types.KeyboardButton("🔙 Back to Main Menu")
        )
    elif lang == 'ru':
        markup.add(
            types.KeyboardButton("📊 Статистика"),
            types.KeyboardButton("👥 Список пользователей")
        )
        markup.add(
            types.KeyboardButton("💎 Баланс API"),
            types.KeyboardButton("📈 Все транзакции")
        )
        markup.add(
            types.KeyboardButton("🔙 Главное меню")
        )
    else:  # uz
        markup.add(
            types.KeyboardButton("📊 Statistika"),
            types.KeyboardButton("👥 Foydalanuvchilar ro'yxati")
        )
        markup.add(
            types.KeyboardButton("💎 API balansi"),
            types.KeyboardButton("📈 Barcha tranzaksiyalar")
        )
        markup.add(
            types.KeyboardButton("🔙 Asosiy menyu")
        )
    
    return markup


def get_buy_method_keyboard(lang: str) -> types.InlineKeyboardMarkup:
    """Get keyboard for selecting buy method"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    if lang == 'en':
        markup.add(
            types.InlineKeyboardButton("🌍 Choose Country First", callback_data="buy_country_first"),
            types.InlineKeyboardButton("📱 Choose Service First", callback_data="buy_service_first")
        )
    elif lang == 'ru':
        markup.add(
            types.InlineKeyboardButton("🌍 Выбрать страну сначала", callback_data="buy_country_first"),
            types.InlineKeyboardButton("📱 Выбрать сервис сначала", callback_data="buy_service_first")
        )
    else:  # uz
        markup.add(
            types.InlineKeyboardButton("🌍 Avval davlatni tanlash", callback_data="buy_country_first"),
            types.InlineKeyboardButton("📱 Avval xizmatni tanlash", callback_data="buy_service_first")
        )
    
    return markup


def get_countries_keyboard(countries_data: dict, page: int = 0, prefix: str = "country", service_code: str = None, price_getter=None) -> types.InlineKeyboardMarkup:
    """Get paginated countries keyboard with optional prices"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # Filter visible countries
    countries = []
    for key, data in countries_data.items():
        if isinstance(data, dict) and data.get('visible') == 1:
            countries.append({
                'id': data.get('id'),
                'name': data.get('eng', 'Unknown'),
                'rus': data.get('rus', ''),
                'key': key
            })
    
    # Sort by name
    countries.sort(key=lambda x: x['name'])
    
    # Pagination
    per_page = 10
    start = page * per_page
    end = start + per_page
    page_countries = countries[start:end]
    
    # Add country buttons (1 per row for better readability)
    for country in page_countries:
        button_text = f"🌍 {country['name']}"
        
        # Add price if service is selected and price getter provided
        if service_code and price_getter:
            price = price_getter(service_code, country['id'])
            if price > 0:
                button_text = f"{button_text} - ${price:.2f}"
        
        callback_data = f"{prefix}_{country['id']}"
        markup.add(types.InlineKeyboardButton(button_text, callback_data=callback_data))
    
    # Navigation buttons
    nav_buttons = []
    if page > 0:
        nav_buttons.append(types.InlineKeyboardButton("⬅️ Previous", callback_data=f"{prefix}_page_{page-1}"))
    if end < len(countries):
        nav_buttons.append(types.InlineKeyboardButton("Next ➡️", callback_data=f"{prefix}_page_{page+1}"))
    
    if nav_buttons:
        markup.row(*nav_buttons)
    
    # Back button
    markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="buy_back"))
    
    return markup


def get_services_keyboard(services_data: list, page: int = 0, prefix: str = "service", country_id: str = None, price_getter=None) -> types.InlineKeyboardMarkup:
    """Get paginated services keyboard with prices"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # Pagination
    per_page = 10
    start = page * per_page
    end = start + per_page
    page_services = services_data[start:end]
    
    # Add service buttons
    for service in page_services:
        code = service.get('code', 'N/A')
        api_name = service.get('name', None)
        
        # Get display name with emoji
        display_name = get_service_display_name(code, api_name)
        
        # Add price if getter provided (with ~ to show approximate)
        if price_getter:
            if country_id:
                # Show approximate exact price for this country
                price = price_getter('exact', code, country_id)
                if price > 0:
                    display_name = f"{display_name} - ~${price:.2f}"
            else:
                # Show approximate minimum price across all countries
                price = price_getter('min', code)
                if price > 0:
                    display_name = f"{display_name} - from ~${price:.2f}"
        
        # Truncate if too long
        if len(display_name) > 40:
            display_name = display_name[:37] + "..."
        
        if country_id:
            callback_data = f"{prefix}_{code}_country_{country_id}"
        else:
            callback_data = f"{prefix}_{code}"
        
        markup.add(types.InlineKeyboardButton(display_name, callback_data=callback_data))
    
    # Navigation buttons
    nav_buttons = []
    if page > 0:
        if country_id:
            nav_buttons.append(types.InlineKeyboardButton("⬅️ Previous", callback_data=f"{prefix}_page_{country_id}_{page-1}"))
        else:
            nav_buttons.append(types.InlineKeyboardButton("⬅️ Previous", callback_data=f"{prefix}_page_{page}_{page-1}"))
    if end < len(services_data):
        if country_id:
            nav_buttons.append(types.InlineKeyboardButton("Next ➡️", callback_data=f"{prefix}_page_{country_id}_{page+1}"))
        else:
            nav_buttons.append(types.InlineKeyboardButton("Next ➡️", callback_data=f"{prefix}_page_{page}_{page+1}"))
    
    if nav_buttons:
        markup.row(*nav_buttons)
    
    # Back button
    if country_id:
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="buy_country_first"))
    else:
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="buy_back"))
    
    return markup


def get_confirmation_keyboard(lang: str, order_id: str) -> types.InlineKeyboardMarkup:
    """Get keyboard for order confirmation - NO back button to preserve order info"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    if lang == 'en':
        markup.add(
            types.InlineKeyboardButton("🔍 Check SMS", callback_data=f"check_{order_id}"),
            types.InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{order_id}")
        )
    elif lang == 'ru':
        markup.add(
            types.InlineKeyboardButton("🔍 Проверить SMS", callback_data=f"check_{order_id}"),
            types.InlineKeyboardButton("❌ Отменить", callback_data=f"cancel_{order_id}")
        )
    else:  # uz
        markup.add(
            types.InlineKeyboardButton("🔍 SMS tekshirish", callback_data=f"check_{order_id}"),
            types.InlineKeyboardButton("❌ Bekor qilish", callback_data=f"cancel_{order_id}")
        )
    
    return markup


def get_order_action_keyboard(lang: str, order_id: str) -> types.InlineKeyboardMarkup:
    """Get keyboard for order actions"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    if lang == 'en':
        markup.add(
            types.InlineKeyboardButton("🔄 Refresh", callback_data=f"check_{order_id}"),
            types.InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{order_id}")
        )
    elif lang == 'ru':
        markup.add(
            types.InlineKeyboardButton("🔄 Обновить", callback_data=f"check_{order_id}"),
            types.InlineKeyboardButton("❌ Отменить", callback_data=f"cancel_{order_id}")
        )
    else:  # uz
        markup.add(
            types.InlineKeyboardButton("🔄 Yangilash", callback_data=f"check_{order_id}"),
            types.InlineKeyboardButton("❌ Bekor qilish", callback_data=f"cancel_{order_id}")
        )
    
    return markup

