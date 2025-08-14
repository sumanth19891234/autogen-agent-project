import asyncio

from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_agentchat.agents import AssistantAgent
from autogen_core import Image
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential
from openai import images


async def main():
    print("Inside main function!!!")
    credentials = DefaultAzureCredential()

    # Create a token provider function
    def get_azure_ad_token():
        token = credentials.get_token("api://ai-proxy-uat-ar-api")
        return token.token

    # Create the model client with direct values
    az_model_client = AzureOpenAIChatCompletionClient(
        azure_deployment="gpt-4o-gs",  # Replace with your actual deployment name
        model="gpt-4o",
        api_version="2024-12-01-preview",
        azure_endpoint="https://ai-sharedinfra-uat-apim.azure-api.net/litellm",
        azure_ad_token_provider=get_azure_ad_token
    )

    assistant_teacher = AssistantAgent(name="mathTeacher", model_client=az_model_client,
    system_message = "You are a Teacher.Explain Concepts clearly and ask followup questions."
                     "Reply with TERMINATE when the task has been completed.")

    assistant_student = AssistantAgent(name="mathStudent", model_client=az_model_client,
    system_message = "You are a Curious student.Ask questions and show your thinking process."
                     "Reply with TERMINATE when the task has been completed.")

    team= RoundRobinGroupChat(participants=[assistant_teacher,assistant_student],
                                   termination_condition=MaxMessageTermination(max_messages=6))
    await Console(team.run_stream("Lets Discuss what is multiplication and How it works"))
    await az_model_client.close()

asyncio.run(main())
