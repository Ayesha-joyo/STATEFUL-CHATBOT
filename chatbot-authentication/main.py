import os  # For accessing environment variables
import chainlit as cl  # Web UI framework for chat applications
import google.generativeai as genai  # Google's Generative AI library
from dotenv import load_dotenv  # For loading environment variables
from typing import Optional, Dict  # Type hints for better code clarity

load_dotenv()


gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)


model = genai.GenerativeModel(
    model_name="gemini-2.0-flash"  
)



@cl.oauth_callback
def oauth_callback(
    provider_id: str,
    token: str,  
    raw_user_data: Dict[str, str],  
    default_user: cl.User,  
) -> Optional[cl.User]:  
    """
    Handle the OAuth callback from GitHub
    Return the user object if authentication is successful, None otherwise
    """

    print(f"Provider: {provider_id}")
    print(f"User data: {raw_user_data}")  

    return default_user  
@cl.on_chat_start
async def handle_chat_start():

    cl.user_session.set("history", [])

    await cl.Message(
        content="Hello! How can I help you today?"
    ).send()  
@cl.on_message
async def handle_message(message: cl.Message):

    history = cl.user_session.get("history")  

    history.append(
        {"role": "user", "content": message.content}
    ) 
    formatted_history = []
    for msg in history:
        formatted_history.append(
            {"role": role, "parts": [{"text": msg["content"]}]}
        )  

    response = model.generate_content(formatted_history)

    response_text = (
        response.text if hasattr(response, "text") else ""
    ) 

    history.append(
        {"role": "assistant", "content": response_text}
    )  
    cl.user_session.set("history", history)  

    await cl.Message(content=response_text).send()  