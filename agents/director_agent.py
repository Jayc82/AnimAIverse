"""
Director Agent - Manages scene direction, camera angles, and shot composition.
Translates scripts into visual storytelling.
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent


class DirectorAgent(BaseAgent):
    """Agent responsible for scene direction and cinematography."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("Director", config)
        self.camera_angles = [
            "wide_shot", "medium_shot", "close_up", "extreme_close_up",
            "over_shoulder", "dutch_angle", "aerial", "tracking"
        ]
        self.shot_compositions = {
            "rule_of_thirds": "Subject positioned at intersection points",
            "centered": "Subject centered for emphasis",
            "leading_lines": "Use of lines to guide viewer's eye",
            "frame_within_frame": "Natural framing elements"
        }
        
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create shot list and camera directions from script.
        
        Args:
            input_data: Dictionary containing:
                - script: Script from writer agent
                - style_context: Visual style preferences
                - genre: Story genre for appropriate direction
                
        Returns:
            Dictionary containing:
                - shot_list: Detailed shot-by-shot breakdown
                - camera_movements: Camera choreography
                - lighting_notes: Lighting setup for each scene
                - pacing_guide: Timing and rhythm information
        """
        script = input_data.get("script", {})
        style_context = input_data.get("style_context", {})
        genre = script.get("genre", "action")
        
        shot_list = self._create_shot_list(script, genre, style_context)
        camera_movements = self._plan_camera_movements(shot_list, genre)
        lighting_notes = self._design_lighting(script, genre)
        pacing_guide = self._create_pacing_guide(script)
        
        self.log_action("direction_planning", {
            "num_shots": len(shot_list),
            "genre": genre,
            "num_scenes": len(script.get("scenes", []))
        })
        
        return {
            "shot_list": shot_list,
            "camera_movements": camera_movements,
            "lighting_notes": lighting_notes,
            "pacing_guide": pacing_guide,
            "metadata": {
                "genre": genre,
                "visual_style": style_context.get("visual_style", "cinematic")
            }
        }
    
    def _create_shot_list(self, script: Dict[str, Any], genre: str, 
                         style_context: Dict) -> List[Dict[str, Any]]:
        """Create detailed shot list from script."""
        scenes = script.get("scenes", [])
        shot_list = []
        shot_number = 1
        
        for scene in scenes:
            scene_num = scene.get("scene_number", 1)
            emotional_tone = scene.get("emotional_tone", "neutral")
            
            # Determine number of shots per scene based on emotional tone
            shots_per_scene = self._calculate_shots_per_scene(emotional_tone, genre)
            
            for i in range(shots_per_scene):
                shot = {
                    "shot_number": shot_number,
                    "scene": scene_num,
                    "camera_angle": self._select_camera_angle(i, emotional_tone, genre),
                    "composition": self._select_composition(i, shots_per_scene),
                    "duration_seconds": scene.get("duration_seconds", 30) // shots_per_scene,
                    "focus": self._determine_focus(i, shots_per_scene),
                    "depth_of_field": self._set_depth_of_field(emotional_tone),
                    "description": self._describe_shot(scene, i, emotional_tone)
                }
                shot_list.append(shot)
                shot_number += 1
        
        return shot_list
    
    def _plan_camera_movements(self, shot_list: List[Dict], genre: str) -> List[Dict[str, Any]]:
        """Plan camera movements for dynamic shots."""
        movements = []
        
        for shot in shot_list:
            movement = {
                "shot_number": shot["shot_number"],
                "type": self._select_movement_type(shot["camera_angle"], genre),
                "speed": self._determine_movement_speed(shot["duration_seconds"]),
                "path": self._define_movement_path(shot["camera_angle"]),
                "transition": self._select_transition(shot["shot_number"], len(shot_list))
            }
            movements.append(movement)
        
        return movements
    
    def _design_lighting(self, script: Dict[str, Any], genre: str) -> Dict[str, Any]:
        """Design lighting setup for scenes."""
        scenes = script.get("scenes", [])
        lighting = {}
        
        for scene in scenes:
            scene_num = scene.get("scene_number", 1)
            time_of_day = scene.get("time_of_day", "day")
            emotional_tone = scene.get("emotional_tone", "neutral")
            
            lighting[f"scene_{scene_num}"] = {
                "time_of_day": time_of_day,
                "key_light": self._set_key_light(time_of_day, emotional_tone),
                "fill_light": self._set_fill_light(emotional_tone),
                "back_light": self._set_back_light(genre),
                "color_temperature": self._determine_color_temp(time_of_day),
                "mood": emotional_tone,
                "shadows": self._configure_shadows(emotional_tone, genre)
            }
        
        return lighting
    
    def _create_pacing_guide(self, script: Dict[str, Any]) -> Dict[str, Any]:
        """Create pacing and rhythm guide for the animation."""
        scenes = script.get("scenes", [])
        
        return {
            "overall_rhythm": "dynamic",
            "scene_transitions": [
                {
                    "from_scene": i,
                    "to_scene": i + 1,
                    "transition_type": self._select_scene_transition(
                        scenes[i].get("emotional_tone", "neutral"),
                        scenes[i + 1].get("emotional_tone", "neutral") if i + 1 < len(scenes) else "neutral"
                    ),
                    "duration": 1.0
                }
                for i in range(len(scenes) - 1)
            ],
            "beat_timing": "on_action",
            "rhythm_notes": "Match pacing to emotional intensity"
        }
    
    def _calculate_shots_per_scene(self, emotional_tone: str, genre: str) -> int:
        """Calculate number of shots needed per scene."""
        base_shots = {"action": 6, "drama": 4, "comedy": 5, "adventure": 5}
        tone_multiplier = {"high_intensity": 1.5, "building_tension": 1.2, "establishing": 0.8, "resolution": 1.0}
        
        base = base_shots.get(genre, 5)
        multiplier = tone_multiplier.get(emotional_tone, 1.0)
        
        return max(3, int(base * multiplier))
    
    def _select_camera_angle(self, shot_index: int, emotional_tone: str, genre: str) -> str:
        """Select appropriate camera angle."""
        if emotional_tone == "high_intensity" and genre == "action":
            angles = ["tracking", "dutch_angle", "close_up", "aerial"]
        elif emotional_tone == "establishing":
            angles = ["wide_shot", "medium_shot", "aerial"]
        else:
            angles = ["medium_shot", "close_up", "over_shoulder", "wide_shot"]
        
        return angles[shot_index % len(angles)]
    
    def _select_composition(self, shot_index: int, total_shots: int) -> str:
        """Select shot composition technique."""
        compositions = ["rule_of_thirds", "centered", "leading_lines", "frame_within_frame"]
        return compositions[shot_index % len(compositions)]
    
    def _determine_focus(self, shot_index: int, total_shots: int) -> str:
        """Determine what should be in focus."""
        if shot_index == 0:
            return "establishing_shot"
        elif shot_index == total_shots - 1:
            return "closing_shot"
        else:
            return "character_action"
    
    def _set_depth_of_field(self, emotional_tone: str) -> str:
        """Set depth of field based on emotional context."""
        if emotional_tone == "high_intensity":
            return "shallow"
        elif emotional_tone == "establishing":
            return "deep"
        else:
            return "medium"
    
    def _describe_shot(self, scene: Dict, shot_index: int, emotional_tone: str) -> str:
        """Generate description for the shot."""
        location = scene.get("location", "Location")
        return f"{location} - Shot {shot_index + 1}: {emotional_tone} tone"
    
    def _select_movement_type(self, camera_angle: str, genre: str) -> str:
        """Select camera movement type."""
        if genre == "action" and camera_angle in ["tracking", "aerial"]:
            return "dynamic_follow"
        elif camera_angle == "wide_shot":
            return "slow_pan"
        elif camera_angle in ["close_up", "extreme_close_up"]:
            return "static"
        else:
            return "smooth_dolly"
    
    def _determine_movement_speed(self, duration: float) -> str:
        """Determine camera movement speed."""
        if duration < 3:
            return "fast"
        elif duration < 7:
            return "medium"
        else:
            return "slow"
    
    def _define_movement_path(self, camera_angle: str) -> str:
        """Define the path of camera movement."""
        paths = {
            "tracking": "follows_subject",
            "aerial": "overhead_arc",
            "wide_shot": "horizontal_pan",
            "medium_shot": "slight_push_in"
        }
        return paths.get(camera_angle, "static")
    
    def _select_transition(self, shot_num: int, total_shots: int) -> str:
        """Select transition between shots."""
        if shot_num == 1:
            return "fade_in"
        elif shot_num == total_shots:
            return "fade_out"
        else:
            return "cut"
    
    def _set_key_light(self, time_of_day: str, emotional_tone: str) -> Dict[str, Any]:
        """Configure key light."""
        intensities = {"dawn": 0.6, "morning": 0.8, "afternoon": 1.0, "evening": 0.7, "night": 0.4, "midnight": 0.3}
        return {
            "intensity": intensities.get(time_of_day, 0.8),
            "angle": "45_degrees",
            "color": self._get_light_color(time_of_day)
        }
    
    def _set_fill_light(self, emotional_tone: str) -> Dict[str, Any]:
        """Configure fill light."""
        return {
            "intensity": 0.3 if emotional_tone == "high_intensity" else 0.5,
            "softness": "medium"
        }
    
    def _set_back_light(self, genre: str) -> Dict[str, Any]:
        """Configure back light."""
        return {
            "intensity": 0.6 if genre == "action" else 0.4,
            "color": "neutral"
        }
    
    def _determine_color_temp(self, time_of_day: str) -> str:
        """Determine color temperature for lighting."""
        temps = {
            "dawn": "cool_5500K",
            "morning": "neutral_6500K",
            "afternoon": "warm_5000K",
            "evening": "warm_4500K",
            "night": "cool_4000K",
            "midnight": "very_cool_7000K"
        }
        return temps.get(time_of_day, "neutral_6500K")
    
    def _configure_shadows(self, emotional_tone: str, genre: str) -> Dict[str, Any]:
        """Configure shadow settings."""
        return {
            "hardness": "hard" if emotional_tone == "high_intensity" else "soft",
            "opacity": 0.8 if genre == "action" else 0.6,
            "color": "neutral"
        }
    
    def _get_light_color(self, time_of_day: str) -> str:
        """Get light color based on time of day."""
        colors = {
            "dawn": "soft_pink",
            "morning": "bright_white",
            "afternoon": "warm_yellow",
            "evening": "orange_amber",
            "night": "cool_blue",
            "midnight": "deep_blue"
        }
        return colors.get(time_of_day, "neutral_white")
    
    def _select_scene_transition(self, from_tone: str, to_tone: str) -> str:
        """Select transition type between scenes."""
        if from_tone == "high_intensity" and to_tone == "resolution":
            return "fade"
        elif from_tone == "establishing" and to_tone == "building_tension":
            return "cut"
        else:
            return "dissolve"
