import streamlit as st
from dotenv import load_dotenv
from stream_lit.session import init_session_state, reset_session_state
from utils import download_pdf, pdf_preprocessing, get_file_stream
from serper import serper_crew_run

# Initialize the app
load_dotenv()
init_session_state()

# Input and chat functions
def input_chat(role, content):
    st.session_state.messages.append({"role": role, "content": content})
    with st.chat_message(role):
        st.markdown(content)

def handle_chat_input(agent_type):
    """Handle user input and generate responses based on the agent type."""
    if prompt := st.chat_input("Ask About the Report ..."):
        input_chat(role="user", content=prompt)
        response_message = prompt_anthropic(prompt) if agent_type == "anthropic" else prompt_openai(prompt)
        input_chat(role="assistant", content=response_message)

# Report handling functions
def search_report(query):
    """Simulate a search for financial reports."""
    try:
        # Replace with actual search logic
        results = serper_crew_run(query=query)
        return results
    except Exception as e:
        st.error(f"Error searching for reports: {e}")
        return []

def download_report(url):
    """Download the report from the given URL."""
    try:
        return download_pdf(url)
    except Exception as e:
        st.error(f"Error downloading report: {e}")
        return None

def load_agent_mode(filepath):
    """Load the agent mode from the downloaded PDF."""
    try:
        agent_mode = pdf_preprocessing(filepath)
        st.session_state.agent_mode = agent_mode
        return agent_mode
    except Exception as e:
        st.error(f"Error loading agent mode: {e}")
        return None

def add_knowledge_base(agent_mode):
    """Add the knowledge base based on the agent type."""
    if agent_mode['agent_type'] == "anthropic":
        st.session_state.anthropic_chat.add_knowledge_base(agent_mode['content'][0])
    elif agent_mode['agent_type'] == "openai":
        st.session_state.openai_chat.add_knowledge_base(agent_mode['content'])

def process_results(results):
    """Process the search results and download the report."""
    if results:
        url = results[0]['url']
        filepath = download_report(url)
        
        if filepath:
            st.session_state.current_report = filepath
            agent_mode = load_agent_mode(filepath)
            if agent_mode:
                add_knowledge_base(agent_mode)
                st.sidebar.success('Report downloaded and knowledge base updated successfully!')
        else:
            st.error('Failed to download the report.')
    else:
        st.error('Error: No results found.')

def set_query():
    """Set the query and process the results."""
    query = st.session_state.query_input
    st.session_state.query = query
    with st.sidebar:
        with st.spinner("Searching for the report..."):
            results = search_report(query)
        with st.spinner("Processing Results..."):
            process_results(results)

# Sidebar rendering functions
def render_sidebar():
    """Render the sidebar component."""
    with st.sidebar:
        if not st.session_state.disable_form:
            st.header('👇 Enter Which Finance Report You Want to Analyze')

            with st.form('report form'):
                query = st.text_input("What finance report do you want to analyze?",placeholder="e.g., Amazon Quarterly Results",key='query_input')
                submit_query = st.form_submit_button('Submit', on_click=set_query)
                st.session_state.disable_form = True
        else:
            st.button('Clear Chat', on_click=clear_chat)

def switch_to_openai():
    st.session_state.agent_mode = get_file_stream(st.session_state.current_report)
    add_knowledge_base(agent_mode=st.session_state.agent_mode)

# Prompt functions for AI models
def prompt_anthropic(prompt):
    """Get a response from the Anthropic model."""
    try:
        st.session_state.anthropic_chat.add_turn_user(prompt)
        response = st.session_state.anthropic_chat.get_response()
        if 'error' in response.keys():
            st.error("Error with Anthropic model.")
            return None
        response_message = response['content'][0]['text']
        st.session_state.anthropic_chat.add_turn_assistant(response_message)
        return response_message
    except Exception as e:
        st.error(f"Error in Anthropic response: {e}")
        switch_to_openai()
        return "Switched To OpenAI, Please Re Enter Your Query"

def prompt_openai(prompt):
    """Get a response from the OpenAI model."""
    try:
        st.session_state.openai_chat.add_turn_user(prompt)
        response = st.session_state.openai_chat.get_response(prompt)
        response_message = st.session_state.openai_chat.turns[-1]['content'][0]['text']
        st.session_state.anthropic_chat.add_turn_assistant(response_message)
        return response_message
    except Exception as e:
        st.error(f"Error in OpenAI response: {e}")
        return None

# Clear chat function
def clear_chat():
    """Clear chat messages and reset form state."""
    reset_session_state()
    st.success("Chat cleared!")

# Main function
def main():
    """Main function to run the Streamlit app."""
    st.title('Finance Report Analyzer')
    render_sidebar()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if st.session_state.agent_mode is not None:
        handle_chat_input(st.session_state.agent_mode['agent_type'])

if __name__ == "__main__":
    main()
