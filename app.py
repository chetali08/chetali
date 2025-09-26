import hashlib
import uuid

# Blockchain-like structure
class BlockchainTicketing:
    def __init__(self):
        self.chain = []  # list to hold tickets (blocks)
        self.events = {
            "Concert": 1500,
            "Sports": 1200,
            "Theatre": 800,
            "Stand-up Comedy": 1000,
            "Workshop": 600
        }

    def generate_ticket_id(self, user_name, event):
        unique_string = user_name + event + str(uuid.uuid4())
        ticket_id = hashlib.sha256(unique_string.encode()).hexdigest()
        return ticket_id

    def purchase_ticket(self, user_name, event):
        if event not in self.events:
            return None
        ticket_id = self.generate_ticket_id(user_name, event)
        block = {
            "user": user_name,
            "event": event,
            "price": self.events[event],
            "ticket_id": ticket_id
        }
        self.chain.append(block)
        return ticket_id

    def verify_ticket(self, ticket_id):
        for block in self.chain:
            if block["ticket_id"] == ticket_id:
                return True, block
        return False, None


# Example simulation
if __name__ == "__main__":
    system = BlockchainTicketing()

    # Sample ticket purchases
    t1 = system.purchase_ticket("Alice", "Concert")
    t2 = system.purchase_ticket("Bob", "Sports")
    t3 = system.purchase_ticket("Charlie", "Workshop")

    print("Generated Ticket IDs:")
    print(f"Alice: {t1}")
    print(f"Bob: {t2}")
    print(f"Charlie: {t3}")

    # Verifying a ticket
    verify_id = t2  # checking Bob's ticket
    is_valid, details = system.verify_ticket(verify_id)

    if is_valid:
        print("\nTicket Verified!")
        print(f"Owner: {details['user']}, Event: {details['event']}, Price: ₹{details['price']}")
    else:
        print("\nInvalid Ticket!")
