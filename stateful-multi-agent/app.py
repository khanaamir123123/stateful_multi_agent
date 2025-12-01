import asyncio
import streamlit as st
from customer_service_agent.agent import customer_service_agent
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from utils import add_user_query_to_history, call_agent_async

# Load environment variables
load_dotenv()

# --- App Configuration ---
st.set_page_config(page_title="Customer Service Chat", page_icon="🤖")
st.title("Customer Service Chat")
st.write("Welcome! I'm here to help with sales, course support, and policy questions. How can I assist you today?")

# --- Initialization (runs once per session) ---
@st.cache_resource
def initialize_services():
    """Initialize services and define cleanup logic."""
    session_service = InMemorySessionService()
    runner = Runner(
        agent=customer_service_agent,
        app_name="Customer Support",
        session_service=session_service,
    )
    try:
        yield session_service, runner
    finally:
        # This block will be executed when the app is shut down
        # or the cache is cleared, properly closing the connection.
        asyncio.run(runner.close())

session_service, runner = initialize_services()

# Define the initial state for a new user session
initial_state = {
    "user_name": "Valued Customer",
    "purchased_courses": [],
    "interaction_history": [],
}

# --- Session State Management ---
# Ensure a session is created and stored in Streamlit's session state
if "session_id" not in st.session_state:
    new_session = session_service.create_session(
        app_name="Customer Support",
        user_id="streamlit_user", # A generic ID for all web users
        state=initial_state,
    )
    st.session_state.session_id = new_session.id
    st.session_state.messages = [] # To store chat history

# --- Chat History Display ---
# Display previous messages from the chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Main Chat Logic ---
async def run_chat_turn(prompt: str):
    """Handles a single turn of the chat conversation."""
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_text = await call_agent_async(
                runner=runner,
                session_id=st.session_state.session_id,
                user_id="streamlit_user",
                query=prompt,
            )
            st.markdown(response_text)

    # Add agent response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})

# --- User Input ---
if prompt := st.chat_input("What can I help you with?"):
    # Streamlit requires running async functions with asyncio.run()
    asyncio.run(run_chat_turn(prompt))
