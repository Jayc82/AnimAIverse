# Quick Start Guide - AnimAIverse

## Installation

```bash
# Clone the repository
git clone https://github.com/Jayc82/AnimAIverse.git
cd AnimAIverse

# Install dependencies
pip install -r requirements.txt
```

## Run Your First Animation

### Option 1: Run the Example
```bash
python animai.py
```

This will create a demo action animation in English.

### Option 2: Python Script
```python
from animai import AnimAIverse

# Initialize
animai = AnimAIverse()

# Create animation
result = animai.create_animation(
    genre="action",        # action, drama, comedy, or adventure
    theme="Space adventure",
    characters=["Hero", "Sidekick", "Villain"],
    duration=5,           # minutes
    language="en"         # or es, fr, ja, zh, etc.
)

# Check result
print(f"Status: {result['status']}")
print(f"Quality: {result['results']['final_edit']['quality_report']['metrics']['overall_score']}")
```

## Multi-Language Example

```python
# Spanish animation
result = animai.create_animation(
    genre="drama",
    theme="Una historia familiar",
    characters=["Padre", "Madre", "Hijo"],
    duration=5,
    language="es"
)

# Japanese animation
result = animai.create_animation(
    genre="adventure",
    theme="冒険の旅",
    characters=["勇者", "魔法使い", "戦士"],
    duration=5,
    language="ja"
)
```

## Available Languages

- **en** - English (Primary)
- **es** - Spanish
- **fr** - French
- **de** - German
- **it** - Italian
- **pt** - Portuguese
- **ja** - Japanese
- **ko** - Korean
- **zh** - Chinese
- **ar** - Arabic
- **ru** - Russian
- **hi** - Hindi

## Test Multi-Language Support

```bash
python test_languages.py
```

## Configuration

Edit `config/config.yaml` to customize:
- Animation resolution and FPS
- Agent parameters
- Memory settings
- Output preferences

## Output

Productions are saved to `output/` directory in JSON format with:
- Complete script with scenes
- Shot-by-shot direction
- Character animations
- Scene compositions
- Final edit with quality report

## Need Help?

- See `README.md` for complete documentation
- See `EXAMPLES.md` for more usage examples
- See `LANGUAGES.md` for language-specific documentation
- See `SUMMARY.md` for technical details

## What's Next?

1. Try different genres (action, drama, comedy, adventure)
2. Experiment with languages
3. Create a multi-episode series
4. Customize style preferences
5. Check learning progress with `animai.get_learning_summary()`

Enjoy creating animations with AI! 🎬✨
