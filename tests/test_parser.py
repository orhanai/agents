"""Unit tests for parser module."""
import pytest
from parser import parse_plan, parse_agent_response, AgentResponse


class TestParsePlan:
    """Test cases for parse_plan function."""
    
    def test_parse_numbered_plan(self):
        """Test parsing a standard numbered plan."""
        text = """Here's the plan:
1. Identify the ticker symbol
2. Search for current price
3. Format the final answer
"""
        result = parse_plan(text)
        assert len(result) == 3
        assert result[0] == "Identify the ticker symbol"
        assert result[1] == "Search for current price"
        assert result[2] == "Format the final answer"
    
    def test_parse_plan_with_extra_text(self):
        """Test parsing plan with surrounding text."""
        text = """I'll help you with that. Here's my plan:

1. First, check the weather API
2. Get temperature data
3. Convert to requested format

This should give us the information we need."""
        result = parse_plan(text)
        assert len(result) == 3
        assert result[0] == "First, check the weather API"
        assert result[1] == "Get temperature data"
        assert result[2] == "Convert to requested format"
    
    def test_parse_plan_with_indentation(self):
        """Test parsing plan with indented items."""
        text = """
    1. Step one
    2. Step two
    3. Step three
"""
        result = parse_plan(text)
        assert len(result) == 3
        assert result[0] == "Step one"
    
    def test_empty_plan(self):
        """Test parsing text with no plan items."""
        text = "This text has no numbered items."
        result = parse_plan(text)
        assert len(result) == 0


class TestParseAgentResponse:
    """Test cases for parse_agent_response function."""
    
    def test_parse_thought(self):
        """Test parsing thought response."""
        text = "Thought: I need to find the Bitcoin ticker symbol first."
        result = parse_agent_response(text)
        assert result.type == "Thought"
        assert result.content == "I need to find the Bitcoin ticker symbol first."
    
    def test_parse_action(self):
        """Test parsing action response."""
        text = 'Action: Search("Bitcoin ticker symbol")'
        result = parse_agent_response(text)
        assert result.type == "Action"
        assert result.content == 'Search("Bitcoin ticker symbol")'
        assert result.metadata["name"] == "Search"
        assert result.metadata["params"] == "Bitcoin ticker symbol"
    
    def test_parse_action_single_quotes(self):
        """Test parsing action with single quotes."""
        text = "Action: Search('current BTC price')"
        result = parse_agent_response(text)
        assert result.type == "Action"
        assert result.metadata["params"] == "current BTC price"
    
    def test_parse_observation(self):
        """Test parsing observation response."""
        text = "Observation: The ticker symbol is BTC"
        result = parse_agent_response(text)
        assert result.type == "Observation"
        assert result.content == "The ticker symbol is BTC"
    
    def test_parse_final_answer(self):
        """Test parsing final answer response."""
        text = "Final Answer: The current price of Bitcoin (BTC) is $54,000."
        result = parse_agent_response(text)
        assert result.type == "Answer"
        assert result.content == "The current price of Bitcoin (BTC) is $54,000."
    
    def test_parse_answer_short_form(self):
        """Test parsing answer with short form."""
        text = "Answer: BTC is trading at $54,000"
        result = parse_agent_response(text)
        assert result.type == "Answer"
        assert result.content == "BTC is trading at $54,000"
    
    def test_parse_plan_item(self):
        """Test parsing plan item."""
        text = "PlanItem: Identify the ticker symbol"
        result = parse_agent_response(text)
        assert result.type == "PlanItem"
        assert result.content == "Identify the ticker symbol"
    
    def test_default_to_thought(self):
        """Test that unprefixed text defaults to Thought."""
        text = "This is just some reasoning without a prefix."
        result = parse_agent_response(text)
        assert result.type == "Thought"
        assert result.content == "This is just some reasoning without a prefix."
    
    def test_whitespace_handling(self):
        """Test handling of extra whitespace."""
        text = "  Thought:   Extra spaces everywhere   "
        result = parse_agent_response(text)
        assert result.type == "Thought"
        assert result.content == "Extra spaces everywhere"