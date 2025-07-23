"""Demo script for the HTML presentation rendering system.

This script demonstrates the complete workflow of generating a deck.json
structure and rendering it as a beautiful HTML presentation.
"""

import os
import webbrowser
from pathlib import Path
from deck_generator import DeckGenerator, save_deck_to_file
from html_renderer import HTMLRenderer, Theme, render_deck_from_dict


def main():
    """Run the presentation demo."""
    print("🎯 HTML Presentation Renderer Demo")
    print("=" * 50)
    
    # Step 1: Generate a sample deck
    print("\n📝 Generating sample deck...")
    generator = DeckGenerator(use_llm=False)  # Using hardcoded content for demo
    deck = generator.generate_sample_deck()
    
    # Save deck to JSON for inspection
    deck_file = save_deck_to_file(deck, "sample_deck.json")
    print(f"   ✅ Deck saved to: {deck_file}")
    
    # Step 2: Render deck in both themes
    print("\n🎨 Rendering HTML presentations...")
    
    # Light theme
    print("   🌞 Rendering light theme...")
    html_light = render_deck_from_dict(deck, Theme.LIGHT)
    light_file = "presentation_light.html"
    with open(light_file, 'w', encoding='utf-8') as f:
        f.write(html_light)
    print(f"   ✅ Light theme saved to: {light_file}")
    
    # Dark theme
    print("   🌙 Rendering dark theme...")
    html_dark = render_deck_from_dict(deck, Theme.DARK)
    dark_file = "presentation_dark.html"
    with open(dark_file, 'w', encoding='utf-8') as f:
        f.write(html_dark)
    print(f"   ✅ Dark theme saved to: {dark_file}")
    
    # Step 3: Generate a custom deck with user input
    print("\n🚀 Generate a custom presentation?")
    user_input = input("Enter a topic (or press Enter to skip): ").strip()
    
    if user_input:
        print(f"\n📝 Generating deck about: {user_input}")
        
        # Check if LLM is available
        use_llm = bool(os.getenv("OPENAI_API_KEY"))
        if use_llm:
            print("   🤖 Using LLM for content generation...")
        else:
            print("   📋 Using template-based content generation...")
        
        generator_custom = DeckGenerator(use_llm=use_llm)
        custom_deck = generator_custom.generate_deck(user_input, num_slides=6)
        
        # Save and render custom deck
        custom_deck_file = save_deck_to_file(custom_deck, "custom_deck.json")
        print(f"   ✅ Custom deck saved to: {custom_deck_file}")
        
        # Render custom deck
        custom_html = render_deck_from_dict(custom_deck, Theme.LIGHT)
        custom_file = "custom_presentation.html"
        with open(custom_file, 'w', encoding='utf-8') as f:
            f.write(custom_html)
        print(f"   ✅ Custom presentation saved to: {custom_file}")
    
    # Step 4: Display summary
    print("\n📊 Summary")
    print("=" * 50)
    print("Generated files:")
    print(f"  - {deck_file} (sample deck structure)")
    print(f"  - {light_file} (light theme presentation)")
    print(f"  - {dark_file} (dark theme presentation)")
    if user_input:
        print(f"  - custom_deck.json (custom deck structure)")
        print(f"  - {custom_file} (custom presentation)")
    
    # Step 5: Open in browser
    print("\n🌐 Opening presentations in browser...")
    try:
        # Open light theme version
        file_path = Path(light_file).absolute()
        webbrowser.open(f"file://{file_path}")
        print(f"   ✅ Opened: {light_file}")
    except Exception as e:
        print(f"   ⚠️  Could not open browser: {e}")
        print(f"   📂 Please open {light_file} manually in your browser")
    
    print("\n✨ Demo complete! Check the generated HTML files.")


def demonstrate_error_handling():
    """Demonstrate error handling capabilities."""
    print("\n🔧 Testing Error Handling")
    print("=" * 50)
    
    # Test with invalid deck structure
    invalid_deck = {
        "title": "Test Deck",
        "slides": [
            {"layout": "invalid_layout", "content": {}},
            {"content": {"title": "Missing layout"}},
            {"layout": "title"}  # Missing content
        ]
    }
    
    renderer = HTMLRenderer()
    html = renderer.render_deck(invalid_deck)
    
    with open("error_handling_demo.html", 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ Error handling demo saved to: error_handling_demo.html")


def demonstrate_all_layouts():
    """Generate a comprehensive demo showing all layout variations."""
    print("\n🎭 Generating All Layout Variations Demo")
    print("=" * 50)
    
    # Create a deck with multiple examples of each layout
    all_layouts_deck = {
        "title": "Complete Layout Showcase",
        "author": "Demo System",
        "description": "Demonstrating all available slide layouts and variations",
        "theme": "light",
        "slides": [
            # Title variations
            {
                "layout": "title",
                "content": {
                    "title": "Welcome to the Layout Showcase",
                    "subtitle": "Exploring All Presentation Possibilities",
                    "content": "This presentation demonstrates every available layout type"
                }
            },
            {
                "layout": "title",
                "content": {
                    "title": "Minimal Title Slide",
                    "subtitle": "Sometimes less is more"
                }
            },
            
            # Two column variations
            {
                "layout": "two_column",
                "content": {
                    "title": "Comparing Technologies",
                    "left_content": "# Traditional Approach\n\nMonolithic architecture with:\n- Single codebase\n- Shared database\n- Centralized deployment",
                    "right_content": "# Modern Approach\n\nMicroservices with:\n- Distributed services\n- Independent databases\n- Container orchestration"
                }
            },
            
            # Bullet points variations
            {
                "layout": "bullet_points",
                "content": {
                    "title": "Project Milestones",
                    "content": "Key deliverables for Q4 2024:",
                    "bullets": [
                        "Complete MVP development by October 15",
                        "User testing and feedback collection",
                        "Performance optimization and security audit",
                        "Documentation and training materials",
                        "Production deployment and monitoring setup"
                    ]
                }
            },
            
            # Image-text variations
            {
                "layout": "image_text",
                "content": {
                    "title": "System Architecture",
                    "image_url": "https://via.placeholder.com/600x400/3498db/ffffff?text=System+Architecture",
                    "image_caption": "High-level system design",
                    "content": "Our architecture follows cloud-native principles with auto-scaling, fault tolerance, and high availability built in from the ground up."
                }
            },
            
            # Quote variations
            {
                "layout": "quote",
                "content": {
                    "quote": "The best time to plant a tree was 20 years ago. The second best time is now.",
                    "author": "Chinese Proverb"
                }
            },
            
            # Full image variations
            {
                "layout": "full_image",
                "content": {
                    "title": "Data Visualization",
                    "image_url": "https://via.placeholder.com/800x600/2ecc71/ffffff?text=Analytics+Dashboard",
                    "image_caption": "Real-time analytics dashboard showing key metrics"
                }
            }
        ]
    }
    
    # Render in both themes
    for theme in [Theme.LIGHT, Theme.DARK]:
        renderer = HTMLRenderer(theme=theme)
        html = renderer.render_deck(all_layouts_deck)
        
        filename = f"all_layouts_{theme.value}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ {theme.value.capitalize()} theme showcase saved to: {filename}")


if __name__ == "__main__":
    # Run main demo
    main()
    
    # Additional demos
    print("\n" + "=" * 50)
    print("Running additional demonstrations...")
    
    demonstrate_error_handling()
    demonstrate_all_layouts()
    
    print("\n🎉 All demos complete!")
    print("Check the generated HTML files in your current directory.")