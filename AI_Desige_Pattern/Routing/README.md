# 🔀 Agent Routing Design Pattern

This folder demonstrates the **Agent Routing** design pattern using the OpenAI Agents SDK. The routing pattern is a fundamental AI agent architecture where a **router agent** intelligently delegates tasks to specialized **worker agents** based on the nature of the request.

## 📁 Contents

- [`routing_ex_01.py`](./routing_ex_01.py) - Creative Content Hub routing example
- [`routing_ex_02.py`](./routing_ex_02.py) - DevOps Incident Triage routing example

## 🎯 What is Agent Routing?

Agent routing is a design pattern where:

1. **Router Agent** - Acts as a "smart dispatcher" that analyzes incoming requests
2. **Specialist Agents** - Handle specific types of tasks in their domain of expertise
3. **Handoff Mechanism** - Seamlessly transfers context and control between agents

```
User Request → Router Agent → Analyzes Request → Routes to Specialist → Returns Result
```

## 🎨 Example 1: Creative Content Hub (`routing_ex_01.py`)

### Overview
A creative content agency system that routes content creation requests to appropriate specialists.

### Agents
- **🎭 Creative Director** (Router)
  - Analyzes content requests
  - Routes to appropriate specialist
  
- **📝 Poet Agent** (Specialist)
  - Handles poetry and verse creation
  - Expert in rhythm, meter, and imagery
  
- **🎬 Scriptwriter Agent** (Specialist)  
  - Creates scripts for videos
  - Focuses on pacing, dialogue, visual storytelling
  
- **📢 Ad Copywriter Agent** (Specialist)
  - Crafts persuasive advertising copy
  - Expert in conversion-focused writing

### Usage Example
```python
# User input: "Write a haiku about technology"
# Router → Poet Agent → Beautiful haiku output

# User input: "Create a 30-second ad script for a coffee shop"  
# Router → Scriptwriter Agent → Video script with scenes and dialogue
```

### Running the Example
```bash
python routing_ex_01.py
```

## 🚨 Example 2: DevOps Incident Triage (`routing_ex_02.py`)

### Overview
An enterprise-grade incident response system that automatically triages DevOps incidents to specialist teams.

### Agents
- **🚨 Incident Triage** (Router)
  - First-line triage for DevOps incidents
  - Routes based on incident type and symptoms
  
- **🔍 Logs Investigator** (Specialist)
  - Handles application/server log errors
  - Expert in 5xx timeouts, exceptions, error spikes
  
- **💰 Cloud Cost Analyst** (Specialist)
  - Manages billing anomalies and spend spikes
  - Analyzes autoscaling events vs traffic baselines
  
- **🚀 Deployment SRE** (Specialist)
  - Handles deployment-related regressions
  - Expert in rollbacks, feature flags, release issues
  
- **🌐 Network Analyst** (Specialist)
  - Manages connectivity and infrastructure issues
  - Expert in DNS, TLS/SSL, WAF/CDN, latency problems

### Routing Logic
- **Logs/Timeouts/5xx/Errors** → Logs Investigator
- **Billing/Cost/Spend/Budget** → Cloud Cost Analyst  
- **Deploy/Release/Rollback/Canary** → Deployment SRE
- **Network/DNS/TLS/WAF/CDN** → Network Analyst

### Sample Incidents
```python
incidents = [
    "Spike in 500s and timeouts 10 minutes after canary release",
    "AWS billing anomaly: spend up 40% in 24h", 
    "Elevated packet loss in EU region with WAF blocks",
    "Users report slow pages, unclear root cause"
]
```

### Running the Example
```bash
python routing_ex_02.py
```

## 🛠️ Prerequisites

### Installation
```bash
# Install OpenAI Agents SDK
pip install openai-agents

# Install dependencies
pip install python-dotenv openai
```

### Environment Setup
```bash
# Set your OpenAI API key
export OPENAI_API_KEY="sk-your-api-key-here"

# Or create a .env file
echo "OPENAI_API_KEY=sk-your-api-key-here" > .env
```

## 🏗️ Architecture Benefits

### 1. **Separation of Concerns**
- Each agent focuses on its specialty
- Clear responsibility boundaries
- Easier to maintain and update

### 2. **Scalability**
- Add new specialists without changing router logic
- Parallel processing capabilities
- Load distribution across specialists

### 3. **Flexibility** 
- Dynamic routing based on request analysis
- Easy to modify routing rules
- Support for complex decision trees

### 4. **Maintainability**
- Modular agent design
- Independent testing of specialists
- Clear debugging paths

## 🔧 Customization Guide

### Adding New Specialists

```python
# 1. Define the specialist agent
new_specialist = Agent(
    name="New Specialist",
    handoff_description="Handles specific type of requests",
    instructions="Detailed instructions for the specialist"
)

# 2. Add to router's handoffs
router_agent = Agent(
    name="Router",
    instructions="Updated routing logic including new specialist",
    handoffs=[existing_agent1, existing_agent2, new_specialist]
)
```

### Modifying Routing Logic

Update the router agent's instructions to include new routing rules:

```python
instructions = """
You are a router agent. Route requests based on:
- Pattern A → Specialist 1
- Pattern B → Specialist 2  
- Pattern C → New Specialist
- Default → General Specialist
"""
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Error: `agents` module not found**
   ```bash
   pip install openai-agents
   ```

2. **API Key Error**
   ```bash
   export OPENAI_API_KEY="your-key-here"
   ```

3. **No Response from Agents**
   - Check API key validity
   - Verify internet connection
   - Check OpenAI service status

4. **Routing Not Working**
   - Review router instructions
   - Check handoff descriptions
   - Verify specialist configurations

### Debug Mode

Add logging to see routing decisions:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Your agent code here
```

## 📚 Advanced Patterns

### Multi-Level Routing
```
User → L1 Router → L2 Router → Specialist
```

### Conditional Routing
```python
# Route based on context, user role, time, etc.
router_instructions = """
Route based on:
- User role (admin/user)
- Time of day (business hours/after hours)
- Incident severity (critical/normal)
"""
```

### Fallback Routing
```python
# Include a general agent as fallback
handoffs=[specialist1, specialist2, general_agent]
```

## 🤝 Contributing

To add new routing examples:

1. Create new `routing_ex_XX.py` file
2. Follow the established pattern:
   - Define specialist agents
   - Create router agent with handoffs
   - Add demo/interactive mode
3. Update this README with example description
4. Add requirements to main requirements.txt

## 📖 Further Reading

- [OpenAI Agents SDK Documentation](https://github.com/openai/agents-sdk)
- [Agent Design Patterns](../README.md)
- [Multi-Agent Systems Best Practices]

---

**Note**: These examples demonstrate core routing concepts. For production use, consider adding error handling, monitoring, rate limiting, and security measures.