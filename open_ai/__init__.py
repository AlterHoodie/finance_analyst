# from dotenv import load_dotenv
# from openai_chat import ConversationHistory

# if __name__=="__main__":
#     load_dotenv(override=True)
#     chat = ConversationHistory(vector_store_id="vs_rjZx77Y6mhWX5RBZuMTYPaBN",
#                                assistant_id="asst_tFMTalMR86OfAh35RqZsqvS6")
#     files = chat.add_knowledge_base("./Eicher-Motors-Limited-Q1-FY-25-Earnings-Conference-Call-transcript.pdf")
#     print(files)
#     while True:
#         question = input('Enter Question:')
#         if question=="exit":
#             break
#         run = chat.get_response(question)
#         turns = chat.turns 
#         print('assistant:',turns[-1]['content'][0]['text'])

#     for file in files.data:
#         deleted_file = chat.delete_knowledge_base(file_id=file.id)
#         print(deleted_file)
    

    
