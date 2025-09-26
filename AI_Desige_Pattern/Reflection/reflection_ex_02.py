from google.adk.agents import SequentialAgent, LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

from google.genai import types
from dotenv import load_dotenv
load_dotenv(override=True)
session_service = InMemorySessionService()


def call_agent_async(query: str, runner, user_id, session_id):
    """Sends a query to the agent and prints the final response."""
    print(f"\n>>> User Query: {query}")

    # Prepare the user's message in ADK format
    content = types.Content(role='user', parts=[types.Part(text=query)])

    final_response_text = "Agent did not produce a final response." # Default

  # Key Concept: run_async executes the agent logic and yields Events.
  # We iterate through events to find the final answer.
    for event in runner.run(user_id=user_id, session_id=session_id, new_message=content):
      # You can uncomment the line below to see *all* events during execution
      # print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

      # Key Concept: is_final_response() marks the concluding message for the turn.
        if event.is_final_response():
          if event.content and event.content.parts:
             # Assuming text response in the first part
             final_response_text = event.content.parts[0].text
          elif event.actions and event.actions.escalate: # Handle potential errors/escalations
             final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
          # Add more checks here if needed (e.g., specific error codes)
          break # Stop processing events once the final response is found

    print(f"<<< Agent Response: {final_response_text}")
# The first agent generates the initial draft.
generator = LlmAgent(
   name="DraftWriter",
   description="Generates initial draft content on a given subject.",
   instruction="Write a short, informative paragraph about the user's subject.",
   output_key="draft_text" # The output is saved to this state key.
)

# The second agent critiques the draft from the first agent.
reviewer = LlmAgent(
   name="FactChecker",
   description="Reviews a given text for factual accuracy and provides a structured critique.",
   instruction="""
   You are a meticulous fact-checker.
   1. Read the text provided in the state key 'draft_text'.
   2. Carefully verify the factual accuracy of all claims.
   3. Your final output must be a dictionary containing two keys:
      - "status": A string, either "ACCURATE" or "INACCURATE".
      - "reasoning": A string providing a clear explanation for your status, citing specific issues if any are found.
   """,
   output_key="review_output" # The structured dictionary is saved here.
)

# The SequentialAgent ensures the generator runs before the reviewer.
review_pipeline = SequentialAgent(
   name="WriteAndReview_Pipeline",
   sub_agents=[generator, reviewer]
)
APP_NAME = "reflection_design_pattern"
USER_ID = "user_1"
SESSION_ID = "session_002"


runner_agent_team = Runner( # Or use InMemoryRunner
            agent=review_pipeline,
            app_name=APP_NAME,
            session_service=session_service
        )

call_agent_async(
    query="Explain the theory of relativity in simple terms.",
    runner=runner_agent_team,
    user_id=USER_ID,
    session_id=SESSION_ID
)
# final_response_text = "Agent did not produce a final response."
# for event in runner_agent_team.run(
#     user_id=USER_ID,
#     session_id=SESSION_ID,
#     new_message=types.Content(role='user', parts=[types.Part(text="Hello there!")])):
#     print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}"
# )
#     if event.is_final_response():
#           if event.content and event.content.parts:
#              # Assuming text response in the first part
#              final_response_text = event.content.parts[0].text
#           elif event.actions and event.actions.escalate: # Handle potential errors/escalations
#              final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
#           # Add more checks here if needed (e.g., specific error codes)
#           break # Stop processing events once the final response is found

# print(f"<<< Agent Response: {final_response_text}")
