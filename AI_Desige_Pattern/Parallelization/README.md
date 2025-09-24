# Parallel LangChain Streamlit App

This Streamlit application demonstrates parallel processing with LangChain by analyzing a topic through multiple chains simultaneously.

## Features

- **Parallel Processing**: Runs three analysis chains simultaneously:
  - Topic summarization
  - Question generation
  - Key terms extraction
- **Synthesis**: Combines all parallel results into a comprehensive analysis
- **Interactive UI**: Clean Streamlit interface for easy topic input and result viewing
- **Download Results**: Option to download analysis results as a text file

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

1. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```

2. Edit the `.env` file and add your API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```
   
   Or if using OpenAI:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### 3. Run the Application

#### Option 1: Using the batch file (Windows)
Double-click `run_app.bat` or run:
```cmd
run_app.bat
```

#### Option 2: Using Python script
```bash
python run_streamlit_app.py
```

#### Option 3: Direct Streamlit command
```bash
streamlit run Parallelization_langchain_streamlit.py
```

## Usage

1. Start the application using one of the methods above
2. Open your browser to `http://localhost:8501`
3. Enter a topic you want to analyze in the text area
4. Click "🚀 Analyze Topic" to start the parallel processing
5. View the results in the organized sections:
   - **Summary**: Concise topic overview
   - **Related Questions**: Three interesting questions about the topic
   - **Key Terms**: 5-10 important terms related to the topic
   - **Comprehensive Analysis**: Synthesized analysis combining all results
6. Optionally download the results as a text file

## Configuration

The app currently uses Groq's Qwen model by default. You can modify the LLM configuration in the code:

```python
llm: Optional[ChatGroq] = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0.7,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
)
```

To switch to OpenAI, uncomment the OpenAI configuration and comment out the Groq configuration.

## File Structure

- `Parallelization_langchain_streamlit.py` - Main Streamlit application
- `run_streamlit_app.py` - Python script to launch the app
- `run_app.bat` - Windows batch file for easy launching
- `.env.example` - Template for environment variables
- `README.md` - This file

## Requirements

- Python 3.7+
- streamlit
- langchain-core
- langchain-groq
- langchain-openai (optional)
- python-dotenv

## Troubleshooting

1. **LLM not initialized error**: Check that your API key is correctly set in the `.env` file
2. **Import errors**: Make sure all requirements are installed with `pip install -r requirements.txt`
3. **Connection issues**: Verify your internet connection and API key validity

## Example Topics

Try these example topics to see the app in action:

- "The history of AI and its impact on modern technology"
- "Climate change and renewable energy solutions"
- "The future of space exploration"
- "Blockchain technology and cryptocurrency"
- "Mental health in the digital age"