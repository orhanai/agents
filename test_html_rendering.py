"""Simple test script for HTML rendering system without external dependencies."""

from html_renderer import HTMLRenderer, Theme

def test_html_renderer():
    """Test the HTML renderer with a sample deck."""
    print("🧪 Testing HTML Renderer...")
    print("=" * 50)
    
    # Create a sample deck
    sample_deck = {
        "title": "Test Presentation",
        "author": "Test System",
        "description": "Testing the HTML rendering system",
        "theme": "light",
        "slides": [
            {
                "layout": "title",
                "content": {
                    "title": "Welcome to the Test",
                    "subtitle": "HTML Rendering Demo",
                    "content": "This is a test of the rendering system"
                }
            },
            {
                "layout": "two_column",
                "content": {
                    "title": "Two Column Test",
                    "left_content": "# Left Side\n\nThis is the left column with:\n- Item 1\n- Item 2",
                    "right_content": "# Right Side\n\nThis is the right column with:\n- Item A\n- Item B"
                }
            },
            {
                "layout": "bullet_points",
                "content": {
                    "title": "Key Features",
                    "content": "The system supports:",
                    "bullets": [
                        "Pure HTML/CSS generation",
                        "Responsive design",
                        "Multiple themes",
                        "Six layout types"
                    ]
                }
            },
            {
                "layout": "quote",
                "content": {
                    "quote": "Simplicity is the ultimate sophistication.",
                    "author": "Leonardo da Vinci"
                }
            }
        ]
    }
    
    # Test light theme
    print("\n📝 Testing Light Theme...")
    renderer_light = HTMLRenderer(theme=Theme.LIGHT)
    html_light = renderer_light.render_deck(sample_deck)
    
    # Save light theme
    with open("test_light.html", "w", encoding="utf-8") as f:
        f.write(html_light)
    print("✅ Light theme rendered successfully! Saved to: test_light.html")
    
    # Test dark theme
    print("\n📝 Testing Dark Theme...")
    renderer_dark = HTMLRenderer(theme=Theme.DARK)
    html_dark = renderer_dark.render_deck(sample_deck)
    
    # Save dark theme
    with open("test_dark.html", "w", encoding="utf-8") as f:
        f.write(html_dark)
    print("✅ Dark theme rendered successfully! Saved to: test_dark.html")
    
    # Verify content
    print("\n🔍 Verifying rendered content...")
    checks = [
        ("<!DOCTYPE html>" in html_light, "HTML document structure"),
        ("Test Presentation" in html_light, "Deck title"),
        ("Welcome to the Test" in html_light, "Slide content"),
        ("--bg-color: #f5f5f5" in html_light, "Light theme styles"),
        ("--bg-color: #1a1a1a" in html_dark, "Dark theme styles"),
        ("responsive" in html_light.lower() or "@media" in html_light, "Responsive design"),
    ]
    
    all_passed = True
    for passed, description in checks:
        status = "✅" if passed else "❌"
        print(f"  {status} {description}")
        if not passed:
            all_passed = False
    
    # Test error handling
    print("\n🔧 Testing error handling...")
    try:
        renderer = HTMLRenderer()
        error_html = renderer.render_deck("invalid input")
        if "Error rendering deck" in error_html:
            print("  ✅ Error handling works correctly")
        else:
            print("  ❌ Error handling failed")
            all_passed = False
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        all_passed = False
    
    # Summary
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ All tests passed!")
        print("\n📂 Generated files:")
        print("  - test_light.html (Light theme presentation)")
        print("  - test_dark.html (Dark theme presentation)")
        print("\n🌐 Open these files in your browser to view the presentations!")
    else:
        print("❌ Some tests failed. Please check the output above.")
    
    return all_passed


if __name__ == "__main__":
    test_html_renderer()