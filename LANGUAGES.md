# Multi-Language Animation Examples

This document demonstrates how to create animations in different languages using AnimAIverse.

## Example 1: English Animation (Default)

```python
from animai import AnimAIverse

animai = AnimAIverse()

result = animai.create_animation(
    genre="action",
    theme="A hero discovers their destiny",
    characters=["Alex - The Chosen One", "Morgan - The Mentor", "Kane - The Adversary"],
    duration=5,
    language="en"
)
```

## Example 2: Spanish Animation

```python
result_es = animai.create_animation(
    genre="drama",
    theme="Una familia reunida después de años",
    characters=["María - La Madre", "Juan - El Hijo", "Carmen - La Hermana"],
    duration=5,
    language="es"
)
```

## Example 3: French Animation

```python
result_fr = animai.create_animation(
    genre="adventure",
    theme="Une quête à travers les montagnes mystiques",
    characters=["Pierre - L'aventurier", "Claire - La guide", "Marcel - Le sage"],
    duration=5,
    language="fr"
)
```

## Example 4: Japanese Animation

```python
result_ja = animai.create_animation(
    genre="action",
    theme="古代の秘宝を守る戦い",
    characters=["勇者 - 主人公", "魔法使い - 仲間", "闇の王 - 敵"],
    duration=5,
    language="ja"
)
```

## Example 5: German Animation

```python
result_de = animai.create_animation(
    genre="comedy",
    theme="Missverständnisse im Büro",
    characters=["Hans - Der Chef", "Greta - Die Assistentin", "Klaus - Der Praktikant"],
    duration=4,
    language="de"
)
```

## Example 6: Multi-Language Series

Create a series with episodes in different languages:

```python
from animai import AnimAIverse

animai = AnimAIverse()

# Define episodes in different languages
episodes = [
    {
        "language": "en",
        "theme": "The Beginning",
        "characters": ["Hero", "Guide", "Enemy"]
    },
    {
        "language": "es",
        "theme": "El Viaje",
        "characters": ["Héroe", "Guía", "Enemigo"]
    },
    {
        "language": "fr",
        "theme": "La Bataille",
        "characters": ["Héros", "Guide", "Ennemi"]
    },
    {
        "language": "ja",
        "theme": "決戦",
        "characters": ["英雄", "導き手", "敵"]
    }
]

results = []
for i, episode in enumerate(episodes):
    print(f"\nCreating Episode {i+1} in {episode['language']}...")
    result = animai.create_animation(
        genre="adventure",
        theme=episode['theme'],
        characters=episode['characters'],
        duration=5,
        language=episode['language']
    )
    results.append(result)

print(f"\n✅ Created {len(results)} episodes in {len(set(e['language'] for e in episodes))} languages!")
```

## Example 7: Language Detection and Switching

```python
from animai import AnimAIverse

animai = AnimAIverse()

# Check current language
current = animai.get_current_language()
print(f"Current language: {current}")

# Get all supported languages
languages = animai.get_supported_languages()
print("\nSupported languages:")
for code, name in languages.items():
    print(f"  {code}: {name}")

# Set a new default language
animai.set_language("es")
print(f"\nLanguage changed to: {animai.get_current_language()}")

# Create animation (will use Spanish by default now)
result = animai.create_animation(
    genre="action",
    theme="Aventura épica",
    duration=5
    # language parameter not needed - uses current language
)
```

## Example 8: Right-to-Left Language (Arabic)

```python
result_ar = animai.create_animation(
    genre="adventure",
    theme="رحلة عبر الصحراء",
    characters=["البطل", "المرشد", "الخصم"],
    duration=5,
    language="ar"
)

# Check text direction
from utils.language_manager import LanguageManager
lang_mgr = LanguageManager()
direction = lang_mgr.get_text_direction("ar")
print(f"Text direction for Arabic: {direction}")  # Output: rtl
```

## Example 9: Chinese Animation

```python
result_zh = animai.create_animation(
    genre="action",
    theme="武侠传奇",
    characters=["剑客", "师傅", "反派"],
    duration=5,
    language="zh"
)
```

## Example 10: Portuguese Animation

```python
result_pt = animai.create_animation(
    genre="comedy",
    theme="Confusões na cidade grande",
    characters=["João - O Otimista", "Ana - A Realista", "Pedro - O Atrapalhado"],
    duration=4,
    language="pt"
)
```

## Language-Specific Features

### Script Generation
Scripts are generated in the target language with:
- Proper grammar and syntax
- Cultural context awareness
- Idiomatic expressions
- Appropriate dialogue style

### Character Names
Use culturally appropriate character names:

```python
# English
characters=["John Smith", "Sarah Jones", "Michael Brown"]

# Japanese
characters=["田中太郎", "佐藤花子", "鈴木一郎"]

# Spanish
characters=["Carlos García", "María López", "José Martínez"]

# Arabic
characters=["أحمد", "فاطمة", "محمد"]
```

### Theme Translation
Themes can be provided in any supported language:

```python
# English
theme="A hero's journey through time"

# Spanish
theme="El viaje de un héroe a través del tiempo"

# French
theme="Le voyage d'un héros à travers le temps"

# Japanese
theme="時を超える英雄の旅"
```

## Best Practices

### 1. Language Consistency
Keep language consistent throughout a production:

```python
# Good - Everything in Spanish
result = animai.create_animation(
    genre="drama",
    theme="Una historia de amor",
    characters=["Carlos", "María"],
    language="es"
)

# Avoid - Mixed languages
result = animai.create_animation(
    genre="drama",
    theme="A love story",  # English theme
    characters=["Carlos", "María"],  # Spanish names
    language="es"  # Spanish production
)
```

### 2. Character Names
Use appropriate names for the target language:

```python
# English production
animai.create_animation(..., language="en", characters=["James", "Emma"])

# Japanese production
animai.create_animation(..., language="ja", characters=["太郎", "花子"])
```

### 3. Genre Names
Genre names are standardized in English across all languages:

```python
# All use English genre names
animai.create_animation(genre="action", language="es")
animai.create_animation(genre="drama", language="ja")
animai.create_animation(genre="comedy", language="fr")
```

### 4. Checking Language Support
Always verify language support before production:

```python
language = "ko"  # Korean
if animai.language_manager.is_language_supported(language):
    result = animai.create_animation(genre="action", language=language)
else:
    print(f"Language {language} not supported")
```

## Troubleshooting

### Issue: Language not supported
**Solution**: Check supported languages list:
```python
languages = animai.get_supported_languages()
print(languages)
```

### Issue: Mixed language output
**Solution**: Ensure all input (theme, characters) matches the target language

### Issue: Character encoding problems
**Solution**: Use UTF-8 encoding for all files and ensure terminal supports Unicode

## Additional Resources

- See `config/languages.yaml` for language configuration
- See `utils/language_manager.py` for implementation details
- Primary language is English (en) - all other languages are supported
- Language affects script generation, dialogue, and UI messages
