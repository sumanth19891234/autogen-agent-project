import asyncio
import os
import subprocess

# Set Node.js in PATH at the beginning
os.environ["PATH"] = r"C:\nvm4w\nodejs;" + os.environ.get("PATH", "")
os.environ["NODE_PATH"] = r"C:\nvm4w\nodejs\node_modules"


from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench

from dotenv import load_dotenv

load_dotenv()

async def main():
    # Test if node is accessible now
    try:
        result = subprocess.run(["node", "-v"], capture_output=True, text=True)
        print(f"Node.js version: {result.stdout}")
    except Exception as e:
        print(f"Node.js test failed: {e}")

    filesystem_server_params = StdioServerParams(
        command="npx",  # Try using npx directly now
        args=[
            "-y",
            "@modelcontextprotocol/server-filesystem",
            r"C:\Users\sgangadharappa\PycharmProjects\agenticAI\AgenticAIAutoGen"
        ],
        read_timeout_seconds=60
    )


    fs_workbench = McpWorkbench( filesystem_server_params )

    async with fs_workbench as fs_wb:
        model_client = OpenAIChatCompletionClient( model="gpt-4o" )

        math_tutor = AssistantAgent( name="MathTutor", model_client=model_client, workbench=fs_wb,
                                    system_message="""You are helpful math tutor.Help the user solve math problems step 
                                                   by step, You have to access file system

                                                        Available filesystem tools:
                                                        - write_file: Create or write content to a file
                                                        - read_file: Read content from an existing file
                                                        - list_directory: List files and directories
                                                        - create_directory: Create a new directory
                                            
                                                        IMPORTANT: When creating files in subdirectories, always create the directory first using create_directory before writing files.
                                                        For simple file operations, save files directly in the root directory without subdirectories.

                                                  When the user says 'THANKS DONE' or similar, acknowledge and say 'LESSON COMPLETE' to end session.

                                                   When the user says 'THANKS DONE' or similar, acknowledge and say "
                                                   "'LESSON COMPLETE' to end session.""" )

        user_proxy = UserProxyAgent( name="Student" )

        # Create team with text termination
        team = RoundRobinGroupChat(
            participants=[user_proxy, math_tutor],
            termination_condition=TextMentionTermination( "LESSON COMPLETE" )
        )

        await Console( team.run_stream( task="I need help with algebra problem. Tutor, feel free to create"
                                             "files to help with student learning " ) )

    await model_client.close()
asyncio.run( main() )
