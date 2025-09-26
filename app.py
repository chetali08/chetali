import streamlit as st
import hashlib
import json
from time import time
import random
import uuid

# ------------------------
# Blockchain Class
# ------------------------
class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_tickets = []
        self.create_block(proof=100, previous_hash='1')  # Genesis block

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'tickets': self.current_tickets,
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.current_tickets = []
        self.chain.append(block)
        return block

    def get_last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    def valid_proof(self, last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def hash(self, block):
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

    def add_ticket(self, ticket):
        if self.ticket_exists(ticket['ticket_id']):
            return False
        self.current_tickets.append(ticket)
        return True

    def ticket_exists(self, ticket_id):
        for block in self.chain:
            for t in block['tickets']:
                if t['ticket_id'] == ticket_id:
                    return True
        for t in self.current_tickets:
            if t['ticket_id'] == ticket_id:
                return True
        return False

    def verify_ticket(self, ticket_id):
        for block in self.chain:
            for t in block['tickets']:
                if t['ticket_id'] == ticket_id:
                    return True, t
        for t in self.current_tickets:
            if t['ticket_id'] == ticket_id:
                return True, t
        return False, None

# ------------------------
# App Initialization
# ------------------------
blockchain = Blockchain()

# Static events with random prices
events = {
    "🎤 Music Concert": random.randint(1000, 2000),
    "⚽ Football Match": random.randint(800, 1500),
    "🎬 Movie Premiere": random.randint(500, 1000),
    "💼 Business Conference": random.randint(1500, 3000),
    "🎮 Esports Tournament": random.randint(700, 1300)
}

# ------------------------
# Streamlit UI
# ------------------------
st.set_page_config(page_title="Blockchain Ticket App", layout="c_
