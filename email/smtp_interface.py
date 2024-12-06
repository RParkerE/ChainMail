import asyncio
import email
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import SMTP

class EmailBlockchainSMTP(SMTP):
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        if not self.is_valid_blockchain_address(address):
            return '550 Invalid blockchain email address'
        envelope.rcpt_tos.append(address)
        return '250 OK'

    def is_valid_blockchain_address(self, address: str) -> bool:
        # Verify if the address follows blockchain wallet format
        return len(address) == 64 and all(c in '0123456789abcdef' for c in address)

class BlockchainEmailServer:
    def __init__(self, host='127.0.0.1', port=8025):
        self.host = host
        self.port = port
        self.controller = Controller(EmailBlockchainSMTP, hostname=host, port=port)

    def start(self):
        self.controller.start()
        print(f"SMTP server running on {self.host}:{self.port}")

    def stop(self):
        self.controller.stop()