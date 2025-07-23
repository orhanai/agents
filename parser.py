"""Parser module for extracting structured information from LLM responses."""
import re
from typing import List, Dict, Any, Literal, Union
from dataclasses import dataclass


ResponseType = Literal["Plan", "PlanItem", "Thought", "Action", "Observation", "Answer"]


@dataclass
class AgentResponse:
    """Represents a parsed agent response."""
    type: ResponseType
    content: str
    metadata: Dict[str, Any] = None


def parse_plan(text: str) -> List[str]:
    """
    Parse a plan from LLM response text.
    Extracts numbered items from the response.
    
    Args:
        text: Raw LLM response containing a numbered plan
        
    Returns:
        List of plan items (without numbers)
    """
    # Look for numbered items (1. 2. 3. etc)
    pattern = r'^\s*\d+\.\s*(.+)$'
    plan_items = []
    
    for line in text.split('\n'):
        match = re.match(pattern, line)
        if match:
            plan_items.append(match.group(1).strip())
    
    return plan_items


def parse_agent_response(text: str) -> AgentResponse:
    """
    Parse agent response to determine its type and content.
    
    Recognizes:
    - Plan: Full plan text
    - PlanItem: Individual plan item
    - Thought: Chain-of-thought reasoning
    - Action: Tool invocation (e.g., "Action: Search('query')")
    - Observation: Result from tool execution
    - Answer: Final answer
    
    Args:
        text: Raw text to parse
        
    Returns:
        AgentResponse with type and content
    """
    text = text.strip()
    
    # Check for explicit type prefixes
    if text.startswith("Plan:"):
        return AgentResponse(type="Plan", content=text[5:].strip())
    
    if text.startswith("PlanItem:"):
        return AgentResponse(type="PlanItem", content=text[9:].strip())
    
    if text.startswith("Thought:"):
        return AgentResponse(type="Thought", content=text[8:].strip())
    
    if text.startswith("Action:"):
        # Extract action and parameters
        action_content = text[7:].strip()
        # Try to parse action format like Search("query")
        action_match = re.match(r'(\w+)\((.*)\)', action_content)
        if action_match:
            action_name = action_match.group(1)
            action_params = action_match.group(2).strip('"\'')
            return AgentResponse(
                type="Action", 
                content=action_content,
                metadata={"name": action_name, "params": action_params}
            )
        return AgentResponse(type="Action", content=action_content)
    
    if text.startswith("Observation:"):
        return AgentResponse(type="Observation", content=text[12:].strip())
    
    if text.startswith("Final Answer:") or text.startswith("Answer:"):
        prefix_len = 13 if text.startswith("Final Answer:") else 7
        return AgentResponse(type="Answer", content=text[prefix_len:].strip())
    
    # Default to Thought if no explicit prefix
    return AgentResponse(type="Thought", content=text)