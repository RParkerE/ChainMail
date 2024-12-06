import json
import os
from typing import Optional
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

class Wallet:
    def __init__(self, private_key: Optional[rsa.RSAPrivateKey] = None):
        if private_key is None:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
        self.private_key = private_key
        self.public_key = private_key.public_key()
        self.address = self._generate_address()

    def _generate_address(self) -> str:
        """Generate a deterministic wallet address from the public key."""
        public_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(public_bytes)
        hash_bytes = digest.finalize()
        return base64.b32encode(hash_bytes).decode('utf-8')[:40]

    def export_private_key(self) -> str:
        """Export the private key in PEM format."""
        private_bytes = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        return private_bytes.decode('utf-8')

    def export_public_key(self) -> str:
        """Export the public key in PEM format."""
        public_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return public_bytes.decode('utf-8')

class WalletManager:
    def __init__(self):
        self.data_dir = self._get_data_dir()
        self.wallets_dir = os.path.join(self.data_dir, 'wallets')
        os.makedirs(self.wallets_dir, exist_ok=True)
        self.current_wallet: Optional[Wallet] = None

    def _get_data_dir(self) -> str:
        """Get or create the data directory for the application."""
        data_dir = os.path.join(os.path.expanduser('~'), '.chainmail')
        os.makedirs(data_dir, exist_ok=True)
        return data_dir

    def _get_wallet_path(self, address: str) -> str:
        """Get the path to a wallet file."""
        return os.path.join(self.wallets_dir, f"{address}.json")

    def create_wallet(self) -> Wallet:
        """Create a new wallet and save it."""
        self.current_wallet = Wallet()
        self.save_wallet(self.current_wallet.address)
        print(f"Created new wallet with address: {self.current_wallet.address}")
        return self.current_wallet

    def load_wallet(self, address: str) -> Optional[Wallet]:
        """Load wallet from file if it exists."""
        try:
            wallet_path = self._get_wallet_path(address)
            if os.path.exists(wallet_path):
                with open(wallet_path, 'r') as f:
                    wallet_data = json.load(f)
                    private_key_pem = wallet_data.get('private_key')
                    if private_key_pem:
                        private_key = serialization.load_pem_private_key(
                            private_key_pem.encode('utf-8'),
                            password=None,
                            backend=default_backend()
                        )
                        self.current_wallet = Wallet(private_key)
                        if self.current_wallet.address == address:
                            print(f"Loaded wallet with address: {self.current_wallet.address}")
                            return self.current_wallet
                        else:
                            print(f"Wallet address mismatch: expected {address}, got {self.current_wallet.address}")
            print(f"No wallet file found for address: {address}")
            return None
        except Exception as e:
            print(f"Error loading wallet: {e}")
            return None

    def save_wallet(self, address: str):
        """Save current wallet to file."""
        if self.current_wallet:
            wallet_data = {
                'private_key': self.current_wallet.export_private_key(),
                'public_key': self.current_wallet.export_public_key(),
                'address': self.current_wallet.address
            }
            try:
                wallet_path = self._get_wallet_path(address)
                with open(wallet_path, 'w') as f:
                    json.dump(wallet_data, f, indent=4)
                print(f"Saved wallet to: {wallet_path}")
            except Exception as e:
                print(f"Error saving wallet: {e}")

    def clear_current_wallet(self):
        """Clear the current wallet from memory."""
        self.current_wallet = None

    def get_current_wallet(self) -> Optional[Wallet]:
        """Get the currently loaded wallet."""
        return self.current_wallet

    def get_wallet_address(self) -> str:
        """Get the current wallet's address."""
        if self.current_wallet:
            return self.current_wallet.address
        return ""