import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.ui import Console
from autogen_core import Image
from autogen_ext.models.openai import OpenAIChatCompletionClient

from dotenv import load_dotenv

load_dotenv()

async def main1():
    model_client = OpenAIChatCompletionClient( model="gpt-4o" )
    assistant = AssistantAgent( name="MultiModalAssistant", model_client=model_client )
    image = Image.from_file("C:\\2025\\AI Training\\AIRahulAutoGenAgenticAI\\Images\\AIModels.png")
    multimodal_message = MultiModalMessage(
        content=["what do you see in this image", image], source="user"
    )
    await Console(assistant.run_stream(task=multimodal_message))
    await model_client.close()


asyncio.run( main1() )
