from .anthropic_chat import AntHistory
from dotenv import load_dotenv
if __name__== "__main__":
    load_dotenv()
    chat = AntHistory()

    # chat.add_turn_user(content = )

    response = chat.get_response()

    print(response)