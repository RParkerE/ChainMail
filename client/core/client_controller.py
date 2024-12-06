from typing import List, Dict
import json
import asyncio
from datetime import datetime
from client.core.wallet_manager import WalletManager
from client.core.email_manager import EmailManager
from client.core.settings_manager import SettingsManager
from PyQt6.QtCore import QObject, pyqtSignal

class ClientController(QObject):
    email_status_changed = pyqtSignal(bool, str)  # Success status and message

    def __init__(self):
        super().__init__()
        self.wallet_manager = WalletManager()
        self.email_manager = EmailManager()
        self.settings_manager = SettingsManager()
        
        # Connect email manager signals
        self.email_manager.email_sent.connect(self._handle_email_sent)
        
        self.load_settings()
        self.current_user = None

    def load_settings(self):
        self.settings = self.settings_manager.load_settings()
        if not self.settings.get('wallet_address'):
            self.create_new_wallet()

    def create_new_wallet(self):
        wallet = self.wallet_manager.create_wallet()
        self.settings['wallet_address'] = wallet.address
        self.settings_manager.save_settings(self.settings)

    def get_emails(self, folder: str) -> List[Dict]:
        return self.email_manager.get_emails(folder)

    def send_email(self, email_data: Dict):
        """Send an email through the email manager."""
        try:
            self.email_manager.send_email(
                from_address=self.settings['wallet_address'],
                to_address=email_data['to'],
                subject=email_data['subject'],
                content=email_data['content']
            )
        except Exception as e:
            self.email_status_changed.emit(False, f"Failed to send email: {str(e)}")

    def _handle_email_sent(self, success: bool, message: str):
        """Handle email sent signal from email manager."""
        self.email_status_changed.emit(success, message)

    def save_draft(self, email_data: Dict):
        self.email_manager.save_draft(email_data)

    def get_wallet_address(self) -> str:
        return self.settings.get('wallet_address', '')

    def update_settings(self, new_settings: Dict):
        self.settings.update(new_settings)
        self.settings_manager.save_settings(self.settings)

    def has_wallet(self) -> bool:
        """Check if a wallet exists."""
        return self.wallet_manager.get_current_wallet() is not None

    def import_wallet(self, file_path: str):
        """Import a wallet from a file."""
        try:
            # Copy wallet file to application wallet location
            import shutil
            shutil.copy2(file_path, self.wallet_manager.wallet_file)
            # Load the wallet
            self.wallet_manager.load_wallet()
            # Update settings with new wallet address
            self.settings['wallet_address'] = self.wallet_manager.get_wallet_address()
            self.settings_manager.save_settings(self.settings)
        except Exception as e:
            raise Exception(f"Failed to import wallet: {str(e)}")

    def create_account(self, password: str) -> str:
        """Create a new account with wallet."""
        # Create wallet without password first
        wallet = self.wallet_manager.create_wallet()
        # Save credentials separately
        self.settings_manager.save_credentials(wallet.address, password)
        # Update settings
        self.settings['wallet_address'] = wallet.address
        self.settings_manager.save_settings(self.settings)
        return wallet.address

    def login(self, wallet_address: str, password: str) -> bool:
        """Login with wallet address and password."""
        if self.settings_manager.verify_credentials(wallet_address, password):
            self.current_user = wallet_address
            if self.wallet_manager.load_wallet(wallet_address):
                self.email_manager.load_emails(wallet_address)
                return True
        return False

    def logout(self):
        """Logout current user."""
        self.current_user = None
        self.wallet_manager.clear_current_wallet()
        self.email_manager.clear_emails()

    def is_logged_in(self) -> bool:
        """Check if a user is currently logged in."""
        return self.current_user is not None
  