# Service Code to Name Mapping
# Common SMS-Activate service codes with friendly names

SERVICE_NAMES = {
    # Popular Services
    'wa': '📱 WhatsApp',
    'tg': '✈️ Telegram',
    'vk': '🔵 VKontakte',
    'ok': '🟠 Odnoklassniki',
    'vi': '💜 Viber',
    'go': '🔍 Google',
    'fb': '📘 Facebook',
    'tw': '🐦 Twitter/X',
    'ig': '📷 Instagram',
    'oi': '📮 Mail.ru',
    'ya': '🟡 Yandex',
    'av': '🛍️ Avito',
    'qw': '💬 Qiwi',
    'we': '💚 WeChat',
    'ub': '🚗 Uber',
    'ym': '💰 YooMoney',
    'ma': '📧 Microsoft',
    'mb': '📱 Mobile Legends',
    'dt': '🎮 Discord',
    
    # Delivery & Food
    'yx': '🍕 Yandex Eda',
    'zn': '🍔 Delivery Club',
    'gl': '🍽️ Glovo',
    'yy': '🛵 Yandex Drive',
    
    # Finance
    'sn': '💵 Snapchat',
    'wp': '💳 Wise',
    'kp': '🏦 Kaspi',
    'sb': '🟢 Sberbank',
    'tb': '⚫ Tinkoff',
    'al': '💙 AliExpress',
    
    # Gaming
    'pf': '🎮 PUBG',
    'bd': '🎯 Blizzard',
    'ea': '🎮 EA Games',
    'st': '🎮 Steam',
    'ep': '🎮 Epic Games',
    
    # Social & Dating
    'tn': '🔥 Tinder',
    'bd': '💕 Badoo',
    'mm': '👥 Mamba',
    'tk': '🎵 TikTok',
    'sc': '👻 Snapchat',
    'rd': '🤖 Reddit',
    'lf': '🎮 Likee',
    
    # Crypto
    'bt': '₿ Bitcoin',
    'bn': '🟡 Binance',
    'cb': '💱 Coinbase',
    'ht': '🔷 Huobi',
    
    # Other Services  
    'am': '🛍️ Amazon',
    'lx': '🚖 Lyft',
    'bp': '📱 BeReal',
    'ft': '📱 Foot Locker',
    'mg': '📱 Megafon',
    'mt': '📱 MTS',
    'bl': '📱 Beeline',
    'io': '🌐 Others',
    'ot': '🌐 Other',
    'any': '🌐 Any Service',
}

def get_service_display_name(code: str, fallback_name: str = None) -> str:
    """
    Get display name for service code
    
    Args:
        code: Service code (e.g., 'wa', 'tg')
        fallback_name: Name from API if available
        
    Returns:
        Formatted display name
    """
    # If we have a mapping, use it
    if code in SERVICE_NAMES:
        return SERVICE_NAMES[code]
    
    # If fallback provided, use it
    if fallback_name:
        # Add emoji based on category
        if 'telegram' in fallback_name.lower():
            return f"✈️ {fallback_name}"
        elif 'whatsapp' in fallback_name.lower():
            return f"📱 {fallback_name}"
        elif any(word in fallback_name.lower() for word in ['bank', 'pay', 'card', 'money']):
            return f"💳 {fallback_name}"
        elif any(word in fallback_name.lower() for word in ['game', 'play', 'steam']):
            return f"🎮 {fallback_name}"
        elif any(word in fallback_name.lower() for word in ['food', 'delivery', 'taxi', 'uber']):
            return f"🍕 {fallback_name}"
        else:
            return f"📱 {fallback_name}"
    
    # Last resort: use code
    return f"📱 {code.upper()}"


def get_country_display_name(country_data: dict, lang: str = 'en') -> str:
    """
    Get display name for country
    
    Args:
        country_data: Country data dict from API
        lang: Language code (en, ru, uz)
        
    Returns:
        Formatted country name
    """
    if lang == 'ru' and country_data.get('rus'):
        return country_data.get('rus')
    elif lang == 'uz' and country_data.get('eng'):
        # Uzbek uses English names for now
        return country_data.get('eng')
    else:
        return country_data.get('eng', 'Unknown')

