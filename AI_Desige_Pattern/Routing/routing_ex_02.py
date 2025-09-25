# DevOps Incident Triage Router using OpenAI Agents SDK
# Prereqs:
#   pip install openai-agents
#   export OPENAI_API_KEY=sk-...

import asyncio
from agents import Agent, Runner, handoffs
from dotenv import load_dotenv
load_dotenv(override=True)

# from agents.extensions.models.litellm_model import LitellmModel

# --- Specialists -------------------------------------------------------------

logs_agent = Agent(
    name="Logs Investigator",
    handoff_description="Handles application/server log error spikes, 5xx timeouts, and exceptions.",
    instructions=(
        "You are a specialist for log-related incidents. "
        "Given an incident summary, produce a concrete step-by-step investigation plan. "
        "Focus on centralized logging queries, error signatures, time windows, and rollback/patch suggestions."
    ),
)

cost_agent = Agent(
    name="Cloud Cost Analyst",
    handoff_description="Handles billing anomalies, spend spikes, and budget overages across clouds.",
    instructions=(
        "You are a cost anomaly specialist. "
        "Given an incident summary, return a clear investigation and mitigation plan. "
        "Focus on cost anomaly breakdowns by service/region, autoscaling events vs traffic baselines, and right-sizing or guardrails."
    ),
)

deploy_agent = Agent(
    name="Deployment SRE",
    handoff_description="Handles regressions related to deployments, releases, rollbacks, and feature flags.",
    instructions=(
        "You are a deployment and release specialist. "
        "Given an incident summary, draft a step-by-step plan to diagnose and mitigate deploy-related regressions. "
        "Focus on diffing releases, health checks, error budgets, and canary rollback or feature flag disable."
    ),
)

network_agent = Agent(
    name="Network Analyst",
    handoff_description="Handles connectivity, DNS, TLS/SSL, WAF/CDN, latency, ingress/egress, and packet loss issues.",
    instructions=(
        "You are a network specialist. "
        "Given an incident summary, produce a concrete action plan. "
        "Focus on connectivity diagnostics, DNS/TLS renewal checks, WAF/CDN behavior, and suggested failovers or cache purges."
    ),
)

# --- Router ------------------------------------------------------------------
# The router uses instructions + handoffs so the LLM can choose the best specialist.
triage_agent = Agent(
    name="Incident Triage",
    instructions=(
        "You are the first-line triage router for DevOps incidents. "
        "Read the incident carefully, then choose exactly one handoff to resolve it. "
        "Rough guidelines: logs/timeouts/5xx/errors -> Logs Investigator; billing/cost/spend/budget/anomaly -> Cloud Cost Analyst; "
        "deploy/release/rollback/canary/feature flag -> Deployment SRE; "
        "network/dns/tls/waf/cdn/latency/packet loss/ingress/egress -> Network Analyst. "
        "If unsure, ask one clarifying question briefly and then select a handoff."
    ),
    handoffs=[
        logs_agent,
        cost_agent,
        deploy_agent,
        network_agent,
        # You can also use handoff(...) to customize input filtering or on_handoff callbacks.
        # e.g., handoff(network_agent, tool_name_override="route_to_network", ...)
    ],
)

# --- Demo --------------------------------------------------------------------

async def main():
    test_incidents = [
        "Spike in 500s and timeouts 10 minutes after the canary release in us-east-1.",
        "AWS billing anomaly: spend up 40% in 24h, autoscaling spiked vs traffic baseline.",
        "Elevated packet loss in EU region with WAF blocks and occasional TLS handshake failures.",
        "Users report slow pages, unclear root cause yet.",
    ]
    for i, msg in enumerate(test_incidents, 1):
        print(f"\n=== Incident {i} ===")
        result = await Runner.run(triage_agent, msg)
        # The chosen specialist will write the final plan; you can inspect traces in the dashboard.
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
