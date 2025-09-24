import os
import asyncio
from typing import Optional
import streamlit as st
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnableParallel, RunnablePassthrough
from dotenv import load_dotenv
load_dotenv(override=True)

# --- Configuration ---
# Ensure your API key environment variable is set (e.g., OPENAI_API_KEY)
try:
#    llm: Optional[ChatOpenAI] = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    
    llm: Optional[ChatGroq] = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0.7,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
    # other params...
)
  
except Exception as e:
   print(f"Error initializing language model: {e}")
   llm = None

# --- Define Independent Chains ---
# These three chains represent distinct tasks that can be executed in parallel.

summarize_chain: Runnable = (
   ChatPromptTemplate.from_messages([
       ("system", "Summarize the following topic concisely:"),
       ("user", "{topic}")
   ])
   | llm
   | StrOutputParser()
)

questions_chain: Runnable = (
   ChatPromptTemplate.from_messages([
("system", "Generate three interesting questions about the following topic:"),
       ("user", "{topic}")
   ])
   | llm
   | StrOutputParser()
)

terms_chain: Runnable = (
   ChatPromptTemplate.from_messages([
       ("system", "Identify 5-10 key terms from the following topic, separated by commas:"),
       ("user", "{topic}")
   ])
   | llm
   | StrOutputParser()
)

# --- Build the Parallel + Synthesis Chain ---

# 1. Define the block of tasks to run in parallel. The results of these,
#    along with the original topic, will be fed into the next step.
map_chain = RunnableParallel(
   {
       "summary": summarize_chain,
       "questions": questions_chain,
       "key_terms": terms_chain,
       "topic": RunnablePassthrough(),  # Pass the original topic through
   }
)

# 2. Define the final synthesis prompt which will combine the parallel results.
synthesis_prompt = ChatPromptTemplate.from_messages([
   ("system", """Based on the following information:
    Summary: {summary}
    Related Questions: {questions}
    Key Terms: {key_terms}
    Synthesize a comprehensive answer."""),
   ("user", "Original topic: {topic}")
])

# 3. Construct the full chain by piping the parallel results directly
#    into the synthesis prompt, followed by the LLM and output parser.
full_parallel_chain = map_chain | synthesis_prompt | llm | StrOutputParser()

# --- Streamlit App Functions ---
async def run_parallel_analysis(topic: str) -> dict:
   """
   Asynchronously invokes the parallel processing chain with a specific topic
   and returns the results.

   Args:
       topic: The input topic to be processed by the LangChain chains.
   
   Returns:
       Dictionary containing the results or error information.
   """
   if not llm:
       return {"error": "LLM not initialized. Please check your API configuration."}

   try:
       # Run each chain individually to show intermediate results
       summary_result = await summarize_chain.ainvoke(topic)
       questions_result = await questions_chain.ainvoke(topic)
       terms_result = await terms_chain.ainvoke(topic)
       
       # Run the full parallel chain for synthesis
       synthesis_result = await full_parallel_chain.ainvoke(topic)
       
       return {
           "summary": summary_result,
           "questions": questions_result,
           "key_terms": terms_result,
           "synthesis": synthesis_result,
           "error": None
       }
   except Exception as e:
       return {"error": f"An error occurred during chain execution: {e}"}

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Parallel LangChain Analysis",
        page_icon="🔗",
        layout="wide"
    )
    
    st.title("🔗 Parallel LangChain Topic Analysis")
    st.markdown("This app demonstrates parallel processing with LangChain by analyzing a topic through multiple chains simultaneously.")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        if llm:
            st.success("✅ LLM initialized successfully")
            if hasattr(llm, 'model_name'):
                st.write(f"Model: {llm.model_name}")
            elif hasattr(llm, 'model'):
                st.write(f"Model: {llm.model}")
        else:
            st.error("❌ LLM not initialized")
            st.write("Please check your API key configuration")
    
    # Main interface
    st.header("📝 Topic Input")
    topic = st.text_area(
        "Enter a topic to analyze:",
        value="The history of AI and its impact on modern technology.",
        height=100,
        help="Enter any topic you'd like to analyze. The system will generate a summary, questions, key terms, and a synthesis."
    )
    
    if st.button("🚀 Analyze Topic", type="primary"):
        if not topic.strip():
            st.error("Please enter a topic to analyze.")
            return
        
        with st.spinner("Running parallel analysis..."):
            # Run the async function
            try:
                results = asyncio.run(run_parallel_analysis(topic))
            except Exception as e:
                st.error(f"Error running analysis: {e}")
                return
        
        if results.get("error"):
            st.error(results["error"])
            return
        
        # Display results
        st.header("📊 Analysis Results")
        
        # Create columns for parallel results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("📋 Summary")
            st.write(results.get("summary", "No summary generated"))
        
        with col2:
            st.subheader("❓ Related Questions")
            st.write(results.get("questions", "No questions generated"))
        
        with col3:
            st.subheader("🔑 Key Terms")
            st.write(results.get("key_terms", "No key terms generated"))
        
        # Synthesis result in full width
        st.subheader("🎯 Comprehensive Analysis")
        st.write(results.get("synthesis", "No synthesis generated"))
        
        # Add download option
        if st.button("📥 Download Results"):
            results_text = f"""
Topic: {topic}

Summary:
{results.get('summary', 'N/A')}

Related Questions:
{results.get('questions', 'N/A')}

Key Terms:
{results.get('key_terms', 'N/A')}

Comprehensive Analysis:
{results.get('synthesis', 'N/A')}
"""
            st.download_button(
                label="Download as Text File",
                data=results_text,
                file_name="topic_analysis.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()
