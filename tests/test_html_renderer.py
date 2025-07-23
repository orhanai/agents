"""Unit tests for the HTML renderer module."""
import pytest
from html_renderer import HTMLRenderer, Theme, LayoutType, SlideContent, render_deck_from_dict


class TestHTMLRenderer:
    """Test cases for HTMLRenderer class."""
    
    def test_init_default_theme(self):
        """Test renderer initialization with default theme."""
        renderer = HTMLRenderer()
        assert renderer.theme == Theme.LIGHT
        assert renderer._theme_styles is not None
    
    def test_init_dark_theme(self):
        """Test renderer initialization with dark theme."""
        renderer = HTMLRenderer(theme=Theme.DARK)
        assert renderer.theme == Theme.DARK
        assert "bg-color: #1a1a1a" in renderer._theme_styles
    
    def test_render_empty_deck(self):
        """Test rendering an empty deck."""
        renderer = HTMLRenderer()
        deck = {"title": "Empty Deck", "slides": []}
        html = renderer.render_deck(deck)
        
        assert "Empty Deck" in html
        assert "<!DOCTYPE html>" in html
        assert "</html>" in html
    
    def test_render_complete_deck(self):
        """Test rendering a complete deck with all metadata."""
        renderer = HTMLRenderer()
        deck = {
            "title": "Test Presentation",
            "author": "Test Author",
            "description": "Test Description",
            "slides": [
                {
                    "layout": "title",
                    "content": {
                        "title": "Welcome",
                        "subtitle": "Test Subtitle"
                    }
                }
            ]
        }
        html = renderer.render_deck(deck)
        
        assert "Test Presentation" in html
        assert "by Test Author" in html
        assert "Welcome" in html
        assert "Test Subtitle" in html
    
    def test_render_title_slide(self):
        """Test rendering a title slide."""
        renderer = HTMLRenderer()
        slide = {
            "layout": "title",
            "content": {
                "title": "Main Title",
                "subtitle": "Subtitle Text",
                "content": "Additional content"
            }
        }
        html = renderer.render_slide(slide, 1)
        
        assert "Main Title" in html
        assert "Subtitle Text" in html
        assert "Additional content" in html
        assert "Slide 1" in html
        assert "title-slide" in html
    
    def test_render_two_column_slide(self):
        """Test rendering a two-column slide."""
        renderer = HTMLRenderer()
        slide = {
            "layout": "two_column",
            "content": {
                "title": "Two Columns",
                "left_content": "Left side content",
                "right_content": "Right side content"
            }
        }
        html = renderer.render_slide(slide, 2)
        
        assert "Two Columns" in html
        assert "Left side content" in html
        assert "Right side content" in html
        assert "two-column" in html
    
    def test_render_bullet_points_slide(self):
        """Test rendering a bullet points slide."""
        renderer = HTMLRenderer()
        slide = {
            "layout": "bullet_points",
            "content": {
                "title": "Key Points",
                "content": "Introduction text",
                "bullets": ["Point 1", "Point 2", "Point 3"]
            }
        }
        html = renderer.render_slide(slide, 3)
        
        assert "Key Points" in html
        assert "Introduction text" in html
        assert "Point 1" in html
        assert "Point 2" in html
        assert "Point 3" in html
        assert "bullet-list" in html
    
    def test_render_image_text_slide(self):
        """Test rendering an image-text slide."""
        renderer = HTMLRenderer()
        slide = {
            "layout": "image_text",
            "content": {
                "title": "Image Example",
                "image_url": "https://example.com/image.jpg",
                "image_caption": "Test caption",
                "content": "Text content"
            }
        }
        html = renderer.render_slide(slide, 4)
        
        assert "Image Example" in html
        assert 'src="https://example.com/image.jpg"' in html
        assert "Test caption" in html
        assert "Text content" in html
        assert "image-text-container" in html
    
    def test_render_quote_slide(self):
        """Test rendering a quote slide."""
        renderer = HTMLRenderer()
        slide = {
            "layout": "quote",
            "content": {
                "quote": "Test quote text",
                "author": "Test Author"
            }
        }
        html = renderer.render_slide(slide, 5)
        
        assert "Test quote text" in html
        assert "— Test Author" in html
        assert "quote-container" in html
        assert "<blockquote" in html
    
    def test_render_full_image_slide(self):
        """Test rendering a full image slide."""
        renderer = HTMLRenderer()
        slide = {
            "layout": "full_image",
            "content": {
                "title": "Full Image",
                "image_url": "https://example.com/full.jpg",
                "image_caption": "Full image caption"
            }
        }
        html = renderer.render_slide(slide, 6)
        
        assert "Full Image" in html
        assert 'src="https://example.com/full.jpg"' in html
        assert "Full image caption" in html
        assert "full-image-container" in html
    
    def test_render_invalid_layout(self):
        """Test rendering with invalid layout type."""
        renderer = HTMLRenderer()
        slide = {
            "layout": "invalid_layout",
            "content": {"title": "Test"}
        }
        html = renderer.render_slide(slide, 1)
        
        # Should default to title layout
        assert "Test" in html
        assert "title-slide" in html
    
    def test_render_missing_content(self):
        """Test rendering with missing content fields."""
        renderer = HTMLRenderer()
        slide = {
            "layout": "bullet_points",
            "content": {}  # No bullets provided
        }
        html = renderer.render_slide(slide, 1)
        
        # Should handle gracefully
        assert "slide" in html
        assert "Slide 1" in html
    
    def test_render_content_markdown(self):
        """Test markdown-like content rendering."""
        renderer = HTMLRenderer()
        content = renderer._render_content("# Heading\n## Subheading\n- Item 1\n- Item 2\nRegular text")
        
        assert "<h3>Heading</h3>" in content
        assert "<h4>Subheading</h4>" in content
        assert "<li>Item 1</li>" in content
        assert "<li>Item 2</li>" in content
        assert "<p>Regular text</p>" in content
    
    def test_error_handling(self):
        """Test error handling in deck rendering."""
        renderer = HTMLRenderer()
        
        # Invalid deck structure
        html = renderer.render_deck("not a dict")
        assert "Error rendering deck" in html
        
        # Invalid slide structure
        html = renderer.render_slide("not a dict", 1)
        assert "Error rendering slide" in html
    
    def test_theme_styles(self):
        """Test theme-specific styling."""
        # Light theme
        light_renderer = HTMLRenderer(Theme.LIGHT)
        light_styles = light_renderer._get_theme_styles()
        assert "--bg-color: #f5f5f5" in light_styles
        assert "--text-color: #333333" in light_styles
        
        # Dark theme
        dark_renderer = HTMLRenderer(Theme.DARK)
        dark_styles = dark_renderer._get_theme_styles()
        assert "--bg-color: #1a1a1a" in dark_styles
        assert "--text-color: #e0e0e0" in dark_styles
    
    def test_responsive_styles(self):
        """Test that responsive CSS is included."""
        renderer = HTMLRenderer()
        base_styles = renderer._get_base_styles()
        
        assert "@media (max-width: 768px)" in base_styles
        assert "grid-template-columns: 1fr;" in base_styles


class TestConvenienceFunctions:
    """Test cases for convenience functions."""
    
    def test_render_deck_from_dict(self):
        """Test rendering from dictionary."""
        deck = {
            "title": "Test Deck",
            "slides": [
                {
                    "layout": "title",
                    "content": {"title": "Test Slide"}
                }
            ]
        }
        
        # Light theme
        html_light = render_deck_from_dict(deck, Theme.LIGHT)
        assert "Test Deck" in html_light
        assert "Test Slide" in html_light
        
        # Dark theme
        html_dark = render_deck_from_dict(deck, Theme.DARK)
        assert "Test Deck" in html_dark
        assert "--bg-color: #1a1a1a" in html_dark


class TestSlideContent:
    """Test cases for SlideContent dataclass."""
    
    def test_slide_content_creation(self):
        """Test creating SlideContent instances."""
        content = SlideContent(
            title="Test Title",
            subtitle="Test Subtitle",
            bullets=["Item 1", "Item 2"]
        )
        
        assert content.title == "Test Title"
        assert content.subtitle == "Test Subtitle"
        assert len(content.bullets) == 2
        assert content.content is None  # Default value