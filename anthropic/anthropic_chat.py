import time 
import anthropic 

class ConversationHistory:
    def __init__(self):
        # Initialize an empty list to store conversation turns
        self.turns = []
        self.client = anthropic.Anthropic()
        self.MODEL_NAME = "claude-3-5-sonnet-20241022"
        self.betas = ["pdfs-2024-09-25", "prompt-caching-2024-07-31"]
        self.max_tokens = 600

    def clear_chat(self):
        self.turns = []

    def add_knowledge_base(self,base64_string):
        self.turns.append({"role": "user",
            "content": [{
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": base64_string
                    }
                }]})

    def add_turn_assistant(self, content):
        # Add an assistant's turn to the conversation history
        self.turns.append({
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": content
                }
            ]
        })

    def add_turn_user(self, content):
        # Add a user's turn to the conversation history
        self.turns.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": content
                }
            ]
        })

    def get_turns(self):
        # Retrieve conversation turns with specific formatting
        result = []
        user_turns_processed = 0

        # Iterate through turns in reverse order
        for turn in reversed(self.turns):
            # Create a shallow copy of the turn (this copies the dictionary)
            ele = turn.copy()

            # If the turn contains nested objects (like lists), make sure to copy those as well
            if "content" in ele:
                ele["content"] = [content.copy() for content in ele["content"]]  # Make a shallow copy of the content list

            if turn["role"] == "user" and user_turns_processed < 2:
                # Add the last two user turns with ephemeral cache control
                ele["content"][0].update({"cache_control": {"type": "ephemeral"}})  # Use .update() to add/modify keys
                result.append(ele)
                user_turns_processed += 1
            else:
                # Add other turns as they are
                result.append(ele)

        # Return the turns in the original order
        return list(reversed(result))
    
    def get_response(self):
    
        try:
            response = self.client.beta.messages.create(
                    model = self.MODEL_NAME,
                    betas = self.betas,
                    max_tokens = self.max_tokens,
                    messages = self.get_turns()
                )
            return {
                'type':response.type,
                'id':response.id,
                'content':[{
                    'text':content.text,
                    'type':content.type
                } for content in response.content],
                'model':response.model,
                'role':response.role,
                'stop_reason':response.stop_reason,
                'stop_sequence':response.stop_sequence,
                'usage':{
                    'cache_creation_input_tokens':response.usage.cache_creation_input_tokens,
                    'cache_read_input_tokens':response.usage.cache_read_input_tokens,
                    'input_tokens':response.usage.input_tokens,
                    'output_tokens':response.usage.output_tokens
                }
            }
        except anthropic.APIConnectionError as e:
            print('Server Could Not Be Reached')
            return e.body
        except anthropic.RateLimitError as e:
            print('Rate Limit Hit')
            return e.body
        except anthropic.StatusError as e:
            print('Non 200 Status recieved')
            return e.body
        except anthropic.AnthropicError as e:
            return e.body
