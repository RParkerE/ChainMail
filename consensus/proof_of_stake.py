import random
from typing import List

class ProofOfStake:
    def __init__(self):
        self.stakers = {}  # wallet_address -> stake_amount
        self.validators = []

    def add_stake(self, wallet_address: str, amount: float):
        if wallet_address in self.stakers:
            self.stakers[wallet_address] += amount
        else:
            self.stakers[wallet_address] = amount

    def select_validator(self) -> str:
        total_stake = sum(self.stakers.values())
        target = random.uniform(0, total_stake)
        current_stake = 0

        for address, stake in self.stakers.items():
            current_stake += stake
            if current_stake >= target:
                return address

        return list(self.stakers.keys())[0]  # Fallback

    def validate_block(self, block, validator_address: str) -> bool:
        # Basic validation rules
        if not block.hash.startswith('0000'):  # Difficulty check
            return False

        if block.previous_hash != self.blockchain.chain[-1].hash:
            return False

        if not self.verify_merkle_root(block):
            return False

        return True

    def verify_merkle_root(self, block) -> bool:
        calculated_root = block.calculate_merkle_root()
        return calculated_root == block.merkle_root