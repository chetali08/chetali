if st.button("Check Price"):
    if not name:
        st.warning("Please enter your name first.")
    else:
        price = events[selected_event]
        st.success(f"Price for **{selected_event}** is ₹{price}")

        if st.button("Confirm & Buy Ticket"):
            # 🔥 Auto-generate ticket ID
            ticket_id = str(uuid.uuid4())[:8]

            ticket_data = {
                "ticket_id": ticket_id,
                "name": name,
                "event": selected_event,
                "price": price
            }

            success = blockchain.add_ticket(ticket_data)
            if success:
                st.success("✅ Ticket Booked!")
                st.write(f"**🎫 Ticket ID:** `{ticket_id}`")  # 👈 Display ticket ID
                st.write(f"**Name:** {name}")
                st.write(f"**Event:** {selected_event}")
                st.write(f"**Price:** ₹{price}")
            else:
                st.error("⚠️ Ticket ID already exists. Try again.")
ticket_id = st.text_input("Enter Ticket ID to verify")

if st.button("Verify"):
    valid, ticket = blockchain.verify_ticket(ticket_id.strip())
    if valid:
        st.success("✅ Ticket is VALID!")
        st.write(f"**Ticket ID:** {ticket['ticket_id']}")
        st.write(f"**Name:** {ticket['name']}")
        st.write(f"**Event:** {ticket['event']}")
        st.write(f"**Price:** ₹{ticket['price']}")
    else:
        st.error("❌ Ticket not found or invalid.")
