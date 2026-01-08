# AnimAIverse Examples

This document provides comprehensive examples for using AnimAIverse.

## Basic Examples

### Example 1: Simple Action Animation

```python
from animai import AnimAIverse

# Initialize
animai = AnimAIverse()

# Create a simple action animation
result = animai.create_animation(
    genre="action",
    theme="Urban rescue mission",
    characters=["Agent X", "Tech Expert", "Crime Boss"],
    duration=3
)

# Print summary
print(f"Quality Score: {result['results']['final_edit']['quality_report']['metrics']['overall_score']}")
```

### Example 2: Drama Series

```python
# Create a character-driven drama
result = animai.create_animation(
    genre="drama",
    theme="Family reunion after years apart",
    characters=["Mother", "Estranged Son", "Sister"],
    duration=5,
    style_preferences={
        "visual_style": "intimate",
        "animation_style": "realistic"
    }
)
```

### Example 3: Comedy Short

```python
# Create a comedic animation
result = animai.create_animation(
    genre="comedy",
    theme="Office mishaps and misunderstandings",
    characters=["Bumbling Boss", "Sarcastic Employee", "Intern"],
    duration=4,
    style_preferences={
        "visual_style": "bright",
        "animation_style": "exaggerated"
    }
)
```

## Advanced Examples

### Example 4: Custom Configuration

```python
from animai import AnimAIverse
import yaml

# Load custom config
custom_config = {
    "animation": {
        "resolution": [2560, 1440],
        "fps": 60,
        "style": "hyper_realistic"
    }
}

# Save custom config
with open('config/custom_config.yaml', 'w') as f:
    yaml.dump(custom_config, f)

# Initialize with custom config
animai = AnimAIverse(config_path='config/custom_config.yaml')

# Create animation
result = animai.create_animation(
    genre="adventure",
    theme="Deep space exploration",
    characters=["Captain", "Android", "Alien Diplomat"],
    duration=8
)
```

### Example 5: Batch Production

```python
from animai import AnimAIverse

animai = AnimAIverse()

# Create multiple episodes
themes = [
    "The hero discovers their power",
    "Training montage and preparation",
    "First confrontation with the villain",
    "Building the team",
    "The final battle"
]

results = []
for i, theme in enumerate(themes):
    print(f"\nCreating Episode {i+1}...")
    result = animai.create_animation(
        genre="action",
        theme=theme,
        characters=["Hero", "Mentor", "Rival", "Villain"],
        duration=5
    )
    results.append(result)
    print(f"Episode {i+1} Quality: {result['results']['final_edit']['quality_report']['metrics']['overall_score']:.2f}")

# Print series summary
print(f"\nSeries Complete: {len(results)} episodes")
avg_quality = sum(r['results']['final_edit']['quality_report']['metrics']['overall_score'] for r in results) / len(results)
print(f"Average Quality: {avg_quality:.2f}")
```

### Example 6: Learning System Integration

```python
from animai import AnimAIverse

animai = AnimAIverse()

# Create several animations
for i in range(5):
    result = animai.create_animation(
        genre="action",
        theme=f"Mission {i+1}",
        duration=3
    )

# Check learning progress
summary = animai.get_learning_summary()
print(f"Total Productions: {summary['total_productions']}")
print(f"Average Quality: {summary['average_quality']:.2f}")
print(f"Improvement Trend: {summary['improvement_trend']}")

# Get recommendations
recommendations = animai.get_style_recommendations("action")
print(f"Recommended Visual Style: {recommendations.get('visual_style')}")
print(f"Confidence: {recommendations.get('confidence'):.2f}")
```

### Example 7: Custom Style Preferences

```python
from animai import AnimAIverse

animai = AnimAIverse()

# Define detailed style preferences
detailed_style = {
    "visual_style": "cyberpunk",
    "animation_style": "fluid",
    "composition_style": "dynamic",
    "color_grading": {
        "contrast": 1.5,
        "saturation": 1.3,
        "temperature": "cool",
        "tint": "blue_purple"
    },
    "preferred_palettes": [
        ["#00FFFF", "#FF00FF", "#0000FF", "#000000"],
        ["#FF1493", "#00CED1", "#FFD700", "#1C1C1C"]
    ]
}

result = animai.create_animation(
    genre="adventure",
    theme="Hacker infiltrates mega-corporation",
    characters=["Hacker", "AI Assistant", "Security Chief"],
    duration=6,
    style_preferences=detailed_style
)
```

### Example 8: Accessing Individual Agent Results

```python
from animai import AnimAIverse

animai = AnimAIverse()

result = animai.create_animation(
    genre="adventure",
    theme="Ancient temple exploration",
    duration=5
)

# Access different agent outputs
script = result['results']['script']
print(f"Title: {script['script']['title']}")
print(f"Number of scenes: {len(script['script']['scenes'])}")

direction = result['results']['direction']
print(f"Number of shots: {len(direction['shot_list'])}")

animation = result['results']['animation']
print(f"Number of character animations: {len(animation['character_animations'])}")

composition = result['results']['composition']
print(f"Number of composed scenes: {len(composition['composed_scenes'])}")

final_edit = result['results']['final_edit']
print(f"Final quality score: {final_edit['quality_report']['metrics']['overall_score']:.2f}")
```

### Example 9: Export Production Data

```python
from animai import AnimAIverse
import json

animai = AnimAIverse()

result = animai.create_animation(
    genre="action",
    theme="Space station emergency",
    duration=5
)

# Export complete production data
with open('my_animation.json', 'w') as f:
    json.dump(result, f, indent=2)

print("Production data exported to my_animation.json")
```

### Example 10: Real-time Status Monitoring

```python
from animai import AnimAIverse
import time
import threading

animai = AnimAIverse()

def monitor_status():
    """Monitor production status in real-time"""
    while True:
        status = animai.get_production_status()
        if status['status'] == 'in_progress':
            print(f"Status: {status['status']} - Completed stages: {status['completed_stages']}/5")
            time.sleep(1)
        elif status['status'] == 'completed':
            print("Production completed!")
            break
        else:
            time.sleep(1)

# Start monitoring in background
monitor_thread = threading.Thread(target=monitor_status)
monitor_thread.start()

# Create animation
result = animai.create_animation(
    genre="adventure",
    theme="Journey through mystical lands",
    duration=7
)

monitor_thread.join()
```

## Tips and Best Practices

### 1. Character Names
Use descriptive character names for better script generation:
```python
characters = [
    "Sarah - Brave archaeologist",
    "Max - Tech-savvy sidekick",
    "Dr. Venom - Ruthless collector"
]
```

### 2. Theme Specificity
More specific themes lead to better narratives:
```python
# Good
theme = "A detective solves a murder in a futuristic city"

# Better
theme = "A cybernetic detective uncovers a conspiracy while investigating a murder in Neo-Tokyo 2157"
```

### 3. Duration Guidelines
- **1-3 minutes**: Quick action sequences or comedy sketches
- **4-7 minutes**: Complete story arcs with character development
- **8-15 minutes**: Complex narratives with multiple plot threads

### 4. Style Consistency
For series production, maintain consistent style preferences:
```python
series_style = {
    "visual_style": "anime",
    "animation_style": "dynamic"
}

for episode in episodes:
    result = animai.create_animation(
        genre="action",
        theme=episode['theme'],
        style_preferences=series_style  # Use same style
    )
```

### 5. Learning Optimization
The system learns better with more productions:
```python
# Run at least 10 productions for meaningful learning insights
for i in range(10):
    result = animai.create_animation(genre="action", duration=3)

# Now check learning summary
summary = animai.get_learning_summary()
```

## Troubleshooting

### Issue: Low Quality Score
**Solution**: Adjust agent temperature settings in config.yaml

### Issue: Inconsistent Styles
**Solution**: Use explicit style_preferences for each production

### Issue: Memory Errors
**Solution**: Reduce duration or clear old learning history

For more examples, see the test files in the repository.
