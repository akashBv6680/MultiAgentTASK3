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
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent_responses' not in st.session_state:
    st.session_state.agent_responses = {}

# Initialize Gemini API
@st.cache_resource
def initialize_gemini():
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai

# Multi-Agent Functions
async def research_agent(task: str, model_name: str, temperature: float, max_tokens: int):
    """Research Agent - Gathers information about the task"""
    client = genai.Client(api_key=st.secrets.get("GEMINI_API_KEY"))
    prompt = f"""As a Research Agent, analyze and gather information about the following task:
{task}

Provide comprehensive research findings, relevant insights, and important considerations."""
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        generation_config={
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }
    )
    return response.text

async def analysis_agent(task: str, model_name: str, temperature: float, max_tokens: int):
    """Analysis Agent - Analyzes the task and provides insights"""
    client = genai.Client(api_key=st.secrets.get("GEMINI_API_KEY"))
    prompt = f"""As an Analysis Agent, thoroughly analyze the following task and provide detailed insights:
{task}

Break down the problem, identify key components, and provide strategic recommendations."""
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        generation_config={
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }
    )
    return response.text

async def planning_agent(task: str, model_name: str, temperature: float, max_tokens: int):
    """Planning Agent - Creates a strategic plan"""
    client = genai.Client(api_key=st.secrets.get("GEMINI_API_KEY"))
    prompt = f"""As a Planning Agent, create a detailed strategic plan for:
{task}

Include phases, milestones, resources needed, timelines, and success metrics."""
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        generation_config={
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }
    )
    return response.text

async def execution_agent(task: str, model_name: str, temperature: float, max_tokens: int):
    """Execution Agent - Proposes implementation steps"""
    client = genai.Client(api_key=st.secrets.get("GEMINI_API_KEY"))
    prompt = f"""As an Execution Agent, propose concrete implementation steps for:
{task}

Provide step-by-step instructions, code examples if applicable, and best practices."""
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        generation_config={
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }
    )
    return response.text

# Main UI
st.title("🤖 Multi-Agent AI System - Task 3")
st.markdown("**Advanced AI Agent Framework with Gemini 2.5 Flash**")
st.markdown("""Powered by:
- 🧠 Google Gemini 2.5 Flash
- 🔄 Multi-Agent Architecture
- ☁️ Streamlit Cloud Deployment""")

# ============ SIDEBAR CONFIGURATION ============
with st.sidebar:
    st.title("⚙️ Configuration")
    
    # Agent Selection
    st.subheader("👥 Select Agents")
    researcher_enabled = st.checkbox("🔍 Research Agent", value=True)
    analyzer_enabled = st.checkbox("📊 Analysis Agent", value=True)
    planner_enabled = st.checkbox("📋 Planning Agent", value=True)
    executor_enabled = st.checkbox("⚡ Execution Agent", value=True)
    
    st.divider()
    
    # Task Input
    st.subheader("📝 Task Configuration")
    task_input = st.text_area(
        "Enter your task:",
        placeholder="Describe the task for the multi-agent system...",
        height=100
    )
    
    # Submit Button for Task Entry
    col_submit = st.columns([0.85, 0.15])
    with col_submit[1]:
        if st.button("📤 Enter", key="task_submit", use_container_width=True):
            if task_input.strip():
                st.toast("✅ Task received! Click 'Run Multi-Agent System' to proceed.", icon="✅")
            else:
                st.warning("⚠️ Please enter a task description")
    
    st.divider()
    
    # Model Settings
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
        help="Controls randomness: lower = deterministic, higher = creative"
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
        if client:
            st.success("✅ Gemini API Connected")
        else:
            st.error("❌ API Key not found in secrets")
    except Exception as e:
        st.error(f"❌ API Error: {str(e)}")

# ============ MAIN CONTENT AREA ============
# Tabs for different sections
tab1, tab2, tab3 = st.tabs(["🎯 Run Agents", "📊 Task History", "ℹ️ About"])

with tab1:
    st.subheader("Multi-Agent Execution")
    
    # Run and Clear buttons
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
        st.session_state.agent_responses = {}
        st.rerun()
    
    if run_button and task_input:
        progress_bar = st.progress(0)
        status_placeholder = st.empty()
        
        agents_to_run = []
        if researcher_enabled:
            agents_to_run.append(("Research Agent", research_agent, "🔍"))
        if analyzer_enabled:
            agents_to_run.append(("Analysis Agent", analysis_agent, "📊"))
        if planner_enabled:
            agents_to_run.append(("Planning Agent", planning_agent, "📋"))
        if executor_enabled:
            agents_to_run.append(("Execution Agent", execution_agent, "⚡"))
        
        total_agents = len(agents_to_run)
        st.session_state.agent_responses = {}
        
        for idx, (agent_name, agent_func, emoji) in enumerate(agents_to_run):
            status_placeholder.info(f"{emoji} {agent_name} is running...")
            
            try:
                response = asyncio.run(agent_func(task_input, model_name, temperature, max_tokens))
                st.session_state.agent_responses[agent_name] = response
                
                # Display agent result
                with st.expander(f"{emoji} {agent_name} - COMPLETED ✅", expanded=(idx < 1)):
                    st.markdown(response)
                
            except Exception as e:
                st.error(f"❌ Error in {agent_name}: {str(e)}")
                st.session_state.agent_responses[agent_name] = f"Error: {str(e)}"
            
            progress_bar.progress((idx + 1) / total_agents)
        
        status_placeholder.success("✅ All agents completed successfully!")

with tab2:
    st.subheader("Task History & Responses")
    if st.session_state.agent_responses:
        st.markdown(f"**Task:** {task_input}")
        st.markdown(f"**Model:** {model_name}")
        st.markdown(f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        st.divider()
        
        for agent_name, response in st.session_state.agent_responses.items():
            with st.expander(f"{agent_name}"):
                st.markdown(response)
    else:
        st.info("No task history yet. Run the agents to see results here.")

with tab3:
    st.subheader("About this Application")
    st.markdown("""
    ### 🤖 Multi-Agent Task 3 - Advanced AI Framework
    
    **Features:**
    - 🐝 Specialized AI Agents (Research, Analysis, Planning, Execution)
    - 🧠 Powered by Google Gemini 2.5 Flash
    - ☁️ Deployed on Streamlit Cloud
    - 📊 Multi-task Processing
    - 📋 Task History Tracking
    
    **Architecture:**
    1. **Research Agent 🔍** - Gathers and processes information
    2. **Analysis Agent 📊** - Analyzes data and extracts insights
    3. **Planning Agent 📋** - Creates strategic plans
    4. **Execution Agent ⚡** - Proposes implementation steps
    
    **How to Use:**
    1. Enter your task in the sidebar
    2. Click the Enter button to confirm
    3. Configure model settings if needed
    4. Click 'Run Multi-Agent System' to execute
    5. View results in the Run Agents tab
    """)

# Footer
st.divider()
st.caption("🤖 Multi-Agent Task 3 - Streamlit Cloud Deployment | Powered by Gemini 2.5 Flash")
