"""
Writer Agent - Generates scripts, storylines, and dialogue.
Specializes in narrative structure and character development.
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent


class WriterAgent(BaseAgent):
    """Agent responsible for creating scripts and storylines."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("Writer", config)
        self.story_templates = {
            "action": "High-intensity action sequences with dynamic pacing",
            "drama": "Character-driven emotional storytelling",
            "comedy": "Humorous situations with timing and wit",
            "adventure": "Exploration and discovery narratives"
        }
        
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate script based on input requirements.
        
        Args:
            input_data: Dictionary containing:
                - genre: Story genre
                - theme: Central theme
                - characters: List of character descriptions
                - duration: Target duration in minutes
                - style_context: Previous style information
                - language: Target language code (default: 'en')
                - language_instruction: Instruction for language generation
                
        Returns:
            Dictionary containing:
                - script: Generated script with scenes
                - character_arcs: Character development notes
                - key_moments: Important plot points
                - dialogue: Character dialogues
                - language: Language used for generation
        """
        genre = input_data.get("genre", "action")
        theme = input_data.get("theme", "")
        characters = input_data.get("characters", [])
        duration = input_data.get("duration", 5)
        style_context = input_data.get("style_context", {})
        language = input_data.get("language", "en")
        language_instruction = input_data.get("language_instruction", "Generate all content in English.")
        
        # Generate script structure
        script = self._generate_script(genre, theme, characters, duration, style_context, language)
        
        # Log the action
        self.log_action("script_generation", {
            "genre": genre,
            "theme": theme,
            "num_characters": len(characters),
            "duration": duration,
            "language": language
        })
        
        return {
            "script": script,
            "character_arcs": self._develop_character_arcs(characters),
            "key_moments": self._identify_key_moments(script),
            "dialogue": self._generate_dialogue(script, characters),
            "language": language,
            "metadata": {
                "genre": genre,
                "theme": theme,
                "duration": duration,
                "language": language
            }
        }
    
    def _generate_script(self, genre: str, theme: str, characters: List[str], 
                        duration: int, style_context: Dict, language: str = "en") -> Dict[str, Any]:
        """Generate the main script structure."""
        template = self.story_templates.get(genre, self.story_templates["action"])
        
        # Calculate number of scenes based on duration (approx 1 scene per minute)
        num_scenes = max(3, duration)
        
        scenes = []
        for i in range(num_scenes):
            scene = {
                "scene_number": i + 1,
                "location": self._generate_location(genre, i, num_scenes),
                "time_of_day": self._determine_time_of_day(i, num_scenes),
                "description": f"{template} - Scene {i + 1} of {num_scenes}",
                "characters_present": characters[:min(3, len(characters))],
                "action_beats": self._generate_action_beats(genre, i, num_scenes),
                "emotional_tone": self._determine_emotional_tone(i, num_scenes, genre),
                "duration_seconds": (duration * 60) // num_scenes
            }
            scenes.append(scene)
        
        return {
            "title": f"{theme.title() if theme else genre.title()} Story",
            "genre": genre,
            "scenes": scenes,
            "total_duration": duration,
            "style_notes": style_context.get("preferred_style", "cinematic")
        }
    
    def _develop_character_arcs(self, characters: List[str]) -> Dict[str, Any]:
        """Develop character arcs for the story."""
        arcs = {}
        for char in characters:
            arcs[char] = {
                "starting_state": "Establishing character",
                "development": "Character faces challenges and grows",
                "resolution": "Character achieves transformation"
            }
        return arcs
    
    def _identify_key_moments(self, script: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify key plot moments in the script."""
        scenes = script.get("scenes", [])
        key_moments = []
        
        for i, scene in enumerate(scenes):
            if i == 0:
                key_moments.append({
                    "type": "opening",
                    "scene": i + 1,
                    "description": "Story introduction and setup"
                })
            elif i == len(scenes) - 1:
                key_moments.append({
                    "type": "climax_resolution",
                    "scene": i + 1,
                    "description": "Story climax and resolution"
                })
            elif i == len(scenes) // 2:
                key_moments.append({
                    "type": "midpoint_twist",
                    "scene": i + 1,
                    "description": "Major plot development"
                })
        
        return key_moments
    
    def _generate_dialogue(self, script: Dict[str, Any], characters: List[str]) -> Dict[str, List[str]]:
        """Generate dialogue for characters."""
        dialogue = {}
        for char in characters:
            dialogue[char] = [
                f"{char}: Opening dialogue that establishes character",
                f"{char}: Dialogue advancing the plot",
                f"{char}: Emotional or action-driven dialogue",
                f"{char}: Closing dialogue wrapping up arc"
            ]
        return dialogue
    
    def _generate_location(self, genre: str, scene_num: int, total_scenes: int) -> str:
        """Generate location for scene."""
        locations = {
            "action": ["Urban rooftop", "Underground facility", "Highway chase", "Warehouse district"],
            "drama": ["Home interior", "Office space", "Park", "Restaurant"],
            "comedy": ["Living room", "Coffee shop", "Street corner", "Party venue"],
            "adventure": ["Ancient temple", "Dense jungle", "Mountain peak", "Ocean vessel"]
        }
        location_list = locations.get(genre, locations["action"])
        return location_list[min(scene_num, len(location_list) - 1)]
    
    def _determine_time_of_day(self, scene_num: int, total_scenes: int) -> str:
        """Determine time of day for visual variety."""
        times = ["dawn", "morning", "afternoon", "evening", "night", "midnight"]
        progress = scene_num / max(1, total_scenes - 1)
        index = int(progress * (len(times) - 1))
        return times[index]
    
    def _generate_action_beats(self, genre: str, scene_num: int, total_scenes: int) -> List[str]:
        """Generate action beats for the scene."""
        if genre == "action":
            return [
                "Character enters with urgency",
                "Obstacle or conflict appears",
                "Dynamic action sequence",
                "Resolution or escalation"
            ]
        elif genre == "drama":
            return [
                "Character emotional state shown",
                "Dialogue reveals conflict",
                "Emotional turning point",
                "Consequence or decision"
            ]
        else:
            return [
                "Scene establishes situation",
                "Character action or reaction",
                "Development or complication",
                "Scene conclusion"
            ]
    
    def _determine_emotional_tone(self, scene_num: int, total_scenes: int, genre: str) -> str:
        """Determine emotional tone for the scene."""
        progress = scene_num / max(1, total_scenes - 1)
        if progress < 0.3:
            return "establishing"
        elif progress < 0.6:
            return "building_tension"
        elif progress < 0.9:
            return "high_intensity"
        else:
            return "resolution"
