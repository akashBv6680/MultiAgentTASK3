#!/usr/bin/env python3
"""
Streamlit Multi-Agent AI System - Task 3
Advanced Multi-Agent Framework with Gemini 2.5 Flash Integration
Deployed on Streamlit Cloud
"""

import streamlit as st
import os
import asyncio
from datetime import datetime
from google import genai
from typing import Optional

# Page configuration
st.set_page_config(
    page_title="🤖 Multi-Agent Task 3",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .agent-box {
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #1f77b4;
        margin: 1rem 0;
        background-color: #f0f2f6;
    }
    .agent-status {
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        display: inline-block;
    }
    .status-active {
        background-color: #90EE90;
        color: #000;
    }
    .status-completed {
        background-color: #87CEEB;
        color: #000;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize Gemini client from Streamlit secrets
@st.cache_resource
def initialize_gemini():
    """Initialize Gemini API client"""
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        st.error("❌ GEMINI_API_KEY not found in Streamlit secrets!")
        st.info("Please add your API key to .streamlit/secrets.toml or Streamlit Cloud secrets")
        st.stop()
    return genai.Client(api_key=api_key)

# Initialize session state
if 'agent_responses' not in st.session_state:
    st.session_state.agent_responses = []
if 'task_history' not in st.session_state:
    st.session_state.task_history = []

# Main UI
st.title("🤖 Multi-Agent AI System - Task 3")
st.markdown("""
**Advanced AI Agent Framework with Gemini 2.5 Flash**

Powered by:
- 🧠 Google Gemini 2.5 Flash
- 🔄 Multi-Agent Architecture
- ☁️ Streamlit Cloud Deployment
""")

# Sidebar configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    st.divider()
    
    # Agent selection
    st.subheader("👥 Select Agents")
    researcher_enabled = st.checkbox("🔍 Research Agent", value=True)
    analyzer_enabled = st.checkbox("📊 Analysis Agent", value=True)
    planner_enabled = st.checkbox("📋 Planning Agent", value=True)
    executor_enabled = st.checkbox("⚡ Execution Agent", value=True)
    
    st.divider()
    
    # Task input
    st.subheader("📝 Task Configuration")
    task_input = st.text_area(
        "Enter your task:",
        placeholder="Describe the task for the multi-agent system...",
        height=100
    )


    # Submit button for task entry
col_submit = st.columns([0.85, 0.15])
with col_submit[1]:
    if st.button("📤 Enter", key="task_submit", use_container_width=True, help="Submit your task"):
        if task_input.strip():
            # Task will be processed with the Run Multi-Agent System button
            st.toast("✅ Task received! Click 'Run Multi-Agent System' to proceed.", icon="✅")
        else:
            st.warning("⚠️ Please enter a task description")

    
    # Model settings
    st.subheader("🔧 Model Settings")
    model_name = st.selectbox(
        "Select Gemini Model",
        ["gemini-2.5-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
        index=0
    )
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Controls randomness: lower = more deterministic, higher = more creative"
    )
    
    max_tokens = st.number_input(
        "Max Tokens",
        min_value=100,
        max_value=4096,
        value=1024,
        step=100
    )
    
    st.divider()
    
    # API Status
    st.subheader("📊 API Status")
    try:
        client = initialize_gemini()
        st.success("✅ Gemini API Connected")
    except Exception as e:
        st.error(f"❌ API Error: {str(e)}")

# Main content area
tab1, tab2, tab3 = st.tabs(["🎯 Run Agents", "📊 Task History", "ℹ️ About"])

with tab1:
    st.subheader("Multi-Agent Execution")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        run_button = st.button(
            "🚀 Run Multi-Agent System",
            type="primary",
            use_container_width=True,
            disabled=not task_input
        )
    
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    if clear_button:
        st.session_state.agent_responses = []
        st.rerun()
    
    if run_button and task_input:
        st.info(f"🔄 Processing task: {task_input[:50]}...")
        
        try:
            client = initialize_gemini()
            
            # Create agent configuration
            agents_config = {
                "researcher": researcher_enabled,
                "analyzer": analyzer_enabled,
                "planner": planner_enabled,
                "executor": executor_enabled
            }
            
            enabled_agents = [k for k, v in agents_config.items() if v]
            
            # Process through each agent
            for agent_type in enabled_agents:
                with st.container():
                    st.markdown(f"<div class='agent-box'>", unsafe_allow_html=True)
                    
                    if agent_type == "researcher":
                        agent_emoji = "🔍"
                        agent_name = "Research Agent"
                        agent_prompt = f"As a Research Agent, gather and analyze information about: {task_input}"
                    elif agent_type == "analyzer":
                        agent_emoji = "📊"
                        agent_name = "Analysis Agent"
                        agent_prompt = f"As an Analysis Agent, analyze and extract insights from: {task_input}"
                    elif agent_type == "planner":
                        agent_emoji = "📋"
                        agent_name = "Planning Agent"
                        agent_prompt = f"As a Planning Agent, create a strategic plan for: {task_input}"
                    else:  # executor
                        agent_emoji = "⚡"
                        agent_name = "Execution Agent"
                        agent_prompt = f"As an Execution Agent, propose implementation steps for: {task_input}"
                    
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"### {agent_emoji} {agent_name}")
                    with col2:
                        st.markdown(f"<span class='agent-status status-active'>ACTIVE</span>", unsafe_allow_html=True)
                    
                    # Call Gemini API
                    with st.spinner(f"Processing with {agent_name}..."):
                        response = client.models.generate_content(
                            model=model_name,
                            contents=agent_prompt,
                            config={
                                "temperature": temperature,
                                "max_output_tokens": max_tokens,
                            }
                        )
                        
                        response_text = response.text
                        
                        # Store in session
                        st.session_state.agent_responses.append({
                            "agent": agent_name,
                            "response": response_text,
                            "timestamp": datetime.now().isoformat()
                        })
                        
                        st.markdown(response_text)
                        st.markdown(f"<span class='agent-status status-completed'>COMPLETED</span>", unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.divider()
            
            st.success("✅ All agents completed successfully!")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Make sure your GEMINI_API_KEY is configured correctly.")

with tab2:
    st.subheader("📊 Task History")
    
    if st.session_state.agent_responses:
        for idx, item in enumerate(st.session_state.agent_responses, 1):
            with st.expander(f"{idx}. {item['agent']} - {item['timestamp']}"):
                st.markdown(item['response'])
                st.caption(f"Timestamp: {item['timestamp']}")
    else:
        st.info("No tasks executed yet. Run the Multi-Agent System to see results.")

with tab3:
    st.subheader("About this Application")
    st.markdown("""
    ## 🤖 Multi-Agent Task 3
    
    **Advanced AI Agent Framework** with Gemini 2.5 Flash Integration
    
    ### Features:
    - ✨ Specialized AI Agents (Research, Analysis, Planning, Execution)
    - 🧠 Powered by Google Gemini 2.5 Flash
    - ☁️ Deployed on Streamlit Cloud
    - 🔄 Multi-task Processing
    - 📊 Task History Tracking
    
    ### Architecture:
    1. **Research Agent** 🔍 - Gathers and processes information
    2. **Analysis Agent** 📊 - Analyzes data and extracts insights
    3. **Planning Agent** 📋 - Creates strategic plans
    4. **Execution Agent** ⚡ - Proposes implementation steps
    
    ### Configuration:
    - Model: Gemini 2.5 Flash (Latest)
    - API: Google GenAI
    - Deployment: Streamlit Cloud
    
    ### Requirements:
    - Python 3.9+
    - Streamlit >= 1.28.0
    - google-genai >= 0.3.0
    - Valid Gemini API Key
    
    ### Setup Instructions:
    1. Clone the repository
    2. Install dependencies: `pip install -r requirements.txt`
    3. Add GEMINI_API_KEY to `.streamlit/secrets.toml`
    4. Run: `streamlit run main.py`
    
    ### Streamlit Cloud Deployment:
    1. Push code to GitHub
    2. Connect to Streamlit Cloud
    3. Add GEMINI_API_KEY to Secrets
    4. Deploy!
    
    ### Author
    **Akash BV** - AI/ML Engineer
    - GitHub: [@akashBv6680](https://github.com/akashBv6680)
    - Portfolio: Multi-Agent AI Systems
    """)

# Footer
st.divider()
st.caption("🤖 Multi-Agent Task 3 - Streamlit Cloud Deployment | Powered by Gemini 2.5 Flash")
