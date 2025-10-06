import asyncio
import json
import os
from dotenv import load_dotenv

from typing import List, Dict
from pydantic import BaseModel
from openai import AsyncOpenAI
from agents import Agent, Runner, function_tool,OpenAIChatCompletionsModel



load_dotenv(override=True)
groq_api_key = os.getenv('GROQ_API_KEY')
print(f"Using GROQ API Key: {groq_api_key}")
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
groq_client = AsyncOpenAI(base_url=GROQ_BASE_URL, api_key=groq_api_key)
llm = OpenAIChatCompletionsModel(model="meta-llama/llama-4-scout-17b-16e-instruct", openai_client=groq_client)

# ============================================================================
# STEP 1: Define structured outputs using Pydantic models
# ============================================================================

class ResearchSubtask(BaseModel):
    """Individual research subtask in the plan"""
    step: int
    task_name: str
    description: str
    tool_name: str
    rationale: str

class ResearchPlan(BaseModel):
    """Complete research plan with all subtasks"""
    product_name: str
    research_goal: str
    subtasks: List[ResearchSubtask]
    estimated_duration: str

class MarketInsight(BaseModel):
    """Market analysis findings"""
    market_size: str
    growth_rate: str
    key_trends: List[str]
    target_demographics: List[str]

class CompetitorInsight(BaseModel):
    """Competitor analysis findings"""
    main_competitors: List[str]
    competitor_strengths: List[str]
    market_gaps: List[str]
    differentiation_opportunities: List[str]

class CustomerInsight(BaseModel):
    """Customer research findings"""
    pain_points: List[str]
    desired_features: List[str]
    price_sensitivity: str
    adoption_barriers: List[str]

class RegulatoryInsight(BaseModel):
    """Regulatory and compliance findings"""
    relevant_regulations: List[str]
    compliance_requirements: List[str]
    risk_level: str
    estimated_compliance_cost: str

class FinalReport(BaseModel):
    """Comprehensive market research report"""
    executive_summary: str
    market_analysis: str
    competitive_landscape: str
    customer_insights: str
    regulatory_considerations: str
    launch_recommendation: str
    confidence_score: float

# ============================================================================
# STEP 2: Define research tools (simulated APIs - replace with real data)
# ============================================================================

@function_tool
def analyze_market_size(product_category: str, region: str) -> MarketInsight:
    """
    Analyze total addressable market size and growth trends
    
    Args:
        product_category: The product category to research
        region: Geographic region for analysis
    """
    # In production: integrate with market research APIs like Statista, IBISWorld
    return MarketInsight(
        market_size=f"${2.5}B USD in {region}",
        growth_rate="18% CAGR",
        key_trends=[
            "Increasing demand for sustainable solutions",
            "Mobile-first user preferences",
            "AI-powered personalization trending",
            "Subscription-based models growing"
        ],
        target_demographics=[
            "Millennials (25-40 years)",
            "Tech-savvy professionals",
            "Urban population"
        ]
    )

@function_tool
def research_competitors(product_category: str) -> CompetitorInsight:
    """
    Identify and analyze key competitors in the space
    
    Args:
        product_category: The product category to research
    """
    # In production: integrate with Crunchbase, SimilarWeb, SEMrush APIs
    return CompetitorInsight(
        main_competitors=[
            "CompetitorA - Market leader with 35% share",
            "CompetitorB - Fast-growing startup with strong UX",
            "CompetitorC - Enterprise-focused solution"
        ],
        competitor_strengths=[
            "Established brand recognition",
            "Large existing customer base",
            "Extensive distribution networks"
        ],
        market_gaps=[
            "Lack of personalization features",
            "Poor mobile experience",
            "Limited integration capabilities",
            "High pricing for SMBs"
        ],
        differentiation_opportunities=[
            "AI-powered recommendations",
            "Superior mobile experience",
            "Flexible pricing tiers",
            "API-first architecture"
        ]
    )

@function_tool
def gather_customer_insights(target_segment: str) -> CustomerInsight:
    """
    Gather insights about customer needs and pain points
    
    Args:
        target_segment: The customer segment to research
    """
    # In production: integrate with survey tools, social listening, user research platforms
    return CustomerInsight(
        pain_points=[
            "Current solutions are too complex to use",
            "High switching costs",
            "Poor customer support",
            "Limited customization options"
        ],
        desired_features=[
            "Intuitive user interface",
            "Real-time collaboration",
            "Mobile accessibility",
            "Advanced analytics dashboard",
            "Third-party integrations"
        ],
        price_sensitivity="Moderate - willing to pay premium for better UX",
        adoption_barriers=[
            "Data migration concerns",
            "Learning curve",
            "Integration with existing tools",
            "Security concerns"
        ]
    )

@function_tool
def assess_regulatory_environment(product_category: str, region: str) -> RegulatoryInsight:
    """
    Assess regulatory requirements and compliance needs
    
    Args:
        product_category: The product category
        region: Geographic region for regulatory analysis
    """
    # In production: integrate with legal databases, compliance platforms
    return RegulatoryInsight(
        relevant_regulations=[
            "GDPR for EU data protection",
            "CCPA for California privacy",
            "Industry-specific compliance standards"
        ],
        compliance_requirements=[
            "Data encryption at rest and in transit",
            "User consent management",
            "Right to data deletion",
            "Regular security audits",
            "Privacy policy disclosure"
        ],
        risk_level="Medium",
        estimated_compliance_cost="$150K-$250K initial setup + $50K annual"
    )

# ============================================================================
# STEP 3: Create Planning Agent (Phase 1 - Plan Generation)
# ============================================================================

def create_planning_agent(llm_q) -> Agent:
    return Agent(
    name="Research Planner",
    instructions="""You are an expert market research planning agent.

Your role is to create comprehensive research plans for new product launches.

When given a product idea and target market, you must:
1. Analyze the research requirements
2. Break down the research into specific subtasks
3. Assign appropriate tools to each subtask
4. Provide clear rationale for each research step

Create a thorough plan covering:
- Market size and trends analysis
- Competitive landscape research
- Customer needs and pain points
- Regulatory and compliance requirements

Be strategic and ensure the plan provides 360-degree market intelligence.""",
    output_type=ResearchPlan,
    model=llm_q
)

# ============================================================================
# STEP 4: Create Execution Agent (Phase 2 - Plan Execution)
# ============================================================================

def create_execution_agent(llm_q) -> Agent:
    return Agent(
    name="Research Executor",
    instructions="""You are a research execution agent that carries out market research tasks.

Your role is to:
1. Execute each research subtask using the appropriate tools
2. Ensure all required data is collected
3. Handle any errors gracefully
4. Provide clear summaries of findings

Available tools:
- analyze_market_size: For market sizing and trend analysis
- research_competitors: For competitive intelligence
- gather_customer_insights: For customer research
- assess_regulatory_environment: For compliance requirements

Execute each task methodically and ensure comprehensive data collection.""",
    tools=[
        analyze_market_size,
        research_competitors,
        gather_customer_insights,
        assess_regulatory_environment
    ],
    model=llm_q
)

# ============================================================================
# STEP 5: Create Synthesis Agent (Phase 3 - Report Generation)
# ============================================================================

def create_synthesis_agent(llm_q) -> Agent:
    return Agent(
    name="Research Synthesizer",
    instructions="""You are an expert market research analyst who synthesizes findings into actionable reports.

Your role is to:
1. Analyze all research findings comprehensively
2. Identify key insights and patterns across different research areas
3. Assess market opportunity and launch viability
4. Provide clear, data-driven recommendations
5. Assign a confidence score (0-1) based on data quality and market signals

Create a professional report with:
- Executive Summary: 2-3 sentences highlighting key recommendation
- Market Analysis: Size, growth, trends, and opportunities
- Competitive Landscape: Gaps, threats, and differentiation strategies
- Customer Insights: Needs, preferences, and adoption factors
- Regulatory Considerations: Compliance requirements and risks
- Launch Recommendation: Clear go/no-go with justification
- Confidence Score: 0-1 scale based on market signals

Be analytical, data-driven, and provide actionable strategic insights.""",
    output_type=FinalReport,
    model=llm_q
)

# ============================================================================
# STEP 6: Orchestrate Planning Pattern Workflow
# ============================================================================

class MarketResearchPlanningSystem:
    """
    Planning Pattern Implementation:
    Phase 1: Generate strategic research plan
    Phase 2: Execute plan using specialized tools
    Phase 3: Synthesize findings into actionable report
    """
    
    def __init__(self,llm=llm):
        self.llm_ = llm
        self.planner = create_planning_agent(self.llm_)
        self.executor = create_execution_agent(self.llm_)
        self.synthesizer = create_synthesis_agent(self.llm_)


    async def run_research(self, product_name: str, product_category: str,
                          target_market: str, region: str = "North America") -> FinalReport:
        """
        Execute complete planning pattern workflow
        """
        print("=" * 80)
        print(f"MARKET RESEARCH PLANNING SYSTEM")
        print(f"Product: {product_name}")
        print(f"Category: {product_category}")
        print(f"Target: {target_market}")
        print("=" * 80)
        
        # PHASE 1: PLAN GENERATION
        print("\n📋 PHASE 1: Generating Research Plan...")
        print("-" * 80)
        
        planning_input = f"""Create a comprehensive market research plan for:

Product Name: {product_name}
Product Category: {product_category}
Target Market: {target_market}
Region: {region}

Generate a detailed research plan with 4 key subtasks covering market analysis, 
competitor research, customer insights, and regulatory assessment."""

        plan_result = await Runner.run(
            self.planner,
            planning_input
        )
        
        research_plan: ResearchPlan = plan_result.final_output
        
        print(f"\n✓ Research Plan Created:")
        print(f"  Goal: {research_plan.research_goal}")
        print(f"  Duration: {research_plan.estimated_duration}")
        print(f"\n  Subtasks:")
        for subtask in research_plan.subtasks:
            print(f"    {subtask.step}. {subtask.task_name}")
            print(f"       Tool: {subtask.tool_name}")
            print(f"       Why: {subtask.rationale}\n")
        
        # PHASE 2: PLAN EXECUTION
        print("\n🔍 PHASE 2: Executing Research Plan...")
        print("-" * 80)
        
        execution_input = f"""Execute the following market research plan:

Product: {product_name}
Category: {product_category}
Region: {region}

Research Tasks:
{json.dumps([{
    'step': st.step,
    'task': st.task_name,
    'tool': st.tool_name,
    'description': st.description
} for st in research_plan.subtasks], indent=2)}

Execute each research task using the appropriate tools. 
Use '{product_category}' as the product_category parameter.
Use '{target_market}' as the target_segment parameter.
Use '{region}' as the region parameter.

Provide comprehensive findings from all research areas."""

        execution_result = await Runner.run(
            self.executor,
            execution_input
        )
        
        research_findings = execution_result.final_output
        
        print(f"\n✓ Research Execution Complete")
        # print(f"  Total turns: {len(execution_result.trace)}")
        # print(f"  Tools used: {sum(1 for turn in execution_result.trace if hasattr(turn, 'tool_calls') and turn.tool_calls)}")
        
        # PHASE 3: SYNTHESIS
        print("\n📊 PHASE 3: Synthesizing Findings...")
        print("-" * 80)
        
        synthesis_input = f"""Synthesize comprehensive market research findings for {product_name}.

RESEARCH PLAN:
{json.dumps({
    'goal': research_plan.research_goal,
    'subtasks': [st.dict() for st in research_plan.subtasks]
}, indent=2)}

RESEARCH FINDINGS:
{research_findings}

Create a comprehensive market research report with strategic recommendations."""

        synthesis_result = await Runner.run(
            self.synthesizer,
            synthesis_input
        )
        
        final_report: FinalReport = synthesis_result.final_output
        
        # Print Report
        print("\n" + "=" * 80)
        print("📈 FINAL MARKET RESEARCH REPORT")
        print("=" * 80)
        print(f"\n{final_report.executive_summary}\n")
        print(f"{'MARKET ANALYSIS':^80}")
        print("-" * 80)
        print(final_report.market_analysis)
        print(f"\n{'COMPETITIVE LANDSCAPE':^80}")
        print("-" * 80)
        print(final_report.competitive_landscape)
        print(f"\n{'CUSTOMER INSIGHTS':^80}")
        print("-" * 80)
        print(final_report.customer_insights)
        print(f"\n{'REGULATORY CONSIDERATIONS':^80}")
        print("-" * 80)
        print(final_report.regulatory_considerations)
        print(f"\n{'LAUNCH RECOMMENDATION':^80}")
        print("-" * 80)
        print(final_report.launch_recommendation)
        print(f"\nConfidence Score: {final_report.confidence_score:.2f}/1.00")
        print("=" * 80)
        
        return final_report

# ============================================================================
# STEP 7: Run the Planning Pattern
# ============================================================================

async def main():
    """Run market research with planning pattern"""
    
    system = MarketResearchPlanningSystem(llm=llm)
    
    # Example: AI-powered fitness coaching app
    report = await system.run_research(
        product_name="FitGenius AI",
        product_category="AI-powered fitness and wellness app",
        target_market="Health-conscious millennials and Gen-Z",
        region="North America"
    )
    
    print(f"\n✅ Planning Pattern Complete!")
    print(f"Recommendation: {report.launch_recommendation}")

if __name__ == "__main__":
    # Ensure OPENAI_API_KEY is set in environment
    asyncio.run(main())
