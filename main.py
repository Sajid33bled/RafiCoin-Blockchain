import hashlib
import datetime
import json
import requests
import secrets
from urllib.parse import urlparse
from flask import Flask, jsonify, request
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256((str(self.index) + str(self.timestamp) + str(self.transactions) + str(self.previous_hash) + str(self.nonce)).encode()).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print("Block mined:", self.hash)

class Transaction:
    def __init__(self, sender, receiver, amount, signature=None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = signature

    def to_dict(self):
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'signature': self.signature
        }

    def sign_transaction(self, private_key):
        if self.sender is None:  # Skip signing for reward transactions
            return

        data = f"{self.sender}{self.receiver}{self.amount}".encode()
        signature = private_key.sign(data, ec.ECDSA(hashes.SHA256()))
        self.signature = signature.hex()

    def is_valid(self, public_key):
        if self.sender is None:  # Reward transactions are automatically valid
            return True

        data = f"{self.sender}{self.receiver}{self.amount}".encode()
        try:
            public_key.verify(bytes.fromhex(self.signature), data, ec.ECDSA(hashes.SHA256()))
            return True
        except Exception as e:
            print(f"Invalid signature: {e}")
            return False

class RafiCoinNetwork:
    contract_address = "0x90efcfac0a160b513c420370b2553c8004b1dc28"
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []
        self.mining_reward = 100
        self.token = MessdakToken()
        self.nodes = set()

    def create_genesis_block(self):
        return Block(0, datetime.datetime.now(), [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        print("Block successfully mined!")
        self.chain.append(new_block)
        self.pending_transactions = []

    def create_transaction(self, transaction):
        if not transaction.is_valid(self.token.get_public_key(transaction.sender)):
            print("Transaction signature invalid.")
            return False

        self.pending_transactions.append(transaction)
        return self.get_latest_block().index + 1

    def mine_pending_transactions(self, miner):
        reward_transaction = Transaction(None, miner, self.mining_reward)
        self.pending_transactions.append(reward_transaction)
        new_block = Block(len(self.chain), datetime.datetime.now(), [t.to_dict() for t in self.pending_transactions], self.get_latest_block().hash)
        self.add_block(new_block)
        self.token.create_transaction(None, miner, self.mining_reward)
        return new_block

    def validate_transactions(self):
        for transaction in self.pending_transactions:
            if not self.token.create_transaction(transaction.sender, transaction.receiver, transaction.amount):
                return False
        return True

    def get_balance(self, address):
        return self.token.get_balance(address)

    def is_chain_valid(self, chain=None):
        if chain is None:
            chain = self.chain
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

            if not self.is_valid_proof(current_block, self.difficulty):
                return False

        return True

    def is_valid_proof(self, block, difficulty):
        return block.hash[:difficulty] == "0" * difficulty

    def add_node(self, node_url):
        parsed_url = urlparse(node_url)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)

        for node in network:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                
                reconstructed_chain = []
                for block_data in chain:
                    transactions = [Transaction(**tx) for tx in block_data['transactions']]
                    block = Block(block_data['index'], block_data['timestamp'], transactions, block_data['previous_hash'])
                    reconstructed_chain.append(block)

                if length > max_length and self.is_chain_valid(reconstructed_chain):
                    max_length = length
                    longest_chain = reconstructed_chain

        if longest_chain:
            self.chain = longest_chain
            return True

        return False

    def resolve_conflicts(self):
        replaced = self.replace_chain()
        if replaced:
            self.pending_transactions = []
        return replaced

class MessdakToken:
    def __init__(self):
        self.total_supply = 1000000  # Offre totale de jetons Messdak
        self.balance = {}  # Dictionnaire pour stocker les soldes des adresses

    def create_transaction(self, sender, receiver, amount):
        if sender not in self.balance:
            self.balance[sender] = self.total_supply
        if receiver not in self.balance:
            self.balance[receiver] = 0

        if self.balance[sender] >= amount:
            self.balance[sender] -= amount
            self.balance[receiver] += amount
            return True
        else:
            return False

    def get_balance(self, address):
        return self.balance.get(address, 0)

    def get_public_key(self, address):
        if address is None:
            return None
        return ec.generate_private_key(ec.SECP256K1()).public_key()

# Flask app setup and endpoints (unchanged for now)
app = Flask(__name__)
blockchain = RafiCoinNetwork()
