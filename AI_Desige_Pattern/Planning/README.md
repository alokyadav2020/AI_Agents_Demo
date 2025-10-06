# 🎯 Planning Design Pattern for AI Agents

This folder demonstrates the **Planning Design Pattern** for AI agents, where agents create structured plans before executing tasks. This pattern is crucial for complex workflows that require strategic thinking and systematic execution.

## 📁 Contents

- `planning_crewai.py` - Planning pattern using CrewAI framework
- `openai_agent_planning.py` - Advanced planning with OpenAI Agents SDK

## 🎯 What is the Planning Design Pattern?

The Planning Design Pattern is a multi-phase approach where AI agents:

1. **Plan Phase** - Break down complex tasks into structured subtasks
2. **Execution Phase** - Execute the plan using specialized tools/agents
3. **Synthesis Phase** - Combine results into comprehensive output

```
User Request → Plan Creation → Plan Execution → Result Synthesis → Final Output
```

### Key Benefits

- **Structured Thinking**: Forces agents to think before acting
- **Better Quality**: Planned approach yields more comprehensive results
- **Transparency**: Clear visibility into agent's reasoning process
- **Flexibility**: Plans can be adjusted based on intermediate results
- **Scalability**: Easy to add new tools and capabilities

## 📝 Example 1: Simple Planning with CrewAI (`planning_crewai.py`)

### Overview
A straightforward implementation showing basic planning pattern for content creation using CrewAI.

### How It Works

**Single Agent Approach:**
- Agent plans the content structure first
- Then writes based on that plan
- Combines planning and execution in one agent

### Code Structure

```python
# Agent with both planning and writing responsibilities
planner_writer_agent = Agent(
    role='Article Planner and Writer',
    goal='Plan and then write a concise, engaging summary',
    backstory='Expert technical writer and content strategist',
    llm=llm
)

# Task with explicit planning instruction
task = Task(
    description="""
    1. Create a bullet-point plan
    2. Write summary based on plan
    """,
    expected_output="""
    ### Plan
    - Bulleted outline
    
    ### Summary
    - Final content
    """
)
```

### Features
- Simple sequential process
- Single agent handles both phases
- Clear output structure with plan and content
- Uses Groq's Qwen model

### Running the Example

```bash
python planning_crewai.py
```

**Example Output:**
```
## Task Result ##

### Plan
- Define reinforcement learning
- Explain importance in AI
- Provide real-world applications
- Discuss future potential

### Summary
Reinforcement learning is a crucial AI paradigm where agents learn optimal 
behaviors through trial and error...
```

## 🚀 Example 2: Advanced Market Research Planning (`openai_agent_planning.py`)

### Overview
A sophisticated three-phase planning system for conducting comprehensive market research using OpenAI Agents SDK.

### Architecture: Three Specialized Agents

#### 1. **Planning Agent** (Phase 1)
- Creates comprehensive research plan
- Identifies required subtasks
- Assigns appropriate tools
- Provides rationale for each step

#### 2. **Execution Agent** (Phase 2)
- Executes research plan systematically
- Uses specialized research tools
- Collects data from multiple sources
- Handles errors gracefully

#### 3. **Synthesis Agent** (Phase 3)
- Analyzes all findings
- Identifies patterns and insights
- Creates comprehensive report
- Provides recommendations with confidence scores

### Research Tools

The system includes four specialized research tools:

```python
@function_tool
def analyze_market_size(product_category: str, region: str) -> MarketInsight:
    """Analyze market size and growth trends"""
    
@function_tool
def research_competitors(product_category: str) -> CompetitorInsight:
    """Identify and analyze competitors"""
    
@function_tool
def gather_customer_insights(target_segment: str) -> CustomerInsight:
    """Gather customer needs and pain points"""
    
@function_tool
def assess_regulatory_environment(product_category: str, region: str) -> RegulatoryInsight:
    """Assess regulatory requirements"""
```

### Workflow Example

**Input:**
```python
system.run_research(
    product_name="FitGenius AI",
    product_category="AI-powered fitness and wellness app",
    target_market="Health-conscious millennials and Gen-Z",
    region="North America"
)
```

**Phase 1: Planning**
```
📋 PHASE 1: Generating Research Plan...

✓ Research Plan Created:
  Goal: Comprehensive market analysis for FitGenius AI
  Duration: 2-3 weeks
  
  Subtasks:
    1. Market Size Analysis
       Tool: analyze_market_size
       Why: Understand total addressable market and growth potential
    
    2. Competitive Intelligence
       Tool: research_competitors
       Why: Identify market gaps and differentiation opportunities
    
    3. Customer Research
       Tool: gather_customer_insights
       Why: Understand user needs and pain points
    
    4. Regulatory Assessment
       Tool: assess_regulatory_environment
       Why: Ensure compliance and assess risk
```

**Phase 2: Execution**
```
🔍 PHASE 2: Executing Research Plan...

[Executes each research task using appropriate tools]
[Collects market data, competitor info, customer insights, regulatory info]

✓ Research Execution Complete
```

**Phase 3: Synthesis**
```
📊 PHASE 3: Synthesizing Findings...

📈 FINAL MARKET RESEARCH REPORT

Executive Summary:
FitGenius AI enters a $2.5B market growing at 18% CAGR with strong 
differentiation opportunities through AI-powered personalization...

MARKET ANALYSIS
- Market size: $2.5B USD in North America
- Growth rate: 18% CAGR
- Key trends: Mobile-first, AI personalization, subscriptions

COMPETITIVE LANDSCAPE
- Market gaps: Poor mobile UX, lack of personalization
- Opportunities: AI recommendations, flexible pricing

CUSTOMER INSIGHTS
- Pain points: Complex interfaces, high switching costs
- Desired features: Intuitive UI, real-time collaboration

REGULATORY CONSIDERATIONS
- GDPR/CCPA compliance required
- Estimated compliance cost: $150K-$250K

LAUNCH RECOMMENDATION
Strong GO recommendation based on market opportunity and gaps

Confidence Score: 0.85/1.00
```

### Data Models (Pydantic)

The system uses strongly-typed data models for each research area:

```python
class ResearchPlan(BaseModel):
    product_name: str
    research_goal: str
    subtasks: List[ResearchSubtask]
    estimated_duration: str

class FinalReport(BaseModel):
    executive_summary: str
    market_analysis: str
    competitive_landscape: str
    customer_insights: str
    regulatory_considerations: str
    launch_recommendation: str
    confidence_score: float
```

### Running the Example

```bash
# Set environment variables
set GROQ_API_KEY=your_groq_key

# Run the system
python openai_agent_planning.py
```

## 🛠️ Setup & Installation

### Prerequisites

```bash
# For planning_crewai.py
pip install crewai langchain-groq python-dotenv

# For openai_agent_planning.py
pip install openai agents pydantic python-dotenv
```

### Environment Setup

Create a `.env` file in the project root:

```env
# For CrewAI example
GROQ_API_KEY=your_groq_api_key_here

# For OpenAI Agents example
GROQ_API_KEY=your_groq_api_key_here
# OR
OPENAI_API_KEY=your_openai_api_key_here
```

## 🔧 Customization Guide

### Adding New Research Tools

```python
@function_tool
def analyze_social_media(product_category: str) -> SocialInsight:
    """Analyze social media sentiment and trends"""
    return SocialInsight(
        sentiment_score=0.75,
        trending_topics=["AI fitness", "personalization"],
        engagement_rate="High"
    )

# Add to execution agent
execution_agent = Agent(
    tools=[
        analyze_market_size,
        research_competitors,
        gather_customer_insights,
        assess_regulatory_environment,
        analyze_social_media  # New tool
    ]
)
```

### Modifying Plan Structure

```python
# Add more subtasks
planning_instructions = """
Create a research plan with 6 subtasks:
1. Market analysis
2. Competitor research
3. Customer insights
4. Regulatory assessment
5. Social media analysis  # New
6. Technology assessment  # New
"""
```

### Switching LLM Providers

```python
# Use OpenAI instead of Groq
from openai import AsyncOpenAI

openai_client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
llm = OpenAIChatCompletionsModel(
    model="gpt-4o-mini", 
    openai_client=openai_client
)
```

## 📊 Comparison: CrewAI vs OpenAI Agents

| Feature | CrewAI Example | OpenAI Agents Example |
|---------|---------------|----------------------|
| **Complexity** | Simple, single-agent | Advanced, multi-agent |
| **Phases** | Implicit 2-phase | Explicit 3-phase |
| **Tools** | No external tools | 4 specialized tools |
| **Output** | Text-based | Structured Pydantic models |
| **Use Case** | Content creation | Market research |
| **Customization** | Easy | Highly flexible |

## 🎓 When to Use Planning Pattern

### ✅ Good Use Cases

- **Research Tasks**: Market analysis, competitive intelligence
- **Content Creation**: Long-form articles, reports, documentation
- **Project Planning**: Software development, product launches
- **Data Analysis**: Multi-source data collection and synthesis
- **Decision Making**: Complex decisions requiring multiple factors

### ❌ Not Ideal For

- **Simple Queries**: "What's the weather?" doesn't need planning
- **Real-time Responses**: Planning adds latency
- **Single-step Tasks**: "Translate this text" is straightforward
- **Creative Exploration**: Sometimes constraints hurt creativity

## 🔮 Advanced Patterns

### Adaptive Planning

```python
# Plan can be modified during execution based on findings
async def adaptive_planning(initial_plan):
    plan = initial_plan
    for step in plan.subtasks:
        result = await execute_step(step)
        if result.needs_deeper_research:
            plan = await replan(plan, result)
    return final_results
```

### Hierarchical Planning

```python
# High-level plan → Detailed sub-plans
high_level_plan = await create_strategic_plan()
for task in high_level_plan.tasks:
    detailed_plan = await create_tactical_plan(task)
    await execute_detailed_plan(detailed_plan)
```

### Collaborative Planning

```python
# Multiple agents contribute to the plan
marketing_plan = await marketing_agent.plan()
technical_plan = await technical_agent.plan()
final_plan = await coordinator.merge_plans([marketing_plan, technical_plan])
```

## 🐛 Troubleshooting

### Common Issues

**1. Planning Agent Creates Invalid Plans**
```python
# Add validation to plan output
class ResearchPlan(BaseModel):
    subtasks: List[ResearchSubtask]
    
    @validator('subtasks')
    def validate_subtasks(cls, v):
        if len(v) < 3:
            raise ValueError("Plan must have at least 3 subtasks")
        return v
```

**2. Execution Phase Fails**
```python
# Add error handling
try:
    result = await Runner.run(executor, input)
except Exception as e:
    print(f"Execution failed: {e}")
    # Fallback or retry logic
```

**3. Synthesis Produces Generic Output**
```python
# Improve synthesis instructions
synthesis_instructions = """
Base your analysis ONLY on the provided research data.
Cite specific numbers and findings.
Avoid generic statements without evidence.
"""
```

## 📈 Performance Tips

1. **Parallel Execution**: Run independent research tasks in parallel
2. **Caching**: Cache research results to avoid redundant API calls
3. **Streaming**: Stream intermediate results for better UX
4. **Token Optimization**: Use concise prompts to reduce costs

## 🔗 Related Patterns

- **Reflection Pattern**: Use planning + reflection for better quality
- **Parallelization Pattern**: Execute plan steps in parallel
- **Routing Pattern**: Route to different planners based on task type

## 📚 Additional Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [OpenAI Agents SDK](https://github.com/openai/agents-sdk)
- [Pydantic Models](https://docs.pydantic.dev/)
- [LangChain Planning](https://python.langchain.com/docs/modules/agents/agent_types/plan_and_execute)

## 🤝 Contributing

To add new planning examples:

1. Create `planning_example_XX.py` with clear phases
2. Document the planning approach
3. Include example outputs
4. Update this README

---

**Created**: October 2025  
**Last Updated**: October 6, 2025

**Next Steps**: Explore combining Planning with Reflection and Parallelization patterns for even more powerful agent systems!
