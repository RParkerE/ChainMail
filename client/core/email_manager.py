import json
import os
import asyncio
from typing import List, Dict
from datetime import datetime
from PyQt6.QtCore import QObject, pyqtSignal, QTimer

class EmailManager(QObject):
    email_sent = pyqtSignal(bool, str)
    emails_updated = pyqtSignal()

    def __init__(self, blockchain=None):
        super().__init__()
        self.data_dir = self._get_data_dir()
        self.emails = {}
        self.blockchain = blockchain
        self.loop = None
        self.current_wallet_address = None
        
        # Setup periodic email checking
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.check_new_emails)
        self.check_timer.setInterval(5000)  # Check every 5 seconds

    def _get_data_dir(self) -> str:
        """Get or create the data directory for the application."""
        data_dir = os.path.join(os.path.expanduser('~'), '.chainmail')
        os.makedirs(data_dir, exist_ok=True)
        return data_dir

    def _get_emails_path(self, wallet_address: str) -> str:
        """Get the path to a user's emails file."""
        return os.path.join(self.data_dir, f'emails_{wallet_address}.json')

    def _get_pending_path(self, to_address: str) -> str:
        """Get the path to pending emails for a wallet."""
        pending_dir = os.path.join(self.data_dir, 'pending')
        os.makedirs(pending_dir, exist_ok=True)
        return os.path.join(pending_dir, f'pending_{to_address}.json')

    def load_emails(self, wallet_address: str):
        """Load emails for a specific wallet address."""
        self.current_wallet_address = wallet_address
        emails_path = self._get_emails_path(wallet_address)
        try:
            if os.path.exists(emails_path):
                with open(emails_path, 'r') as f:
                    self.emails = json.load(f)
            else:
                self.emails = {
                    'inbox': [],
                    'sent': [],
                    'drafts': [],
                    'archive': [],
                    'spam': [],
                    'trash': []
                }
                self._save_emails()
            
            # Start checking for new emails
            self.check_timer.start()
            self.check_new_emails()  # Check immediately
            self.emails_updated.emit()
        except Exception as e:
            print(f"Error loading emails: {e}")
            self.emails = {
                'inbox': [],
                'sent': [],
                'drafts': [],
                'archive': [],
                'spam': [],
                'trash': []
            }

    def check_new_emails(self):
        """Check for new pending emails."""
        if not self.current_wallet_address:
            return

        pending_path = self._get_pending_path(self.current_wallet_address)
        if os.path.exists(pending_path):
            try:
                with open(pending_path, 'r') as f:
                    pending_emails = json.load(f)
                
                # Add pending emails to inbox
                self.emails['inbox'].extend(pending_emails)
                self._save_emails()
                
                # Clear pending emails
                os.remove(pending_path)
                
                # Notify UI of new emails
                self.emails_updated.emit()
            except Exception as e:
                print(f"Error processing pending emails: {e}")

    def send_email(self, from_address: str, to_address: str, subject: str, content: str):
        """Send an email and save to sent folder."""
        email_data = {
            'from': from_address,
            'to': to_address,
            'subject': subject,
            'content': content,
            'date': datetime.now().isoformat(),
            'read': False
        }
        
        # Add to sent folder
        self.emails['sent'].append(email_data)
        self._save_emails()

        # Save to recipient's pending folder
        self._save_pending_email(to_address, email_data)

        # Simulate blockchain operation
        try:
            self.email_sent.emit(True, "Email sent successfully")
        except Exception as e:
            self.email_sent.emit(False, f"Failed to send email: {str(e)}")

    def _save_pending_email(self, to_address: str, email_data: Dict):
        """Save email to recipient's pending folder."""
        pending_path = self._get_pending_path(to_address)
        try:
            # Load existing pending emails
            pending_emails = []
            if os.path.exists(pending_path):
                with open(pending_path, 'r') as f:
                    pending_emails = json.load(f)
            
            # Add new email
            pending_emails.append(email_data)
            
            # Save updated pending emails
            with open(pending_path, 'w') as f:
                json.dump(pending_emails, f, indent=4)
        except Exception as e:
            print(f"Error saving pending email: {e}")

    def clear_emails(self):
        """Clear loaded emails from memory and stop checking."""
        self.check_timer.stop()
        self.emails = {}
        self.current_wallet_address = None

    def _save_emails(self):
        """Save emails to file."""
        if self.current_wallet_address:
            try:
                emails_path = self._get_emails_path(self.current_wallet_address)
                with open(emails_path, 'w') as f:
                    json.dump(self.emails, f, indent=4)
            except Exception as e:
                print(f"Error saving emails: {e}")

    def get_emails(self, folder: str) -> List[Dict]:
        """Get emails from a specific folder."""
        return self.emails.get(folder.lower(), [])

    async def _send_email_blockchain(self, email_data: Dict):
        """Send email through blockchain (placeholder)."""
        # TODO: Implement actual blockchain communication
        await asyncio.sleep(1)  # Simulate blockchain operation
        if self.blockchain:
            # Here we would actually send the email through the blockchain
            pass

    def save_draft(self, email_data: Dict):
        """Save email as draft."""
        email_data['date'] = datetime.now().isoformat()
        self.emails['drafts'].append(email_data)
        self._save_emails() 