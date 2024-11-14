from dotenv import load_dotenv
from .openai_chat import OpenAIHistory
import os 
if __name__=="__main__":
    load_dotenv(override=True)
    chat = OpenAIHistory(vector_store_id=os.getenv("VECTOR_STORE_ID"),
                            assistant_id=os.getenv("ASSISTANT_ID"))
    files = chat.add_knowledge_base("")
    print(files)
    while True:
        question = input('Enter Question:')
        if question=="exit":
            break
        run = chat.get_response(question)
        turns = chat.turns 
        print(run)
        print('assistant:',turns[-1]['content'][0]['text'])

    for file in files.data:
        deleted_file = chat.delete_knowledge_base(file_id=file.id)
        # print(deleted_file)
    

    
