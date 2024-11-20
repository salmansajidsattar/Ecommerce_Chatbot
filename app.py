import streamlit as st
import sys
import os

# Get the absolute path to the core directory
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
core_dir = os.path.join(project_dir, 'core')
if core_dir not in sys.path:
    sys.path.insert(0, core_dir)  # Prefer prepend to avoid any potential conflicts
# Now, try importing pandas_Agent
from agent import pandas_Agent

def main():
    # Set up the page layout and title
    st.set_page_config(page_title="E-Commerce Chatbot", layout="wide")
    st.title("E-Commerce Chatbot")

    # Input for username
    username = st.text_input("Username", value="admin")

    # Initialize chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Text input for user query
    user_query = st.text_input("Ask me anything about our products!")

    # Send button to submit query
    send_button = st.button("Send")

    # Interaction handling
    if send_button and user_query:
        with st.spinner('Waiting for bot response...'):
            # Adding user query to chat history
            st.session_state.chat_history.append(f"You: {user_query}")

            # Call the pandas_Agent function with the username and query
            response_dict = pandas_Agent(username, user_query, './Data/ecommerce_data.csv')  # Adjust the path to your actual data file
            print(response_dict)
            # Extracting the output part of the response
            response_output = response_dict.get('output', 'No response')  # Safeguard with 'No response' in case 'output' key is missing

        # Adding bot response to chat history
        st.session_state.chat_history.append(f"Bot: {response_output}")

    # Display the chat history
    for chat in st.session_state.chat_history:
        st.markdown(f"> {chat}", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
