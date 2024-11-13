from dotenv import load_dotenv
import datetime
import os
from crewai import Crew,Process
from crewai_tools import SerperDevTool

from .serper_agents import serper_search_agent,serper_filter_agent
from .serper_tasks import serper_search_task,serper_filter_task
from .serper_output import WebsiteList

load_dotenv()
def serper_crew_run(query):
    ## Tool
    serper_tool = SerperDevTool()

    ## Input
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    ## LLM
    llm = "claude-3-5-sonnet-20241022"

    ## Agents
    serper_search_agent_ = serper_search_agent(tools=[serper_tool],llm = llm)
    serper_filter_agent_ = serper_filter_agent(llm = llm)
    
    ## Tasks
    serper_search_task_ = serper_search_task(
        agent = serper_search_agent_ 
    ) 
    serper_filter_task_ = serper_filter_task(
        agent = serper_filter_agent_,
        context=[serper_search_task_],
        output_model=WebsiteList
    )

    ## Crew
    crew = Crew(
        agents = [serper_search_agent_,serper_filter_agent_],
        tasks = [serper_search_task_,serper_filter_task_],
        process = Process.sequential ,
        verbose = True
    )

    try:
        result = crew.kickoff(
            inputs = {
                'user_query':query,
                'date':date
            }
        )
        return result['websites']
    except:
        return []
