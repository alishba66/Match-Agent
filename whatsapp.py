import chainlit as cl
from agents import function_tool
import requests
import os

@function_tool
def send_whatsapp_message(number:str, message : str) -> str:
    """users the ultramessage API to send a custom whatsapp message to the specified phone number.
      Returns a success message if sent successfully, or an error message if the request fails to send."""

    instance_id = os.getenv("Instance_ID")
    token = os.getenv("Token")

    url = f"https://api.ultramsg.com/{instance_id}/messages/chat"

    print(f"Attempting to send WhatsApp message to {number} with body: {message}")
    
    payload ={
    "token" : token,
    "to" : number ,
    "body" : message
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
      return f" message sent successfully to {number}"
    else :
      return f" failed to send message. Error: {response.text}"