"""Agent module for orchestrating the plan-think-act loop."""

import os
import logging
from typing import List, Dict, Any
from dataclasses import dataclass
import openai
from dotenv import load_dotenv
from parser import parse_plan, parse_agent_response, AgentResponse

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("agent.log")],
)
logger = logging.getLogger(__name__)


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
    logger.info(f"🚀 Starting agent with prompt: {prompt}")

    # Initialize OpenAI client
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    logger.info("✅ OpenAI client initialized")

    # Phase 1: Generate Plan
    logger.info("📋 Phase 1: Generating plan...")
    plan_prompt = (
        f"Task: {prompt}\nGenerate a Plan: list each subtask as a numbered checklist."
    )

    plan_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that breaks down tasks into numbered steps.",
            },
            {"role": "user", "content": plan_prompt},
        ],
        temperature=0.7,
    )

    plan_text = plan_response.choices[0].message.content
    logger.info(f"📝 Generated plan text: {plan_text}")

    plan_items = parse_plan(plan_text)
    logger.info(f"✅ Parsed {len(plan_items)} plan items: {plan_items}")

    # Initialize log
    log: List[AgentResponse] = []
    logger.info("🔧 Phase 2: Starting plan execution...")

    # Phase 2: Execute each plan item
    for i, item in enumerate(plan_items, 1):
        logger.info(f"🎯 Executing plan item {i}/{len(plan_items)}: {item}")

        # Add plan item to log
        log.append(AgentResponse(type="PlanItem", content=item))

        # Initialize conversation for this subtask
        messages = [
            {
                "role": "system",
                "content": """You are an agent that thinks step by step.
When given a subtask:
1. First respond with "Thought:" followed by your reasoning
2. Then either:
   - "Action: Search('query')" to search for information
   - "Final Answer: your answer" when you have enough information""",
            },
            {"role": "user", "content": f"Subtask: {item}\nThought:"},
        ]

        # Execute subtask loop
        subtask_step = 1
        while True:
            logger.info(f"💭 Subtask step {subtask_step}: Getting initial thought...")

            response = client.chat.completions.create(
                model="gpt-3.5-turbo", messages=messages, temperature=0.7
            )

            response_text = response.choices[0].message.content
            logger.info(f"💭 Thought response: {response_text}")

            # Parse the response
            parsed = parse_agent_response("Thought: " + response_text)
            log.append(parsed)

            # Add to conversation
            messages.append({"role": "assistant", "content": response_text})

            # Check if we need to continue
            messages.append({"role": "user", "content": "Continue:"})

            logger.info("⏭️ Asking agent to continue...")

            continue_response = client.chat.completions.create(
                model="gpt-3.5-turbo", messages=messages, temperature=0.7
            )

            continue_text = continue_response.choices[0].message.content
            continue_parsed = parse_agent_response(continue_text)
            logger.info(
                f"⏭️ Continue response ({continue_parsed.type}): {continue_text}"
            )

            if continue_parsed.type == "Action":
                # Execute the action (simulate search)
                logger.info(f"🔍 Executing action: {continue_parsed.content}")
                log.append(continue_parsed)

                # Simulate search results
                observation = _execute_action(continue_parsed)
                logger.info(f"👀 Action observation: {observation}")
                obs_response = AgentResponse(type="Observation", content=observation)
                log.append(obs_response)

                # Add to conversation
                messages.append({"role": "assistant", "content": continue_text})
                messages.append(
                    {
                        "role": "user",
                        "content": f"Observation: {observation}\nContinue:",
                    }
                )
                subtask_step += 1

            elif continue_parsed.type == "Answer":
                # Final answer reached
                logger.info(f"✅ Final answer for subtask: {continue_parsed.content}")
                log.append(continue_parsed)
                break
            else:
                # Add to log and continue
                logger.info(
                    f"📝 Adding to log ({continue_parsed.type}): {continue_parsed.content}"
                )
                log.append(continue_parsed)
                messages.append({"role": "assistant", "content": continue_text})
                subtask_step += 1

    # Extract final answer from log
    logger.info("🔍 Extracting final answer from execution log...")
    final_answer = None
    for entry in reversed(log):
        if entry.type == "Answer":
            final_answer = entry.content
            break

    if final_answer:
        logger.info(f"🎉 Final answer found: {final_answer}")
    else:
        logger.warning("⚠️ No final answer found in execution log")

    logger.info("✅ Agent execution completed successfully")
    return AgentResult(plan_items=plan_items, log=log, final_answer=final_answer)


def _execute_action(action: AgentResponse) -> str:
    """
    Execute an action and return the observation.

    For this MVP, we simulate search results.
    In a real implementation, this would call actual tools.
    """
    logger.info(f"🛠️ Executing action with metadata: {action.metadata}")

    if action.metadata and action.metadata.get("name") == "Search":
        query = action.metadata.get("params", "")
        logger.info(f"🔍 Performing search for query: '{query}'")

        # Simulate search results based on common queries
        if "bitcoin ticker" in query.lower():
            result = "BTC"
        elif "price of btc" in query.lower() or "bitcoin price" in query.lower():
            result = "It's $54,000"
        elif "weather" in query.lower():
            result = "It's 72°F and sunny"
        else:
            result = (
                f"Search results for '{query}': Various relevant information found."
            )

        logger.info(f"🔍 Search result: {result}")
        return result

    logger.info("✅ Generic action executed successfully")
    return "Action executed successfully."
