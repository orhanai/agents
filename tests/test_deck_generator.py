"""Unit tests for the deck generator module."""
import pytest
import json
import os
from pathlib import Path
from deck_generator import DeckGenerator, DeckMetadata, Slide, save_deck_to_file, load_deck_from_file


class TestDeckGenerator:
    """Test cases for DeckGenerator class."""
    
    def test_init_without_llm(self):
        """Test generator initialization without LLM."""
        generator = DeckGenerator(use_llm=False)
        assert generator.use_llm is False
        assert generator.client is None
    
    def test_generate_sample_deck(self):
        """Test generating a sample deck."""
        generator = DeckGenerator()
        deck = generator.generate_sample_deck()
        
        # Check deck structure
        assert "title" in deck
        assert "author" in deck
        assert "slides" in deck
        assert deck["title"] == "Introduction to Modern Web Development"
        
        # Check slides
        assert len(deck["slides"]) == 6
        
        # Check each layout type is present
        layouts = [slide["layout"] for slide in deck["slides"]]
        assert "title" in layouts
        assert "two_column" in layouts
        assert "bullet_points" in layouts
        assert "image_text" in layouts
        assert "quote" in layouts
        assert "full_image" in layouts
    
    def test_generate_deck_basic(self):
        """Test generating a deck with basic parameters."""
        generator = DeckGenerator(use_llm=False)
        deck = generator.generate_deck("Python Programming", num_slides=5)
        
        assert deck["title"] == "Presentation: Python Programming"
        assert deck["author"] == "Expert Presenter"
        assert len(deck["slides"]) == 5
        
        # First slide should be title
        assert deck["slides"][0]["layout"] == "title"
    
    def test_generate_metadata(self):
        """Test metadata generation without LLM."""
        generator = DeckGenerator(use_llm=False)
        metadata = generator._generate_metadata("Machine Learning")
        
        assert isinstance(metadata, DeckMetadata)
        assert "Machine Learning" in metadata.title
        assert metadata.author == "Expert Presenter"
        assert metadata.theme in ["light", "dark"]
    
    def test_generate_title_slide(self):
        """Test title slide generation."""
        generator = DeckGenerator(use_llm=False)
        slide = generator._generate_title_slide("Data Science")
        
        assert isinstance(slide, Slide)
        assert slide.layout == "title"
        assert slide.content["title"] == "Data Science"
        assert "subtitle" in slide.content
        assert "content" in slide.content
    
    def test_generate_slide_by_layout(self):
        """Test generating slides for each layout type."""
        generator = DeckGenerator(use_llm=False)
        topic = "Test Topic"
        
        # Two column
        slide = generator._generate_slide_by_layout(topic, "two_column", 1)
        assert slide.layout == "two_column"
        assert "left_content" in slide.content
        assert "right_content" in slide.content
        
        # Bullet points
        slide = generator._generate_slide_by_layout(topic, "bullet_points", 2)
        assert slide.layout == "bullet_points"
        assert "bullets" in slide.content
        assert len(slide.content["bullets"]) == 5
        
        # Image text
        slide = generator._generate_slide_by_layout(topic, "image_text", 3)
        assert slide.layout == "image_text"
        assert "image_url" in slide.content
        assert "content" in slide.content
        
        # Quote
        slide = generator._generate_slide_by_layout(topic, "quote", 4)
        assert slide.layout == "quote"
        assert "quote" in slide.content
        assert "author" in slide.content
        
        # Full image
        slide = generator._generate_slide_by_layout(topic, "full_image", 5)
        assert slide.layout == "full_image"
        assert "image_url" in slide.content
        assert "image_caption" in slide.content
    
    def test_deck_structure_validity(self):
        """Test that generated decks have valid structure."""
        generator = DeckGenerator(use_llm=False)
        deck = generator.generate_deck("Testing", num_slides=3)
        
        # Required fields
        assert "title" in deck
        assert "author" in deck
        assert "slides" in deck
        
        # Each slide has required fields
        for slide in deck["slides"]:
            assert "layout" in slide
            assert "content" in slide
            assert isinstance(slide["content"], dict)


class TestDeckMetadata:
    """Test cases for DeckMetadata dataclass."""
    
    def test_metadata_creation(self):
        """Test creating DeckMetadata instances."""
        metadata = DeckMetadata(
            title="Test Title",
            author="Test Author",
            description="Test Description",
            theme="dark"
        )
        
        assert metadata.title == "Test Title"
        assert metadata.author == "Test Author"
        assert metadata.description == "Test Description"
        assert metadata.theme == "dark"
    
    def test_metadata_defaults(self):
        """Test DeckMetadata default values."""
        metadata = DeckMetadata(
            title="Title",
            author="Author"
        )
        
        assert metadata.description is None
        assert metadata.theme == "light"


class TestSlideDataclass:
    """Test cases for Slide dataclass."""
    
    def test_slide_creation(self):
        """Test creating Slide instances."""
        slide = Slide(
            layout="title",
            content={"title": "Test", "subtitle": "Sub"}
        )
        
        assert slide.layout == "title"
        assert slide.content["title"] == "Test"
        assert slide.content["subtitle"] == "Sub"


class TestFileOperations:
    """Test cases for file operations."""
    
    def test_save_and_load_deck(self, tmp_path):
        """Test saving and loading deck to/from file."""
        # Create a test deck
        deck = {
            "title": "Test Deck",
            "author": "Tester",
            "slides": [
                {
                    "layout": "title",
                    "content": {"title": "Test Slide"}
                }
            ]
        }
        
        # Save to file
        filename = str(tmp_path / "test_deck.json")
        saved_path = save_deck_to_file(deck, filename)
        
        assert saved_path == filename
        assert os.path.exists(saved_path)
        
        # Load from file
        loaded_deck = load_deck_from_file(saved_path)
        
        assert loaded_deck["title"] == deck["title"]
        assert loaded_deck["author"] == deck["author"]
        assert len(loaded_deck["slides"]) == len(deck["slides"])
        assert loaded_deck["slides"][0]["content"]["title"] == "Test Slide"
    
    def test_save_deck_default_filename(self, tmp_path, monkeypatch):
        """Test saving deck with default filename."""
        monkeypatch.chdir(tmp_path)
        
        deck = {"title": "Test", "slides": []}
        saved_path = save_deck_to_file(deck)
        
        assert saved_path == "deck.json"
        assert os.path.exists("deck.json")
    
    def test_load_nonexistent_file(self):
        """Test loading from non-existent file."""
        with pytest.raises(FileNotFoundError):
            load_deck_from_file("nonexistent.json")
    
    def test_save_load_special_characters(self, tmp_path):
        """Test saving/loading deck with special characters."""
        deck = {
            "title": "Test with 'quotes' and \"double quotes\"",
            "author": "Author & Co.",
            "slides": [
                {
                    "layout": "quote",
                    "content": {
                        "quote": "This has\nnewlines\tand\ttabs",
                        "author": "Someone — Special"
                    }
                }
            ]
        }
        
        filename = str(tmp_path / "special_chars.json")
        save_deck_to_file(deck, filename)
        loaded_deck = load_deck_from_file(filename)
        
        assert loaded_deck["title"] == deck["title"]
        assert loaded_deck["slides"][0]["content"]["quote"] == deck["slides"][0]["content"]["quote"]