"""Streamlit UI for the Agent MVP."""
import streamlit as st
import os
from agent import run_agent, AgentResult
from parser import AgentResponse


def format_log_entry(entry: AgentResponse) -> str:
    """Format a log entry for display."""
    type_emoji = {
        "PlanItem": "📋",
        "Thought": "💭",
        "Action": "🔧",
        "Observation": "👁️",
        "Answer": "✅"
    }
    
    emoji = type_emoji.get(entry.type, "📝")
    return f"{emoji} **{entry.type}:** {entry.content}"


def main():
    st.set_page_config(
        page_title="Streamlit Agent MVP",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Streamlit Agent MVP")
    st.markdown("An LLM agent that can plan, think, and act to solve tasks.")
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        st.error("Please set your OPENAI_API_KEY environment variable.")
        st.stop()
    
    # Input section
    with st.container():
        st.subheader("Task Input")
        user_input = st.text_area(
            "Enter your task or question:",
            placeholder="e.g., Get current price of Bitcoin",
            height=100
        )
        
        col1, col2 = st.columns([1, 5])
        with col1:
            run_button = st.button("🚀 Run", type="primary", use_container_width=True)
    
    # Results section
    if run_button and user_input:
        with st.spinner("Agent is thinking..."):
            try:
                result = run_agent(user_input)
                
                # Display results in two columns
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.subheader("📝 Plan")
                    for i, item in enumerate(result.plan_items, 1):
                        st.markdown(f"{i}. {item}")
                
                with col2:
                    st.subheader("📊 Execution Log")
                    
                    # Group log entries by plan item
                    current_plan_item = None
                    for entry in result.log:
                        if entry.type == "PlanItem":
                            if current_plan_item is not None:
                                st.markdown("---")
                            current_plan_item = entry.content
                            st.markdown(f"### {format_log_entry(entry)}")
                        else:
                            st.markdown(format_log_entry(entry))
                    
                    # Display final answer prominently
                    if result.final_answer:
                        st.markdown("---")
                        st.success(f"**Final Answer:** {result.final_answer}")
                        
            except Exception as e:
                st.error(f"Error running agent: {str(e)}")
                st.exception(e)
    
    # Instructions
    with st.expander("ℹ️ How it works"):
        st.markdown("""
        1. **Enter a task** - Type your question or task in the input area
        2. **Click Run** - The agent will create a plan and execute it
        3. **Watch the process** - See the agent's plan and step-by-step execution
        
        The agent follows this process:
        - **Plan**: Breaks down your task into subtasks
        - **Think**: Reasons about each subtask
        - **Act**: Executes actions (like search) when needed
        - **Observe**: Processes results from actions
        - **Answer**: Provides a final response
        """)


if __name__ == "__main__":
    main()