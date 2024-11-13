import streamlit as st
from dotenv import load_dotenv
import open_ai
from serper import serper_crew_run
import time 
from utils import download_pdf


if "current_report" not in st.session_state:
    st.session_state.current_report = None 

if __name__=="__main__":
    load_dotenv()

    st.title('Bleh')

    with st.sidebar:
        st.header('👇 Enter Which Finance Report You Want to Analyze')

        with st.form('report form'):
            query = st.text_input(
                "What finance report do you want to analyze?",
                placeholder="e.g., Amazon Quarterly Results"
            )
            submit_query = st.form_submit_button('Submit')

    if query and submit_query:
        with st.chat_message("assistant"):
            st.markdown("Searching for Results")
        # results = serper_crew_run(query)
        results = [{'url': 'https://ir.aboutamazon.com/files/doc_financials/2024/q3/AMZN-Q3-2024-Earnings-Release.pdf', 'site': 'Amazon Investor Relations', 'description': 'Most recent official Q3 2024 earnings release containing detailed financial results, showing net sales increase of 11% to $158.9 billion compared with Q3 2023, including comprehensive quarterly financial data, segment performance, and future guidance'}, {'url': 'https://ir.aboutamazon.com/files/doc_financials/2024/q1/Webslides_Q124_Final.pdf', 'site': 'Amazon Investor Relations', 'description': 'Q1 2024 earnings presentation slides providing visual representation of financial performance, key metrics, business highlights, and detailed breakdown of segment-wise results with supporting graphs and charts'}, {'url': 'https://ir.aboutamazon.com/files/doc_financials/2023/q4/AMZN-Q4-2023-Earnings-Release.pdf', 'site': 'Amazon Investor Relations', 'description': 'Q4 2023 earnings release document containing detailed financial statements, year-end results, and Q1 2024 guidance, providing historical context and year-over-year performance metrics'}]
        if results:
            with st.chat_message("assistant"):
                st.markdown("Found Results, Starting Download")
            url = results[0]['url']
            filepath = download_pdf(url)
            with st.chat_message("assistant"):
                st.markdown(filepath)


                        

        
