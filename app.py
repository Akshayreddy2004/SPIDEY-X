import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

from memory.database import (
    init_db,
    save_memory,
    get_memory_count,
    save_user_memory,
    get_user_memory
)

# Load Environment Variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

# Page Config
st.set_page_config(
    page_title="SPIDEY-X",
    page_icon="🕷️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Key Check
if not api_key:
    st.error("Groq API Key not found.")
    st.stop()

# Groq Client
client = Groq(api_key=api_key)

# Database Initialize
init_db()

# Sidebar
with st.sidebar:

    st.title("🕷️ SPIDEY-X")

    st.markdown("---")

    st.write("Version 2.5")

    memory_count = get_memory_count()

    st.write(f"🧠 Memories Stored: {memory_count}")

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Main UI
st.title("🕷️ SPIDEY-X")
st.caption("Your Personal AI Assistant")

# System Prompt
system_prompt = """
You are SPIDEY-X.

A smart AI assistant.

Be helpful, professional and concise.

Always introduce yourself as SPIDEY-X when asked.
"""

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Previous Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
prompt = st.chat_input("Ask SPIDEY-X anything...")

if prompt:

    lower_prompt = prompt.lower()

    # ==========================
    # SAVE NAME
    # ==========================

    if "my name is" in lower_prompt:

        name = prompt.split("is", 1)[1].strip()

        save_user_memory("name", name)

        with st.chat_message("assistant"):
            st.markdown(
                f"🧠 I'll remember your name, **{name}**."
            )

        st.stop()

    # ==========================
    # SAVE GOAL
    # ==========================

    if "my goal is" in lower_prompt:

        goal = prompt.split("is", 1)[1].strip()

        save_user_memory("goal", goal)

        with st.chat_message("assistant"):
            st.markdown(
                f"🎯 I'll remember your goal: **{goal}**"
            )

        st.stop()

    # ==========================
    # RECALL NAME
    # ==========================

    if "what is my name" in lower_prompt:

        saved_name = get_user_memory("name")

        with st.chat_message("assistant"):

            if saved_name:
                st.markdown(
                    f"Your name is **{saved_name}**."
                )
            else:
                st.markdown(
                    "I don't know your name yet."
                )

        st.stop()

    # ==========================
    # RECALL GOAL
    # ==========================

    if "what is my goal" in lower_prompt:

        saved_goal = get_user_memory("goal")

        with st.chat_message("assistant"):

            if saved_goal:
                st.markdown(
                    f"Your goal is **{saved_goal}**."
                )
            else:
                st.markdown(
                    "I don't know your goal yet."
                )

        st.stop()

    # Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    try:

        with st.chat_message("assistant"):

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    }
                ] + st.session_state.messages,
                temperature=0.7,
                max_tokens=1024
            )

            reply = response.choices[0].message.content

            save_memory(prompt, reply)

            st.markdown(reply)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": reply
            }
        )

    except Exception as e:
        st.error(f"Error: {e}")