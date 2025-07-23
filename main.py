"""Streamlit UI for the Agent MVP."""
import streamlit as st
import os
from agent import run_agent, AgentResult
from parser import AgentResponse
from deck_generator import DeckGenerator, save_deck_to_file
from html_renderer import HTMLRenderer, Theme, render_deck_from_dict
import base64


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


def render_presentation_builder():
    """Render the presentation builder interface."""
    st.header("🎨 Presentation Builder")
    st.markdown("Generate beautiful HTML presentations from structured data.")
    
    # Presentation options
    col1, col2 = st.columns(2)
    
    with col1:
        topic = st.text_input(
            "Presentation Topic",
            placeholder="e.g., Machine Learning Fundamentals",
            help="Enter the topic for your presentation"
        )
        
        num_slides = st.slider(
            "Number of Slides",
            min_value=3,
            max_value=10,
            value=6,
            help="Select how many slides to generate"
        )
    
    with col2:
        theme = st.selectbox(
            "Theme",
            options=["Light", "Dark"],
            help="Choose the visual theme for your presentation"
        )
        
        use_llm = st.checkbox(
            "Use AI for Content Generation",
            value=False,
            help="Enable to use OpenAI for generating presentation content"
        )
    
    # Generate button
    if st.button("🚀 Generate Presentation", type="primary"):
        if not topic:
            st.error("Please enter a presentation topic.")
            return
        
        with st.spinner("Generating presentation..."):
            try:
                # Generate deck
                generator = DeckGenerator(use_llm=use_llm)
                deck = generator.generate_deck(topic, num_slides)
                
                # Save deck JSON
                deck_file = save_deck_to_file(deck, f"{topic.replace(' ', '_')}_deck.json")
                
                # Render HTML
                selected_theme = Theme.DARK if theme == "Dark" else Theme.LIGHT
                html_content = render_deck_from_dict(deck, selected_theme)
                
                # Save HTML file
                html_file = f"{topic.replace(' ', '_')}_presentation.html"
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                st.success(f"✅ Presentation generated successfully!")
                
                # Display preview
                st.subheader("📄 Preview")
                
                # Create download links
                col1, col2 = st.columns(2)
                
                with col1:
                    # Download HTML
                    b64_html = base64.b64encode(html_content.encode()).decode()
                    href_html = f'<a href="data:text/html;base64,{b64_html}" download="{html_file}">📥 Download HTML</a>'
                    st.markdown(href_html, unsafe_allow_html=True)
                
                with col2:
                    # Download JSON
                    with open(deck_file, 'r') as f:
                        json_content = f.read()
                    b64_json = base64.b64encode(json_content.encode()).decode()
                    href_json = f'<a href="data:application/json;base64,{b64_json}" download="{deck_file}">📥 Download JSON</a>'
                    st.markdown(href_json, unsafe_allow_html=True)
                
                # Show deck structure
                with st.expander("📊 Deck Structure", expanded=False):
                    st.json(deck)
                
                # Show HTML preview (limited)
                with st.expander("👁️ HTML Preview", expanded=True):
                    st.components.v1.html(html_content, height=600, scrolling=True)
                    
            except Exception as e:
                st.error(f"Error generating presentation: {str(e)}")
                st.exception(e)
    
    # Sample presentation
    st.markdown("---")
    st.subheader("🎯 Try a Sample")
    
    if st.button("Generate Sample Presentation"):
        with st.spinner("Generating sample..."):
            try:
                generator = DeckGenerator(use_llm=False)
                deck = generator.generate_sample_deck()
                
                # Render in light theme
                html_content = render_deck_from_dict(deck, Theme.LIGHT)
                
                st.success("✅ Sample presentation generated!")
                
                # Show preview
                with st.expander("👁️ Sample Preview", expanded=True):
                    st.components.v1.html(html_content, height=600, scrolling=True)
                
                # Download link
                b64 = base64.b64encode(html_content.encode()).decode()
                href = f'<a href="data:text/html;base64,{b64}" download="sample_presentation.html">📥 Download Sample HTML</a>'
                st.markdown(href, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error generating sample: {str(e)}")


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
        st.warning("⚠️ OpenAI API key not found. Some features may be limited.")
    
    # Navigation
    tab1, tab2 = st.tabs(["🤖 Agent", "🎨 Presentation Builder"])
    
    with tab1:
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
    
    with tab2:
        render_presentation_builder()


if __name__ == "__main__":
    main()