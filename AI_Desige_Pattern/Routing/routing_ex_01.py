import asyncio
from openai import OpenAI
from agents import Agent, Runner
from dotenv import load_dotenv
load_dotenv(override=True)
# from agents.extensions.models.litellm_model import LitellmModel

# It is recommended to set the API key as an environment variable.
# import os
# os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

# --- 1. Define the Specialist Agents ---

poet_agent = Agent(
    name="Poet Agent",
    # The handoff_description provides context to the router agent.
    handoff_description="This agent is a master of poetic forms and styles. Use it for any requests related to poetry.",
    instructions="You are a world-renowned poet. Your purpose is to craft beautiful and evocative poetry in the style requested by the user. Pay close attention to rhythm, meter, and imagery.",
)

scriptwriter_agent = Agent(
    name="Scriptwriter Agent",
    handoff_description="This agent specializes in writing scripts for short videos. It understands pacing, dialogue, and visual storytelling.",
    instructions="You are a professional scriptwriter. Your task is to write a compelling script based on the user's prompt. Include scene headings, character actions, and dialogue.",
)

ad_copywriter_agent = Agent(
    name="Ad Copywriter Agent",
    handoff_description="This agent is an expert in crafting persuasive and engaging advertising copy.",
    instructions="You are a senior advertising copywriter. Your goal is to write concise, impactful, and persuasive copy that grabs the reader's attention and drives them to action.",
)


# --- 2. Define the Router Agent ---

creative_director_agent = Agent(
    name="Creative Director",
    instructions="You are the Creative Director of a content agency. Your job is to analyze the user's request and delegate it to the most appropriate specialist on your team.",
    # The handoffs list defines which agents this router can delegate to.
    handoffs=[poet_agent, scriptwriter_agent, ad_copywriter_agent],
)

# --- 3. Run the Agentic Workflow ---

async def main():
    print("Welcome to the Creative Content Hub! How can I help you today?")
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # The Runner executes the agentic workflow, starting with the router.
        result = await Runner.run(creative_director_agent, user_input)
        print(f"Assistant: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())