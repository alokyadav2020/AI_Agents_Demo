import streamlit as st
import os
import asyncio
from dotenv import load_dotenv
from typing import List, Union
from pydantic import BaseModel
from openai import AsyncOpenAI
from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel
load_dotenv(override=True)
groq_api_key = os.getenv('GROQ_API_KEY')
print(f"Using GROQ API Key: {groq_api_key}")
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
groq_client = AsyncOpenAI(base_url=GROQ_BASE_URL, api_key=groq_api_key)
llm = OpenAIChatCompletionsModel(model="meta-llama/llama-4-scout-17b-16e-instruct", openai_client=groq_client)
# google_api_key = os.getenv('GOOGLE_API_KEY')
# # GROQ_BASE_URL = "https://api.groq.com/openai/v1"
# GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
# google_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)
# llm = OpenAIChatCompletionsModel(model="gemini-2.5-pro", openai_client=google_client)




# Load environment variables
load_dotenv(override=True)

# ============================================================================
# STEP 1: Define structured outputs using Pydantic models
# ============================================================================

class ExerciseDay(BaseModel):
    """Single day exercise routine"""
    day: str
    focus: str
    exercises: List[str]
    sets_reps: List[str]
    duration: str
    notes: str

class ExercisePlan(BaseModel):
    """Complete weekly exercise plan"""
    user_name: str
    fitness_goal: str
    weekly_schedule: List[ExerciseDay]
    warm_up_routine: str
    cool_down_routine: str
    progressive_overload_strategy: str
    safety_precautions: List[str]

class MealDay(BaseModel):
    """Single day meal plan"""
    day: str
    breakfast: str
    mid_morning_snack: str
    lunch: str
    evening_snack: str
    dinner: str
    total_calories: str
    protein_grams: str
    carbs_grams: str
    fats_grams: str

class DietPlan(BaseModel):
    """Complete weekly diet plan"""
    user_name: str
    diet_preference: str
    daily_calorie_target: str
    macronutrient_split: str
    weekly_meals: List[MealDay]
    meal_timing_guidelines: str
    hydration_recommendations: str
    supplement_suggestions: List[str]

class ComprehensiveReport(BaseModel):
    """Final integrated fitness report"""
    executive_summary: str
    user_profile_analysis: str
    exercise_plan_overview: str
    diet_plan_overview: str
    integration_strategy: str
    progress_tracking_methods: List[str]
    weekly_milestones: List[str]
    success_tips: List[str]
    safety_reminders: List[str]
    confidence_score: float

# ============================================================================
# STEP 2: Define fitness tools (knowledge-based functions)
# ============================================================================

@function_tool
def calculate_bmi(weight_kg: Union[str, float], height_cm: Union[str, float]) -> dict:
    """
    Calculate Body Mass Index (BMI)
    
    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
    """
    # Convert to float in case strings are passed
    weight_kg = float(weight_kg)
    height_cm = float(height_cm)
    
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        category = "Normal weight"
    elif 25 <= bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    
    return {
        "bmi": round(bmi, 2),
        "category": category,
        "recommendation": f"Your BMI is {round(bmi, 2)} ({category})"
    }

@function_tool
def calculate_tdee(weight_kg: Union[str, float], height_cm: Union[str, float], age: Union[str, int], gender: str, activity_level: str = "moderate") -> dict:
    """
    Calculate Total Daily Energy Expenditure (TDEE)
    
    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
        age: Age in years
        gender: Male or Female
        activity_level: sedentary, light, moderate, active, very_active
    """
    # Convert to correct types in case strings are passed
    weight_kg = float(weight_kg)
    height_cm = float(height_cm)
    age = int(age)
    
    # Calculate BMR using Mifflin-St Jeor Equation
    if gender.lower() == "male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    
    # Activity multipliers
    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }
    
    multiplier = activity_multipliers.get(activity_level.lower(), 1.55)
    tdee = bmr * multiplier
    
    return {
        "bmr": round(bmr, 0),
        "tdee": round(tdee, 0),
        "maintenance_calories": round(tdee, 0),
        "weight_loss_calories": round(tdee * 0.85, 0),
        "muscle_gain_calories": round(tdee * 1.15, 0)
    }

@function_tool
def get_exercise_recommendations(goal: str, fitness_level: str, body_fat: Union[str, float]) -> dict:
    """
    Get exercise type recommendations based on goals
    
    Args:
        goal: Fitness goal (muscle gain, fat loss, general fitness)
        fitness_level: beginner, intermediate, advanced
        body_fat: Body fat percentage
    """
    # Convert to float in case string is passed
    body_fat = float(body_fat)
    
    recommendations = {
        "muscle_gain": {
            "workout_split": "Push/Pull/Legs or Upper/Lower",
            "frequency": "4-6 days per week",
            "rep_range": "8-12 reps for hypertrophy",
            "cardio": "2-3 sessions per week (low intensity)",
            "rest": "48 hours between same muscle groups"
        },
        "fat_loss": {
            "workout_split": "Full body or Upper/Lower",
            "frequency": "4-5 days per week",
            "rep_range": "12-15 reps with shorter rest",
            "cardio": "4-5 sessions per week (mix HIIT and steady state)",
            "rest": "Active recovery recommended"
        },
        "general_fitness": {
            "workout_split": "Full body workouts",
            "frequency": "3-4 days per week",
            "rep_range": "10-15 reps",
            "cardio": "3 sessions per week",
            "rest": "At least 1 full rest day per week"
        }
    }
    
    goal_key = "muscle_gain" if "muscle" in goal.lower() else \
               "fat_loss" if "fat" in goal.lower() or "loss" in goal.lower() else \
               "general_fitness"
    
    return recommendations.get(goal_key, recommendations["general_fitness"])

@function_tool
def get_nutrition_recommendations(goal: str, tdee: Union[str, float], weight_kg: Union[str, float], diet_preference: str) -> dict:
    """
    Get nutrition recommendations based on goals
    
    Args:
        goal: Fitness goal
        tdee: Total Daily Energy Expenditure
        weight_kg: Body weight in kg
        diet_preference: Vegetarian or Non-Vegetarian
    """
    # Convert to float in case strings are passed
    tdee = float(tdee)
    weight_kg = float(weight_kg)
    
    if "muscle" in goal.lower():
        calorie_target = tdee * 1.15
        protein_per_kg = 2.0
        carbs_percent = 0.40
        fats_percent = 0.25
    elif "fat" in goal.lower() or "loss" in goal.lower():
        calorie_target = tdee * 0.85
        protein_per_kg = 2.2
        carbs_percent = 0.35
        fats_percent = 0.30
    else:
        calorie_target = tdee
        protein_per_kg = 1.6
        carbs_percent = 0.40
        fats_percent = 0.30
    
    protein_grams = weight_kg * protein_per_kg
    protein_calories = protein_grams * 4
    
    remaining_calories = calorie_target - protein_calories
    carbs_calories = remaining_calories * carbs_percent / (carbs_percent + fats_percent)
    fats_calories = remaining_calories * fats_percent / (carbs_percent + fats_percent)
    
    carbs_grams = carbs_calories / 4
    fats_grams = fats_calories / 9
    
    return {
        "daily_calories": round(calorie_target, 0),
        "protein_grams": round(protein_grams, 0),
        "carbs_grams": round(carbs_grams, 0),
        "fats_grams": round(fats_grams, 0),
        "protein_percent": round((protein_calories / calorie_target) * 100, 0),
        "carbs_percent": round((carbs_calories / calorie_target) * 100, 0),
        "fats_percent": round((fats_calories / calorie_target) * 100, 0),
        "diet_preference": diet_preference
    }

# ============================================================================
# STEP 3: Create Specialized Agents (Two-Phase Approach)
# ============================================================================

# Phase 1: Calculator Agents (with tools, NO output_type to avoid JSON mode conflict)
def create_fitness_calculator_agent(llm) -> Agent:
    """Create a calculator agent that runs tools to gather fitness metrics"""
    return Agent(
        name="Fitness Calculator Agent",
        instructions="""You are a fitness metrics calculator.

Your role is to calculate key fitness metrics using the available tools:
1. Use calculate_bmi to get Body Mass Index
2. Use get_exercise_recommendations to get workout type recommendations

Provide all calculated metrics clearly in your response.""",
        tools=[calculate_bmi, get_exercise_recommendations],
        # NO output_type - avoid JSON mode + tools conflict
        model=llm
    )

def create_nutrition_calculator_agent(llm) -> Agent:
    """Create a calculator agent that runs tools to gather nutrition metrics"""
    return Agent(
        name="Nutrition Calculator Agent",
        instructions="""You are a nutrition metrics calculator.

Your role is to calculate key nutrition metrics using the available tools:
1. Use calculate_tdee to get Total Daily Energy Expenditure
2. Use get_nutrition_recommendations to get macro targets

Provide all calculated metrics clearly in your response.""",
        tools=[calculate_tdee, get_nutrition_recommendations],
        # NO output_type - avoid JSON mode + tools conflict
        model=llm
    )

# Phase 2: Planning Agents (with output_type, NO tools)
def create_exercise_planner_agent(llm) -> Agent:
    """Create an exercise planning agent (NO tools, only planning)"""
    return Agent(
        name="Exercise Planner Agent",
        instructions="""You are an expert fitness trainer and exercise scientist.

Your role is to create detailed, personalized exercise plans based on:
- User's physical stats (age, gender, weight, height, body fat, muscle strength)
- Calculated fitness metrics (BMI, exercise recommendations)
- Fitness goals and experience level
- Medical conditions and safety considerations

When creating exercise plans:
1. Use the provided calculated metrics
2. Design a complete weekly schedule with specific exercises
3. Include sets, reps, rest periods, and progression strategies
4. Provide warm-up and cool-down routines
5. Add safety precautions based on medical conditions
6. Ensure the plan is realistic and sustainable

Create comprehensive, science-based workout plans that are safe and effective.

IMPORTANT: Return your response as a properly structured JSON matching the ExercisePlan schema.""",
        # NO tools here - only structured output
        output_type=ExercisePlan,
        model=llm
    )

def create_diet_planner_agent(llm) -> Agent:
    """Create a diet planning agent (NO tools, only planning)"""
    return Agent(
        name="Diet Planner Agent",
        instructions="""You are an expert nutritionist and registered dietitian.

Your role is to create detailed, personalized nutrition plans based on:
- User's physical stats and metabolic needs
- Calculated nutrition metrics (TDEE, macro targets)
- Fitness goals (muscle gain, fat loss, maintenance)
- Dietary preferences (vegetarian, non-vegetarian, vegan)
- Medical conditions requiring dietary modifications

When creating diet plans:
1. Use the provided calculated metrics
2. Design a complete 7-day meal plan with specific foods and portions
3. Ensure macronutrient targets are met daily
4. Provide meal timing strategies to support training
5. Include hydration and supplement recommendations
6. Account for dietary restrictions and preferences
7. Make meals practical, affordable, and culturally appropriate

Create evidence-based nutrition plans that are sustainable and enjoyable.

IMPORTANT: Return your response as a properly structured JSON matching the DietPlan schema.""",
        # NO tools here - only structured output
        output_type=DietPlan,
        model=llm
    )

def create_synthesis_agent(llm) -> Agent:
    """Create a master planning and synthesis agent"""
    return Agent(
        name="Fitness Synthesis Agent",
        instructions="""You are a master fitness consultant who integrates exercise and nutrition plans.

Your role is to:
1. Analyze the exercise plan provided
2. Analyze the diet plan provided
3. Create a comprehensive, integrated fitness strategy
4. Ensure exercise and nutrition plans work synergistically
5. Provide practical implementation guidance
6. Set realistic timelines and milestones
7. Add motivational strategies and success tips

Create a professional report that includes:
- Executive Summary (2-3 sentences with key recommendation)
- User Profile Analysis (assessment of current state and potential)
- Exercise Plan Overview (summary of training approach)
- Diet Plan Overview (summary of nutrition strategy)
- Integration Strategy (how diet supports training and vice versa)
- Progress Tracking Methods (specific metrics to monitor)
- Weekly Milestones (what to expect week by week)
- Success Tips (psychological and practical advice)
- Safety Reminders (important precautions)
- Confidence Score (0-1 scale based on plan feasibility)

Be encouraging, practical, and evidence-based in your recommendations.

IMPORTANT: Return your response as a properly structured JSON matching the ComprehensiveReport schema.""",
        output_type=ComprehensiveReport,
        model=llm
    )

# ============================================================================
# STEP 4: Fitness Planning System
# ============================================================================

class FitnessPlanningSystem:
    """
    Multi-agent fitness planning system using Two-Phase Planning Pattern:
    Phase 1a: Fitness Calculator (runs tools, no structured output)
    Phase 1b: Nutrition Calculator (runs tools, no structured output)
    Phase 2a: Exercise Planner (uses calculations, structured output)
    Phase 2b: Diet Planner (uses calculations, structured output)
    Phase 3: Synthesis Agent (integrates plans, structured output)
    """
    
    def __init__(self, llm=llm):
        self.llm_ = llm
        
        # Phase 1: Calculator agents (with tools, NO output_type)
        self.fitness_calculator = create_fitness_calculator_agent(self.llm_)
        self.nutrition_calculator = create_nutrition_calculator_agent(self.llm_)
        
        # Phase 2: Planning agents (NO tools, with output_type)
        self.exercise_planner = create_exercise_planner_agent(self.llm_)
        self.diet_planner = create_diet_planner_agent(self.llm_)
        
        # Phase 3: Synthesis agent (NO tools, with output_type)
        self.synthesis_agent = create_synthesis_agent(self.llm_)
    
    async def create_fitness_plan(self, user_data: dict) -> tuple:
        """
        Execute complete fitness planning workflow with two-phase approach
        
        Returns:
            Tuple of (exercise_plan, diet_plan, comprehensive_report)
        """
        
        # Create user profile prompt
        user_prompt = f"""
Create a personalized fitness plan for:

Personal Information:
- Name: {user_data['name']}
- Gender: {user_data['gender']}
- Age: {user_data['age']} years
- Weight: {user_data['weight']} kg
- Height: {user_data['height']} cm
- Body Fat: {user_data['body_fat']}%
- Muscle Strength: {user_data['muscle_strength']} N

Goals & Preferences:
- Diet Preference: {user_data['diet_preference']}
- Fitness Goal: {user_data['goal']}
- Medical Conditions: {user_data['medical_condition']}
"""
        
        # ===================================================================
        # PHASE 1A: Run Fitness Calculator (calculates BMI and exercise recs)
        # ===================================================================
        fitness_calc_prompt = f"""
{user_prompt}

Calculate fitness metrics for this user:
1. Calculate BMI using their weight ({user_data['weight']} kg) and height ({user_data['height']} cm)
2. Get exercise recommendations based on their goal: {user_data['goal']} and body fat: {user_data['body_fat']}%
"""
        
        fitness_calc_result = await Runner.run(
            self.fitness_calculator,
            fitness_calc_prompt
        )
        fitness_metrics = fitness_calc_result.final_output  # String with tool results
        
        # ===================================================================
        # PHASE 1B: Run Nutrition Calculator (calculates TDEE and macro recs)
        # ===================================================================
        nutrition_calc_prompt = f"""
{user_prompt}

Calculate nutrition metrics for this user:
1. Calculate TDEE using weight ({user_data['weight']} kg), height ({user_data['height']} cm), age ({user_data['age']}), gender ({user_data['gender']})
2. Get nutrition recommendations based on goal: {user_data['goal']}, calculated TDEE, weight ({user_data['weight']} kg), and diet preference: {user_data['diet_preference']}
"""
        
        nutrition_calc_result = await Runner.run(
            self.nutrition_calculator,
            nutrition_calc_prompt
        )
        nutrition_metrics = nutrition_calc_result.final_output  # String with tool results
        
        # ===================================================================
        # PHASE 2A: Create Exercise Plan (using calculated metrics)
        # ===================================================================
        exercise_prompt = f"""
{user_prompt}

CALCULATED FITNESS METRICS:
{fitness_metrics}

Using the calculated BMI and exercise recommendations above, create a detailed weekly exercise plan.
Focus on the user's goal: {user_data['goal']}
Consider medical conditions: {user_data['medical_condition']}

Provide a complete exercise plan with weekly schedule, warm-up/cool-down routines, and safety precautions.
"""
        
        exercise_result = await Runner.run(
            self.exercise_planner,
            exercise_prompt
        )
        exercise_plan: ExercisePlan = exercise_result.final_output
        
        # ===================================================================
        # PHASE 2B: Create Diet Plan (using calculated metrics)
        # ===================================================================
        diet_prompt = f"""
{user_prompt}

CALCULATED NUTRITION METRICS:
{nutrition_metrics}

Using the calculated TDEE and nutrition recommendations above, create a detailed 7-day diet plan.
Diet preference: {user_data['diet_preference']}
Goal: {user_data['goal']}
Medical conditions: {user_data['medical_condition']}

Provide a complete diet plan with meal timing, hydration, and supplement recommendations.
"""
        
        diet_result = await Runner.run(
            self.diet_planner,
            diet_prompt
        )
        diet_plan: DietPlan = diet_result.final_output
        
        # ===================================================================
        # PHASE 3: Create Comprehensive Report (synthesize both plans)
        # ===================================================================
        synthesis_prompt = f"""
Create a comprehensive fitness report integrating the following plans:

USER PROFILE:
{user_prompt}

EXERCISE PLAN SUMMARY:
- Goal: {exercise_plan.fitness_goal}
- Schedule: {len(exercise_plan.weekly_schedule)} days per week
- Focus Areas: {', '.join([day.focus for day in exercise_plan.weekly_schedule])}

DIET PLAN SUMMARY:
- Diet Type: {diet_plan.diet_preference}
- Calorie Target: {diet_plan.daily_calorie_target}
- Macros: {diet_plan.macronutrient_split}

Create an integrated report that shows how these plans work together to achieve the user's goals.
"""
        
        synthesis_result = await Runner.run(
            self.synthesis_agent,
            synthesis_prompt
        )
        comprehensive_report: ComprehensiveReport = synthesis_result.final_output
        
        return exercise_plan, diet_plan, comprehensive_report

# ============================================================================
# STEP 5: Streamlit UI
# ============================================================================

def format_exercise_plan(plan: ExercisePlan) -> str:
    """Format exercise plan as readable text"""
    output = f"# Exercise Plan for {plan.user_name}\n\n"
    output += f"**Fitness Goal:** {plan.fitness_goal}\n\n"
    
    output += "## Weekly Schedule\n\n"
    for day in plan.weekly_schedule:
        output += f"### {day.day} - {day.focus}\n"
        output += f"**Duration:** {day.duration}\n\n"
        output += "**Exercises:**\n"
        for i, (exercise, sets_reps) in enumerate(zip(day.exercises, day.sets_reps), 1):
            output += f"{i}. {exercise} - {sets_reps}\n"
        output += f"\n**Notes:** {day.notes}\n\n"
    
    output += f"## Warm-Up Routine\n{plan.warm_up_routine}\n\n"
    output += f"## Cool-Down Routine\n{plan.cool_down_routine}\n\n"
    output += f"## Progressive Overload Strategy\n{plan.progressive_overload_strategy}\n\n"
    output += "## Safety Precautions\n"
    for precaution in plan.safety_precautions:
        output += f"- {precaution}\n"
    
    return output

def format_diet_plan(plan: DietPlan) -> str:
    """Format diet plan as readable text"""
    output = f"# Diet Plan for {plan.user_name}\n\n"
    output += f"**Diet Preference:** {plan.diet_preference}\n"
    output += f"**Daily Calorie Target:** {plan.daily_calorie_target}\n"
    output += f"**Macronutrient Split:** {plan.macronutrient_split}\n\n"
    
    output += "## 7-Day Meal Plan\n\n"
    for day in plan.weekly_meals:
        output += f"### {day.day}\n"
        output += f"**Breakfast:** {day.breakfast}"
        output += f"\n**Mid-Morning Snack:** {day.mid_morning_snack}"
        output += f"\n**Lunch:** {day.lunch}\n"
        output += f"\n**Evening Snack:** {day.evening_snack}"
        output += f"\n**Dinner:** {day.dinner}\n"
        output += f"\n**Daily Totals:** {day.total_calories} | "
        output += f"Protein: {day.protein_grams} | Carbs: {day.carbs_grams} | Fats: {day.fats_grams}\n\n"
    
    output += f"## Meal Timing Guidelines\n{plan.meal_timing_guidelines}\n\n"
    output += f"## Hydration Recommendations\n{plan.hydration_recommendations}\n\n"
    output += "## Supplement Suggestions\n"
    for supplement in plan.supplement_suggestions:
        output += f"- {supplement}\n"
    
    return output

def format_comprehensive_report(report: ComprehensiveReport) -> str:
    """Format comprehensive report as readable text"""
    output = "# Comprehensive Fitness Report\n\n"
    output += f"## Executive Summary\n{report.executive_summary}\n\n"
    output += f"## User Profile Analysis\n{report.user_profile_analysis}\n\n"
    output += f"## Exercise Plan Overview\n{report.exercise_plan_overview}\n\n"
    output += f"## Diet Plan Overview\n{report.diet_plan_overview}\n\n"
    output += f"## Integration Strategy\n{report.integration_strategy}\n\n"
    
    output += "## Progress Tracking Methods\n"
    for method in report.progress_tracking_methods:
        output += f"- {method}\n"
    
    output += "\n## Weekly Milestones\n"
    for milestone in report.weekly_milestones:
        output += f"- {milestone}\n"
    
    output += "\n## Success Tips\n"
    for tip in report.success_tips:
        output += f"- {tip}\n"
    
    output += "\n## Safety Reminders\n"
    for reminder in report.safety_reminders:
        output += f"- {reminder}\n"
    
    output += f"\n**Confidence Score:** {report.confidence_score:.2f}/1.00\n"
    
    return output

def main():
    st.set_page_config(page_title="Fitness & Diet Planner", page_icon="💪", layout="wide")
    
    st.title("🏋️ AI-Powered Fitness & Diet Planner")
    st.markdown("*Powered by OpenAI Agent SDK*")
    st.markdown("---")
    
    # Sidebar for user input
    with st.sidebar:
        st.header("📝 Your Profile")
        
        name = st.text_input("Name", value="Alok")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        age = st.number_input("Age (years)", min_value=10, max_value=100, value=33)
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=71.0, step=0.1)
        height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=169.5, step=0.1)
        body_fat = st.number_input("Body Fat (%)", min_value=5.0, max_value=50.0, value=14.0, step=0.1)
        muscle_strength = st.number_input("Muscle Strength (N)", min_value=10.0, max_value=100.0, value=36.2, step=0.1)
        
        st.markdown("---")
        
        diet_preference = st.selectbox("Diet Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
        goal = st.text_area("Fitness Goal", value="Muscle gain and body fitness")
        medical_condition = st.text_area("Medical Conditions", value="None", 
                                        help="Enter any medical conditions like Diabetes, High BP, etc.")
        
        st.markdown("---")
        generate_button = st.button("🚀 Generate My Plan", type="primary", use_container_width=True)
    
    # Main content area
    if generate_button:
        # Validate API key
        if not os.getenv("OPENAI_API_KEY"):
            st.error("⚠️ OpenAI API key not found! Please set OPENAI_API_KEY environment variable.")
            st.stop()
        
        # Collect user data
        user_data = {
            'name': name,
            'gender': gender,
            'age': age,
            'weight': weight,
            'height': height,
            'body_fat': body_fat,
            'muscle_strength': muscle_strength,
            'diet_preference': diet_preference,
            'goal': goal,
            'medical_condition': medical_condition
        }
        
        # Display user profile
        st.header("👤 Your Profile Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Age", f"{age} years")
            st.metric("Weight", f"{weight} kg")
        with col2:
            st.metric("Height", f"{height} cm")
            st.metric("Body Fat", f"{body_fat}%")
        with col3:
            st.metric("Muscle Strength", f"{muscle_strength} N")
            st.metric("Gender", gender)
        with col4:
            st.metric("Diet", diet_preference)
        
        st.markdown("**Goal:** " + goal)
        st.markdown("**Medical Conditions:** " + medical_condition)
        st.markdown("---")
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Initialize system
            status_text.text("🔧 Initializing AI Agent System...")
            progress_bar.progress(10)
            system = FitnessPlanningSystem(llm=llm)
            
            # Run async agent workflow
            status_text.text("🤖 Running Multi-Agent Fitness Planning System...")
            progress_bar.progress(20)
            
            # Create and run event loop for async operations
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            status_text.text("💪 Exercise Agent: Creating workout plan...")
            progress_bar.progress(30)
            
            # Run the async function
            exercise_plan, diet_plan, comprehensive_report = loop.run_until_complete(
                system.create_fitness_plan(user_data)
            )
            
            progress_bar.progress(100)
            status_text.text("✅ Complete!")
            
            import time
            time.sleep(0.5)
            progress_bar.empty()
            status_text.empty()
            
            # Display results in tabs
            st.header("📊 Your Personalized Fitness Plan")
            
            tab1, tab2, tab3 = st.tabs(["🏋️ Exercise Plan", "🥗 Diet Plan", "📋 Comprehensive Report"])
            
            with tab1:
                exercise_text = format_exercise_plan(exercise_plan)
                st.markdown(exercise_text)
                
                st.download_button(
                    label="📥 Download Exercise Plan",
                    data=exercise_text,
                    file_name=f"{name}_exercise_plan.md",
                    mime="text/markdown"
                )
            
            with tab2:
                diet_text = format_diet_plan(diet_plan)
                st.markdown(diet_text)
                
                st.download_button(
                    label="📥 Download Diet Plan",
                    data=diet_text,
                    file_name=f"{name}_diet_plan.md",
                    mime="text/markdown"
                )
            
            with tab3:
                report_text = format_comprehensive_report(comprehensive_report)
                st.markdown(report_text)
                
                st.download_button(
                    label="📥 Download Complete Report",
                    data=report_text,
                    file_name=f"{name}_fitness_report.md",
                    mime="text/markdown"
                )
            
            st.success("🎉 Your personalized fitness plan is ready!")
            
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("Please make sure your OpenAI API key is valid and you have access to GPT-4.")
    
    else:
        # Welcome message
        st.info("👈 Fill in your profile details in the sidebar and click 'Generate My Plan' to get started!")
        
        st.markdown("""
        ### 🌟 What You'll Get:
        
        #### 🏋️ **Personalized Exercise Plan**
        - Custom workout routines based on your fitness level
        - Detailed exercise schedules with sets and reps
        - Progressive training recommendations
        - Safety guidelines for your medical conditions
        
        #### 🥗 **Customized Diet Plan**
        - Calculated calorie and macro requirements
        - 7-day meal plan tailored to your preferences
        - Meal timing and portion recommendations
        - Supplement suggestions
        
        #### 📋 **Comprehensive Report**
        - Integrated exercise and nutrition strategy
        - Progress tracking recommendations
        - Motivational guidance and tips
        - Timeline for achieving your goals
        
        ---
        
        ### 🤖 Powered by Multi-Agent AI System
        
        This app uses **three specialized AI agents** working together:
        
        1. **Exercise Agent** - Expert fitness trainer with tools:
           - BMI Calculator
           - Exercise Recommendations
        
        2. **Diet Agent** - Professional nutritionist with tools:
           - TDEE Calculator
           - Nutrition Recommendations
        
        3. **Planner Agent** - Master fitness consultant
           - Integrates exercise and diet plans
           - Creates comprehensive reports
        
        Built with **OpenAI Agent SDK** for intelligent, coordinated planning.
        
        ---
        
        ### 📝 Tips for Best Results:
        1. Be honest about your current fitness level
        2. Clearly state your goals
        3. Mention all medical conditions
        4. Follow the plan consistently
        5. Track your progress regularly
        """)

if __name__ == "__main__":
    main()
