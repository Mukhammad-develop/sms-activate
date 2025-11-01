"""
Database module for user management and transactions
"""

import json
import os
from datetime import datetime
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)


class Database:
    """Simple JSON-based database for user data"""
    
    def __init__(self, db_file: str = 'users.json'):
        self.db_file = db_file
        self.data = self._load()
    
    def _load(self) -> Dict:
        """Load database from file"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading database: {e}")
                return self._default_structure()
        return self._default_structure()
    
    def _default_structure(self) -> Dict:
        """Default database structure"""
        return {
            'users': {},
            'transactions': [],
            'activations': []
        }
    
    def _save(self):
        """Save database to file"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving database: {e}")
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        return self.data['users'].get(str(user_id))
    
    def create_user(self, user_id: int, username: str = None, first_name: str = None) -> Dict:
        """Create a new user"""
        user_data = {
            'user_id': user_id,
            'username': username,
            'first_name': first_name,
            'balance': 0.0,
            'language': 'en',
            'created_at': datetime.now().isoformat(),
            'total_spent': 0.0,
            'total_activations': 0
        }
        self.data['users'][str(user_id)] = user_data
        self._save()
        logger.info(f"Created new user: {user_id}")
        return user_data
    
    def update_user(self, user_id: int, **kwargs):
        """Update user data"""
        user_key = str(user_id)
        if user_key in self.data['users']:
            self.data['users'][user_key].update(kwargs)
            self._save()
    
    def get_or_create_user(self, user_id: int, username: str = None, first_name: str = None) -> Dict:
        """Get existing user or create new one"""
        user = self.get_user(user_id)
        if not user:
            user = self.create_user(user_id, username, first_name)
        return user
    
    def set_language(self, user_id: int, language: str):
        """Set user language"""
        self.update_user(user_id, language=language)
    
    def get_language(self, user_id: int) -> str:
        """Get user language"""
        user = self.get_user(user_id)
        return user.get('language', 'en') if user else 'en'
    
    def get_balance(self, user_id: int) -> float:
        """Get user balance"""
        user = self.get_user(user_id)
        return user.get('balance', 0.0) if user else 0.0
    
    def add_balance(self, user_id: int, amount: float, description: str = ""):
        """Add balance to user"""
        user = self.get_user(user_id)
        if user:
            new_balance = user.get('balance', 0.0) + amount
            self.update_user(user_id, balance=new_balance)
            
            # Add transaction
            self.add_transaction(user_id, amount, 'add', description)
            logger.info(f"Added {amount} to user {user_id}. New balance: {new_balance}")
    
    def deduct_balance(self, user_id: int, amount: float, description: str = "") -> bool:
        """Deduct balance from user. Returns True if successful."""
        user = self.get_user(user_id)
        if user:
            current_balance = user.get('balance', 0.0)
            if current_balance >= amount:
                new_balance = current_balance - amount
                total_spent = user.get('total_spent', 0.0) + amount
                self.update_user(user_id, balance=new_balance, total_spent=total_spent)
                
                # Add transaction
                self.add_transaction(user_id, amount, 'deduct', description)
                logger.info(f"Deducted {amount} from user {user_id}. New balance: {new_balance}")
                return True
        return False
    
    def add_transaction(self, user_id: int, amount: float, type: str, description: str = ""):
        """Add transaction record"""
        transaction = {
            'user_id': user_id,
            'amount': amount,
            'type': type,
            'description': description,
            'timestamp': datetime.now().isoformat()
        }
        self.data['transactions'].append(transaction)
        self._save()
    
    def get_user_transactions(self, user_id: int, limit: int = 50) -> List[Dict]:
        """Get user transactions"""
        transactions = [t for t in self.data['transactions'] if t['user_id'] == user_id]
        return sorted(transactions, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def add_activation(self, user_id: int, activation_data: Dict):
        """Add activation record"""
        activation = {
            'user_id': user_id,
            'activation_id': activation_data.get('activationId'),
            'phone_number': activation_data.get('phoneNumber'),
            'service': activation_data.get('service'),
            'country': activation_data.get('countryCode'),
            'cost': activation_data.get('activationCost'),
            'status': 'active',
            'created_at': datetime.now().isoformat()
        }
        self.data['activations'].append(activation)
        
        # Update user stats
        user = self.get_user(user_id)
        if user:
            total = user.get('total_activations', 0) + 1
            self.update_user(user_id, total_activations=total)
        
        self._save()
    
    def update_activation(self, activation_id: str, **kwargs):
        """Update activation record"""
        for activation in self.data['activations']:
            if str(activation.get('activation_id')) == str(activation_id):
                activation.update(kwargs)
                self._save()
                break
    
    def get_user_activations(self, user_id: int, limit: int = 50) -> List[Dict]:
        """Get user activations"""
        activations = [a for a in self.data['activations'] if a['user_id'] == user_id]
        return sorted(activations, key=lambda x: x['created_at'], reverse=True)[:limit]
    
    def get_all_users(self) -> List[Dict]:
        """Get all users"""
        return list(self.data['users'].values())
    
    def get_all_transactions(self, limit: int = 100) -> List[Dict]:
        """Get all transactions"""
        return sorted(self.data['transactions'], key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def get_all_activations(self, limit: int = 100) -> List[Dict]:
        """Get all activations"""
        return sorted(self.data['activations'], key=lambda x: x['created_at'], reverse=True)[:limit]
    
    def get_statistics(self) -> Dict:
        """Get overall statistics"""
        users = self.get_all_users()
        transactions = self.data['transactions']
        activations = self.data['activations']
        
        total_users = len(users)
        total_balance = sum(u.get('balance', 0) for u in users)
        total_spent = sum(u.get('total_spent', 0) for u in users)
        total_activations = len(activations)
        
        # Recent activity
        today = datetime.now().date()
        today_transactions = [t for t in transactions 
                            if datetime.fromisoformat(t['timestamp']).date() == today]
        today_activations = [a for a in activations 
                           if datetime.fromisoformat(a['created_at']).date() == today]
        
        return {
            'total_users': total_users,
            'total_balance': total_balance,
            'total_spent': total_spent,
            'total_activations': total_activations,
            'today_transactions': len(today_transactions),
            'today_activations': len(today_activations)
        }

