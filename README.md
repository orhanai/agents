# Streamlit Agent MVP

A minimal Streamlit application that demonstrates an LLM agent capable of planning, reasoning (chain-of-thought), and acting (tool calls) using OpenAI's Chat API. Now includes a powerful HTML presentation rendering system!

## Overview

This project implements:
1. **LLM Agent** - A simple agent that plans, thinks, and acts
2. **HTML Presentation Builder** - Convert JSON structures into beautiful HTML presentations

### Agent Features
- **Plans** - Decomposes user tasks into numbered subtasks
- **Thinks** - Uses chain-of-thought reasoning for each subtask
- **Acts** - Executes actions (like search) and observes results
- **Answers** - Provides a final answer based on the execution

### Presentation Builder Features
- **6 Layout Types** - Title, Two-Column, Image-Text, Bullet Points, Quote, Full Image
- **Theme Support** - Light and dark themes with consistent styling
- **Responsive Design** - Works on mobile, tablet, and desktop
- **Pure HTML/CSS** - No JavaScript dependencies
- **LLM Integration** - Optional AI-powered content generation

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   User      │     │  Streamlit  │     │   Agent     │
│   Input     │────▶│     UI      │────▶│   Logic     │
└─────────────┘     └─────────────┘     └─────────────┘
                            │                    │
                            ▼                    ▼
                    ┌─────────────┐     ┌─────────────┐
                    │   Display   │     │   OpenAI    │
                    │  Plan/Log   │◀────│     API     │
                    └─────────────┘     └─────────────┘
                            │
                            ▼
                    ┌─────────────┐     ┌─────────────┐
                    │    HTML     │────▶│  Beautiful  │
                    │  Renderer   │     │Presentations│
                    └─────────────┘     └─────────────┘
```

## Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd streamlit-agent-mvp
```

2. Install dependencies:
```bash
pip install .
```

3. Set your OpenAI API key (optional, for enhanced features):
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

### Running the Streamlit App

```bash
streamlit run main.py
```

The app provides two main features:
1. **Agent Tab** - Run the LLM agent for task execution
2. **Presentation Builder Tab** - Create HTML presentations

### Using the Presentation Builder

1. Enter a topic for your presentation
2. Choose the number of slides (3-10)
3. Select a theme (Light or Dark)
4. Optionally enable AI content generation
5. Click "Generate Presentation"
6. Download the HTML file or view the preview

### Running the Demo

```bash
python demo_presentation.py
```

This will:
- Generate sample presentations showcasing all layouts
- Create both light and dark theme versions
- Demonstrate error handling
- Open the presentations in your browser

## Presentation Layouts

### 1. Title Slide
Perfect for opening slides with title, subtitle, and optional content.

### 2. Two-Column Layout
Side-by-side content for comparisons or parallel information.

### 3. Image-Text Layout
Combines an image with accompanying text content.

### 4. Bullet Points
Clean list format for key points or agenda items.

### 5. Quote Slide
Highlighted quotes with author attribution.

### 6. Full Image
Full-screen images with optional captions.

## Project Structure

```
streamlit-agent-mvp/
├── README.md              # This file
├── pyproject.toml         # Project configuration
├── main.py                # Streamlit UI with presentation builder
├── agent.py               # Agent orchestration logic
├── parser.py              # Response parsing utilities
├── html_renderer.py       # HTML presentation renderer
├── deck_generator.py      # Presentation content generator
├── demo_presentation.py   # Demo script for presentations
└── tests/
    ├── test_parser.py     # Parser unit tests
    ├── test_html_renderer.py  # Renderer unit tests
    └── test_deck_generator.py # Generator unit tests
```

## Example deck.json Structure

```json
{
  "title": "My Presentation",
  "author": "John Doe",
  "theme": "light",
  "slides": [
    {
      "layout": "title",
      "content": {
        "title": "Welcome",
        "subtitle": "An Introduction",
        "content": "Additional details"
      }
    },
    {
      "layout": "bullet_points",
      "content": {
        "title": "Key Points",
        "bullets": ["Point 1", "Point 2", "Point 3"]
      }
    }
  ]
}
```

## API Reference

### HTMLRenderer

```python
from html_renderer import HTMLRenderer, Theme

# Create renderer
renderer = HTMLRenderer(theme=Theme.DARK)

# Render deck
html = renderer.render_deck(deck_data)

# Render single slide
slide_html = renderer.render_slide(slide_data, slide_number=1)
```

### DeckGenerator

```python
from deck_generator import DeckGenerator

# Create generator
generator = DeckGenerator(use_llm=True)

# Generate deck
deck = generator.generate_deck("Machine Learning", num_slides=6)

# Generate sample deck
sample = generator.generate_sample_deck()
```

## Testing

Run the test suite:
```bash
pytest tests/
```

## Requirements

- Python 3.10+
- Streamlit >= 1.25.0
- OpenAI >= 1.82.0 (optional, for AI features)