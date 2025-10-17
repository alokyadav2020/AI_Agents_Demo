# 🏋️ AI-Powered Fitness & Diet Planner

An intelligent multi-agent system that creates personalized fitness and diet plans using OpenAI's Agent SDK. This application leverages specialized AI agents working together to deliver comprehensive, science-based workout routines and nutrition plans tailored to individual goals and requirements.

## 🌟 Features

### 💪 Personalized Exercise Plans
- Custom workout routines based on fitness level and goals
- Detailed weekly schedules with specific exercises, sets, and reps
- Warm-up and cool-down routines
- Progressive overload strategies
- Safety precautions based on medical conditions

### 🥗 Customized Diet Plans
- Calculated TDEE (Total Daily Energy Expenditure)
- Personalized macronutrient split (protein, carbs, fats)
- Complete 7-day meal plan with portions
- Meal timing guidelines optimized for training
- Hydration and supplement recommendations
- Support for vegetarian, non-vegetarian, and vegan diets

### 📋 Comprehensive Integration
- Synergistic exercise and nutrition strategy
- Progress tracking methods
- Weekly milestones and expectations
- Success tips and motivational guidance
- Safety reminders tailored to medical conditions
- Confidence score for plan feasibility

## 🤖 Multi-Agent Architecture

The application uses a **Two-Phase Planning Pattern** with five specialized AI agents:

### Phase 1: Calculator Agents (Data Collection)
1. **Fitness Calculator Agent**
   - Calculates BMI (Body Mass Index)
   - Provides exercise type recommendations
   - Uses tools without structured output

2. **Nutrition Calculator Agent**
   - Calculates TDEE and BMR
   - Generates macronutrient recommendations
   - Uses tools without structured output

### Phase 2: Planning Agents (Structured Output)
3. **Exercise Planner Agent**
   - Creates detailed weekly workout plans
   - Designs warm-up/cool-down routines
   - Implements progressive overload strategies
   - Returns structured ExercisePlan output

4. **Diet Planner Agent**
   - Creates 7-day meal plans
   - Ensures macronutrient targets are met
   - Provides meal timing and hydration strategies
   - Returns structured DietPlan output

### Phase 3: Synthesis Agent
5. **Fitness Synthesis Agent**
   - Integrates exercise and nutrition plans
   - Creates comprehensive fitness reports
   - Provides practical implementation guidance
   - Returns structured ComprehensiveReport output

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI Framework**: OpenAI Agent SDK
- **LLM**: Meta Llama (via GROQ API) or Google Gemini
- **Data Validation**: Pydantic
- **Environment**: Python 3.8+

## 📋 Prerequisites

- Python 3.8 or higher
- GROQ API key or Google API key
- Environment variables configured

## 🚀 Installation

1. **Clone the repository**
   ```bash
   cd AI_AGENTS/fitness_agent_app
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   # OR
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## 🎯 Usage

1. **Run the Streamlit application**
   ```bash
   streamlit run app.py
   ```

2. **Fill in your profile**
   - Enter personal information (name, age, gender, weight, height)
   - Provide body composition metrics (body fat %, muscle strength)
   - Select diet preference (Vegetarian/Non-Vegetarian/Vegan)
   - Specify fitness goals
   - List any medical conditions

3. **Generate your plan**
   - Click "🚀 Generate My Plan" button
   - Wait for the multi-agent system to process
   - Review your personalized plans in the tabs

4. **Download your plans**
   - Export Exercise Plan as Markdown
   - Export Diet Plan as Markdown
   - Export Comprehensive Report as Markdown

## 📊 Input Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| Name | Text | Your name | Alok |
| Gender | Select | Male/Female/Other | Male |
| Age | Number | Age in years | 33 |
| Weight | Number | Weight in kilograms | 71.0 |
| Height | Number | Height in centimeters | 169.5 |
| Body Fat | Number | Body fat percentage | 14.0 |
| Muscle Strength | Number | Muscle strength in Newtons | 36.2 |
| Diet Preference | Select | Dietary restrictions | Vegetarian |
| Fitness Goal | Text | Your fitness objectives | Muscle gain and body fitness |
| Medical Conditions | Text | Any health conditions | None/Diabetes/High BP |

## 🧮 Built-in Tools

### BMI Calculator
```python
calculate_bmi(weight_kg, height_cm) -> dict
```
Calculates Body Mass Index and provides weight category classification.

### TDEE Calculator
```python
calculate_tdee(weight_kg, height_cm, age, gender, activity_level) -> dict
```
Calculates Total Daily Energy Expenditure using Mifflin-St Jeor Equation.

### Exercise Recommendations
```python
get_exercise_recommendations(goal, fitness_level, body_fat) -> dict
```
Provides workout split, frequency, and rep range recommendations.

### Nutrition Recommendations
```python
get_nutrition_recommendations(goal, tdee, weight_kg, diet_preference) -> dict
```
Calculates optimal calorie and macronutrient targets.

## 📁 Project Structure

```
fitness_agent_app/
├── app.py                 # Main Streamlit application
├── README.md             # This file
└── .env                  # Environment variables (not tracked)
```

## 🔧 Configuration

### Switching LLM Models

The app supports multiple LLM providers:

**Using GROQ (Default):**
```python
groq_api_key = os.getenv('GROQ_API_KEY')
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
groq_client = AsyncOpenAI(base_url=GROQ_BASE_URL, api_key=groq_api_key)
llm = OpenAIChatCompletionsModel(model="meta-llama/llama-4-scout-17b-16e-instruct", openai_client=groq_client)
```

**Using Google Gemini:**
```python
google_api_key = os.getenv('GOOGLE_API_KEY')
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
google_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)
llm = OpenAIChatCompletionsModel(model="gemini-2.5-pro", openai_client=google_client)
```

## 📝 Output Examples

### Exercise Plan Output
- Weekly schedule (7 days)
- Exercise names with sets/reps
- Duration and rest periods
- Warm-up and cool-down routines
- Progressive overload strategy
- Safety precautions

### Diet Plan Output
- 7-day meal plan
- Breakfast, snacks, lunch, dinner
- Daily calorie and macro totals
- Meal timing guidelines
- Hydration recommendations
- Supplement suggestions

### Comprehensive Report Output
- Executive summary
- User profile analysis
- Exercise and diet plan overviews
- Integration strategy
- Progress tracking methods
- Weekly milestones
- Success tips and safety reminders
- Confidence score (0-1)

## ⚠️ Important Notes

1. **Medical Disclaimer**: This app provides fitness guidance based on AI recommendations. Always consult with healthcare professionals before starting any new fitness or diet program.

2. **API Keys**: Ensure your API keys are properly configured in the `.env` file and never commit them to version control.

3. **Agent Workflow**: The two-phase approach separates tool usage from structured output to avoid JSON mode conflicts with the OpenAI API.

4. **Async Processing**: The app uses asyncio for efficient agent coordination and parallel processing.

## 🐛 Troubleshooting

### Common Issues

**"OpenAI API key not found"**
- Ensure `.env` file exists with correct API key
- Check that `load_dotenv()` is called before accessing keys

**Agent execution errors**
- Verify API key is valid and has sufficient credits
- Check internet connection
- Ensure all required packages are installed

**Structured output errors**
- Verify Pydantic models match agent output types
- Check that planning agents don't use tools (conflict with JSON mode)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is part of the AI_Agents_Demo repository.

## 👨‍💻 Author

Built with ❤️ using OpenAI Agent SDK and Streamlit

## 🔗 Related Projects

Check out other AI agents in the parent directory:
- Data Extraction Agents
- Deep Search OpenAI Agent
- Finance Agent
- Web Research Agent

---

**Built with OpenAI Agent SDK** | **Powered by Multi-Agent Intelligence**
