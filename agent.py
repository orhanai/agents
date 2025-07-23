"""Agent module for orchestrating the plan-think-act loop."""
import os
from typing import List, Dict, Any
from dataclasses import dataclass
import openai
from parser import parse_plan, parse_agent_response, AgentResponse


@dataclass
class AgentResult:
    """Result from running the agent."""
    plan_items: List[str]
    log: List[AgentResponse]
    final_answer: str = None


def run_agent(prompt: str) -> AgentResult:
    """
    Run the agent on a given prompt.
    
    1. Plan phase: Generate a numbered checklist of subtasks
    2. Execution phase: For each subtask, think and act
    
    Args:
        prompt: User's task/question
        
    Returns:
        AgentResult containing plan items and execution log
    """
    # Initialize OpenAI client
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Phase 1: Generate Plan
    plan_prompt = f"Task: {prompt}\nGenerate a Plan: list each subtask as a numbered checklist."
    
    plan_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that breaks down tasks into numbered steps."},
            {"role": "user", "content": plan_prompt}
        ],
        temperature=0.7
    )
    
    plan_text = plan_response.choices[0].message.content
    plan_items = parse_plan(plan_text)
    
    # Initialize log
    log: List[AgentResponse] = []
    
    # Phase 2: Execute each plan item
    for item in plan_items:
        # Add plan item to log
        log.append(AgentResponse(type="PlanItem", content=item))
        
        # Initialize conversation for this subtask
        messages = [
            {"role": "system", "content": """You are an agent that thinks step by step.
When given a subtask:
1. First respond with "Thought:" followed by your reasoning
2. Then either:
   - "Action: Search('query')" to search for information
   - "Final Answer: your answer" when you have enough information"""},
            {"role": "user", "content": f"Subtask: {item}\nThought:"}
        ]
        
        # Execute subtask loop
        while True:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7
            )
            
            response_text = response.choices[0].message.content
            
            # Parse the response
            parsed = parse_agent_response("Thought: " + response_text)
            log.append(parsed)
            
            # Add to conversation
            messages.append({"role": "assistant", "content": response_text})
            
            # Check if we need to continue
            messages.append({"role": "user", "content": "Continue:"})
            
            continue_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7
            )
            
            continue_text = continue_response.choices[0].message.content
            continue_parsed = parse_agent_response(continue_text)
            
            if continue_parsed.type == "Action":
                # Execute the action (simulate search)
                log.append(continue_parsed)
                
                # Simulate search results
                observation = _execute_action(continue_parsed)
                obs_response = AgentResponse(type="Observation", content=observation)
                log.append(obs_response)
                
                # Add to conversation
                messages.append({"role": "assistant", "content": continue_text})
                messages.append({"role": "user", "content": f"Observation: {observation}\nContinue:"})
                
            elif continue_parsed.type == "Answer":
                # Final answer reached
                log.append(continue_parsed)
                break
            else:
                # Add to log and continue
                log.append(continue_parsed)
                messages.append({"role": "assistant", "content": continue_text})
    
    # Extract final answer from log
    final_answer = None
    for entry in reversed(log):
        if entry.type == "Answer":
            final_answer = entry.content
            break
    
    return AgentResult(
        plan_items=plan_items,
        log=log,
        final_answer=final_answer
    )


def _execute_action(action: AgentResponse) -> str:
    """
    Execute an action and return the observation.
    
    For this MVP, we simulate search results.
    In a real implementation, this would call actual tools.
    """
    if action.metadata and action.metadata.get("name") == "Search":
        query = action.metadata.get("params", "")
        
        # Simulate search results based on common queries
        if "bitcoin ticker" in query.lower():
            return "BTC"
        elif "price of btc" in query.lower() or "bitcoin price" in query.lower():
            return "It's $54,000"
        elif "weather" in query.lower():
            return "It's 72°F and sunny"
        else:
            return f"Search results for '{query}': Various relevant information found."
    
    return "Action executed successfully."