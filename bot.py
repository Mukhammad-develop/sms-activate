#!/usr/bin/env python3
"""
SMS-Activate Telegram Bot with Multi-language Support
A bot to interact with SMS-Activate API with user balance management
"""

import os
import logging
import requests
import time
import threading
from datetime import datetime
from typing import Optional, Dict, Any
import telebot
from telebot import types
import json

from database import Database
from languages import LANGUAGES, get_text, get_language_keyboard
from keyboards import (
    get_main_keyboard, 
    get_admin_keyboard,
    get_purchase_submenu,
    get_balance_submenu,
    get_settings_submenu,
    get_superuser_submenu,
    get_buy_method_keyboard,
    get_countries_keyboard,
    get_services_keyboard,
    get_confirmation_keyboard,
    get_order_action_keyboard
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ================================
# SUPERUSER CONFIGURATION
# ================================
# PASTE YOUR TELEGRAM USER ID HERE
SUPERUSER_ID = 7514237434  # Replace with your Telegram user ID

# LOG CHANNEL - All actions will be logged here
LOG_CHANNEL = "@dawefsgrdntfghmfnbdrsefasgrdhtfj"  # Group/channel for logging all actions

# PROFIT MARGIN (2.0 = 100% markup, 3.0 = 200% markup)
PRICE_MULTIPLIER = 2.0  # You charge users 2x the API price

# PRICE CONFIGURATION
# WARNING: getPrices API returns estimated prices that don't match actual costs!
# Real prices only come from getNumber API when actually purchasing
# For now, we show getPrices × 2 as estimates, but actual charge may differ
CURRENCY_MULTIPLIER = 1.0   # Currency conversion (1.0 = no conversion)

# AUTO-CANCEL FOR FAILED PURCHASES
# Track orders that failed due to insufficient balance
# Cancel them every 3 minutes to recover money
FAILED_ORDERS_CLEANUP_INTERVAL = 180  # seconds (3 minutes)

# ANTI-ABUSE SYSTEM
# Block users who accumulate $20+ in failed purchases for 20 minutes
FAILED_PURCHASE_THRESHOLD = 20.0  # USD
FAILED_PURCHASE_BLOCK_TIME = 1200  # seconds (20 minutes)
SAFETY_BALANCE_MULTIPLIER = 2.0  # User needs 2x price to bypass block

# AUTO-REFUND SYSTEM
# Check for expired orders and automatically refund users
AUTO_REFUND_CHECK_INTERVAL = 300  # seconds (5 minutes)
# ================================


class SMSActivateAPI:
    """Wrapper for SMS-Activate API"""
    
    BASE_URL = "https://api.sms-activate.ae/stubs/handler_api.php"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    def _make_request(self, action: str, **params) -> str:
        """Make a request to SMS-Activate API"""
        params['api_key'] = self.api_key
        params['action'] = action
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
    
    def get_balance(self) -> str:
        """Get account balance"""
        return self._make_request('getBalance')
    
    def get_services_list(self, country: Optional[str] = None, lang: str = 'en') -> Dict:
        """Get list of available services"""
        params = {'lang': lang}
        if country:
            params['country'] = country
        
        result = self._make_request('getServicesList', **params)
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"error": result}
    
    def get_countries(self) -> Dict:
        """Get list of all countries"""
        result = self._make_request('getCountries')
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"error": result}
    
    def get_prices(self, service: Optional[str] = None, country: Optional[str] = None) -> Dict:
        """Get current prices by country"""
        params = {}
        if service:
            params['service'] = service
        if country:
            params['country'] = country
        
        result = self._make_request('getPrices', **params)
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"error": result}
    
    def get_number_v2(self, service: str, country: str, **kwargs) -> Dict:
        """Request a virtual number (v2 with more details)"""
        params = {
            'service': service,
            'country': country
        }
        params.update(kwargs)
        
        result = self._make_request('getNumberV2', **params)
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"error": result}
    
    def get_status_v2(self, activation_id: str) -> Dict:
        """Get activation status v2 (with more details)"""
        result = self._make_request('getStatusV2', id=activation_id)
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"error": result}
    
    def set_status(self, activation_id: str, status: int) -> str:
        """Change activation status"""
        return self._make_request('setStatus', id=activation_id, status=status)


class SMSActivateBot:
    """Telegram bot for SMS-Activate with user management"""
    
    def __init__(self, bot_token: str, api_key: str, superuser_id: int):
        self.bot = telebot.TeleBot(bot_token)
        self.api = SMSActivateAPI(api_key)
        self.db = Database()
        self.superuser_id = superuser_id
        self.superuser_username = None  # Will be fetched
        self.user_states = {}  # Store user conversation states
        self.cached_countries = None  # Cache countries data
        self.cached_services = None   # Cache services data
        self.cached_prices = None      # Cache prices data
        self.failed_orders = []  # Track orders that failed due to insufficient balance
        self.failed_orders_lock = threading.Lock()  # Thread-safe access
        self.failed_purchases_tracker = {}  # Track failed purchase amounts per user {user_id: [(amount, timestamp), ...]}
        self.failed_purchases_lock = threading.Lock()  # Thread-safe access
        
        # Fetch superuser info
        self._fetch_superuser_info()
        
        # Start background cleanup thread
        self._start_cleanup_thread()
        
        # Start auto-refund thread
        self._start_autorefund_thread()
        
        self._register_handlers()
    
    def _register_handlers(self):
        """Register all command and message handlers"""
        
        @self.bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            self.handle_start(message)
        
        @self.bot.message_handler(commands=['language'])
        def change_language(message):
            self.handle_language(message)
        
        @self.bot.message_handler(commands=['balance'])
        def send_balance(message):
            self.handle_balance(message)
        
        @self.bot.message_handler(commands=['deposit'])
        def request_deposit(message):
            self.handle_deposit(message)
        
        @self.bot.message_handler(commands=['services'])
        def send_services(message):
            self.handle_services(message)
        
        @self.bot.message_handler(commands=['countries'])
        def send_countries(message):
            self.handle_countries(message)
        
        @self.bot.message_handler(commands=['prices'])
        def send_prices(message):
            self.handle_prices(message)
        
        @self.bot.message_handler(commands=['buy'])
        def buy_number(message):
            self.handle_buy(message)
        
        @self.bot.message_handler(commands=['myorders'])
        def my_orders(message):
            self.handle_myorders(message)
        
        @self.bot.message_handler(commands=['check'])
        def check_status(message):
            self.handle_check(message)
        
        @self.bot.message_handler(commands=['cancel'])
        def cancel_order(message):
            self.handle_cancel(message)
        
        @self.bot.message_handler(commands=['history'])
        def transaction_history(message):
            self.handle_history(message)
        
        # Superuser commands
        @self.bot.message_handler(commands=['stats'])
        def show_stats(message):
            self.handle_stats(message)
        
        @self.bot.message_handler(commands=['users'])
        def list_users(message):
            self.handle_users(message)
        
        @self.bot.message_handler(commands=['addbalance'])
        def add_balance(message):
            self.handle_addbalance(message)
        
        @self.bot.message_handler(commands=['deductbalance'])
        def deduct_balance(message):
            self.handle_deductbalance(message)
        
        @self.bot.message_handler(commands=['mainbalance'])
        def main_balance(message):
            self.handle_mainbalance(message)
        
        @self.bot.message_handler(commands=['allhistory'])
        def all_history(message):
            self.handle_allhistory(message)
        
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_handler(call):
            self.handle_callback(call)
        
        # Main menu button handlers
        @self.bot.message_handler(func=lambda message: message.text in [
            "🛒 Purchase", "🛒 Покупка", "🛒 Sotib olish"
        ])
        def button_purchase_menu(message):
            self.handle_purchase_menu(message)
        
        @self.bot.message_handler(func=lambda message: message.text in [
            "💰 Balance", "💰 Баланс", "💰 Balans"
        ])
        def button_balance_menu(message):
            self.handle_balance_menu(message)
        
        @self.bot.message_handler(func=lambda message: message.text in [
            "⚙️ Settings", "⚙️ Настройки", "⚙️ Sozlamalar"
        ])
        def button_settings_menu(message):
            self.handle_settings_menu(message)
        
        @self.bot.message_handler(func=lambda message: message.text in [
            "🔐 Superuser", "🔐 Суперпользователь", "🔐 Supermenejer"
        ])
        def button_superuser_menu(message):
            self.handle_superuser_menu(message)
        
        # Back to main menu button
        @self.bot.message_handler(func=lambda message: message.text in [
            "🔙 Back to Main Menu", "🔙 Главное меню", "🔙 Назад в главное меню", "🔙 Asosiy menyu"
        ])
        def button_back_main(message):
            self.handle_back_to_main(message)
        
        # Purchase submenu handlers
        @self.bot.message_handler(func=lambda message: message.text in [
            "🛍️ Buy Number", "🛍️ Купить номер", "🛍️ Raqam sotib olish"
        ])
        def button_buy(message):
            self.handle_buy_button(message)
        
        @self.bot.message_handler(func=lambda message: message.text in [
            "📊 My Orders", "📊 Мои заказы", "📊 Buyurtmalarim"
        ])
        def button_myorders(message):
            self.handle_myorders(message)
        
        @self.bot.message_handler(func=lambda message: message.text in [
            "📋 Services", "📋 Сервисы", "📋 Xizmatlar"
        ])
        def button_services(message):
            self.handle_services(message)
        
        @self.bot.message_handler(func=lambda message: message.text in [
            "🌍 Countries", "🌍 Страны", "🌍 Davlatlar"
        ])
        def button_countries(message):
            self.handle_countries(message)
        
        @self.bot.message_handler(func=lambda message: message.text in [
            "💵 Prices", "💵 Цены", "💵 Narxlar"
        ])
        def button_prices(message):
            self.handle_prices(message)
        
        # Balance submenu handlers
        @self.bot.message_handler(func=lambda message: message.text in [
            "💳 Check Balance", "💳 Проверить баланс", "💳 Balansni tekshirish"
        ])
        def button_check_balance(message):
            self.handle_balance(message)
        
        @self.bot.message_handler(func=lambda message: message.text in [
            "➕ Deposit", "➕ Пополнить", "➕ To'ldirish"
        ])
        def button_deposit(message):
            self.handle_deposit(message)
        
        @self.bot.message_handler(func=lambda message: message.text in [
            "📜 Transaction History", "📜 История транзакций", "📜 Tranzaksiyalar tarixi"
        ])
        def button_history(message):
            self.handle_history(message)
        
        # Settings submenu handlers
        @self.bot.message_handler(func=lambda message: message.text in [
            "🌐 Change Language", "🌐 Изменить язык", "🌐 Tilni o'zgartirish"
        ])
        def button_language(message):
            self.handle_language(message)
        
        @self.bot.message_handler(func=lambda message: message.text in [
            "❓ Help", "❓ Помощь", "❓ Yordam"
        ])
        def button_help(message):
            self.handle_start(message)
        
        # Superuser submenu handlers
        @self.bot.message_handler(func=lambda message: message.text in [
            "📊 Statistics", "📊 Статистика", "📊 Statistika"
        ])
        def button_stats(message):
            self.handle_stats(message)
        
        @self.bot.message_handler(func=lambda message: message.text in [
            "👥 Users List", "👥 Список пользователей", "👥 Foydalanuvchilar ro'yxati"
        ])
        def button_users(message):
            self.handle_users(message)
        
        @self.bot.message_handler(func=lambda message: message.text in [
            "💎 API Balance", "💎 Баланс API", "💎 API balansi"
        ])
        def button_mainbalance(message):
            self.handle_mainbalance(message)
        
        @self.bot.message_handler(func=lambda message: message.text in [
            "📈 All Transactions", "📈 Все транзакции", "📈 Barcha tranzaksiyalar"
        ])
        def button_allhistory(message):
            self.handle_allhistory(message)
    
    def _fetch_superuser_info(self):
        """Fetch superuser username from Telegram"""
        try:
            user_info = self.bot.get_chat(self.superuser_id)
            if user_info.username:
                # Escape underscores for Markdown
                escaped_username = user_info.username.replace('_', '\\_')
                self.superuser_username = f"@{escaped_username}"
            else:
                self.superuser_username = f"User ID: {self.superuser_id}"
            logger.info(f"Superuser username: @{user_info.username if user_info.username else self.superuser_id}")
        except Exception as e:
            logger.error(f"Could not fetch superuser info: {e}")
            self.superuser_username = f"User ID: {self.superuser_id}"
    
    def get_admin_contact(self) -> str:
        """Get admin contact info"""
        return self.superuser_username or f"User ID: {self.superuser_id}"
    
    def log_to_channel(self, message: str, user_id: int = None, username: str = None):
        """Send log message to LOG_CHANNEL"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Build log message
            log_text = f"🕐 {timestamp}\n\n{message}"
            
            # Add user info if provided
            if user_id or username:
                log_text += "\n\n👤 **User Info:**"
                if user_id:
                    log_text += f"\n• ID: `{user_id}`"
                if username:
                    log_text += f"\n• Username: @{username}"
            
            # Send to channel
            self.bot.send_message(LOG_CHANNEL, log_text, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Failed to log to channel: {e}")
    
    def _start_cleanup_thread(self):
        """Start background thread to cancel failed orders every 3 minutes"""
        def cleanup_worker():
            while True:
                try:
                    time.sleep(FAILED_ORDERS_CLEANUP_INTERVAL)
                    self._cancel_failed_orders()
                except Exception as e:
                    logger.error(f"Error in cleanup thread: {e}")
        
        cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
        cleanup_thread.start()
        logger.info("Started background cleanup thread for failed orders")
    
    def _cancel_failed_orders(self):
        """Cancel all orders in failed_orders list"""
        with self.failed_orders_lock:
            if not self.failed_orders:
                return
            
            logger.info(f"Attempting to cancel {len(self.failed_orders)} failed orders...")
            
            cancelled_count = 0
            remaining_orders = []
            
            for order in self.failed_orders:
                activation_id = order.get('activation_id')
                timestamp = order.get('timestamp', 0)
                
                # Try to cancel
                try:
                    result = self.api.set_status(activation_id, 8)
                    if 'ACCESS_CANCEL' in str(result):
                        cancelled_count += 1
                        logger.info(f"Successfully cancelled failed order {activation_id}")
                    else:
                        # Keep trying if cancel failed
                        if time.time() - timestamp < 1200:  # Keep trying for 20 minutes
                            remaining_orders.append(order)
                        else:
                            logger.warning(f"Gave up on order {activation_id} after 20 minutes")
                except Exception as e:
                    logger.error(f"Error cancelling {activation_id}: {e}")
                    # Keep trying
                    if time.time() - timestamp < 1200:
                        remaining_orders.append(order)
            
            self.failed_orders = remaining_orders
            
            if cancelled_count > 0:
                logger.info(f"Cancelled {cancelled_count} failed orders, {len(remaining_orders)} remaining")
        
        # Also cleanup old failed purchase records
        self._cleanup_failed_purchases()
    
    def _cleanup_failed_purchases(self):
        """Remove failed purchase records older than block time"""
        with self.failed_purchases_lock:
            current_time = time.time()
            for user_id in list(self.failed_purchases_tracker.keys()):
                # Filter out records older than block time
                self.failed_purchases_tracker[user_id] = [
                    (amount, timestamp) for amount, timestamp in self.failed_purchases_tracker[user_id]
                    if current_time - timestamp < FAILED_PURCHASE_BLOCK_TIME
                ]
                # Remove user if no records left
                if not self.failed_purchases_tracker[user_id]:
                    del self.failed_purchases_tracker[user_id]
    
    def track_failed_purchase(self, user_id: int, amount: float):
        """Track a failed purchase attempt"""
        with self.failed_purchases_lock:
            if user_id not in self.failed_purchases_tracker:
                self.failed_purchases_tracker[user_id] = []
            self.failed_purchases_tracker[user_id].append((amount, time.time()))
            logger.info(f"Tracked failed purchase for user {user_id}: ${amount:.2f}")
    
    def get_failed_purchases_total(self, user_id: int) -> float:
        """Get total failed purchase amount for user in last 20 minutes"""
        with self.failed_purchases_lock:
            if user_id not in self.failed_purchases_tracker:
                return 0.0
            
            current_time = time.time()
            total = sum(
                amount for amount, timestamp in self.failed_purchases_tracker[user_id]
                if current_time - timestamp < FAILED_PURCHASE_BLOCK_TIME
            )
            return total
    
    def is_user_blocked(self, user_id: int, required_amount: float, user_balance: float) -> tuple:
        """
        Check if user is blocked from purchasing
        Returns: (is_blocked: bool, reason: str, failed_total: float)
        """
        failed_total = self.get_failed_purchases_total(user_id)
        
        # If failed purchases < threshold, not blocked
        if failed_total < FAILED_PURCHASE_THRESHOLD:
            return (False, "", failed_total)
        
        # If user has 2x the required amount, allow purchase
        safety_amount = required_amount * SAFETY_BALANCE_MULTIPLIER
        if user_balance >= safety_amount:
            return (False, "", failed_total)
        
        # User is blocked
        return (True, f"Too many failed purchases (${failed_total:.2f}). Need ${safety_amount:.2f} to proceed.", failed_total)
    
    def _start_autorefund_thread(self):
        """Start background thread to check for expired orders and auto-refund"""
        def autorefund_worker():
            while True:
                try:
                    time.sleep(AUTO_REFUND_CHECK_INTERVAL)
                    self._check_expired_orders()
                except Exception as e:
                    logger.error(f"Error in auto-refund thread: {e}")
        
        autorefund_thread = threading.Thread(target=autorefund_worker, daemon=True)
        autorefund_thread.start()
        logger.info("Started background auto-refund thread for expired orders")
    
    def _check_expired_orders(self):
        """Check all active orders for expired/cancelled status and auto-refund"""
        try:
            # Get all users with active orders
            users = self.db.get_all_users()
            refund_count = 0
            
            for user in users:
                user_id = user['user_id']
                activations = self.db.get_user_activations(user_id)
                
                for activation in activations:
                    # Only check active orders (not cancelled, not completed)
                    if activation.get('status') in ['active', 'pending', None]:
                        activation_id = activation.get('activation_id')
                        
                        try:
                            # Check status from API
                            status_result = self.api.get_status(activation_id)
                            
                            # If order is cancelled/expired by API
                            if 'STATUS_CANCEL' in str(status_result):
                                # Refund user
                                user_paid = float(activation.get('cost', 0))
                                phone_number = activation.get('phone_number', 'N/A')
                                service = activation.get('service', 'N/A')
                                
                                self.db.add_balance(user_id, user_paid, f"Auto-refund for expired order {activation_id}")
                                self.db.update_activation(activation_id, status='cancelled')
                                
                                refund_count += 1
                                logger.info(f"Auto-refunded ${user_paid:.2f} to user {user_id} for expired order {activation_id}")
                                
                                # Log to channel
                                self.log_to_channel(
                                    f"🔄 **Auto-Refund - Order Expired**\n\n"
                                    f"🆔 **Order ID:** `{activation_id}`\n"
                                    f"📞 **Phone:** +{phone_number}\n"
                                    f"🔷 **Service:** {service}\n"
                                    f"💰 **Refunded:** ${user_paid:.2f}\n"
                                    f"📝 **Reason:** Order expired (20 min timeout)",
                                    user_id=user_id,
                                    username=None
                                )
                                
                                # Try to notify user
                                try:
                                    lang = self.get_user_lang(user_id)
                                    if lang == 'en':
                                        notify_text = f"🔄 **Auto-Refund**\n\nOrder `{activation_id}` expired after 20 minutes.\n\n💰 Refunded: ${user_paid:.2f}"
                                    elif lang == 'ru':
                                        notify_text = f"🔄 **Авто-возврат**\n\nЗаказ `{activation_id}` истёк через 20 минут.\n\n💰 Возвращено: ${user_paid:.2f}"
                                    else:
                                        notify_text = f"🔄 **Avto-qaytarish**\n\nBuyurtma `{activation_id}` 20 daqiqadan keyin tugadi.\n\n💰 Qaytarildi: ${user_paid:.2f}"
                                    
                                    self.bot.send_message(user_id, notify_text, parse_mode='Markdown')
                                except Exception as e:
                                    logger.error(f"Could not notify user {user_id}: {e}")
                        
                        except Exception as e:
                            logger.error(f"Error checking order {activation_id}: {e}")
                            continue
            
            if refund_count > 0:
                logger.info(f"Auto-refunded {refund_count} expired orders")
        
        except Exception as e:
            logger.error(f"Error in _check_expired_orders: {e}")
    
    def get_prices_data(self):
        """Fetch and cache prices"""
        if not self.cached_prices:
            try:
                self.cached_prices = self.api.get_prices()
                logger.info("Prices cached successfully")
            except Exception as e:
                logger.error(f"Error fetching prices: {e}")
                self.cached_prices = {}
        return self.cached_prices
    
    def get_service_min_price(self, service_code: str) -> float:
        """Get minimum price for a service across all countries"""
        prices = self.get_prices_data()
        min_price = float('inf')
        
        for country_id, services in prices.items():
            if isinstance(services, dict) and service_code in services:
                service_data = services[service_code]
                if isinstance(service_data, dict):
                    # Use 'retail' price (actual price), not 'cost' (wholesale)
                    cost = service_data.get('retail') or service_data.get('cost', 0)
                    try:
                        cost_float = float(cost)
                        if cost_float > 0 and cost_float < min_price:
                            min_price = cost_float
                    except:
                        pass
        
        if min_price == float('inf'):
            return 0
        
        # Apply currency conversion and 2x markup (prices are estimates)
        return min_price * CURRENCY_MULTIPLIER * PRICE_MULTIPLIER
    
    def get_exact_price(self, service_code: str, country_id: str) -> float:
        """Get exact price for service in specific country"""
        prices = self.get_prices_data()
        
        if str(country_id) in prices:
            services = prices[str(country_id)]
            if isinstance(services, dict) and service_code in services:
                service_data = services[service_code]
                if isinstance(service_data, dict):
                    # Use 'retail' price (actual price), not 'cost' (wholesale)
                    cost = service_data.get('retail') or service_data.get('cost', 0)
                    try:
                        cost_float = float(cost)
                        # Calculate display price (estimate only)
                        final_price = cost_float * CURRENCY_MULTIPLIER * PRICE_MULTIPLIER
                        # Log for debugging
                        logger.info(f"Price for {service_code} in country {country_id}: getPrices={cost_float}, Display=${final_price:.2f} (ESTIMATE)")
                        # Apply currency conversion and 2x markup
                        return final_price
                    except:
                        pass
        
        return 0
    
    def is_superuser(self, user_id: int) -> bool:
        """Check if user is superuser"""
        return user_id == self.superuser_id
    
    def get_user_lang(self, user_id: int) -> str:
        """Get user language"""
        return self.db.get_language(user_id)
    
    def handle_purchase_menu(self, message):
        """Handle Purchase main menu button"""
        user_id = message.from_user.id
        lang = self.get_user_lang(user_id)
        
        text = "🛒 " + ("Purchase Menu" if lang == 'en' else "Меню покупки" if lang == 'ru' else "Sotib olish menyusi")
        text += "\n\n" + ("Choose an option:" if lang == 'en' else "Выберите опцию:" if lang == 'ru' else "Tanlang:")
        
        keyboard = get_purchase_submenu(lang)
        self.bot.send_message(message.chat.id, text, reply_markup=keyboard)
    
    def handle_balance_menu(self, message):
        """Handle Balance main menu button"""
        user_id = message.from_user.id
        lang = self.get_user_lang(user_id)
        
        text = "💰 " + ("Balance Menu" if lang == 'en' else "Меню баланса" if lang == 'ru' else "Balans menyusi")
        text += "\n\n" + ("Choose an option:" if lang == 'en' else "Выберите опцию:" if lang == 'ru' else "Tanlang:")
        
        keyboard = get_balance_submenu(lang)
        self.bot.send_message(message.chat.id, text, reply_markup=keyboard)
    
    def handle_settings_menu(self, message):
        """Handle Settings main menu button"""
        user_id = message.from_user.id
        lang = self.get_user_lang(user_id)
        
        text = "⚙️ " + ("Settings Menu" if lang == 'en' else "Меню настроек" if lang == 'ru' else "Sozlamalar menyusi")
        text += "\n\n" + ("Choose an option:" if lang == 'en' else "Выберите опцию:" if lang == 'ru' else "Tanlang:")
        
        keyboard = get_settings_submenu(lang)
        self.bot.send_message(message.chat.id, text, reply_markup=keyboard)
    
    def handle_superuser_menu(self, message):
        """Handle Superuser main menu button"""
        user_id = message.from_user.id
        lang = self.get_user_lang(user_id)
        
        if not self.is_superuser(user_id):
            text = get_text(lang, 'admin_only')
            self.bot.send_message(message.chat.id, text)
            return
        
        text = "🔐 " + ("Superuser Menu" if lang == 'en' else "Меню суперпользователя" if lang == 'ru' else "Supermenejer menyusi")
        text += "\n\n" + ("Choose an option:" if lang == 'en' else "Выберите опцию:" if lang == 'ru' else "Tanlang:")
        
        keyboard = get_superuser_submenu(lang)
        self.bot.send_message(message.chat.id, text, reply_markup=keyboard)
    
    def handle_back_to_main(self, message):
        """Handle Back to Main Menu button"""
        user_id = message.from_user.id
        lang = self.get_user_lang(user_id)
        
        text = "🏠 " + ("Main Menu" if lang == 'en' else "Главное меню" if lang == 'ru' else "Asosiy menyu")
        
        keyboard = get_admin_keyboard(lang) if self.is_superuser(user_id) else get_main_keyboard(lang)
        self.bot.send_message(message.chat.id, text, reply_markup=keyboard)
    
    def handle_start(self, message):
        """Handle /start and /help commands"""
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        
        # Create or get user
        user = self.db.get_or_create_user(user_id, username, first_name)
        lang = self.get_user_lang(user_id)
        
        # If new user, show language selection first
        if user.get('language') == 'en' and 'created_at' in user:
            # Check if just created (within last second)
            created = datetime.fromisoformat(user['created_at'])
            if (datetime.now() - created).total_seconds() < 2:
                self.bot.send_message(
                    message.chat.id,
                    "Please select your language / Выберите язык / Tilni tanlang:",
                    reply_markup=get_language_keyboard()
                )
                return
        
        welcome_text = get_text(lang, 'welcome', admin=self.get_admin_contact())
        
        # Add Privacy Policy and Terms agreement
        privacy_link = "https://rentry.co/SMS-ACTIVATE-BOBO"
        if lang == 'en':
            welcome_text += f"\n\n🚫 *Privacy Policy & Terms*\n\n"
            welcome_text += f"By continuing to use this bot, you agree to our [Privacy Policy & Terms and Conditions]({privacy_link}).\n\n"
            welcome_text += f"Please read them carefully before using the service."
        elif lang == 'ru':
            welcome_text += f"\n\n🚫 *Политика конфиденциальности и Условия*\n\n"
            welcome_text += f"Продолжая использовать этого бота, вы соглашаетесь с нашей [Политикой конфиденциальности и Условиями использования]({privacy_link}).\n\n"
            welcome_text += f"Пожалуйста, внимательно прочитайте их перед использованием сервиса."
        else:  # uz
            welcome_text += f"\n\n🚫 *Maxfiylik Siyosati va Foydalanish Shartlari*\n\n"
            welcome_text += f"Ushbu botdan foydalanishni davom ettirish orqali siz bizning [Maxfiylik Siyosati va Foydalanish Shartlarimizga]({privacy_link}) rozilik bildirasiz.\n\n"
            welcome_text += f"Iltimos, xizmatdan foydalanishdan oldin diqqat bilan o'qing."
        
        # Get appropriate keyboard
        if self.is_superuser(user_id):
            keyboard = get_admin_keyboard(lang)
            welcome_text += "\n\n🔐 *Superuser Commands:*\n"
            welcome_text += "/addbalance <user_id> <amount>\n"
            welcome_text += "/deductbalance <user_id> <amount>\n"
        else:
            keyboard = get_main_keyboard(lang)
        
        self.bot.send_message(
            message.chat.id,
            welcome_text,
            parse_mode='Markdown',
            reply_markup=keyboard
        )
    
    def handle_language(self, message):
        """Handle /language command"""
        lang = self.get_user_lang(message.from_user.id)
        text = get_text(lang, 'language_select')
        
        self.bot.send_message(
            message.chat.id,
            text,
            reply_markup=get_language_keyboard()
        )
    
    def handle_balance(self, message):
        """Handle /balance command"""
        user_id = message.from_user.id
        lang = self.get_user_lang(user_id)
        
        balance = self.db.get_balance(user_id)
        text = get_text(lang, 'balance', balance=balance)
        
        keyboard = get_admin_keyboard(lang) if self.is_superuser(user_id) else get_main_keyboard(lang)
        self.bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=keyboard)
    
    def handle_deposit(self, message):
        """Handle /deposit command"""
        user_id = message.from_user.id
        lang = self.get_user_lang(user_id)
        
        text = get_text(lang, 'deposit_request', user_id=user_id, admin=self.get_admin_contact())
        self.bot.send_message(message.chat.id, text, parse_mode='Markdown')
    
    def handle_services(self, message):
        """Handle /services command"""
        user_id = message.from_user.id
        lang = self.get_user_lang(user_id)
        
        try:
            loading = "🔄 Loading..." if lang == 'en' else "🔄 Загрузка..." if lang == 'ru' else "🔄 Yuklanmoqda..."
            self.bot.send_message(message.chat.id, loading)
            
            services = self.api.get_services_list(lang=lang)
            
            if 'error' in services:
                self.bot.send_message(message.chat.id, f"⚠️ Error: {services['error']}")
                return
            
            if services.get('status') == 'success' and 'services' in services:
                services_list = services['services']
                
                response = "📋 " + ("Services" if lang == 'en' else "Сервисы" if lang == 'ru' else "Xizmatlar") + "\n\n"
                
                for i, service in enumerate(services_list[:30]):
                    code = service.get('code', 'N/A')
                    name = service.get('name', 'N/A')
                    response += f"`{code}` - {name}\n"
                
                if len(services_list) > 30:
                    response += f"\n_...{len(services_list) - 30} more_"
                
                self.bot.send_message(message.chat.id, response, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Error fetching services: {e}")
            text = get_text(lang, 'error_occurred')
            self.bot.send_message(message.chat.id, text)
    
    def handle_countries(self, message):
        """Handle /countries command"""
        user_id = message.from_user.id
        lang = self.get_user_lang(user_id)
        
        try:
            loading = "🔄 Loading..." if lang == 'en' else "🔄 Загрузка..." if lang == 'ru' else "🔄 Yuklanmoqda..."
            self.bot.send_message(message.chat.id, loading)
            
            countries = self.api.get_countries()
            
            if 'error' in countries:
                self.bot.send_message(message.chat.id, f"⚠️ Error: {countries['error']}")
                return
            
            response = "🌍 " + ("Countries" if lang == 'en' else "Страны" if lang == 'ru' else "Davlatlar") + "\n\n"
            
            for country_key, country_data in list(countries.items())[:30]:
                if isinstance(country_data, dict):
                    country_id = country_data.get('id', 'N/A')
                    country_name = country_data.get('eng', 'N/A')
                    if lang == 'ru':
                        country_name = country_data.get('rus', country_name)
                    visible = "✅" if country_data.get('visible') == 1 else "❌"
                    response += f"{visible} `{country_id}` - {country_name}\n"
            
            if len(countries) > 30:
                response += f"\n_...{len(countries) - 30} more_"
            
            self.bot.send_message(message.chat.id, response, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Error fetching countries: {e}")
            text = get_text(lang, 'error_occurred')
            self.bot.send_message(message.chat.id, text)
    
    def handle_prices(self, message):
        """Handle /prices command"""
        user_id = message.from_user.id
        lang = self.get_user_lang(user_id)
        
        parts = message.text.split()
        service = parts[1] if len(parts) > 1 else None
        country = parts[2] if len(parts) > 2 else None
        
        try:
            loading = "🔄 Loading..." if lang == 'en' else "🔄 Загрузка..." if lang == 'ru' else "🔄 Yuklanmoqda..."
            self.bot.send_message(message.chat.id, loading)
            
            prices = self.api.get_prices(service=service, country=country)
            
            if 'error' in prices:
                self.bot.send_message(message.chat.id, f"⚠️ Error: {prices['error']}")
                return
            
            if not prices or len(prices) == 0:
                usage_text = "Usage: `/prices [service] [country]`"
                if lang == 'ru':
                    usage_text = "Использование: `/prices [сервис] [страна]`"
                elif lang == 'uz':
                    usage_text = "Foydalanish: `/prices [xizmat] [davlat]`"
                self.bot.send_message(message.chat.id, usage_text, parse_mode='Markdown')
                return
            
            response = "💵 " + ("Prices" if lang == 'en' else "Цены" if lang == 'ru' else "Narxlar") + "\n\n"
            
            count = 0
            for country_id, services in list(prices.items())[:5]:
                response += f"*Country {country_id}:*\n"
                if isinstance(services, dict):
                    for service_code, details in list(services.items())[:5]:
                        if isinstance(details, dict):
                            api_cost = details.get('cost', 0)
                            # Show user price (2x markup)
                            try:
                                user_price = float(api_cost) * PRICE_MULTIPLIER
                                cost_display = f"{user_price:.2f}"
                            except:
                                cost_display = 'N/A'
                            quantity = details.get('count', 'N/A')
                            response += f"  • `{service_code}`: ${cost_display} USD ({quantity} " + ("available" if lang == 'en' else "доступно" if lang == 'ru' else "mavjud") + ")\n"
                            count += 1
                response += "\n"
                
                if count > 20:
                    response += "_Limited output..._\n"
                    break
            
            self.bot.send_message(message.chat.id, response, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Error fetching prices: {e}")
            text = get_text(lang, 'error_occurred')
            self.bot.send_message(message.chat.id, text)
    
    def handle_buy_button(self, message):
        """Handle buy button press"""
        user_id = message.from_user.id
        lang = self.get_user_lang(user_id)
        
        text = "🛒 " + ("Choose how to buy:" if lang == 'en' else "Выберите способ покупки:" if lang == 'ru' else "Sotib olish usulini tanlang:")
        
        self.bot.send_message(
            message.chat.id,
            text,
            reply_markup=get_buy_method_keyboard(lang)
        )
    
    def handle_buy(self, message):
        """Handle /buy command (legacy support)"""
        user_id = message.from_user.id
        lang = self.get_user_lang(user_id)
        
        parts = message.text.split()
        
        if len(parts) < 3:
            text = get_text(lang, 'buy_usage')
            self.bot.send_message(message.chat.id, text, parse_mode='Markdown')
            return
        
        service = parts[1]
        country = parts[2]
        
        # Check user balance first
        user_balance = self.db.get_balance(user_id)
        
        try:
            text = get_text(lang, 'buy_processing')
            self.bot.send_message(message.chat.id, text)
            
            result = self.api.get_number_v2(service, country)
            
            if 'error' in result:
                error_msg = result['error']
                
                if 'NO_NUMBERS' in error_msg:
                    error_text = get_text(lang, 'buy_no_numbers')
                elif 'NO_BALANCE' in error_msg:
                    # This means SMS-Activate API account is empty (admin's problem)
                    if lang == 'en':
                        error_text = "❌ Service temporarily unavailable\n\nPlease try again later or contact admin."
                    elif lang == 'ru':
                        error_text = "❌ Сервис временно недоступен\n\nПопробуйте позже или свяжитесь с админом."
                    else:
                        error_text = "❌ Xizmat vaqtincha mavjud emas\n\nKeyinroq urinib ko'ring yoki admin bilan bog'laning."
                    
                    # Notify superuser
                    try:
                        admin_msg = f"⚠️ SMS-Activate API NO_BALANCE ERROR!\n\nUser {user_id} tried to buy {service} but your SMS-Activate account has insufficient balance.\n\nPlease top up your SMS-Activate account!"
                        self.bot.send_message(self.superuser_id, admin_msg)
                    except:
                        pass
                elif 'BAD_SERVICE' in error_msg:
                    error_text = get_text(lang, 'buy_invalid_service')
                else:
                    error_text = error_msg
                
                text = get_text(lang, 'buy_error', error=error_text)
                self.bot.send_message(message.chat.id, text, parse_mode='Markdown')
                return
            
            # Extract data
            activation_id = result.get('activationId', 'N/A')
            phone_number = result.get('phoneNumber', 'N/A')
            api_cost = float(result.get('activationCost', 0))  # What we pay to API
            user_cost = api_cost * PRICE_MULTIPLIER  # What we charge user (2x profit)
            country_code = result.get('countryCode', 'N/A')
            
            # Check if user has enough balance (using marked up price)
            if user_balance < user_cost:
                # Show actual price in error message
                needed = user_cost - user_balance
                if lang == 'en':
                    text = f"❌ **Insufficient Balance**\n\n"
                    text += f"💰 **Actual Price:** ${user_cost:.2f}\n"
                    text += f"💳 **Your Balance:** ${user_balance:.2f}\n"
                    text += f"📉 **Needed:** ${needed:.2f}\n\n"
                    text += f"Please top up your balance with /deposit"
                elif lang == 'ru':
                    text = f"❌ **Недостаточно Средств**\n\n"
                    text += f"💰 **Фактическая цена:** ${user_cost:.2f}\n"
                    text += f"💳 **Ваш баланс:** ${user_balance:.2f}\n"
                    text += f"📉 **Требуется:** ${needed:.2f}\n\n"
                    text += f"Пожалуйста, пополните баланс через /deposit"
                else:
                    text = f"❌ **Balans Yetarli Emas**\n\n"
                    text += f"💰 **Haqiqiy narx:** ${user_cost:.2f}\n"
                    text += f"💳 **Sizning balansingiz:** ${user_balance:.2f}\n"
                    text += f"📉 **Kerak:** ${needed:.2f}\n\n"
                    text += f"Iltimos /deposit orqali balansni to'ldiring"
                
                self.bot.send_message(message.chat.id, text, parse_mode='Markdown')
                
                # Cancel the activation
                try:
                    self.api.set_status(activation_id, 8)
                except:
                    pass
                return
            
            # Deduct balance (charge user the marked up price)
            success = self.db.deduct_balance(
                user_id, 
                user_cost, 
                f"Order {activation_id}: {service} in country {country_code}"
            )
            
            if not success:
                text = get_text(lang, 'no_balance')
                self.bot.send_message(message.chat.id, text, parse_mode='Markdown')
                
                # Cancel the activation
                try:
                    self.api.set_status(activation_id, 8)
                except:
                    pass
                return
            
            # Save activation (store what user paid, not API cost)
            result['service'] = service
            result['activationCost'] = user_cost  # Override with user's price
            self.db.add_activation(user_id, result)
            
            # Send success message (show user their price, not API cost)
            text = get_text(
                lang, 
                'buy_success',
                order_id=activation_id,
                phone=phone_number,
                service=service,
                country=country_code,
                cost=user_cost
            )
            self.bot.send_message(message.chat.id, text, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error buying number: {e}")
            text = get_text(lang, 'error_occurred')
            self.bot.send_message(message.chat.id, text)
    
    def handle_myorders(self, message):
        """Handle My Orders - show active orders with inline buttons"""
        user_id = message.from_user.id
        lang = self.get_user_lang(user_id)
        
        # Get only active/waiting orders
        activations = self.db.get_user_activations(user_id, limit=20)
        
        # Filter to show only active orders (not cancelled/completed)
        active_orders = [a for a in activations if a.get('status') in ['active', 'waiting', 'pending', None]]
        
        if not active_orders:
            if lang == 'en':
                text = "📊 **My Orders**\n\nYou have no active orders.\n\nOrders appear here after purchase and remain until completed or cancelled."
            elif lang == 'ru':
                text = "📊 **Мои Заказы**\n\nУ вас нет активных заказов.\n\nЗаказы появляются здесь после покупки и остаются до завершения или отмены."
            else:
                text = "📊 **Buyurtmalarim**\n\nSizda faol buyurtmalar yo'q.\n\nBuyurtmalar sotib olishdan keyin shu yerda ko'rinadi va tugatilgunga yoki bekor qilinguncha qoladi."
            
            self.bot.send_message(message.chat.id, text, parse_mode='Markdown')
            return
        
        # Show header
        if lang == 'en':
            text = f"📊 **My Orders** ({len(active_orders)} active)\n\nTap any order to manage:"
        elif lang == 'ru':
            text = f"📊 **Мои Заказы** ({len(active_orders)} активных)\n\nНажмите на заказ для управления:"
        else:
            text = f"📊 **Buyurtmalarim** ({len(active_orders)} faol)\n\nBoshqarish uchun buyurtmaga bosing:"
        
        # Create inline keyboard with order buttons
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        for activation in active_orders:
            order_id = activation.get('activation_id', 'N/A')
            service = activation.get('service', 'N/A')
            phone = activation.get('phone_number', 'N/A')
            
            # Get service name
            service_display = service
            if self.cached_services:
                for svc in self.cached_services:
                    if svc.get('code') == service:
                        service_display = svc.get('name', service)
                        break
            
            # Create button text with service and partial phone
            if phone and phone != 'N/A':
                phone_display = phone[-4:] if len(phone) > 4 else phone
                button_text = f"📱 {service_display} ...{phone_display}"
            else:
                button_text = f"📱 {service_display} - #{order_id}"
            
            markup.add(types.InlineKeyboardButton(button_text, callback_data=f"order_view_{order_id}"))
        
        self.bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)
    
    def handle_order_view(self, call, activation_id):
        """Show order details with check/cancel buttons"""
        user_id = call.from_user.id
        lang = self.get_user_lang(user_id)
        
        # Get order from database
        activations = self.db.get_user_activations(user_id)
        order = None
        for activation in activations:
            if str(activation.get('activation_id')) == str(activation_id):
                order = activation
                break
        
        if not order:
            text = "❌ Order not found"
            self.bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
            return
        
        # Extract order details
        order_id = order.get('activation_id', 'N/A')
        service = order.get('service', 'N/A')
        phone = order.get('phone_number', 'N/A')
        cost = order.get('cost', 0)
        status = order.get('status', 'active')
        
        # Get service name
        service_display = service
        if self.cached_services:
            for svc in self.cached_services:
                if svc.get('code') == service:
                    service_display = svc.get('name', service)
                    break
        
        # Build message
        if lang == 'en':
            text = f"📱 **Order Details**\n\n"
            text += f"**Order ID:** `{order_id}`\n"
            text += f"**Service:** {service_display}\n"
            text += f"**Phone:** `{phone}`\n"
            text += f"**Cost:** ${cost:.2f}\n"
            text += f"**Status:** {status}\n\n"
            text += "⏳ Waiting for SMS..."
        elif lang == 'ru':
            text = f"📱 **Детали Заказа**\n\n"
            text += f"**ID Заказа:** `{order_id}`\n"
            text += f"**Сервис:** {service_display}\n"
            text += f"**Телефон:** `{phone}`\n"
            text += f"**Цена:** ${cost:.2f}\n"
            text += f"**Статус:** {status}\n\n"
            text += "⏳ Ожидание SMS..."
        else:
            text = f"📱 **Buyurtma Tafsilotlari**\n\n"
            text += f"**Buyurtma ID:** `{order_id}`\n"
            text += f"**Xizmat:** {service_display}\n"
            text += f"**Telefon:** `{phone}`\n"
            text += f"**Narx:** ${cost:.2f}\n"
            text += f"**Holat:** {status}\n\n"
            text += "⏳ SMS kutilmoqda..."
        
        # Create keyboard with check and cancel buttons
        keyboard = get_confirmation_keyboard(lang, order_id)
        
        self.bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=keyboard
        )
    
    def handle_check(self, message):
        """Handle /check command"""
        user_id = message.from_user.id
        lang = self.get_user_lang(user_id)
        
        parts = message.text.split()
        
        if len(parts) < 2:
            text = get_text(lang, 'check_usage')
            self.bot.send_message(message.chat.id, text, parse_mode='Markdown')
            return
        
        activation_id = parts[1]
        
        try:
            text = get_text(lang, 'check_processing')
            self.bot.send_message(message.chat.id, text)
            
            status_result = self.api.get_status_v2(activation_id)
            
            if 'error' in status_result:
                error_msg = status_result['error']
                
                if 'STATUS_CANCEL' in error_msg:
                    text = get_text(lang, 'check_cancelled')
                elif 'NO_ACTIVATION' in error_msg:
                    text = get_text(lang, 'check_not_found')
                else:
                    text = f"⚠️ {error_msg}"
                
                self.bot.send_message(message.chat.id, text, parse_mode='Markdown')
                return
            
            # Parse status
            verification_type = status_result.get('verificationType', 0)
            
            if verification_type == 0:
                sms_data = status_result.get('sms', {})
                if sms_data and sms_data.get('code'):
                    code = sms_data.get('code', 'N/A')
                    text = sms_data.get('text', 'N/A')
                    date_time = sms_data.get('dateTime', 'N/A')
                    
                    response = get_text(
                        lang,
                        'check_success',
                        order_id=activation_id,
                        code=code,
                        text=text,
                        time=date_time
                    )
                else:
                    response = get_text(lang, 'check_waiting', order_id=activation_id)
            else:
                response = get_text(lang, 'check_waiting', order_id=activation_id)
            
            self.bot.send_message(message.chat.id, response, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error checking status: {e}")
            text = get_text(lang, 'error_occurred')
            self.bot.send_message(message.chat.id, text)
    
    def handle_cancel(self, message):
        """Handle /cancel command"""
        user_id = message.from_user.id
        lang = self.get_user_lang(user_id)
        
        parts = message.text.split()
        
        if len(parts) < 2:
            text = get_text(lang, 'cancel_usage')
            self.bot.send_message(message.chat.id, text, parse_mode='Markdown')
            return
        
        activation_id = parts[1]
        
        try:
            text = get_text(lang, 'cancel_processing')
            self.bot.send_message(message.chat.id, text)
            
            result = self.api.set_status(activation_id, 8)
            
            if 'ACCESS_CANCEL' in result:
                # Find the activation and refund (refund what user paid)
                for activation in self.db.get_user_activations(user_id):
                    if str(activation.get('activation_id')) == str(activation_id):
                        user_paid = float(activation.get('cost', 0))
                        self.db.add_balance(user_id, user_paid, f"Refund for order {activation_id}")
                        self.db.update_activation(activation_id, status='cancelled')
                        break
                
                text = get_text(lang, 'cancel_success')
            elif 'EARLY_CANCEL_DENIED' in result:
                text = get_text(lang, 'cancel_early')
            elif 'NO_ACTIVATION' in result:
                text = get_text(lang, 'check_not_found')
            else:
                text = get_text(lang, 'cancel_failed', error=result)
            
            self.bot.send_message(message.chat.id, text, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error canceling: {e}")
            text = get_text(lang, 'error_occurred')
            self.bot.send_message(message.chat.id, text)
    
    def handle_history(self, message):
        """Handle /history command"""
        user_id = message.from_user.id
        lang = self.get_user_lang(user_id)
        
        transactions = self.db.get_user_transactions(user_id, limit=10)
        
        if not transactions:
            text = get_text(lang, 'history_empty')
            self.bot.send_message(message.chat.id, text)
            return
        
        response = get_text(lang, 'history_title')
        
        for trans in transactions:
            date = trans.get('timestamp', '')[:10]
            trans_type = "➕" if trans.get('type') == 'add' else "➖"
            amount = trans.get('amount', 0)
            description = trans.get('description', '')
            
            response += get_text(
                lang,
                'history_item',
                date=date,
                type=trans_type,
                amount=amount,
                description=description
            )
        
        self.bot.send_message(message.chat.id, response, parse_mode='Markdown')
    
    # ========== SUPERUSER COMMANDS ==========
    
    def handle_stats(self, message):
        """Handle /stats command (superuser only)"""
        user_id = message.from_user.id
        lang = self.get_user_lang(user_id)
        
        if not self.is_superuser(user_id):
            text = get_text(lang, 'admin_only')
            self.bot.send_message(message.chat.id, text)
            return
        
        stats = self.db.get_statistics()
        
        response = get_text(lang, 'stats_title')
        response += f"👥 Total Users: {stats['total_users']}\n"
        response += f"💰 Total Balance (Users): ${stats['total_balance']:.2f} USD\n"
        response += f"💸 Total Spent: ${stats['total_spent']:.2f} USD\n"
        response += f"📱 Total Activations: {stats['total_activations']}\n\n"
        response += f"📊 Today:\n"
        response += f"  • Transactions: {stats['today_transactions']}\n"
        response += f"  • Activations: {stats['today_activations']}\n"
        
        self.bot.send_message(message.chat.id, response, parse_mode='Markdown')
    
    def handle_users(self, message):
        """Handle /users command (superuser only)"""
        user_id = message.from_user.id
        lang = self.get_user_lang(user_id)
        
        if not self.is_superuser(user_id):
            text = get_text(lang, 'admin_only')
            self.bot.send_message(message.chat.id, text)
            return
        
        users = self.db.get_all_users()
        
        response = f"👥 *All Users* ({len(users)})\n\n"
        
        for user in users[:20]:
            uid = user.get('user_id')
            username = user.get('username', 'N/A')
            balance = user.get('balance', 0)
            total_activations = user.get('total_activations', 0)
            
            response += f"• ID: `{uid}` @{username}\n"
            response += f"  Balance: ${balance:.2f} USD | Orders: {total_activations}\n\n"
        
        if len(users) > 20:
            response += f"_...and {len(users) - 20} more users_"
        
        self.bot.send_message(message.chat.id, response, parse_mode='Markdown')
    
    def handle_addbalance(self, message):
        """Handle /addbalance command (superuser only)"""
        user_id = message.from_user.id
        lang = self.get_user_lang(user_id)
        
        if not self.is_superuser(user_id):
            text = get_text(lang, 'admin_only')
            self.bot.send_message(message.chat.id, text)
            return
        
        parts = message.text.split()
        
        if len(parts) < 3:
            self.bot.send_message(
                message.chat.id,
                "⚠️ *Usage:* `/addbalance <user_id> <amount>`\n\n*Example:* `/addbalance 123456 100`",
                parse_mode='Markdown'
            )
            return
        
        try:
            target_user_id = int(parts[1])
            amount = float(parts[2])
            
            self.db.add_balance(target_user_id, amount, f"Added by admin {user_id}")
            
            self.bot.send_message(
                message.chat.id,
                f"✅ Added ${amount:.2f} USD to user `{target_user_id}`",
                parse_mode='Markdown'
            )
            
            # Log to channel
            self.log_to_channel(
                f"➕ **Admin Added Balance**\n\n"
                f"💰 **Amount:** +${amount:.2f} USD\n"
                f"👤 **Target User ID:** `{target_user_id}`",
                user_id=user_id,
                username=message.from_user.username
            )
            
            # Notify user
            try:
                target_lang = self.get_user_lang(target_user_id)
                notify_text = f"✅ Your balance has been updated!\n\n+${amount:.2f} USD added by administrator"
                if target_lang == 'ru':
                    notify_text = f"✅ Ваш баланс обновлён!\n\n+${amount:.2f} USD добавлено администратором"
                elif target_lang == 'uz':
                    notify_text = f"✅ Balansingiz yangilandi!\n\n+${amount:.2f} USD administrator tomonidan qo'shildi"
                
                self.bot.send_message(target_user_id, notify_text)
            except:
                pass
            
        except ValueError:
            self.bot.send_message(message.chat.id, "⚠️ Invalid user ID or amount")
        except Exception as e:
            logger.error(f"Error adding balance: {e}")
            self.bot.send_message(message.chat.id, f"❌ Error: {str(e)}")
    
    def handle_deductbalance(self, message):
        """Handle /deductbalance command (superuser only)"""
        user_id = message.from_user.id
        lang = self.get_user_lang(user_id)
        
        if not self.is_superuser(user_id):
            text = get_text(lang, 'admin_only')
            self.bot.send_message(message.chat.id, text)
            return
        
        parts = message.text.split()
        
        if len(parts) < 3:
            self.bot.send_message(
                message.chat.id,
                "⚠️ *Usage:* `/deductbalance <user_id> <amount>`\n\n*Example:* `/deductbalance 123456 50`",
                parse_mode='Markdown'
            )
            return
        
        try:
            target_user_id = int(parts[1])
            amount = float(parts[2])
            
            success = self.db.deduct_balance(target_user_id, amount, f"Deducted by admin {user_id}")
            
            if success:
                self.bot.send_message(
                    message.chat.id,
                    f"✅ Deducted ${amount:.2f} USD from user `{target_user_id}`",
                    parse_mode='Markdown'
                )
                
                # Log to channel
                self.log_to_channel(
                    f"➖ **Admin Deducted Balance**\n\n"
                    f"💰 **Amount:** -${amount:.2f} USD\n"
                    f"👤 **Target User ID:** `{target_user_id}`",
                    user_id=user_id,
                    username=message.from_user.username
                )
            else:
                self.bot.send_message(message.chat.id, "⚠️ Insufficient balance or user not found")
            
        except ValueError:
            self.bot.send_message(message.chat.id, "⚠️ Invalid user ID or amount")
        except Exception as e:
            logger.error(f"Error deducting balance: {e}")
            self.bot.send_message(message.chat.id, f"❌ Error: {str(e)}")
    
    def handle_mainbalance(self, message):
        """Handle /mainbalance command (superuser only)"""
        user_id = message.from_user.id
        lang = self.get_user_lang(user_id)
        
        if not self.is_superuser(user_id):
            text = get_text(lang, 'admin_only')
            self.bot.send_message(message.chat.id, text)
            return
        
        try:
            balance = self.api.get_balance()
            
            if balance.startswith('ACCESS_BALANCE:'):
                amount = balance.split(':')[1].strip()
                response = f"💰 *Main API Balance*\n\nBalance: `{amount}` (in API currency)"
            else:
                response = f"⚠️ *Error*\n\n{balance}"
            
            self.bot.send_message(message.chat.id, response, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Error fetching balance: {e}")
            self.bot.send_message(message.chat.id, "❌ Failed to fetch main balance")
    
    def handle_allhistory(self, message):
        """Handle /allhistory command (superuser only)"""
        user_id = message.from_user.id
        lang = self.get_user_lang(user_id)
        
        if not self.is_superuser(user_id):
            text = get_text(lang, 'admin_only')
            self.bot.send_message(message.chat.id, text)
            return
        
        transactions = self.db.get_all_transactions(limit=20)
        
        if not transactions:
            self.bot.send_message(message.chat.id, "📭 No transactions yet.")
            return
        
        response = "📜 *All Transactions*\n\n"
        
        for trans in transactions:
            uid = trans.get('user_id')
            date = trans.get('timestamp', '')[:10]
            trans_type = "➕" if trans.get('type') == 'add' else "➖"
            amount = trans.get('amount', 0)
            description = trans.get('description', '')
            
            response += f"• User `{uid}`: {trans_type} ${amount:.2f} USD\n"
            response += f"  {date} - {description}\n\n"
        
        self.bot.send_message(message.chat.id, response, parse_mode='Markdown')
    
    def handle_callback(self, call):
        """Handle callback queries"""
        user_id = call.from_user.id
        lang = self.get_user_lang(user_id)
        
        try:
            # Language selection
            if call.data.startswith('lang_'):
                lang_code = call.data.split('_')[1]
                
                if lang_code in LANGUAGES:
                    self.db.set_language(user_id, lang_code)
                    text = get_text(lang_code, 'language_changed')
                    self.bot.answer_callback_query(call.id, text)
                    self.bot.edit_message_text(
                        text,
                        call.message.chat.id,
                        call.message.message_id
                    )
                    
                    # Log language change
                    lang_name = LANGUAGES[lang_code]['name']
                    self.log_to_channel(
                        f"🌐 **Language Changed**\n\n"
                        f"📝 **New Language:** {lang_name}",
                        user_id=user_id,
                        username=call.from_user.username
                    )
                    
                    # Show welcome message with keyboard
                    welcome_text = get_text(lang_code, 'welcome', admin=self.get_admin_contact())
                    
                    # Add Privacy Policy and Terms agreement
                    privacy_link = "https://rentry.co/SMS-ACTIVATE-BOBO"
                    if lang_code == 'en':
                        welcome_text += f"\n\n🚫 *Privacy Policy & Terms*\n\n"
                        welcome_text += f"By continuing to use this bot, you agree to our [Privacy Policy & Terms and Conditions]({privacy_link}).\n\n"
                        welcome_text += f"Please read them carefully before using the service."
                    elif lang_code == 'ru':
                        welcome_text += f"\n\n🚫 *Политика конфиденциальности и Условия*\n\n"
                        welcome_text += f"Продолжая использовать этого бота, вы соглашаетесь с нашей [Политикой конфиденциальности и Условиями использования]({privacy_link}).\n\n"
                        welcome_text += f"Пожалуйста, внимательно прочитайте их перед использованием сервиса."
                    else:  # uz
                        welcome_text += f"\n\n🚫 *Maxfiylik Siyosati va Foydalanish Shartlari*\n\n"
                        welcome_text += f"Ushbu botdan foydalanishni davom ettirish orqali siz bizning [Maxfiylik Siyosati va Foydalanish Shartlarimizga]({privacy_link}) rozilik bildirasiz.\n\n"
                        welcome_text += f"Iltimos, xizmatdan foydalanishdan oldin diqqat bilan o'qing."
                    
                    keyboard = get_admin_keyboard(lang_code) if self.is_superuser(user_id) else get_main_keyboard(lang_code)
                    
                    self.bot.send_message(
                        call.message.chat.id,
                        welcome_text,
                        parse_mode='Markdown',
                        reply_markup=keyboard
                    )
            
            # Buy method selection
            elif call.data == 'buy_country_first':
                self.bot.answer_callback_query(call.id)
                self.handle_buy_country_first(call)
            
            elif call.data == 'buy_service_first':
                self.bot.answer_callback_query(call.id)
                self.handle_buy_service_first(call)
            
            # Country selection
            elif call.data.startswith('country_'):
                if '_page_' in call.data:
                    # Pagination
                    page = int(call.data.split('_')[-1])
                    self.bot.answer_callback_query(call.id)
                    self.handle_buy_country_first(call, page)
                else:
                    # Country selected
                    country_id = call.data.split('_')[1]
                    self.bot.answer_callback_query(call.id)
                    self.handle_country_selected(call, country_id)
            
            # Service pagination (after country)
            elif call.data.startswith('service_page_') and call.data.count('_') == 3:
                # Format: service_page_{country_id}_{page}
                parts = call.data.split('_')
                country_id = parts[2]
                page = int(parts[3])
                self.bot.answer_callback_query(call.id)
                self.handle_country_selected_with_page(call, country_id, page)
            
            # Purchase confirmation
            elif call.data.startswith('confirm_purchase_'):
                parts = call.data.split('_')
                service_code = parts[2]
                country_id = parts[3]
                self.bot.answer_callback_query(call.id)
                self.handle_purchase(call, service_code, country_id, confirmed=True)
            
            # Service selection (after country) - show confirmation
            elif call.data.startswith('service_') and '_country_' in call.data:
                parts = call.data.split('_')
                service_code = parts[1]
                country_id = parts[3]
                self.bot.answer_callback_query(call.id)
                self.handle_purchase(call, service_code, country_id, confirmed=False)
            
            # Service selection (service first flow)
            elif call.data.startswith('svc_'):
                if '_page_' in call.data:
                    # Pagination
                    page = int(call.data.split('_')[-1])
                    self.bot.answer_callback_query(call.id)
                    self.handle_buy_service_first(call, page)
                else:
                    # Service selected
                    service_code = call.data.split('_')[1]
                    self.bot.answer_callback_query(call.id)
                    self.handle_service_selected(call, service_code)
            
            # Country pagination (after service)
            elif call.data.startswith('ctry_page_'):
                # Format: ctry_page_{service_code}_{page}
                parts = call.data.split('_')
                service_code = parts[2]
                page = int(parts[3])
                self.bot.answer_callback_query(call.id)
                self.handle_service_selected(call, service_code, page)
            
            # Country selection (after service) - show confirmation
            elif call.data.startswith('ctry_') and '_service_' in call.data:
                parts = call.data.split('_')
                country_id = parts[1]
                service_code = parts[3]
                self.bot.answer_callback_query(call.id)
                self.handle_purchase(call, service_code, country_id, confirmed=False)
            
            # View order details from My Orders
            elif call.data.startswith('order_view_'):
                activation_id = call.data.split('_')[2]
                self.bot.answer_callback_query(call.id)
                self.handle_order_view(call, activation_id)
            
            # Check order status
            elif call.data.startswith('check_'):
                activation_id = call.data.split('_')[1]
                self.bot.answer_callback_query(call.id)
                self.handle_check_callback(call, activation_id)
            
            # Cancel order
            elif call.data.startswith('cancel_'):
                activation_id = call.data.split('_')[1]
                self.bot.answer_callback_query(call.id)
                self.handle_cancel_callback(call, activation_id)
            
            # Back button
            elif call.data == 'buy_back':
                self.bot.answer_callback_query(call.id)
                text = "🛒 " + ("Choose how to buy:" if lang == 'en' else "Выберите способ покупки:" if lang == 'ru' else "Sotib olish usulini tanlang:")
                self.bot.edit_message_text(
                    text,
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=get_buy_method_keyboard(lang)
                )
            
            # Main menu
            elif call.data == 'main_menu':
                self.bot.answer_callback_query(call.id)
                self.bot.delete_message(call.message.chat.id, call.message.message_id)
                keyboard = get_admin_keyboard(lang) if self.is_superuser(user_id) else get_main_keyboard(lang)
                self.bot.send_message(
                    call.message.chat.id,
                    "🏠 " + ("Main Menu" if lang == 'en' else "Главное меню" if lang == 'ru' else "Asosiy menyu"),
                    reply_markup=keyboard
                )
                
        except Exception as e:
            logger.error(f"Callback error: {e}")
            self.bot.answer_callback_query(call.id, "Error occurred")
    
    def handle_buy_country_first(self, call, page=0):
        """Handle buying by choosing country first"""
        lang = self.get_user_lang(call.from_user.id)
        
        # Get countries if not cached
        if not self.cached_countries:
            try:
                self.cached_countries = self.api.get_countries()
            except Exception as e:
                logger.error(f"Error fetching countries: {e}")
                self.bot.send_message(call.message.chat.id, "❌ Error loading countries")
                return
        
        text = "🌍 " + ("Select Country:" if lang == 'en' else "Выберите страну:" if lang == 'ru' else "Davlatni tanlang:")
        
        keyboard = get_countries_keyboard(self.cached_countries, page, prefix="country")
        
        self.bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard
        )
    
    def handle_buy_service_first(self, call, page=0):
        """Handle buying by choosing service first"""
        lang = self.get_user_lang(call.from_user.id)
        
        # Get services if not cached
        if not self.cached_services:
            try:
                result = self.api.get_services_list(lang=lang)
                if result.get('status') == 'success':
                    self.cached_services = result.get('services', [])
            except Exception as e:
                logger.error(f"Error fetching services: {e}")
                self.bot.send_message(call.message.chat.id, "❌ Error loading services")
                return
        
        # Show approximate prices in menu
        def price_getter(price_type, service_code, country_id=None):
            if price_type == 'min':
                return self.get_service_min_price(service_code)
            elif price_type == 'exact' and country_id:
                return self.get_exact_price(service_code, country_id)
            return 0
        
        text = "📱 " + ("Select Service:" if lang == 'en' else "Выберите сервис:" if lang == 'ru' else "Xizmatni tanlang:")
        
        keyboard = get_services_keyboard(self.cached_services, page, prefix="svc", price_getter=price_getter)
        
        self.bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard
        )
    
    def handle_country_selected(self, call, country_id, page=0):
        """Handle when country is selected (show services for that country)"""
        lang = self.get_user_lang(call.from_user.id)
        
        # Get services if not cached
        if not self.cached_services:
            try:
                result = self.api.get_services_list(lang=lang)
                if result.get('status') == 'success':
                    self.cached_services = result.get('services', [])
            except Exception as e:
                logger.error(f"Error fetching services: {e}")
                self.bot.send_message(call.message.chat.id, "❌ Error loading services")
                return
        
        # Find country name
        country_name = f"Country {country_id}"
        if self.cached_countries:
            for key, data in self.cached_countries.items():
                if isinstance(data, dict) and str(data.get('id')) == str(country_id):
                    country_name = data.get('eng', country_name)
                    if lang == 'ru':
                        country_name = data.get('rus', country_name)
                    break
        
        # Show approximate prices in menu
        def price_getter(price_type, service_code, cid=None):
            if price_type == 'exact':
                return self.get_exact_price(service_code, country_id)
            return 0
        
        text = f"📱 " + ("Select Service for" if lang == 'en' else "Выберите сервис для" if lang == 'ru' else "Xizmatni tanlang") + f" {country_name}:"
        
        keyboard = get_services_keyboard(self.cached_services, page, prefix="service", country_id=country_id, price_getter=price_getter)
        
        self.bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard
        )
    
    def handle_country_selected_with_page(self, call, country_id, page):
        """Handle pagination for services after country selection"""
        self.handle_country_selected(call, country_id, page)
    
    def handle_service_selected(self, call, service_code, page=0):
        """Handle when service is selected (show countries for that service)"""
        lang = self.get_user_lang(call.from_user.id)
        
        # Store selected service in user state
        self.user_states[call.from_user.id] = {'service': service_code}
        
        # Get countries if not cached
        if not self.cached_countries:
            try:
                self.cached_countries = self.api.get_countries()
            except Exception as e:
                logger.error(f"Error fetching countries: {e}")
                self.bot.send_message(call.message.chat.id, "❌ Error loading countries")
                return
        
        # Find service name
        service_name = service_code
        if self.cached_services:
            for svc in self.cached_services:
                if svc.get('code') == service_code:
                    service_name = svc.get('name', service_code)
                    break
        
        text = f"🌍 " + ("Select Country for" if lang == 'en' else "Выберите страну для" if lang == 'ru' else "Davlatni tanlang") + f" {service_name}:"
        
        # Create keyboard with country selection and prices
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        # Filter visible countries
        countries = []
        for key, data in self.cached_countries.items():
            if isinstance(data, dict) and data.get('visible') == 1:
                countries.append({
                    'id': data.get('id'),
                    'name': data.get('eng' if lang == 'en' else 'rus' if lang == 'ru' else 'eng', 'Unknown'),
                    'key': key
                })
        
        # Sort and paginate
        countries.sort(key=lambda x: x['name'])
        
        # Pagination
        per_page = 10
        start = page * per_page
        end = start + per_page
        page_countries = countries[start:end]
        
        # Add country buttons with approximate prices
        for country in page_countries:
            button_text = f"🌍 {country['name']}"
            
            # Add approximate price for this service in this country
            price = self.get_exact_price(service_code, country['id'])
            if price > 0:
                button_text = f"{button_text} - ~${price:.2f}"
            
            callback_data = f"ctry_{country['id']}_service_{service_code}"
            markup.add(types.InlineKeyboardButton(button_text, callback_data=callback_data))
        
        # Navigation buttons
        nav_buttons = []
        if page > 0:
            nav_buttons.append(types.InlineKeyboardButton("⬅️ Previous", callback_data=f"ctry_page_{service_code}_{page-1}"))
        if end < len(countries):
            nav_buttons.append(types.InlineKeyboardButton("Next ➡️", callback_data=f"ctry_page_{service_code}_{page+1}"))
        
        if nav_buttons:
            markup.row(*nav_buttons)
        
        # Back button
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="buy_service_first"))
        
        self.bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )
    
    def handle_purchase(self, call, service_code, country_id, confirmed=False):
        """Handle actual purchase with confirmation"""
        user_id = call.from_user.id
        lang = self.get_user_lang(user_id)
        
        # Check user balance first
        user_balance = self.db.get_balance(user_id)
        
        # If not confirmed, show price and ask for confirmation
        if not confirmed:
            try:
                # First, get the price without actually buying
                # We'll do a quick price check from getPrices as estimate
                prices = self.get_prices_data()
                estimated_cost = 0
                
                if str(country_id) in prices:
                    services = prices[str(country_id)]
                    if isinstance(services, dict) and service_code in services:
                        service_data = services[service_code]
                        if isinstance(service_data, dict):
                            api_price = float(service_data.get('retail') or service_data.get('cost', 0))
                            estimated_cost = api_price * PRICE_MULTIPLIER
                
                # Find service and country names
                service_name = service_code
                if self.cached_services:
                    for svc in self.cached_services:
                        if svc.get('code') == service_code:
                            service_name = svc.get('name', service_code)
                            break
                
                country_name = f"Country {country_id}"
                if self.cached_countries:
                    for key, data in self.cached_countries.items():
                        if isinstance(data, dict) and str(data.get('id')) == str(country_id):
                            country_name = data.get('eng', country_name)
                            if lang == 'ru':
                                country_name = data.get('rus', country_name)
                            break
                
                # Show confirmation with estimated price
                if lang == 'en':
                    confirm_text = f"📱 **Purchase Confirmation**\n\n"
                    confirm_text += f"**Service:** {service_name}\n"
                    confirm_text += f"**Country:** {country_name}\n"
                    confirm_text += f"**Price:** ~${estimated_cost:.2f}\n\n"
                    confirm_text += f"⚠️ **Important:** Exact price determined at purchase\n"
                    confirm_text += f"_Final charge may be ±20% different_\n\n"
                    confirm_text += f"💰 Your balance: ${user_balance:.2f}\n\n"
                    confirm_text += "Continue with purchase?"
                elif lang == 'ru':
                    confirm_text = f"📱 **Подтверждение Покупки**\n\n"
                    confirm_text += f"**Сервис:** {service_name}\n"
                    confirm_text += f"**Страна:** {country_name}\n"
                    confirm_text += f"**Цена:** ~${estimated_cost:.2f}\n\n"
                    confirm_text += f"⚠️ **Важно:** Точная цена определяется при покупке\n"
                    confirm_text += f"_Итоговая сумма может отличаться на ±20%_\n\n"
                    confirm_text += f"💰 Ваш баланс: ${user_balance:.2f}\n\n"
                    confirm_text += "Продолжить покупку?"
                else:
                    confirm_text = f"📱 **Sotib Olishni Tasdiqlash**\n\n"
                    confirm_text += f"**Xizmat:** {service_name}\n"
                    confirm_text += f"**Davlat:** {country_name}\n"
                    confirm_text += f"**Narx:** ~${estimated_cost:.2f}\n\n"
                    confirm_text += f"⚠️ **Muhim:** Aniq narx xarid vaqtida aniqlanadi\n"
                    confirm_text += f"_Yakuniy summa ±20% farq qilishi mumkin_\n\n"
                    confirm_text += f"💰 Balansingiz: ${user_balance:.2f}\n\n"
                    confirm_text += "Xaridni davom ettirasizmi?"
                
                # Create confirmation buttons
                markup = types.InlineKeyboardMarkup(row_width=2)
                confirm_btn = types.InlineKeyboardButton(
                    "✅ " + ("Confirm" if lang == 'en' else "Подтвердить" if lang == 'ru' else "Tasdiqlash"),
                    callback_data=f"confirm_purchase_{service_code}_{country_id}"
                )
                cancel_btn = types.InlineKeyboardButton(
                    "❌ " + ("Cancel" if lang == 'en' else "Отмена" if lang == 'ru' else "Bekor qilish"),
                    callback_data="buy_back"
                )
                markup.row(confirm_btn, cancel_btn)
                
                self.bot.edit_message_text(
                    confirm_text,
                    call.message.chat.id,
                    call.message.message_id,
                    parse_mode='Markdown',
                    reply_markup=markup
                )
                return
                
            except Exception as e:
                logger.error(f"Error showing confirmation: {e}")
                # If confirmation fails, proceed to purchase anyway
                pass
        
        # Confirmed or confirmation failed - proceed with purchase
        # BUT FIRST: Check estimated balance to avoid wasting API calls
        try:
            # Get estimated price BEFORE calling API
            prices = self.get_prices_data()
            estimated_cost = 0
            
            if str(country_id) in prices:
                services = prices[str(country_id)]
                if isinstance(services, dict) and service_code in services:
                    service_data = services[service_code]
                    if isinstance(service_data, dict):
                        api_price = float(service_data.get('retail') or service_data.get('cost', 0))
                        estimated_cost = api_price * PRICE_MULTIPLIER
            
            # ANTI-ABUSE CHECK: Is user blocked?
            is_blocked, block_reason, failed_total = self.is_user_blocked(user_id, estimated_cost, user_balance)
            
            if is_blocked:
                # User is blocked due to too many failed purchases
                safety_amount = estimated_cost * SAFETY_BALANCE_MULTIPLIER
                time_remaining = FAILED_PURCHASE_BLOCK_TIME / 60  # minutes
                
                if lang == 'en':
                    text = f"🚫 **Temporarily Blocked**\n\n"
                    text += f"You have ${failed_total:.2f} in failed purchases in the last {time_remaining:.0f} minutes.\n\n"
                    text += f"To continue purchasing, you need:\n"
                    text += f"💰 **${safety_amount:.2f}** (2x the price)\n\n"
                    text += f"💳 Your current balance: ${user_balance:.2f}\n"
                    text += f"📉 You need ${safety_amount - user_balance:.2f} more\n\n"
                    text += f"⏰ Block will be lifted automatically in {time_remaining:.0f} minutes."
                elif lang == 'ru':
                    text = f"🚫 **Временная Блокировка**\n\n"
                    text += f"У вас ${failed_total:.2f} неудачных покупок за последние {time_remaining:.0f} минут.\n\n"
                    text += f"Чтобы продолжить, вам нужно:\n"
                    text += f"💰 **${safety_amount:.2f}** (2x от цены)\n\n"
                    text += f"💳 Ваш баланс: ${user_balance:.2f}\n"
                    text += f"📉 Нужно еще ${safety_amount - user_balance:.2f}\n\n"
                    text += f"⏰ Блокировка снимется автоматически через {time_remaining:.0f} минут."
                else:
                    text = f"🚫 **Vaqtincha Bloklangan**\n\n"
                    text += f"Sizda oxirgi {time_remaining:.0f} daqiqada ${failed_total:.2f} muvaffaqiyatsiz xaridlar.\n\n"
                    text += f"Davom etish uchun kerak:\n"
                    text += f"💰 **${safety_amount:.2f}** (narxdan 2x)\n\n"
                    text += f"💳 Sizning balansingiz: ${user_balance:.2f}\n"
                    text += f"📉 Yana ${safety_amount - user_balance:.2f} kerak\n\n"
                    text += f"⏰ Blok {time_remaining:.0f} daqiqadan keyin avtomatik ochiladi."
                
                self.bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
                
                # Log to channel
                self.log_to_channel(
                    f"🚫 **User Blocked - Anti-Abuse**\n\n"
                    f"💰 **Failed Total:** ${failed_total:.2f}\n"
                    f"🔷 **Attempted Service:** {service_code}\n"
                    f"💳 **User Balance:** ${user_balance:.2f}\n"
                    f"📉 **Required:** ${safety_amount:.2f}",
                    user_id=user_id,
                    username=call.from_user.username
                )
                return
            
            loading_text = "🔄 " + ("Processing..." if lang == 'en' else "Обработка..." if lang == 'ru' else "Qayta ishlanmoqda...")
            self.bot.edit_message_text(
                loading_text,
                call.message.chat.id,
                call.message.message_id
            )
            
            # NOW call API (only if user has estimated balance and not blocked)
            result = self.api.get_number_v2(service_code, country_id)
            
            if 'error' in result:
                error_msg = result['error']
                
                if 'NO_NUMBERS' in error_msg:
                    error_text = get_text(lang, 'buy_no_numbers')
                    
                    # Log to channel
                    self.log_to_channel(
                        f"⚠️ **Purchase Failed - No Numbers Available**\n\n"
                        f"🔷 **Service:** {service_code}\n"
                        f"🌍 **Country:** {country_id}\n"
                        f"📝 **Error:** No numbers available",
                        user_id=user_id,
                        username=call.from_user.username
                    )
                    
                elif 'NO_BALANCE' in error_msg:
                    # This means SMS-Activate API account is empty (admin's problem)
                    if lang == 'en':
                        error_text = "❌ Service temporarily unavailable\n\nPlease try again later or contact admin."
                    elif lang == 'ru':
                        error_text = "❌ Сервис временно недоступен\n\nПопробуйте позже или свяжитесь с админом."
                    else:
                        error_text = "❌ Xizmat vaqtincha mavjud emas\n\nKeyinroq urinib ko'ring yoki admin bilan bog'laning."
                    
                    # Log to channel
                    self.log_to_channel(
                        f"🚨 **Purchase Failed - API Balance Empty**\n\n"
                        f"🔷 **Service:** {service_code}\n"
                        f"🌍 **Country:** {country_id}\n"
                        f"📝 **Error:** Admin's SMS-Activate account has no balance!",
                        user_id=user_id,
                        username=call.from_user.username
                    )
                    
                    # Notify superuser
                    try:
                        admin_msg = f"⚠️ SMS-Activate API NO_BALANCE ERROR!\n\nUser {user_id} tried to buy {service_code} but your SMS-Activate account has insufficient balance.\n\nPlease top up your SMS-Activate account!"
                        self.bot.send_message(self.superuser_id, admin_msg)
                    except:
                        pass
                        
                elif 'BAD_SERVICE' in error_msg:
                    error_text = get_text(lang, 'buy_invalid_service')
                    
                    # Log to channel
                    self.log_to_channel(
                        f"⚠️ **Purchase Failed - Invalid Service**\n\n"
                        f"🔷 **Service:** {service_code}\n"
                        f"🌍 **Country:** {country_id}\n"
                        f"📝 **Error:** Bad service code",
                        user_id=user_id,
                        username=call.from_user.username
                    )
                    
                else:
                    error_text = error_msg
                    
                    # Log to channel
                    self.log_to_channel(
                        f"❌ **Purchase Failed - API Error**\n\n"
                        f"🔷 **Service:** {service_code}\n"
                        f"🌍 **Country:** {country_id}\n"
                        f"📝 **Error:** {error_msg}",
                        user_id=user_id,
                        username=call.from_user.username
                    )
                
                text = get_text(lang, 'buy_error', error=error_text)
                self.bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
                return
            
            # Extract data
            activation_id = result.get('activationId', 'N/A')
            phone_number = result.get('phoneNumber', 'N/A')
            api_cost = float(result.get('activationCost', 0))  # What we pay to API
            user_cost = api_cost * PRICE_MULTIPLIER  # What we charge user (2x profit)
            country_code = result.get('countryCode', 'N/A')
            
            # Check if user has enough balance (using marked up price)
            if user_balance < user_cost:
                # Show actual price in error message
                needed = user_cost - user_balance
                if lang == 'en':
                    text = f"❌ **Insufficient Balance**\n\n"
                    text += f"💰 **Actual Price:** ${user_cost:.2f}\n"
                    text += f"💳 **Your Balance:** ${user_balance:.2f}\n"
                    text += f"📉 **Needed:** ${needed:.2f}\n\n"
                    text += f"Please top up your balance with /deposit"
                elif lang == 'ru':
                    text = f"❌ **Недостаточно Средств**\n\n"
                    text += f"💰 **Фактическая цена:** ${user_cost:.2f}\n"
                    text += f"💳 **Ваш баланс:** ${user_balance:.2f}\n"
                    text += f"📉 **Требуется:** ${needed:.2f}\n\n"
                    text += f"Пожалуйста, пополните баланс через /deposit"
                else:
                    text = f"❌ **Balans Yetarli Emas**\n\n"
                    text += f"💰 **Haqiqiy narx:** ${user_cost:.2f}\n"
                    text += f"💳 **Sizning balansingiz:** ${user_balance:.2f}\n"
                    text += f"📉 **Kerak:** ${needed:.2f}\n\n"
                    text += f"Iltimos /deposit orqali balansni to'ldiring"
                
                self.bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
                
                # Track failed purchase for anti-abuse system
                self.track_failed_purchase(user_id, user_cost)
                
                # Log to channel
                failed_total = self.get_failed_purchases_total(user_id)
                self.log_to_channel(
                    f"⚠️ **Purchase Failed - Insufficient Balance**\n\n"
                    f"🆔 **Order ID:** `{activation_id}`\n"
                    f"📞 **Phone:** +{phone_number}\n"
                    f"🔷 **Service:** {service_code}\n"
                    f"🌍 **Country:** {country_code}\n"
                    f"💰 **Required:** ${user_cost:.2f}\n"
                    f"💳 **User Balance:** ${user_balance:.2f}\n"
                    f"📉 **Short:** ${needed:.2f}\n"
                    f"🚨 **Total Failed (20min):** ${failed_total:.2f}",
                    user_id=user_id,
                    username=call.from_user.username
                )
                
                # Add to failed orders for automatic cancellation every 3 minutes
                with self.failed_orders_lock:
                    self.failed_orders.append({
                        'activation_id': activation_id,
                        'timestamp': time.time(),
                        'user_id': user_id
                    })
                    logger.info(f"Added order {activation_id} to failed orders cleanup queue")
                
                # Try immediate cancel
                try:
                    self.api.set_status(activation_id, 8)
                except:
                    pass
                return
            
            # Deduct balance (charge user the marked up price)
            success = self.db.deduct_balance(
                user_id, 
                user_cost, 
                f"Order {activation_id}: {service_code} in country {country_code}"
            )
            
            if not success:
                text = get_text(lang, 'no_balance')
                self.bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
                
                # Add to failed orders for automatic cancellation every 3 minutes
                with self.failed_orders_lock:
                    self.failed_orders.append({
                        'activation_id': activation_id,
                        'timestamp': time.time(),
                        'user_id': user_id
                    })
                    logger.info(f"Added order {activation_id} to failed orders cleanup queue")
                
                # Try immediate cancel
                try:
                    self.api.set_status(activation_id, 8)
                except:
                    pass
                return
            
            # Save activation (store what user paid, not API cost)
            result['service'] = service_code
            result['activationCost'] = user_cost  # Override with user's price
            self.db.add_activation(user_id, result)
            
            # Send success message (show user their price, not API cost)
            text = get_text(
                lang, 
                'buy_success',
                order_id=activation_id,
                phone=phone_number,
                service=service_code,
                country=country_code,
                cost=user_cost
            )
            
            keyboard = get_confirmation_keyboard(lang, activation_id)
            
            self.bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='Markdown',
                reply_markup=keyboard
            )
            
            # Log to channel
            self.log_to_channel(
                f"✅ **Purchase Successful**\n\n"
                f"📞 **Phone:** +{phone_number}\n"
                f"🆔 **Order ID:** `{activation_id}`\n"
                f"🔷 **Service:** {service_code}\n"
                f"🌍 **Country:** {country_code}\n"
                f"💰 **Cost:** ${user_cost:.2f} USD",
                user_id=user_id,
                username=call.from_user.username
            )
            
        except Exception as e:
            logger.error(f"Error buying number: {e}")
            
            # Log to channel
            self.log_to_channel(
                f"❌ **Purchase Failed - Exception**\n\n"
                f"🔷 **Service:** {service_code}\n"
                f"🌍 **Country:** {country_id}\n"
                f"📝 **Error:** {str(e)}",
                user_id=user_id,
                username=call.from_user.username
            )
            
            text = get_text(lang, 'error_occurred')
            self.bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    
    def handle_check_callback(self, call, activation_id):
        """Handle check status callback"""
        user_id = call.from_user.id
        lang = self.get_user_lang(user_id)
        
        # Get original message text to preserve order info
        original_text = call.message.text or call.message.caption or ""
        
        try:
            status_result = self.api.get_status_v2(activation_id)
            
            if 'error' in status_result:
                error_msg = status_result['error']
                
                if 'STATUS_CANCEL' in error_msg:
                    text = get_text(lang, 'check_cancelled')
                elif 'NO_ACTIVATION' in error_msg:
                    text = get_text(lang, 'check_not_found')
                else:
                    text = f"⚠️ {error_msg}"
                
                # Keep original order info
                if "Order ID:" in original_text or "ID Заказа:" in original_text or "Buyurtma ID:" in original_text:
                    text = original_text.split("⏳")[0] + "\n\n" + text
                
                self.bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
                return
            
            # Parse status
            verification_type = status_result.get('verificationType', 0)
            
            if verification_type == 0:
                sms_data = status_result.get('sms', {})
                if sms_data and sms_data.get('code'):
                    code = sms_data.get('code', 'N/A')
                    text = sms_data.get('text', 'N/A')
                    date_time = sms_data.get('dateTime', 'N/A')
                    
                    response = get_text(
                        lang,
                        'check_success',
                        order_id=activation_id,
                        code=code,
                        text=text,
                        time=date_time
                    )
                    
                    # Preserve original order details
                    if "Phone Number:" in original_text or "Телефон:" in original_text or "Telefon:" in original_text:
                        order_details = original_text.split("⏳")[0]
                        response = order_details + "\n\n✅ *SMS Received!*\n\n" + f"*Code:* `{code}`\n*Text:* {text}\n*Time:* {date_time}"
                    
                    self.bot.edit_message_text(
                        response,
                        call.message.chat.id,
                        call.message.message_id,
                        parse_mode='Markdown'
                    )
                    
                    # Log to channel
                    self.log_to_channel(
                        f"📨 **SMS Received**\n\n"
                        f"🆔 **Order ID:** `{activation_id}`\n"
                        f"🔢 **Code:** `{code}`\n"
                        f"📝 **Text:** {text}\n"
                        f"🕐 **Time:** {date_time}",
                        user_id=user_id,
                        username=call.from_user.username
                    )
                else:
                    # Still waiting - preserve original order info
                    if "Order ID:" in original_text or "ID Заказа:" in original_text or "Buyurtma ID:" in original_text:
                        order_info = original_text.split("⏳")[0]
                        waiting_msg = "\n⏳ *" + ("Waiting for SMS..." if lang == 'en' else "Ожидание SMS..." if lang == 'ru' else "SMS kutilmoqda...") + "*\n\n"
                        last_check = "🔄 " + ("Last checked:" if lang == 'en' else "Последняя проверка:" if lang == 'ru' else "Oxirgi tekshiruv:") + f" {datetime.now().strftime('%H:%M:%S')}"
                        response = order_info + waiting_msg + last_check
                    else:
                        response = get_text(lang, 'check_waiting', order_id=activation_id)
                    
                    keyboard = get_order_action_keyboard(lang, activation_id)
                    
                    self.bot.edit_message_text(
                        response,
                        call.message.chat.id,
                        call.message.message_id,
                        parse_mode='Markdown',
                        reply_markup=keyboard
                    )
            else:
                # Voice/call verification - preserve order info
                if "Order ID:" in original_text or "ID Заказа:" in original_text or "Buyurtma ID:" in original_text:
                    order_info = original_text.split("⏳")[0]
                    waiting_msg = "\n⏳ *" + ("Waiting for verification..." if lang == 'en' else "Ожидание верификации..." if lang == 'ru' else "Tasdiqlash kutilmoqda...") + "*\n\n"
                    last_check = "🔄 " + ("Last checked:" if lang == 'en' else "Последняя проверка:" if lang == 'ru' else "Oxirgi tekshiruv:") + f" {datetime.now().strftime('%H:%M:%S')}"
                    response = order_info + waiting_msg + last_check
                else:
                    response = get_text(lang, 'check_waiting', order_id=activation_id)
                
                keyboard = get_order_action_keyboard(lang, activation_id)
                
                self.bot.edit_message_text(
                    response,
                    call.message.chat.id,
                    call.message.message_id,
                    parse_mode='Markdown',
                    reply_markup=keyboard
                )
            
        except Exception as e:
            logger.error(f"Error checking status: {e}")
            # Preserve order info even on error
            error_text = get_text(lang, 'error_occurred')
            if "Order ID:" in original_text or "ID Заказа:" in original_text or "Buyurtma ID:" in original_text:
                error_text = original_text.split("⏳")[0] + "\n\n" + error_text
                keyboard = get_order_action_keyboard(lang, activation_id)
                self.bot.edit_message_text(error_text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=keyboard)
            else:
                self.bot.edit_message_text(error_text, call.message.chat.id, call.message.message_id)
    
    def handle_cancel_callback(self, call, activation_id):
        """Handle cancel order callback"""
        user_id = call.from_user.id
        lang = self.get_user_lang(user_id)
        
        # Get original message text to preserve order info
        original_text = call.message.text or call.message.caption or ""
        
        try:
            result = self.api.set_status(activation_id, 8)
            
            if 'ACCESS_CANCEL' in result:
                # Find the activation and refund (refund what user paid)
                refund_amount = 0
                phone_number = ""
                service_code = ""
                for activation in self.db.get_user_activations(user_id):
                    if str(activation.get('activation_id')) == str(activation_id):
                        user_paid = float(activation.get('cost', 0))
                        refund_amount = user_paid
                        phone_number = activation.get('phone_number', '')
                        service_code = activation.get('service', '')
                        self.db.add_balance(user_id, user_paid, f"Refund for order {activation_id}")
                        self.db.update_activation(activation_id, status='cancelled')
                        break
                
                text = get_text(lang, 'cancel_success')
                # Add order info for reference
                if "Order ID:" in original_text or "ID Заказа:" in original_text or "Buyurtma ID:" in original_text:
                    order_info = original_text.split("⏳")[0]
                    text = order_info + "\n\n✅ " + text
                
                # Log to channel
                self.log_to_channel(
                    f"❌ **Order Cancelled**\n\n"
                    f"🆔 **Order ID:** `{activation_id}`\n"
                    f"📞 **Phone:** +{phone_number}\n"
                    f"🔷 **Service:** {service_code}\n"
                    f"💰 **Refunded:** ${refund_amount:.2f} USD",
                    user_id=user_id,
                    username=call.from_user.username
                )
                
            elif 'EARLY_CANCEL_DENIED' in result:
                # IMPORTANT: Keep order details when early cancel is denied
                if "Order ID:" in original_text or "ID Заказа:" in original_text or "Buyurtma ID:" in original_text:
                    order_info = original_text.split("⏳")[0]
                    error_msg = "\n\n⚠️ *" + ("Cannot cancel within first 2 minutes" if lang == 'en' else "Нельзя отменить в первые 2 минуты" if lang == 'ru' else "Dastlabki 2 daqiqada bekor qilib bo'lmaydi") + "*\n\n"
                    wait_msg = "⏳ " + ("Please wait and try again, or check for SMS" if lang == 'en' else "Подождите и попробуйте снова, или проверьте SMS" if lang == 'ru' else "Kuting va qayta urinib ko'ring, yoki SMS ni tekshiring")
                    text = order_info + error_msg + wait_msg
                    keyboard = get_order_action_keyboard(lang, activation_id)
                    self.bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=keyboard)
                    return
                else:
                    text = get_text(lang, 'cancel_early')
                    
            elif 'NO_ACTIVATION' in result:
                text = get_text(lang, 'check_not_found')
            else:
                text = get_text(lang, 'cancel_failed', error=result)
                # Keep order info on other errors too
                if "Order ID:" in original_text or "ID Заказа:" in original_text or "Buyurtma ID:" in original_text:
                    order_info = original_text.split("⏳")[0]
                    text = order_info + "\n\n" + text
                    keyboard = get_order_action_keyboard(lang, activation_id)
                    self.bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=keyboard)
                    return
            
            self.bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error canceling: {e}")
            error_text = get_text(lang, 'error_occurred')
            # Preserve order info on error
            if "Order ID:" in original_text or "ID Заказа:" in original_text or "Buyurtma ID:" in original_text:
                order_info = original_text.split("⏳")[0]
                error_text = order_info + "\n\n" + error_text
                keyboard = get_order_action_keyboard(lang, activation_id)
                self.bot.edit_message_text(error_text, call.message.chat.id, call.message.message_id, parse_mode='Markdown', reply_markup=keyboard)
            else:
                self.bot.edit_message_text(error_text, call.message.chat.id, call.message.message_id)
    
    def run(self):
        """Start the bot"""
        logger.info("Starting SMS-Activate Bot...")
        logger.info(f"Superuser ID: {self.superuser_id}")
        try:
            self.bot.infinity_polling()
        except Exception as e:
            logger.error(f"Bot crashed: {e}")


def main():
    """Main function"""
    # Try to import config
    try:
        import config
        config.validate_config()
        BOT_TOKEN = config.TELEGRAM_BOT_TOKEN
        SMS_ACTIVATE_API_KEY = config.SMS_ACTIVATE_API_KEY
    except ImportError:
        # Fallback to environment variables
        BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
        SMS_ACTIVATE_API_KEY = os.getenv('SMS_ACTIVATE_API_KEY')
        
        if not BOT_TOKEN or not SMS_ACTIVATE_API_KEY:
            print("\n❌ Error: Missing configuration")
            print("\nPlease set environment variables or create .env file:")
            print("  - TELEGRAM_BOT_TOKEN")
            print("  - SMS_ACTIVATE_API_KEY")
            return
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print(f"\n❌ {e}")
        return
    
    # Check superuser ID
    if SUPERUSER_ID == 0:
        print("\n⚠️  WARNING: SUPERUSER_ID is not set!")
        print("Please edit bot.py and set your Telegram user ID")
        print("You can get your ID by messaging @userinfobot on Telegram")
        print("\nBot will start but superuser commands will not work.")
        print()
    
    # Create and run bot
    bot = SMSActivateBot(BOT_TOKEN, SMS_ACTIVATE_API_KEY, SUPERUSER_ID)
    bot.run()


if __name__ == '__main__':
    main()
