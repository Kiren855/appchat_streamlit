import streamlit as st
import hashlib
from datetime import datetime, timezone

# Block structure for blockchain
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(f"{self.index}{self.timestamp}{self.data}{self.previous_hash}".encode())
        return sha.hexdigest()

# Blockchain structure
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # Use dictionary to synchronize data structure
        return Block(0, str(datetime.now(timezone.utc)), {"user": "Genesis", "message": "Genesis Block"}, "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        latest_block = self.get_latest_block()
        new_block = Block(len(self.chain), str(datetime.now(timezone.utc)), data, latest_block.hash)
        self.chain.append(new_block)

# Initialize blockchain
blockchain = Blockchain()

# Streamlit WebChat UI
st.title("WebChat-App with Blockchain")

st.write("### Chat History (stored on blockchain)")

# Display all messages in blockchain
for block in blockchain.chain:
    if isinstance(block.data, dict):  # Ensure data is a dictionary
        st.write(f"**User**: {block.data.get('user', 'N/A')}")
        st.write(f"**Message**: {block.data.get('message', '')}")
    else:
        st.write(f"**User**: N/A")
        st.write(f"**Message**: {block.data}")
    st.write(f"**Timestamp**: {block.timestamp}")
    st.write(f"**Hash**: `{block.hash}`")
    st.write("---")

# Chat input
st.write("### Send a New Message")

user = st.text_input("Your Name")
message = st.text_input("Your Message")

if st.button("Send"):
    if user and message:
        blockchain.add_block({"user": user, "message": message})
        st.success("Message sent and stored on the blockchain!")
        st.experimental_rerun()  # Refresh to show the new message
    else:
        st.error("Please enter both your name and message.")
