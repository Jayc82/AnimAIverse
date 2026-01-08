# Quick Setup Guide for AnimAIverse

This guide will get you up and running with AnimAIverse in 5 minutes.

## Prerequisites

- Python 3.8+ installed
- pip package manager
- Git (for cloning)

## Step 1: Get the Code

```bash
git clone https://github.com/Jayc82/AnimAIverse.git
cd AnimAIverse
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask and Flask-CORS (web app)
- Gunicorn (production server)
- OpenAI and Anthropic (AI engines)
- PyYAML, Pillow, NumPy (core utilities)
- Colorama, tqdm (CLI enhancements)

## Step 3: Configure API Keys

### Option A: Environment Variables (Recommended)

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use any text editor
```

Add:
```
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
```

### Option B: Export Directly

```bash
export OPENAI_API_KEY=sk-your-openai-key-here
export ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
```

### Getting API Keys

**OpenAI**: https://platform.openai.com/api-keys
**Anthropic**: https://console.anthropic.com/settings/keys

## Step 4: Run AnimAIverse

### Option A: Web App (Recommended)

```bash
python app_on_the_go.py
```

Then open http://localhost:5000 in your browser (works on mobile too!)

### Option B: Command Line

```bash
python animai.py
```

This runs a demo animation creation.

## Step 5: Create Your First Animation

### Using Web App:

1. Fill in the form:
   - Genre: action, drama, comedy, or adventure
   - Theme: "A hero's journey"
   - Characters: "Hero, Villain, Mentor"
   - Duration: 5 minutes
   - Language: English (or any of 12 supported languages)

2. Click "Create Animation"

3. Wait for the 9-agent pipeline to complete

4. View results with:
   - Characters generated
   - Voice types used
   - VFX shots created
   - Quality score

### Using Python:

```python
from animai import AnimAIverse

animai = AnimAIverse()

result = animai.create_animation(
    genre="action",
    theme="A hero saves the world",
    characters=["Hero", "Villain"],
    duration=5,
    language="en"
)

print(f"Quality Score: {result['results']['final_edit']['quality_report']['metrics']['overall_score']}")
```

## Common Issues

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "API Key Not Found"
Make sure you've set your environment variables:
```bash
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY
```

### Port Already in Use
Change the port:
```bash
export FLASK_PORT=8080
python app_on_the_go.py
```

## Next Steps

- **Deploy to Cloud**: See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- **Advanced Features**: See [ADVANCED_FEATURES.md](ADVANCED_FEATURES.md) for details on all agents
- **Multi-Language**: See [LANGUAGES.md](LANGUAGES.md) for language support
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for usage examples

## Quick Deploy

Deploy to Heroku in 2 minutes:

```bash
./deploy.sh heroku my-animaiverse-app
```

That's it! You're ready to create revolutionary animations! 🚀

## Help

- Documentation: See README.md
- Issues: https://github.com/Jayc82/AnimAIverse/issues
- Examples: See EXAMPLES.md
