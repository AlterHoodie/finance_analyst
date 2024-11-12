from crewai import Task
from textwrap import dedent
import datetime

def serper_search_task(agent)->Task:
    return Task(
    description=dedent("""
        The task is to search for the most relevant and high-quality financial reports in PDF format for a specified company based on the user query: "{user_query}".
            
            The user query may request different types of financial reports, such as:
            - Quarterly Reports
            - Annual Reports
            - Earnings Statements
            - Balance Sheets
            etc
            The query may also specify a time period (e.g., Q2 FY 2025, fiscal year 2024). If no time period is specified, retrieve the most recent report available.[latest date: {date} (YYYY-MM-DD)]
        Refine the search query to get precise and reliable results based on the user's request. Ensure that the reports contain comprehensive financial data, including key financial indicators.
        Make Use of Advanced Search Filters like site:<site>, after:<after date> etc
        You can choose not to use them if you are not getting good results
    """),
    expected_output=dedent("""
        The output should include a list of the most relevant financial PDF reports retrieved from the web, including:
        1. Links to the downloaded PDFs or the files themselves if possible.
        The goal is to provide the Financial Analysis team with trustworthy financial reports for detailed analysis.
    """),
    agent=agent
    )


def serper_filter_task(agent, output_model, context) -> Task:
    return Task(
        description=dedent("""
            **Task**: take the list of links retrieved by the retrieval agents and select the best PDF document based on the user's query:"{user_query}".
            
            **Responsibilities**:
            1. Review the list of retrieved PDF URLs and analyze their content.
            2. Evaluate the relevance of each document based on its title, description, and content (if available).
            3. Select the most relevant PDF documents that provides detailed and accurate financial data (if applicable).
            4. Pick top 5 or 3, sort them by most relevance and return a list, starting from the most relevant document
            4. Return the selected document in the following JSON format:
               ```json
               [{{"url": "<url>",
                   "site": "<site name>",
                   "description": "<description>"}},{{"url": "<url>",
                   "site": "<site name>",
                   "description": "<description>"}}...]
               ```
            
            **Important**:
            - Focus on selecting the documents that best matches the user's query, considering the content and title.
            - Prioritize authoritative and trustworthy sources for financial documents.
            - Ensure that the document contains detailed financial information if the query pertains to financial reports (e.g., earnings reports, annual reports).
            
        """),
        expected_output=dedent("""
            The output should include a list of the most relevant PDF reports retrieved based on the user's query.
            The result must be in the following JSON format:
            ```json
            [{{"url": "<url>",
                   "site": "<site name>",
                   "description": "<description>"}},{{"url": "<url>",
                   "site": "<site name>",
                   "description": "<description>"...}}]
            
            ```
            Example output:
            ```json
            [{{"url": "https://example.com/financial-report-2023.pdf",
                "site": "Example Company",
                "description": "Annual report for Example Company, including detailed financial statements and analysis."}},{{"url": "https://example-2.com/financial-report-202X.pdf",
                "site": "Example Company",
                "description": "Annual report for Example Company, including detailed financial statements and analysis."}}]
            
            ```
            The goal is to provide the Financial Analysis team with the best and most relevant document for detailed analysis.
        """),
        agent=agent,
        output_json=output_model,
        context=context  # Pass the context, such as the user query, as part of the task input
    )
