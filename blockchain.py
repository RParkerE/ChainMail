import hashlib
import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import base64
from cryptography.hazmat.primitives import serialization
from network.node import Node
from email.handler import EmailHandler
from wallet.resolver import WalletResolver
from consensus.proof_of_stake import ProofOfStake
from email.smtp_interface import BlockchainEmailServer

class EmailChunk:
    def __init__(self, chunk_id, encrypted_content, recipient_address):
        self.chunk_id = chunk_id
        self.encrypted_content = encrypted_content
        self.recipient_address = recipient_address
        self.timestamp = datetime.datetime.now()

class Block:
    def __init__(self, email_chunks, previous_hash):
        self.email_chunks = email_chunks
        self.previous_hash = previous_hash
        self.timestamp = datetime.datetime.now()
        self.nonce = 0
        self.merkle_root = self.calculate_merkle_root()
        self.hash = self.calculate_hash()

    def calculate_merkle_root(self):
        if not self.email_chunks:
            return hashlib.sha256("empty".encode()).hexdigest()

        chunk_hashes = [hashlib.sha256(str(chunk.encrypted_content).encode()).hexdigest()
                       for chunk in self.email_chunks]
        return self._build_merkle_tree(chunk_hashes)

    def _build_merkle_tree(self, hashes):
        if len(hashes) == 1:
            return hashes[0]
        new_hashes = []
        for i in range(0, len(hashes)-1, 2):
            combined = hashes[i] + hashes[i+1]
            new_hashes.append(hashlib.sha256(combined.encode()).hexdigest())
        if len(hashes) % 2 == 1:
            new_hashes.append(hashes[-1])
        return self._build_merkle_tree(new_hashes)

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.email_chunks).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8') +
                   str(self.nonce).encode('utf-8'))
        return sha.hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:len(difficulty)] != difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

        print(f"Block mined: {self.hash}")

genesis_block = Block("Genesis Block", "0")

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block("Genesis Block", "0")

    def add_block(self, new_block):
        new_block.previous_hash = self.chain[-1].hash
        new_block.mine_block("0000")
        self.chain.append(new_block)

class Wallet:
    def __init__(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()
        self.address = self.generate_address()

    def generate_address(self):
        # Generate a wallet address from the public key
        public_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return hashlib.sha256(public_bytes).hexdigest()

class EmailProtocol:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.chunk_size = 1024  # Size of each email chunk in bytes

    def send_email(self, sender_wallet, recipient_address, content):
        # Split email into chunks and encrypt each chunk
        chunks = [content[i:i+self.chunk_size] for i in range(0, len(content), self.chunk_size)]
        encrypted_chunks = []

        for i, chunk in enumerate(chunks):
            # Encrypt chunk with recipient's public key
            encrypted_chunk = self.encrypt_chunk(chunk, recipient_address)
            chunk_obj = EmailChunk(i, encrypted_chunk, recipient_address)
            encrypted_chunks.append(chunk_obj)

        # Create new block with encrypted chunks
        new_block = Block(encrypted_chunks, self.blockchain.chain[-1].hash)
        self.blockchain.add_block(new_block)

class EmailBlockchain:
    def __init__(self, host='127.0.0.1', port=8000):
        self.blockchain = Blockchain()
        self.wallet_resolver = WalletResolver()
        self.consensus = ProofOfStake()
        self.node = Node(host, port)
        self.email_handler = EmailHandler(self.blockchain, None)
        self.smtp_server = BlockchainEmailServer()

    async def start(self):
        await self.node.start()
        self.smtp_server.start()

    def stop(self):
        self.smtp_server.stop()

