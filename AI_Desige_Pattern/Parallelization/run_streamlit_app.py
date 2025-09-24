#!/usr/bin/env python3
"""
Simple script to run the Parallel LangChain Streamlit app.
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit app"""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_file = os.path.join(script_dir, "Parallelization_langchain_streamlit.py")
    
    # Check if the app file exists
    if not os.path.exists(app_file):
        print(f"Error: App file not found at {app_file}")
        sys.exit(1)
    
    print("Starting Parallel LangChain Streamlit App...")
    print(f"App file: {app_file}")
    print("Opening browser at: http://localhost:8501")
    print("\nTo stop the app, press Ctrl+C in the terminal")
    print("-" * 50)
    
    try:
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", app_file,
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\nApp stopped by user")
    except Exception as e:
        print(f"Error running app: {e}")

if __name__ == "__main__":
    main()