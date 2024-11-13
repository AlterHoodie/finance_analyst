from .serper_crew import serper_crew_run

__all__ = ['serper_crew_run']
if __name__=="__main__":
    query = input('Enter Search Query:')
    results = serper_crew_run(query=query)
    print(results)