import asyncio
from pydantic import BaseModel
from openai import AsyncOpenAI
from agents import Agent, Handoff, Runner,OpenAIChatCompletionsModel
from dotenv import load_dotenv
load_dotenv(override=True)
import os
groq_api_key = os.getenv('GROQ_API_KEY')
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
groq_client = AsyncOpenAI(base_url=GROQ_BASE_URL, api_key=groq_api_key)
llm = OpenAIChatCompletionsModel(model="meta-llama/llama-4-scout-17b-16e-instruct", openai_client=groq_client)
# A typed critique schema ensures structured feedback
class Critique(BaseModel):
    score: int  # 0-10
    strengths: str
    issues: str
    actionable_improvements: str

# Drafter agent: produces release notes from a changelog
drafter = Agent(
    name="Release Notes Drafter",
    instructions=(
        "Write clear, concise release notes from the provided changelog for a technical audience. "
        "Use crisp headings, bullet points, and avoid marketing fluff. "
        "Do not invent features or dates. Keep to facts present in the changelog."
    ),
    model=llm,
    handoff_description="Creates a professional first draft of release notes from a changelog."
)

# Critic agent: returns JSON-typed critique with a score and improvements
critic = Agent(
    name="Technical Editor Critic",
    instructions=(
        "Critique the provided release notes for accuracy, completeness, clarity, and structure. "
        "Check for: unsupported claims, missing key changes, duplicated points, and vague phrasing. "
        "Return a JSON object matching the output schema with: score (0-10), strengths, issues, "
        "and actionable_improvements with concrete edits. Higher score means publish-ready."
    ),
    model=llm,
    output_type=Critique,  # SDK will parse final_output into this Pydantic model
    handoff_description="Scores drafts and proposes actionable, concrete improvements."
)

async def reflective_release_notes(changelog: str, target_score: int = 8, max_iters: int = 3):
    prompt = (
        "Changelog:\n"
        f"{changelog}\n\n"
        "Task: Draft publish-ready release notes for developers. "
        "Include only what is present in the changelog. Avoid hype and speculation."
    )
    draft_text = None

    for step in range(1, max_iters + 1):
        # 1) Draft
        draft_res = await Runner.run(drafter, prompt)
        draft_text = draft_res.final_output

        # 2) Critique
        critique_res = await Runner.run(
            critic,
            f"Draft to review:\n{draft_text}\n\nReturn structured critique JSON per the schema."
        )
        critique = critique_res.final_output_as(Critique)

        # 3) Check stopping condition
        if critique.score >= target_score:
            return {
                "final_notes": draft_text,
                "iterations": step,
                "score": critique.score,
                "reflection": critique.actionable_improvements
            }

        # 4) Revise prompt with actionable improvements
        prompt = (
            "Revise these release notes strictly following the actionable improvements below, "
            "keeping correct content and structure intact where possible.\n\n"
            f"Current draft:\n{draft_text}\n\n"
            f"Actionable improvements:\n{critique.actionable_improvements}\n\n"
            "Return only the revised release notes."
        )

    # Return best-effort after max iterations
    return {
        "final_notes": draft_text,
        "iterations": max_iters,
        "score": critique.score,
        "reflection": critique.actionable_improvements
    }

# Example usage
if __name__ == "__main__":
    sample_changelog = """
    - Add OAuth2 device flow for CLI login
    - Deprecate legacy /v1/search endpoint (EOL in 60 days)
    - Fix GPU memory leak in batch inference with >16K tokens
    - Improve latency by ~20% for streaming responses
    """
    result = asyncio.run(reflective_release_notes(sample_changelog))
    print(f"Score: {result['score']} (iters={result['iterations']})\n")
    print(result["final_notes"])