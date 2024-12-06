from typing import List
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class EmailHandler:
    def __init__(self, blockchain, wallet):
        self.blockchain = blockchain
        self.wallet = wallet

    def retrieve_emails(self, wallet_address: str) -> List[dict]:
        emails = []
        for block in self.blockchain.chain:
            for chunk in block.email_chunks:
                if chunk.recipient_address == wallet_address:
                    try:
                        decrypted_content = self.decrypt_chunk(
                            chunk.encrypted_content,
                            self.wallet.private_key
                        )
                        emails.append({
                            'content': decrypted_content,
                            'timestamp': chunk.timestamp,
                            'chunk_id': chunk.chunk_id
                        })
                    except Exception as e:
                        print(f"Failed to decrypt chunk: {e}")

        return self.reconstruct_emails(emails)

    def decrypt_chunk(self, encrypted_content: bytes, private_key):
        return private_key.decrypt(
            encrypted_content,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def reconstruct_emails(self, chunks: List[dict]) -> List[dict]:
        # Group chunks by timestamp (assuming same timestamp for same email)
        email_groups = {}
        for chunk in chunks:
            timestamp = chunk['timestamp']
            if timestamp not in email_groups:
                email_groups[timestamp] = []
            email_groups[timestamp].append(chunk)

        # Reconstruct emails from chunks
        complete_emails = []
        for timestamp, chunks in email_groups.items():
            sorted_chunks = sorted(chunks, key=lambda x: x['chunk_id'])
            complete_content = ''.join(chunk['content'].decode() for chunk in sorted_chunks)
            complete_emails.append({
                'content': complete_content,
                'timestamp': timestamp
            })

        return complete_emails