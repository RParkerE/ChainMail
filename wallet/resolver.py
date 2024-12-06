import sqlite3
from typing import Optional

class WalletResolver:
    def __init__(self, db_path: str = "wallets.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS wallet_mappings
            (wallet_address TEXT PRIMARY KEY, public_key BLOB)
        ''')
        conn.commit()
        conn.close()

    def register_wallet(self, wallet_address: str, public_key: bytes):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO wallet_mappings VALUES (?, ?)',
                 (wallet_address, public_key))
        conn.commit()
        conn.close()

    def get_public_key(self, wallet_address: str) -> Optional[bytes]:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT public_key FROM wallet_mappings WHERE wallet_address = ?',
                 (wallet_address,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None