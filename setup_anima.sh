#!/bin/bash

# ANIMA Setup Script
# Prepares the ANIMA token system for first run

echo "=================================="
echo "🪙  ANIMA SETUP"
echo "   The Bitcoin of Animation"
echo "=================================="
echo ""

# Create token data directory
echo "📁 Creating token data directory..."
mkdir -p token
echo "   ✓ token/ directory created"

# Create data storage directory
echo "📁 Creating data storage..."
mkdir -p token_data
echo "   ✓ token_data/ directory created"

# Check Python version
echo ""
echo "🐍 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Python version: $python_version"

if command -v python3 &> /dev/null; then
    echo "   ✓ Python 3 found"
else
    echo "   ✗ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Check if requirements are installed
echo ""
echo "📦 Checking dependencies..."
if python3 -c "import yaml" 2>/dev/null; then
    echo "   ✓ PyYAML installed"
else
    echo "   ⚠ PyYAML not found. Installing..."
    pip3 install pyyaml
fi

# Create initial configuration if it doesn't exist
if [ ! -f "config/config.yaml" ]; then
    echo ""
    echo "⚙️  Creating default configuration..."
    mkdir -p config
    cat > config/config.yaml << 'EOF'
# AnimAIverse ANIMA Configuration

animation:
  resolution: [1920, 1080]
  fps: 30
  style: "cinematic"
  quality: "high"

agents:
  writer:
    enabled: true
  director:
    enabled: true
  animator:
    enabled: true
  character_generator:
    enabled: true
  graphics:
    enabled: true
  voice:
    enabled: true
  special_effects:
    enabled: true
  scene_composer:
    enabled: true
  editor:
    enabled: true

memory:
  style_memory_path: "memory/style_memory.json"
  learning_history_path: "memory/learning_history.json"
  adaptive_learning_path: "memory/adaptive_learning.json"

token:
  data_path: "token_data"
  initial_supply: 10000000
  decimals: 8
EOF
    echo "   ✓ Default config created at config/config.yaml"
else
    echo "   ✓ Configuration file exists"
fi

# All set!
echo ""
echo "=================================="
echo "✅ SETUP COMPLETE!"
echo "=================================="
echo ""
echo "🚀 Quick Start:"
echo "   1. Run demo:  python3 demo_anima.py"
echo "   2. Start app: python3 anima_app.py"
echo ""
echo "📚 Documentation:"
echo "   - User Guide:    ANIMA_README.md"
echo "   - Technical:     ANIMA_TECHNICAL.md"
echo "   - Tokenomics:    ANIMA_TOKENOMICS.md"
echo ""
echo "🌟 Welcome to ANIMA - The Bitcoin of Animation!"
echo ""
