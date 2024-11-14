import time 
from openai import OpenAI
from dotenv import load_dotenv

class OpenAIHistory:
    def __init__(self,vector_store_id,assistant_id):
        self.vector_store_id = vector_store_id
        self.assistant_id = assistant_id
        self.turns = []
        self.client = OpenAI()
        self.thread_id = self.initialize_thread()

    def initialize_thread(self):
        thread = self.client.beta.threads.create(
            tool_resources = {
                'file_search':{
            "vector_store_ids":[self.vector_store_id]
        }
            }
        ) 
        return thread.id
    def clear_chat(self):
        self.turns = []    
        ## TODO Delete all messages in a thread

    def get_file_list(self):
        file_list = self.client.beta.vector_stores.files.list(
                vector_store_id = self.vector_store_id
            )
        return file_list

    def add_knowledge_base(self,file_stream):
        try:

            file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
                vector_store_id = self.vector_store_id,
                files = file_stream
            )
            file_list = self.get_file_list()
            return file_list

        except Exception as e:
            return {
                'type':'error',
                'error':e
            }
    def delete_knowledge_base(self,file_id):
        deleted_vector_store_file = self.client.beta.vector_stores.files.delete(
            vector_store_id = self.vector_store_id,
            file_id = file_id
        )
        return deleted_vector_store_file
    
    def add_turn_assistant(self,content):
        self.turns.append({
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": content
                }
            ]
        })

    def add_turn_user(self,content):

            self.turns.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": content
                }
            ]
            })
    
    def get_response(self,user_content):
        try:
            message = self.client.beta.threads.messages.create(
                thread_id = self.thread_id,
                role="user",
                content = user_content
            )

            run = self.client.beta.threads.runs.create_and_poll(
        thread_id=self.thread_id, assistant_id=self.assistant_id)
            
            messages = list(self.client.beta.threads.messages.list(thread_id=self.thread_id, run_id=run.id))
            assistant_content = '\n'.join(message.content[0].text.value for message in messages)

            self.add_turn_user(user_content)
            self.add_turn_assistant(assistant_content)

            return run 
        except Exception as e:
            return e
    

        

        


