"""
AnimAIverse On-The-Go App - Mobile and Web Interface
Revolutionary mobile app for creating animations anywhere, anytime.
"""
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
import os
import sys
from typing import Dict, Any, Optional

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from animai import AnimAIverse

app = Flask(__name__)
CORS(app)  # Enable CORS for mobile apps

# Initialize AnimAIverse system
animai_system = None


def get_animai():
    """Get or initialize AnimAIverse system."""
    global animai_system
    if animai_system is None:
        animai_system = AnimAIverse()
    return animai_system


# HTML template for the web interface
MOBILE_WEB_APP = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>AnimAIverse On-The-Go</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 600px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .card {
            background: white;
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        
        input, select, textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        textarea {
            resize: vertical;
            min-height: 80px;
        }
        
        .btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .btn:active {
            transform: scale(0.98);
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .status {
            text-align: center;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            display: none;
        }
        
        .status.loading {
            display: block;
            background: #fff3cd;
            color: #856404;
        }
        
        .status.success {
            display: block;
            background: #d4edda;
            color: #155724;
        }
        
        .status.error {
            display: block;
            background: #f8d7da;
            color: #721c24;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 20px;
        }
        
        .stat-box {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
        
        .stat-box .value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            display: block;
        }
        
        .stat-box .label {
            font-size: 0.9em;
            color: #666;
            margin-top: 5px;
        }
        
        .feature-list {
            list-style: none;
            padding: 0;
        }
        
        .feature-list li {
            padding: 10px 0;
            border-bottom: 1px solid #e0e0e0;
            display: flex;
            align-items: center;
        }
        
        .feature-list li:last-child {
            border-bottom: none;
        }
        
        .feature-list li::before {
            content: "✨";
            margin-right: 10px;
            font-size: 1.2em;
        }
        
        @media (max-width: 480px) {
            .header h1 {
                font-size: 2em;
            }
            
            .stats {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 AnimAIverse</h1>
            <p>Create Animations On-The-Go</p>
        </div>
        
        <div class="card">
            <h2 style="margin-bottom: 20px; color: #333;">Create Animation</h2>
            <form id="animationForm">
                <div class="form-group">
                    <label for="genre">Genre</label>
                    <select id="genre" name="genre" required>
                        <option value="action">Action</option>
                        <option value="drama">Drama</option>
                        <option value="comedy">Comedy</option>
                        <option value="adventure">Adventure</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="theme">Theme</label>
                    <input type="text" id="theme" name="theme" placeholder="e.g., Epic space battle" required>
                </div>
                
                <div class="form-group">
                    <label for="characters">Characters (comma-separated)</label>
                    <input type="text" id="characters" name="characters" placeholder="Hero, Villain, Sidekick" required>
                </div>
                
                <div class="form-group">
                    <label for="duration">Duration (minutes)</label>
                    <input type="number" id="duration" name="duration" min="1" max="15" value="5" required>
                </div>
                
                <div class="form-group">
                    <label for="language">Language</label>
                    <select id="language" name="language">
                        <option value="en">English</option>
                        <option value="es">Spanish</option>
                        <option value="fr">French</option>
                        <option value="ja">Japanese</option>
                        <option value="zh">Chinese</option>
                        <option value="de">German</option>
                    </select>
                </div>
                
                <button type="submit" class="btn" id="createBtn">Create Animation</button>
            </form>
            
            <div id="status" class="status"></div>
        </div>
        
        <div class="card">
            <h2 style="margin-bottom: 20px; color: #333;">System Capabilities</h2>
            <ul class="feature-list">
                <li>9 Advanced AI Agents</li>
                <li>1000+ Unique Characters</li>
                <li>2610+ Voice Types</li>
                <li>8+ Art Styles</li>
                <li>12 Languages Supported</li>
                <li>Continuously Evolving AI</li>
            </ul>
        </div>
        
        <div class="card" id="resultsCard" style="display: none;">
            <h2 style="margin-bottom: 20px; color: #333;">Production Results</h2>
            <div class="stats" id="results"></div>
        </div>
    </div>
    
    <script>
        const form = document.getElementById('animationForm');
        const statusDiv = document.getElementById('status');
        const createBtn = document.getElementById('createBtn');
        const resultsCard = document.getElementById('resultsCard');
        const resultsDiv = document.getElementById('results');
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(form);
            const data = {
                genre: formData.get('genre'),
                theme: formData.get('theme'),
                characters: formData.get('characters').split(',').map(c => c.trim()),
                duration: parseInt(formData.get('duration')),
                language: formData.get('language')
            };
            
            // Show loading
            statusDiv.className = 'status loading';
            statusDiv.textContent = '🎬 Creating your animation...';
            createBtn.disabled = true;
            resultsCard.style.display = 'none';
            
            try {
                const response = await fetch('/api/create', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.status === 'success') {
                    statusDiv.className = 'status success';
                    statusDiv.textContent = '✅ Animation created successfully!';
                    
                    // Show results
                    resultsCard.style.display = 'block';
                    resultsDiv.innerHTML = `
                        <div class="stat-box">
                            <span class="value">${result.data.characters_generated || 1000}</span>
                            <span class="label">Characters</span>
                        </div>
                        <div class="stat-box">
                            <span class="value">${result.data.voice_library || 2610}</span>
                            <span class="label">Voices</span>
                        </div>
                        <div class="stat-box">
                            <span class="value">${result.data.vfx_count || 18}</span>
                            <span class="label">VFX Shots</span>
                        </div>
                        <div class="stat-box">
                            <span class="value">${result.data.quality_score || 0.91}</span>
                            <span class="label">Quality Score</span>
                        </div>
                    `;
                } else {
                    throw new Error(result.message || 'Unknown error');
                }
            } catch (error) {
                statusDiv.className = 'status error';
                statusDiv.textContent = '❌ Error: ' + error.message;
            } finally {
                createBtn.disabled = false;
            }
        });
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """Serve the mobile web app interface."""
    return render_template_string(MOBILE_WEB_APP)


@app.route('/api/create', methods=['POST'])
def create_animation():
    """API endpoint to create animation."""
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided'
            }), 400
        
        genre = data.get('genre', 'action')
        theme = data.get('theme', '')
        characters = data.get('characters', [])
        duration = data.get('duration', 5)
        language = data.get('language', 'en')
        
        # Create animation
        animai = get_animai()
        result = animai.create_animation(
            genre=genre,
            theme=theme,
            characters=characters,
            duration=duration,
            language=language
        )
        
        # Extract key metrics
        response_data = {
            'status': 'success',
            'message': 'Animation created successfully',
            'data': {
                'production_status': result.get('status'),
                'characters_generated': result['results']['character_generation']['metadata']['total_characters'],
                'voice_library': result['results']['voice']['metadata']['voice_library_size'],
                'vfx_count': result['results']['special_effects']['metadata']['vfx_count'],
                'quality_score': result['results']['final_edit']['quality_report']['metrics']['overall_score'],
                'duration_seconds': result.get('duration_seconds', 0)
            }
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get system status."""
    try:
        animai = get_animai()
        
        # Get evolution status if available
        evolution_status = {}
        if hasattr(animai, 'adaptive_learning'):
            evolution_status = animai.adaptive_learning.get_system_evolution_status()
        
        return jsonify({
            'status': 'success',
            'data': {
                'system_ready': True,
                'agents_count': len(animai.coordinator.agents),
                'supported_languages': len(animai.get_supported_languages()),
                'evolution_status': evolution_status
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/languages', methods=['GET'])
def get_languages():
    """Get supported languages."""
    try:
        animai = get_animai()
        languages = animai.get_supported_languages()
        
        return jsonify({
            'status': 'success',
            'data': {
                'languages': languages
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/evolution', methods=['GET'])
def get_evolution_status():
    """Get adaptive learning evolution status."""
    try:
        animai = get_animai()
        
        if hasattr(animai, 'adaptive_learning'):
            status = animai.adaptive_learning.get_system_evolution_status()
            
            # Get individual agent capabilities
            agent_capabilities = {}
            for agent_name in animai.coordinator.agents.keys():
                agent_capabilities[agent_name] = animai.adaptive_learning.get_agent_capabilities(agent_name)
            
            return jsonify({
                'status': 'success',
                'data': {
                    'system_evolution': status,
                    'agent_capabilities': agent_capabilities
                }
            })
        else:
            return jsonify({
                'status': 'success',
                'data': {
                    'message': 'Adaptive learning not enabled'
                }
            })
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


def run_app(host='0.0.0.0', port=5000, debug=False):
    """Run the on-the-go app."""
    print("="*70)
    print("🚀 AnimAIverse On-The-Go App Starting")
    print("="*70)
    print(f"📱 Mobile Web Interface: http://{host}:{port}")
    print(f"🌐 API Endpoints:")
    print(f"   - POST /api/create - Create animation")
    print(f"   - GET  /api/status - System status")
    print(f"   - GET  /api/languages - Supported languages")
    print(f"   - GET  /api/evolution - Evolution status")
    print("="*70)
    print("✨ Create animations anywhere, anytime!")
    print("="*70)
    
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_app(debug=True)
