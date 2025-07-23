"""Deck Generator for creating presentation JSON structures.

This module provides functionality to generate deck.json structures,
including sample data and LLM-powered content generation.
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import random
import os
from openai import OpenAI


@dataclass
class DeckMetadata:
    """Metadata for a presentation deck."""
    title: str
    author: str
    description: Optional[str] = None
    theme: str = "light"


@dataclass
class Slide:
    """Individual slide structure."""
    layout: str
    content: Dict[str, Any]


class DeckGenerator:
    """Generate deck.json structures with various content."""
    
    def __init__(self, use_llm: bool = False):
        """Initialize the deck generator.
        
        Args:
            use_llm: Whether to use LLM for content generation
        """
        self.use_llm = use_llm
        self.client = None
        
        if use_llm and os.getenv("OPENAI_API_KEY"):
            self.client = OpenAI()
    
    def generate_deck(self, topic: str, num_slides: int = 6) -> Dict[str, Any]:
        """Generate a complete deck structure.
        
        Args:
            topic: The presentation topic
            num_slides: Number of slides to generate
            
        Returns:
            Dictionary representing the deck.json structure
        """
        metadata = self._generate_metadata(topic)
        slides = self._generate_slides(topic, num_slides)
        
        deck = {
            "title": metadata.title,
            "author": metadata.author,
            "description": metadata.description,
            "theme": metadata.theme,
            "slides": [asdict(slide) for slide in slides]
        }
        
        return deck
    
    def generate_sample_deck(self) -> Dict[str, Any]:
        """Generate a sample deck with hardcoded content showcasing all layouts."""
        slides = [
            Slide(
                layout="title",
                content={
                    "title": "Introduction to Modern Web Development",
                    "subtitle": "Building Scalable Applications",
                    "content": "A comprehensive guide to current best practices"
                }
            ),
            Slide(
                layout="two_column",
                content={
                    "title": "Frontend vs Backend",
                    "left_content": "# Frontend Technologies\n\n- React/Vue/Angular\n- TypeScript\n- CSS Frameworks\n- Build Tools",
                    "right_content": "# Backend Technologies\n\n- Node.js/Python/Go\n- REST/GraphQL APIs\n- Databases\n- Cloud Services"
                }
            ),
            Slide(
                layout="bullet_points",
                content={
                    "title": "Key Development Principles",
                    "content": "Essential principles every developer should follow:",
                    "bullets": [
                        "Write clean, readable code",
                        "Follow DRY (Don't Repeat Yourself)",
                        "Test early and often",
                        "Document your code",
                        "Use version control effectively"
                    ]
                }
            ),
            Slide(
                layout="image_text",
                content={
                    "title": "Modern Architecture Patterns",
                    "image_url": "https://via.placeholder.com/600x400/4a9eff/ffffff?text=Microservices+Architecture",
                    "image_caption": "Microservices enable scalable, maintainable systems",
                    "content": "Microservices architecture breaks down applications into small, independent services that communicate through APIs. This approach offers better scalability, fault isolation, and technology flexibility."
                }
            ),
            Slide(
                layout="quote",
                content={
                    "quote": "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.",
                    "author": "Martin Fowler"
                }
            ),
            Slide(
                layout="full_image",
                content={
                    "title": "The Development Workflow",
                    "image_url": "https://via.placeholder.com/800x600/0066cc/ffffff?text=CI/CD+Pipeline",
                    "image_caption": "Continuous Integration and Deployment streamline the development process"
                }
            )
        ]
        
        return {
            "title": "Introduction to Modern Web Development",
            "author": "Tech Presenter",
            "description": "A sample presentation showcasing all slide layouts",
            "theme": "light",
            "slides": [asdict(slide) for slide in slides]
        }
    
    def _generate_metadata(self, topic: str) -> DeckMetadata:
        """Generate deck metadata."""
        if self.use_llm and self.client:
            # Use LLM to generate creative title and author
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Generate a presentation title and author name."},
                        {"role": "user", "content": f"Topic: {topic}. Provide a creative title and professional author name. Format: Title: [title]\nAuthor: [name]"}
                    ],
                    max_tokens=100
                )
                
                content = response.choices[0].message.content
                lines = content.strip().split('\n')
                title = topic  # default
                author = "Presenter"  # default
                
                for line in lines:
                    if line.startswith("Title:"):
                        title = line.replace("Title:", "").strip()
                    elif line.startswith("Author:"):
                        author = line.replace("Author:", "").strip()
                
                return DeckMetadata(
                    title=title,
                    author=author,
                    description=f"A presentation about {topic}",
                    theme=random.choice(["light", "dark"])
                )
            except:
                pass
        
        # Fallback to simple generation
        return DeckMetadata(
            title=f"Presentation: {topic}",
            author="Expert Presenter",
            description=f"An informative presentation about {topic}",
            theme="light"
        )
    
    def _generate_slides(self, topic: str, num_slides: int) -> List[Slide]:
        """Generate slides for the deck."""
        slides = []
        
        # Always start with a title slide
        slides.append(self._generate_title_slide(topic))
        
        # Generate remaining slides with varied layouts
        layouts = ["two_column", "bullet_points", "image_text", "quote", "full_image"]
        
        for i in range(1, min(num_slides, 6)):
            layout = layouts[(i - 1) % len(layouts)]
            slide = self._generate_slide_by_layout(topic, layout, i + 1)
            slides.append(slide)
        
        return slides
    
    def _generate_title_slide(self, topic: str) -> Slide:
        """Generate a title slide."""
        if self.use_llm and self.client:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Generate a title slide for a presentation."},
                        {"role": "user", "content": f"Create a title, subtitle, and brief description for a presentation about: {topic}"}
                    ],
                    max_tokens=150
                )
                
                content = response.choices[0].message.content
                # Parse the response (simplified)
                lines = content.strip().split('\n')
                
                return Slide(
                    layout="title",
                    content={
                        "title": lines[0] if lines else topic,
                        "subtitle": lines[1] if len(lines) > 1 else "An Informative Presentation",
                        "content": lines[2] if len(lines) > 2 else ""
                    }
                )
            except:
                pass
        
        # Fallback
        return Slide(
            layout="title",
            content={
                "title": topic,
                "subtitle": "Key Insights and Information",
                "content": "Let's explore this topic together"
            }
        )
    
    def _generate_slide_by_layout(self, topic: str, layout: str, slide_num: int) -> Slide:
        """Generate a slide based on layout type."""
        if layout == "two_column":
            return Slide(
                layout="two_column",
                content={
                    "title": f"Key Aspects of {topic}",
                    "left_content": f"# Aspect {slide_num}A\n\n- Point 1\n- Point 2\n- Point 3",
                    "right_content": f"# Aspect {slide_num}B\n\n- Point A\n- Point B\n- Point C"
                }
            )
        
        elif layout == "bullet_points":
            return Slide(
                layout="bullet_points",
                content={
                    "title": f"Important Points about {topic}",
                    "content": "Consider these key factors:",
                    "bullets": [
                        f"Key point {i} about {topic}" for i in range(1, 6)
                    ]
                }
            )
        
        elif layout == "image_text":
            return Slide(
                layout="image_text",
                content={
                    "title": f"Visualizing {topic}",
                    "image_url": f"https://via.placeholder.com/600x400/4a9eff/ffffff?text={topic.replace(' ', '+')}",
                    "image_caption": f"A visual representation of {topic}",
                    "content": f"This diagram illustrates the key concepts of {topic}. Understanding these visual elements helps grasp the complexity and relationships involved."
                }
            )
        
        elif layout == "quote":
            quotes = [
                ("The best way to predict the future is to invent it.", "Alan Kay"),
                ("Innovation distinguishes between a leader and a follower.", "Steve Jobs"),
                ("The only way to do great work is to love what you do.", "Steve Jobs"),
            ]
            quote, author = random.choice(quotes)
            
            return Slide(
                layout="quote",
                content={
                    "quote": quote,
                    "author": author
                }
            )
        
        else:  # full_image
            return Slide(
                layout="full_image",
                content={
                    "title": f"{topic} in Practice",
                    "image_url": f"https://via.placeholder.com/800x600/0066cc/ffffff?text={topic.replace(' ', '+')}+Visualization",
                    "image_caption": f"Real-world application of {topic}"
                }
            )


def save_deck_to_file(deck: Dict[str, Any], filename: str = "deck.json") -> str:
    """Save a deck to a JSON file.
    
    Args:
        deck: The deck dictionary
        filename: Output filename
        
    Returns:
        Path to the saved file
    """
    with open(filename, 'w') as f:
        json.dump(deck, f, indent=2)
    
    return filename


def load_deck_from_file(filename: str) -> Dict[str, Any]:
    """Load a deck from a JSON file.
    
    Args:
        filename: Input filename
        
    Returns:
        The deck dictionary
    """
    with open(filename, 'r') as f:
        return json.load(f)