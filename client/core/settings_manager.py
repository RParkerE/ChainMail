import json
import os
from typing import Dict
import hashlib
import base64

class SettingsManager:
    def __init__(self, settings_file: str = "settings.json"):
        self.data_dir = os.path.join(os.path.expanduser('~'), '.chainmail')
        os.makedirs(self.data_dir, exist_ok=True)
        self.settings_file = os.path.join(self.data_dir, settings_file)
        self.credentials_file = os.path.join(self.data_dir, 'credentials.json')
        self.default_settings = {
            'wallet_address': '',
            'node_address': 'localhost',
            'node_port': 8000,
            'auto_sync': True,
            'sync_interval': 5,
            'encryption_enabled': True
        }

    def load_settings(self) -> Dict:
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    return {**self.default_settings, **settings}
            return self.default_settings
        except Exception as e:
            print(f"Error loading settings: {e}")
            return self.default_settings

    def save_settings(self, settings: Dict):
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def _hash_password(self, password: str) -> str:
        """Hash a password for storing."""
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        return base64.b64encode(salt + key).decode('utf-8')

    def _verify_password(self, stored_password: str, provided_password: str) -> bool:
        """Verify a stored password against a provided password."""
        try:
            decoded = base64.b64decode(stored_password.encode('utf-8'))
            salt = decoded[:32]
            stored_key = decoded[32:]
            new_key = hashlib.pbkdf2_hmac(
                'sha256',
                provided_password.encode('utf-8'),
                salt,
                100000
            )
            return stored_key == new_key
        except Exception:
            return False

    def save_credentials(self, wallet_address: str, password: str):
        """Save credentials for a wallet."""
        try:
            credentials = {}
            if os.path.exists(self.credentials_file):
                with open(self.credentials_file, 'r') as f:
                    credentials = json.load(f)
            
            credentials[wallet_address] = self._hash_password(password)
            
            with open(self.credentials_file, 'w') as f:
                json.dump(credentials, f, indent=4)
        except Exception as e:
            print(f"Error saving credentials: {e}")

    def verify_credentials(self, wallet_address: str, password: str) -> bool:
        """Verify login credentials."""
        try:
            if os.path.exists(self.credentials_file):
                with open(self.credentials_file, 'r') as f:
                    credentials = json.load(f)
                    stored_password = credentials.get(wallet_address)
                    if stored_password:
                        return self._verify_password(stored_password, password)
        except Exception as e:
            print(f"Error verifying credentials: {e}")
        return False 