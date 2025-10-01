from agents import Agent, WebSearchTool, ModelSettings,OpenAIChatCompletionsModel
from  llm_client import return_google_client

google_client = return_google_client()
llm = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=google_client)

INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 "
    "words. Capture the main points. Write succintly, no need to have complete sentences or good "
    "grammar. This will be consumed by someone synthesizing a report, so its vital you capture the "
    "essence and ignore any fluff. Do not include any additional commentary other than the summary itself."
)

search_agent = Agent(
    name="Search agent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="low")],
    model=llm,
    model_settings=ModelSettings(tool_choice="required"),
)