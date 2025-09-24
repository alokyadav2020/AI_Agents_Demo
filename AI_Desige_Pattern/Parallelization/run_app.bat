@echo off
echo Starting Parallel LangChain Streamlit App...
echo.
echo Make sure you have:
echo 1. Installed requirements: pip install -r requirements.txt
echo 2. Set your API keys in .env file (GROQ_API_KEY or OPENAI_API_KEY)
echo.
echo Opening browser at: http://localhost:8501
echo To stop the app, press Ctrl+C in this terminal
echo.
pause
streamlit run Parallelization_langchain_streamlit.py --server.port 8501 --server.address localhost