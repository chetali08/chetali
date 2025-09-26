import streamlit as st
import hashlib
import json
from time import time

# Simple blockchain class simulating ticket storage
class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_tickets = []
        self.create_block(previous_hash='1', proof=100)  # Genesis block

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
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def add_ticket(self, ticket_id, buyer_name):
        # Check ticket uniqueness (no duplicates)
        for block in self.chain:
            for ticket in block['tickets']:
                if ticket['ticket_id'] == ticket_id:
                    return False  # Ticket ID already exists
        for ticket in self.current_tickets:
            if ticket['ticket_id'] == ticket_id:
                return False

        self.current_tickets.append({
            'ticket_id': ticket_id,
            'buyer_name': buyer_name
        })
        return True

    def verify_ticket(self, ticket_id):
        for block in self.chain:
            for ticket in block['tickets']:
                if ticket['ticket_id'] == ticket_id:
                    return True, ticket['buyer_name']
        for ticket in self.current_tickets:
            if ticket['ticket_id'] == ticket_id:
                return True, ticket['buyer_name']
        return False, None

# Initialize blockchain instance
blockchain = Blockchain()

# Streamlit UI
st.title("🎟️ Blockchain-based Event Ticketing System")

menu = st.sidebar.selectbox("Menu", ["Buy Ticket", "Verify Ticket", "View Blockchain"])

if menu == "Buy Ticket":
    st.header("Buy a Ticket")
    ticket_id = st.text_input("Enter unique Ticket ID")
    buyer_name = st.text_input("Your Name")

    if st.button("Buy Ticket"):
        if ticket_id == "" or buyer_name == "":
            st.warning("Please enter both Ticket ID and your name.")
        else:
            success = blockchain.add_ticket(ticket_id, buyer_name)
            if success:
                st.success(f"Ticket '{ticket_id}' bought successfully for {buyer_name}!")
            else:
                st.error("Ticket ID already exists! Please use a unique Ticket ID.")

elif menu == "Verify Ticket":
    st.header("Verify Ticket Validity")
    ticket_id = st.text_input("Enter Ticket ID to Verify")

    if st.button("Verify"):
        if ticket_id == "":
            st.warning("Please enter a Ticket ID.")
        else:
            valid, buyer = blockchain.verify_ticket(ticket_id)
            if valid:
                st.success(f"Ticket ID '{ticket_id}' is VALID, owned by {buyer}.")
            else:
                st.error("Ticket ID NOT FOUND or invalid.")

elif menu == "View Blockchain":
    st.header("Blockchain Ledger")
    for block in blockchain.chain:
        st.write(f"Block Index: {block['index']}")
        st.write(f"Timestamp: {block['timestamp']}")
        st.write(f"Previous Hash: {block['previous_hash']}")
        st.write(f"Proof: {block['proof']}")
        st.write("Tickets:")
        for ticket in block['tickets']:
            st.write(f"- {ticket['ticket_id']} owned by {ticket['buyer_name']}")
        st.write("---")

    # Button to mine block and confirm current tickets
    if st.button("Confirm Tickets (Mine Block)"):
        last_block = blockchain.get_last_block()
        last_proof = last_block['proof']
        proof = blockchain.proof_of_work(last_proof)
        previous_hash = blockchain.hash(last_block)
        block = blockchain.create_block(proof, previous_hash)
        st.success(f"New block mined! Block index: {block['index']}")

