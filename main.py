from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool 
from dotenv import load_dotenv
import os
from openai import AsyncOpenAI
import asyncio
from whatsapp import send_whatsapp_message
import chainlit as cl

load_dotenv()
set_tracing_disabled(True)


API_KEY = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

@function_tool
def get_user_data(min_age: int) -> list[dict]:
    "Retrieve user data based on a minimum age"
    users = [
        {"name": "Ali", "age": 23, "gender": "Male", "education": "BSc Computer Science"},
        {"name": "Babar", "age": 20, "gender": "Male", "education": "Intermediate"},
        {"name": "Chota", "age": 19, "gender": "Male", "education": "Matric"},
        {"name": "Ayesha", "age": 25, "gender": "Female", "education": "MBA"},
        {"name": "Sara", "age": 22, "gender": "Female", "education": "BS Psychology"},
        {"name": "Usman", "age": 28, "gender": "Male", "education": "MSc Mathematics"},
        {"name": "Fatima", "age": 21, "gender": "Female", "education": "BA English"},
        {"name": "Hamza", "age": 26, "gender": "Male", "education": "BBA"},
        {"name": "Zainab", "age": 24, "gender": "Female", "education": "BS IT"},
        {"name": "Bilal", "age": 30, "gender": "Male", "education": "PhD Chemistry"},
        {"name": "Amna", "age": 19, "gender": "Female", "education": "Intermediate"},
        {"name": "Fahad", "age": 27, "gender": "Male", "education": "MPhil Physics"},
        {"name": "Mariam", "age": 23, "gender": "Female", "education": "BEd"},
        {"name": "Rehan", "age": 22, "gender": "Male", "education": "BS Software Engineering"},
        {"name": "Sana", "age": 24, "gender": "Female", "education": "MSc Zoology"},
        {"name": "Imran", "age": 29, "gender": "Male", "education": "MBA"},
        {"name": "Iqra", "age": 25, "gender": "Female", "education": "BS Botany"},
        {"name": "Yasir", "age": 20, "gender": "Male", "education": "Diploma in Electrical"},
        {"name": "Areeba", "age": 21, "gender": "Female", "education": "BCom"},
        {"name": "Noman", "age": 26, "gender": "Male", "education": "MSc Economics"},
        {"name": "Hina", "age": 28, "gender": "Female", "education": "MPhil Education"},
        {"name": "Jawad", "age": 24, "gender": "Male", "education": "BS Civil Engineering"},
        {"name": "Laiba", "age": 22, "gender": "Female", "education": "BS Sociology"},
        {"name": "Tariq", "age": 23, "gender": "Male", "education": "BSc Statistics"},
        {"name": "Mehwish", "age": 25, "gender": "Female", "education": "MSc Geography"},
        {"name": "Zeeshan", "age": 27, "gender": "Male", "education": "MS Data Science"},
    ]
    return [user for user in users if user["age"] >= min_age]



match_agent = Agent(
    name="match_agent",
    instructions="""
You are the perfect match finder agent. Your job is to collect user name, and ask the user of which age you want a proposal.
"""
,
    model=model,
    tools=[get_user_data , send_whatsapp_message]
)

@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])
    await cl.Message("Hi beta, here’s a Match-finder Agent.").send()

@cl.on_message
async def main(message: cl.Message):
    await cl.Message("Thinking...").send()
    history = cl.user_session.get("history") or []
    history.append({"role": "user", "content": message.content})

    result = await Runner.run(  
        starting_agent=match_agent,
        input=history
    )

    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)
    await cl.Message(content=result.final_output).send()
