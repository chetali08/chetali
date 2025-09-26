import streamlit as st
import hashlib
import json
from time import time
import qrcode
from io import BytesIO
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
        # Prevent duplicate ticket IDs
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
# Generate QR Code
# ------------------------
def generate_qr_code(data):
    qr = qrcode.QRCode(box_size=5, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf)
    return buf.getvalue()

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
st.set_page_config(page_title="Blockchain Ticket App", layout="centered")
st.title("🎟️ Blockchain Event Ticketing System")

menu = st.sidebar.selectbox("Menu", ["Buy Ticket", "Verify Ticket", "Blockchain"])

# ------------------------
# Buy Ticket
# ------------------------
if menu == "Buy Ticket":
    st.header("🎫 Book Your Ticket")
    name = st.text_input("Enter your name")
    selected_event = st.selectbox("Choose an event", list(events.keys()))

    if st.button("Buy Ticket"):
        if not name:
            st.warning("Please enter your name.")
        else:
            ticket_id = str(uuid.uuid4())[:8]  # Short unique ID
            price = events[selected_event]
            ticket_data = {
                "ticket_id": ticket_id,
                "name": name,
                "event": selected_event,
                "price": price
            }

            success = blockchain.add_ticket(ticket_data)
            if success:
                st.success(f"🎉 Ticket Purchased! Ticket ID: `{ticket_id}`")
                st.write(f"**Name:** {name}")
                st.write(f"**Event:** {selected_event}")
                st.write(f"**Price:** ₹{price}")
                
                # Generate and show QR code
                qr_content = f"TicketID: {ticket_id}, Name: {name}, Event: {selected_event}, Price: ₹{price}"
                qr_img = generate_qr_code(qr_content)
                st.image(qr_img, caption="Your Ticket QR Code")
            else:
                st.error("Ticket ID already exists. Try again.")

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
                st.write(f"**Name:** {ticket['name']}")
                st.write(f"**Event:** {ticket['event']}")
                st.write(f"**Price:** ₹{ticket['price']}")
                st.write(f"**Ticket ID:** {ticket['ticket_id']}")
            else:
                st.error("❌ Ticket not found or invalid.")

# ------------------------
# View Blockchain
# ------------------------
elif menu == "Blockchain":
    st.header("⛓️ Blockchain Ledger")
    for block in blockchain.chain:
        st.subheader(f"Block {block['index']}")
        st.write(f"⏱️ Timestamp: {block['timestamp']}")
        st.write(f"🔐 Previous Hash: {block['previous_hash']}")
        st.write(f"💡 Proof: {block['proof']}")
        if block['tickets']:
            st.write("🎫 Tickets:")
            for t in block['tickets']:
                st.write(f"- {t['ticket_id']} | {t['name']} | {t['event']} | ₹{t['price']}")
        else:
            st.write("No tickets in this block.")
        st.markdown("---")

    if st.button("🪙 Mine New Block"):
        last_block = blockchain.get_last_block()
        proof = blockchain.proof_of_work(last_block['proof'])
        previous_hash = blockchain.hash(last_block)
        block = blockchain.create_block(proof, previous_hash)
        st.success(f"✅ Block {block['index']} mined and tickets confirmed!")

