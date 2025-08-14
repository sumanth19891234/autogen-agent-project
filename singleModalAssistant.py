import asyncio
from autogen_agentchat.ui import Console
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential

async def main():
    print("Inside main function!!!")
    credentials = DefaultAzureCredential()

    # Create a token provider function
    def get_azure_ad_token():
        token = credentials.get_token("api://ai-proxy-uat-ar-api")
        return token.token

    # Create the model client with direct values
    az_model_client = AzureOpenAIChatCompletionClient(
        azure_deployment="gpt-4",  # Replace with your actual deployment name
        model="gpt-4",
        api_version="2024-12-01-preview",
        azure_endpoint="https://ai-sharedinfra-uat-apim.azure-api.net/litellm",
        azure_ad_token_provider=get_azure_ad_token
    )

    assistant = AssistantAgent(name="assistant", model_client=az_model_client)
    await Console(assistant.run_stream(task="what is 25 + 5?"))
    await az_model_client.close()

asyncio.run(main())