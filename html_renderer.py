"""HTML Renderer for converting deck.json structures to styled HTML presentations.

This module provides a complete HTML rendering system that transforms JSON deck
structures into visually appealing, responsive HTML presentations without JavaScript.
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class LayoutType(Enum):
    """Supported slide layout types."""
    TITLE = "title"
    TWO_COLUMN = "two_column"
    IMAGE_TEXT = "image_text"
    BULLET_POINTS = "bullet_points"
    QUOTE = "quote"
    FULL_IMAGE = "full_image"


class Theme(Enum):
    """Available presentation themes."""
    LIGHT = "light"
    DARK = "dark"


@dataclass
class SlideContent:
    """Container for slide content data."""
    title: Optional[str] = None
    subtitle: Optional[str] = None
    content: Optional[str] = None
    left_content: Optional[str] = None
    right_content: Optional[str] = None
    image_url: Optional[str] = None
    image_caption: Optional[str] = None
    bullets: Optional[List[str]] = None
    quote: Optional[str] = None
    author: Optional[str] = None


class HTMLRenderer:
    """Renders deck.json structures into styled HTML presentations."""
    
    def __init__(self, theme: Theme = Theme.LIGHT):
        """Initialize the HTML renderer with a theme.
        
        Args:
            theme: The presentation theme (light or dark)
        """
        self.theme = theme
        self._theme_styles = self._get_theme_styles()
    
    def render_deck(self, deck_data: Dict[str, Any]) -> str:
        """Render a complete deck from JSON data.
        
        Args:
            deck_data: Dictionary containing deck metadata and slides
            
        Returns:
            Complete HTML string for the presentation
        """
        try:
            title = deck_data.get("title", "Untitled Presentation")
            author = deck_data.get("author", "")
            slides = deck_data.get("slides", [])
            
            # Build HTML document
            html = self._build_html_document(title, author, slides)
            return html
            
        except Exception as e:
            return self._render_error(f"Error rendering deck: {str(e)}")
    
    def render_slide(self, slide_data: Dict[str, Any], slide_number: int) -> str:
        """Render a single slide.
        
        Args:
            slide_data: Dictionary containing slide layout and content
            slide_number: The slide number for identification
            
        Returns:
            HTML string for the slide
        """
        try:
            layout_type = slide_data.get("layout", "title")
            content = slide_data.get("content", {})
            
            # Convert to LayoutType enum
            try:
                layout = LayoutType(layout_type)
            except ValueError:
                layout = LayoutType.TITLE
            
            # Parse content into SlideContent object
            slide_content = self._parse_slide_content(content)
            
            # Render based on layout type
            renderer_map = {
                LayoutType.TITLE: self._render_title_slide,
                LayoutType.TWO_COLUMN: self._render_two_column_slide,
                LayoutType.IMAGE_TEXT: self._render_image_text_slide,
                LayoutType.BULLET_POINTS: self._render_bullet_points_slide,
                LayoutType.QUOTE: self._render_quote_slide,
                LayoutType.FULL_IMAGE: self._render_full_image_slide,
            }
            
            renderer = renderer_map.get(layout, self._render_title_slide)
            slide_html = renderer(slide_content, slide_number)
            
            return slide_html
            
        except Exception as e:
            return self._render_error(f"Error rendering slide {slide_number}: {str(e)}")
    
    def _build_html_document(self, title: str, author: str, slides: List[Dict]) -> str:
        """Build the complete HTML document."""
        slides_html = []
        for i, slide in enumerate(slides, 1):
            slides_html.append(self.render_slide(slide, i))
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        {self._get_base_styles()}
        {self._theme_styles}
    </style>
</head>
<body>
    <div class="presentation-container">
        <header class="presentation-header">
            <h1>{title}</h1>
            {f'<p class="author">by {author}</p>' if author else ''}
        </header>
        <main class="slides-container">
            {''.join(slides_html)}
        </main>
        <footer class="presentation-footer">
            <p>Generated with HTML Renderer</p>
        </footer>
    </div>
</body>
</html>"""
    
    def _get_base_styles(self) -> str:
        """Get base CSS styles for all themes."""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            overflow-x: hidden;
        }
        
        .presentation-container {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .presentation-header {
            padding: 2rem;
            text-align: center;
            border-bottom: 2px solid var(--border-color);
        }
        
        .presentation-header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        .author {
            font-style: italic;
            opacity: 0.8;
        }
        
        .slides-container {
            flex: 1;
            padding: 2rem;
        }
        
        .slide {
            max-width: 1200px;
            margin: 0 auto 4rem;
            padding: 3rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            background: var(--slide-bg);
            min-height: 600px;
            display: flex;
            flex-direction: column;
            position: relative;
        }
        
        .slide-number {
            position: absolute;
            top: 1rem;
            right: 1rem;
            font-size: 0.875rem;
            opacity: 0.6;
        }
        
        .slide h2 {
            font-size: 2rem;
            margin-bottom: 1.5rem;
            color: var(--heading-color);
        }
        
        .slide h3 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: var(--subheading-color);
        }
        
        .slide p {
            margin-bottom: 1rem;
            color: var(--text-color);
        }
        
        .slide img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
        }
        
        .two-column {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            align-items: start;
        }
        
        .image-text-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            align-items: center;
        }
        
        .bullet-list {
            list-style: none;
            padding-left: 0;
        }
        
        .bullet-list li {
            position: relative;
            padding-left: 2rem;
            margin-bottom: 1rem;
            color: var(--text-color);
        }
        
        .bullet-list li:before {
            content: "•";
            position: absolute;
            left: 0;
            color: var(--accent-color);
            font-size: 1.5rem;
            line-height: 1.2;
        }
        
        .quote-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            height: 100%;
        }
        
        .quote {
            font-size: 1.75rem;
            font-style: italic;
            color: var(--quote-color);
            margin-bottom: 1.5rem;
            position: relative;
            padding: 0 3rem;
        }
        
        .quote:before,
        .quote:after {
            position: absolute;
            font-size: 3rem;
            color: var(--accent-color);
            opacity: 0.3;
        }
        
        .quote:before {
            content: "\\201C";
            left: 0;
            top: -1rem;
        }
        
        .quote:after {
            content: "\\201D";
            right: 0;
            bottom: -2rem;
        }
        
        .quote-author {
            font-size: 1.125rem;
            color: var(--subheading-color);
        }
        
        .full-image-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
        }
        
        .full-image-container img {
            max-height: 500px;
            object-fit: contain;
        }
        
        .image-caption {
            margin-top: 1rem;
            font-style: italic;
            color: var(--subheading-color);
            text-align: center;
        }
        
        .title-slide {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        
        .title-slide h2 {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        .title-slide h3 {
            font-size: 1.75rem;
            opacity: 0.9;
        }
        
        .error-slide {
            background: #fee;
            border: 2px solid #fcc;
            color: #c00;
        }
        
        .presentation-footer {
            padding: 2rem;
            text-align: center;
            border-top: 2px solid var(--border-color);
            opacity: 0.7;
        }
        
        @media (max-width: 768px) {
            .slide {
                padding: 2rem;
                min-height: 400px;
            }
            
            .two-column,
            .image-text-container {
                grid-template-columns: 1fr;
            }
            
            .slide h2 {
                font-size: 1.5rem;
            }
            
            .title-slide h2 {
                font-size: 2rem;
            }
            
            .quote {
                font-size: 1.25rem;
            }
        }
        """
    
    def _get_theme_styles(self) -> str:
        """Get theme-specific CSS variables."""
        if self.theme == Theme.DARK:
            return """
            :root {
                --bg-color: #1a1a1a;
                --text-color: #e0e0e0;
                --heading-color: #ffffff;
                --subheading-color: #b0b0b0;
                --slide-bg: #2a2a2a;
                --border-color: #404040;
                --accent-color: #4a9eff;
                --quote-color: #d0d0d0;
            }
            
            body {
                background: var(--bg-color);
                color: var(--text-color);
            }
            """
        else:
            return """
            :root {
                --bg-color: #f5f5f5;
                --text-color: #333333;
                --heading-color: #000000;
                --subheading-color: #666666;
                --slide-bg: #ffffff;
                --border-color: #e0e0e0;
                --accent-color: #0066cc;
                --quote-color: #555555;
            }
            
            body {
                background: var(--bg-color);
                color: var(--text-color);
            }
            """
    
    def _parse_slide_content(self, content: Dict[str, Any]) -> SlideContent:
        """Parse content dictionary into SlideContent object."""
        return SlideContent(
            title=content.get("title"),
            subtitle=content.get("subtitle"),
            content=content.get("content"),
            left_content=content.get("left_content"),
            right_content=content.get("right_content"),
            image_url=content.get("image_url"),
            image_caption=content.get("image_caption"),
            bullets=content.get("bullets", []),
            quote=content.get("quote"),
            author=content.get("author"),
        )
    
    def _render_title_slide(self, content: SlideContent, slide_number: int) -> str:
        """Render a title slide."""
        return f"""
        <div class="slide title-slide">
            <span class="slide-number">Slide {slide_number}</span>
            <h2>{content.title or 'Untitled Slide'}</h2>
            {f'<h3>{content.subtitle}</h3>' if content.subtitle else ''}
            {f'<p>{content.content}</p>' if content.content else ''}
        </div>
        """
    
    def _render_two_column_slide(self, content: SlideContent, slide_number: int) -> str:
        """Render a two-column slide."""
        return f"""
        <div class="slide">
            <span class="slide-number">Slide {slide_number}</span>
            {f'<h2>{content.title}</h2>' if content.title else ''}
            <div class="two-column">
                <div class="column-left">
                    {self._render_content(content.left_content or '')}
                </div>
                <div class="column-right">
                    {self._render_content(content.right_content or '')}
                </div>
            </div>
        </div>
        """
    
    def _render_image_text_slide(self, content: SlideContent, slide_number: int) -> str:
        """Render an image-text slide."""
        return f"""
        <div class="slide">
            <span class="slide-number">Slide {slide_number}</span>
            {f'<h2>{content.title}</h2>' if content.title else ''}
            <div class="image-text-container">
                <div class="image-side">
                    {f'<img src="{content.image_url}" alt="{content.title or "Slide image"}">' if content.image_url else '<p>No image provided</p>'}
                    {f'<p class="image-caption">{content.image_caption}</p>' if content.image_caption else ''}
                </div>
                <div class="text-side">
                    {self._render_content(content.content or '')}
                </div>
            </div>
        </div>
        """
    
    def _render_bullet_points_slide(self, content: SlideContent, slide_number: int) -> str:
        """Render a bullet points slide."""
        bullets_html = '\n'.join([f'<li>{bullet}</li>' for bullet in (content.bullets or [])])
        
        return f"""
        <div class="slide">
            <span class="slide-number">Slide {slide_number}</span>
            {f'<h2>{content.title}</h2>' if content.title else ''}
            {f'<p>{content.content}</p>' if content.content else ''}
            <ul class="bullet-list">
                {bullets_html}
            </ul>
        </div>
        """
    
    def _render_quote_slide(self, content: SlideContent, slide_number: int) -> str:
        """Render a quote slide."""
        return f"""
        <div class="slide">
            <span class="slide-number">Slide {slide_number}</span>
            <div class="quote-container">
                <blockquote class="quote">
                    {content.quote or 'No quote provided'}
                </blockquote>
                {f'<p class="quote-author">— {content.author}</p>' if content.author else ''}
            </div>
        </div>
        """
    
    def _render_full_image_slide(self, content: SlideContent, slide_number: int) -> str:
        """Render a full image slide."""
        return f"""
        <div class="slide">
            <span class="slide-number">Slide {slide_number}</span>
            {f'<h2>{content.title}</h2>' if content.title else ''}
            <div class="full-image-container">
                {f'<img src="{content.image_url}" alt="{content.title or "Full image"}">' if content.image_url else '<p>No image provided</p>'}
                {f'<p class="image-caption">{content.image_caption}</p>' if content.image_caption else ''}
            </div>
        </div>
        """
    
    def _render_content(self, content: str) -> str:
        """Render text content with basic markdown-like formatting."""
        # Simple markdown-like processing
        lines = content.split('\n')
        html_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            elif line.startswith('# '):
                html_lines.append(f'<h3>{line[2:]}</h3>')
            elif line.startswith('## '):
                html_lines.append(f'<h4>{line[3:]}</h4>')
            elif line.startswith('- '):
                html_lines.append(f'<li>{line[2:]}</li>')
            else:
                html_lines.append(f'<p>{line}</p>')
        
        return '\n'.join(html_lines)
    
    def _render_error(self, error_message: str) -> str:
        """Render an error slide."""
        return f"""
        <div class="slide error-slide">
            <h2>Rendering Error</h2>
            <p>{error_message}</p>
        </div>
        """


def render_deck_from_json(json_path: str, theme: Theme = Theme.LIGHT) -> str:
    """Convenience function to render a deck from a JSON file.
    
    Args:
        json_path: Path to the deck.json file
        theme: The presentation theme
        
    Returns:
        Complete HTML string for the presentation
    """
    try:
        with open(json_path, 'r') as f:
            deck_data = json.load(f)
        
        renderer = HTMLRenderer(theme=theme)
        return renderer.render_deck(deck_data)
        
    except Exception as e:
        return f"<html><body><h1>Error loading deck</h1><p>{str(e)}</p></body></html>"


def render_deck_from_dict(deck_data: Dict[str, Any], theme: Theme = Theme.LIGHT) -> str:
    """Convenience function to render a deck from a dictionary.
    
    Args:
        deck_data: Dictionary containing deck metadata and slides
        theme: The presentation theme
        
    Returns:
        Complete HTML string for the presentation
    """
    renderer = HTMLRenderer(theme=theme)
    return renderer.render_deck(deck_data)