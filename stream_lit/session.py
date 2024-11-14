import streamlit as st
from ant import AntHistory
from open_ai import OpenAIHistory
import os

def init_session_state():
    """Initialize session state variables"""
    if "current_report" not in st.session_state:
        st.session_state.current_report = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "agent_mode" not in st.session_state:
        st.session_state.agent_mode = None
    if "anthropic_chat" not in st.session_state:
        st.session_state.anthropic_chat = AntHistory()
    if "openai_chat" not in st.session_state:
        st.session_state.openai_chat = OpenAIHistory(vector_store_id=os.getenv("VECTOR_STORE_ID"),
                               assistant_id=os.getenv("ASSISTANT_ID"))
        files = st.session_state.openai_chat.get_file_list()
        for file in files.data:
            deleted_file = st.session_state.openai_chat.delete_knowledge_base(file_id=file.id)
            print(deleted_file)
    if "disable_form" not in st.session_state:
        st.session_state.disable_form = False
    if "query" not in st.session_state:
        st.session_state.query = None

def reset_session_state():
    st.session_state.current_report = None
    st.session_state.messages = []
    st.session_state.agent_mode = None
    st.session_state.anthropic_chat = AntHistory()
    st.session_state.openai_chat = OpenAIHistory(vector_store_id=os.getenv("VECTOR_STORE_ID"),
                               assistant_id=os.getenv("ASSISTANT_ID"))
    files = st.session_state.openai_chat.get_file_list()
    for file in files.data:
            deleted_file = st.session_state.openai_chat.delete_knowledge_base(file_id=file.id)
    st.session_state.disable_form = False
    st.session_state.disable_form = False
    st.session_state.query = None