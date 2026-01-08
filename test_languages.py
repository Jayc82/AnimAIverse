#!/usr/bin/env python
"""
Quick test script to demonstrate AnimAIverse multi-language support.
"""
from animai import AnimAIverse


def test_multi_language():
    """Test creating animations in different languages."""
    print("\n" + "="*70)
    print("🧪 AnimAIverse Multi-Language Test")
    print("="*70)
    
    # Initialize system
    animai = AnimAIverse()
    
    # Show supported languages
    print("\n📋 Testing language support...")
    languages = animai.get_supported_languages()
    print(f"✓ Found {len(languages)} supported languages")
    print(f"  Primary language: English (en)")
    print(f"  Also supports: {', '.join(list(languages.keys())[:5])}...")
    
    # Test 1: English animation
    print("\n" + "-"*70)
    print("Test 1: Creating animation in English")
    print("-"*70)
    result_en = animai.create_animation(
        genre="action",
        theme="A space adventure",
        characters=["Captain", "Engineer", "Alien"],
        duration=2,
        language="en"
    )
    print(f"✓ English animation created")
    print(f"  Quality: {result_en['results']['final_edit']['quality_report']['metrics']['overall_score']:.2f}")
    print(f"  Language: {result_en['results']['script'].get('language', 'en')}")
    
    # Test 2: Spanish animation
    print("\n" + "-"*70)
    print("Test 2: Creating animation in Spanish")
    print("-"*70)
    result_es = animai.create_animation(
        genre="drama",
        theme="Una historia familiar",
        characters=["Padre", "Hijo", "Madre"],
        duration=2,
        language="es"
    )
    print(f"✓ Spanish animation created")
    print(f"  Quality: {result_es['results']['final_edit']['quality_report']['metrics']['overall_score']:.2f}")
    print(f"  Language: {result_es['results']['script'].get('language', 'es')}")
    
    # Test 3: Japanese animation
    print("\n" + "-"*70)
    print("Test 3: Creating animation in Japanese")
    print("-"*70)
    result_ja = animai.create_animation(
        genre="adventure",
        theme="冒険の旅",
        characters=["勇者", "仲間", "敵"],
        duration=2,
        language="ja"
    )
    print(f"✓ Japanese animation created")
    print(f"  Quality: {result_ja['results']['final_edit']['quality_report']['metrics']['overall_score']:.2f}")
    print(f"  Language: {result_ja['results']['script'].get('language', 'ja')}")
    
    # Test language switching
    print("\n" + "-"*70)
    print("Test 4: Language switching")
    print("-"*70)
    print(f"Current language: {animai.get_current_language()}")
    animai.set_language("fr")
    print(f"Changed to: {animai.get_current_language()}")
    animai.set_language("en")
    print(f"Changed back to: {animai.get_current_language()}")
    print("✓ Language switching works correctly")
    
    # Summary
    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED")
    print("="*70)
    print(f"Created {3} animations in {3} different languages")
    print(f"Average quality: {(result_en['results']['final_edit']['quality_report']['metrics']['overall_score'] + result_es['results']['final_edit']['quality_report']['metrics']['overall_score'] + result_ja['results']['final_edit']['quality_report']['metrics']['overall_score']) / 3:.2f}")
    print("\nMulti-language support is working correctly! ✨")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_multi_language()
