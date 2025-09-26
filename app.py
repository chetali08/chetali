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
# App Setup
# ------------------------

st.set_page_config(page_title="Blockchain Ticket App", layout="centered")
st.title("🎟️ Blockchain-Based Event Ticketing System")

blockchain = Blockchain()

# Generate static events with random prices
events = {
    "🎤 Music Concert": random.randint(1000, 2000),
    "⚽ Football Match": random.randint(800, 1500),
    "🎬 Movie Premiere": random.randint(500, 1000),
    "💼 Business Conference": random.randint(1500, 3000),
    "🎮 Esports Tournament": random.randint(700, 1300)
}

menu = st.sidebar.selectbox("Navigation", ["Buy Ticket", "Verify Ticket", "Blockchain Ledger"])

# ------------------------
# Buy Ticket
# ------------------------
if menu == "Buy Ticket":
    st.header("🎫 Book Your Ticket")

    name = st.text_input("Enter your name")
    selected_event = st.selectbox("Choose an event", list(events.keys()))

    if st.button("Check Price"):
        if not name:
            st.warning("Please enter your name first.")
        else:
            price = events[selected_event]
            st.success(f"Price for **{selected_event}** is ₹{price}")

            if st.button("Confirm & Buy Ticket"):
                # Auto-generate ticket ID
                ticket_id = str(uuid.uuid4())[:8]
                ticket_data = {
                    "ticket_id": ticket_id,
                    "name": name,
                    "event": selected_event,
                    "price": price
                }

                success = blockchain.add_ticket(ticket_data)
                if success:
                    st.success("✅ Ticket Booked Successfully!")
                    st.write(f"**🎫 Ticket ID:** `{ticket_id}`")
                    st.write(f"**Name:** {name}")
                    st.write(f"**Event:** {selected_event}")
                    st.write(f"**Price:** ₹{price}")
                else:
                    st.error("⚠️ This ticket ID already exists. Try again.")

# ------------------------
# Verify Ticket
# ------------------------
elif menu == "Verify Ticket":
    st.header("🔍 Verify Your Ticket")

    ticket_id = st.text_input("Enter Ticket ID to verify")

    if st.button("Verify"):
        if not ticket_id:
            st.warning("Please enter a Ticket ID.")
        else:
            valid, ticket = blockchain.verify_ticket(ticket_id.strip())
            if valid:
                st.success("✅ Ticket is VALID!")
                st.write(f"**Ticket ID:** {ticket['ticket_id']}")
                st.write(f"**Name:** {ticket['name']}")
                st.write(f"**Event:** {ticket['event']}")
                st.write(f"**Price:** ₹{ticket['price']}")
            else:
                st.error("❌ Ticket not found or invalid.")

# ------------------------
# Blockchain View
# ------------------------
elif menu == "Blockchain Ledger":
    st.header("⛓️ Blockchain Ledger")

    for block in blockchain.chain:
        st.subheader(f"Block {block['index']}")
        st.write(f"⏱️ Timestamp: {block['timestamp']}")
        st.write(f"🔐 Previous Hash: {block['previous_hash']}")
        st.write(f"💡 Proof: {block['proof']}")
        st.write("🎫 Tickets:")
        if block['tickets']:
            for t in block['tickets']:
                st.markdown(f"- **{t['ticket_id']}** | {t['name']} | {t['event']} | ₹{t['price']}")
        else:
            st.write("- No tickets in this block.")
        st.markdown("---")

    if st.button("🪙 Mine New Block"):
        last_block = blockchain.get_last_block()
        proof = blockchain.proof_of_work(last_block['proof'])
        previous_hash = blockchain.hash(last_block)
        block = blockchain.create_block(proof, previous_hash)
        st.success(f"✅ Block {block['index']} mined and tickets confirmed!")

