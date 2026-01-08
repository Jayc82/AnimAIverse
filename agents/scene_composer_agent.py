"""
Scene Composer Agent - Assembles scenes, manages visual elements, and composites.
Brings together all elements into cohesive scenes.
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent


class SceneComposerAgent(BaseAgent):
    """Agent responsible for scene composition and visual assembly."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("SceneComposer", config)
        
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compose scenes from all previous agent outputs.
        
        Args:
            input_data: Dictionary containing:
                - script: Script from writer
                - shot_list: Shots from director
                - character_animations: Animations from animator
                - style_context: Visual style preferences
                
        Returns:
            Dictionary containing:
                - composed_scenes: Fully assembled scenes
                - visual_effects: VFX specifications
                - backgrounds: Background and environment data
                - layering: Composition layer information
        """
        script = input_data.get("script", {})
        shot_list = input_data.get("shot_list", [])
        character_animations = input_data.get("character_animations", [])
        style_context = input_data.get("style_context", {})
        
        composed_scenes = self._compose_scenes(script, shot_list, character_animations)
        visual_effects = self._design_visual_effects(shot_list, script)
        backgrounds = self._create_backgrounds(script)
        layering = self._organize_layers(composed_scenes)
        
        self.log_action("scene_composition", {
            "num_scenes": len(composed_scenes),
            "num_shots": len(shot_list),
            "has_vfx": len(visual_effects) > 0
        })
        
        return {
            "composed_scenes": composed_scenes,
            "visual_effects": visual_effects,
            "backgrounds": backgrounds,
            "layering": layering,
            "metadata": {
                "composition_style": style_context.get("composition_style", "cinematic"),
                "color_grading": self._determine_color_grading(script)
            }
        }
    
    def _compose_scenes(self, script: Dict, shot_list: List[Dict], 
                       character_animations: List[Dict]) -> List[Dict[str, Any]]:
        """Compose complete scenes from all elements."""
        scenes = script.get("scenes", [])
        composed = []
        
        for scene in scenes:
            scene_num = scene.get("scene_number", 1)
            
            # Get shots for this scene
            scene_shots = [s for s in shot_list if s.get("scene") == scene_num]
            
            # Get animations for this scene
            scene_animations = [a for a in character_animations 
                              if a.get("shot_number") in [s["shot_number"] for s in scene_shots]]
            
            composed_scene = {
                "scene_number": scene_num,
                "title": scene.get("location", f"Scene {scene_num}"),
                "duration": scene.get("duration_seconds", 30),
                "shots": self._assemble_shots(scene_shots, scene_animations),
                "environment": self._define_environment(scene),
                "atmosphere": self._create_atmosphere(scene),
                "color_palette": self._select_color_palette(scene),
                "props": self._place_props(scene),
                "characters": scene.get("characters_present", [])
            }
            composed.append(composed_scene)
        
        return composed
    
    def _design_visual_effects(self, shot_list: List[Dict], script: Dict) -> List[Dict[str, Any]]:
        """Design visual effects for shots."""
        vfx = []
        scenes = script.get("scenes", [])
        
        for shot in shot_list:
            scene_idx = shot.get("scene", 1) - 1
            if scene_idx < len(scenes):
                scene = scenes[scene_idx]
                emotional_tone = scene.get("emotional_tone", "neutral")
                
                if emotional_tone == "high_intensity":
                    vfx.append({
                        "shot_number": shot["shot_number"],
                        "effects": [
                            {
                                "type": "motion_blur",
                                "intensity": 0.8,
                                "enabled": True
                            },
                            {
                                "type": "speed_lines",
                                "intensity": 0.6,
                                "enabled": True
                            },
                            {
                                "type": "impact_flash",
                                "color": "white",
                                "duration": 2
                            }
                        ],
                        "particles": self._generate_particle_effects(emotional_tone),
                        "post_processing": self._apply_post_processing(emotional_tone)
                    })
        
        return vfx
    
    def _create_backgrounds(self, script: Dict) -> List[Dict[str, Any]]:
        """Create background specifications for scenes."""
        scenes = script.get("scenes", [])
        backgrounds = []
        
        for scene in scenes:
            bg = {
                "scene_number": scene.get("scene_number", 1),
                "location": scene.get("location", "Generic location"),
                "time_of_day": scene.get("time_of_day", "day"),
                "sky": self._generate_sky(scene.get("time_of_day", "day")),
                "lighting": self._generate_ambient_lighting(scene),
                "depth_layers": self._create_depth_layers(scene.get("location", "")),
                "details": self._add_environmental_details(scene.get("location", "")),
                "weather": self._determine_weather(scene)
            }
            backgrounds.append(bg)
        
        return backgrounds
    
    def _organize_layers(self, composed_scenes: List[Dict]) -> Dict[str, Any]:
        """Organize composition layers."""
        return {
            "layer_structure": [
                {"name": "background", "z_index": 0, "opacity": 1.0},
                {"name": "environment_far", "z_index": 10, "opacity": 1.0},
                {"name": "environment_mid", "z_index": 20, "opacity": 1.0},
                {"name": "characters", "z_index": 30, "opacity": 1.0},
                {"name": "props_foreground", "z_index": 40, "opacity": 1.0},
                {"name": "effects", "z_index": 50, "opacity": 0.9},
                {"name": "overlay", "z_index": 60, "opacity": 0.8}
            ],
            "blending_modes": {
                "background": "normal",
                "effects": "screen",
                "overlay": "multiply"
            },
            "depth_of_field": {
                "enabled": True,
                "focus_distance": 10.0,
                "aperture": 2.8
            }
        }
    
    def _determine_color_grading(self, script: Dict) -> Dict[str, Any]:
        """Determine color grading for the animation."""
        genre = script.get("genre", "action")
        
        color_grades = {
            "action": {
                "contrast": 1.3,
                "saturation": 1.2,
                "temperature": "cool",
                "tint": "blue_orange",
                "shadows": "crushed",
                "highlights": "boosted"
            },
            "drama": {
                "contrast": 1.1,
                "saturation": 0.9,
                "temperature": "warm",
                "tint": "neutral",
                "shadows": "lifted",
                "highlights": "natural"
            },
            "comedy": {
                "contrast": 1.0,
                "saturation": 1.3,
                "temperature": "bright",
                "tint": "vibrant",
                "shadows": "light",
                "highlights": "airy"
            },
            "adventure": {
                "contrast": 1.2,
                "saturation": 1.1,
                "temperature": "natural",
                "tint": "earth_tones",
                "shadows": "moderate",
                "highlights": "dynamic"
            }
        }
        
        return color_grades.get(genre, color_grades["action"])
    
    def _assemble_shots(self, scene_shots: List[Dict], 
                       scene_animations: List[Dict]) -> List[Dict[str, Any]]:
        """Assemble individual shots with all elements."""
        assembled = []
        
        for shot in scene_shots:
            shot_anims = [a for a in scene_animations 
                         if a.get("shot_number") == shot.get("shot_number")]
            
            assembled_shot = {
                "shot_number": shot.get("shot_number"),
                "camera": {
                    "angle": shot.get("camera_angle"),
                    "composition": shot.get("composition"),
                    "focus": shot.get("focus")
                },
                "characters": [a.get("character") for a in shot_anims],
                "duration": shot.get("duration_seconds", 5),
                "elements": self._gather_shot_elements(shot)
            }
            assembled.append(assembled_shot)
        
        return assembled
    
    def _define_environment(self, scene: Dict) -> Dict[str, Any]:
        """Define environment specifications."""
        location = scene.get("location", "Generic location")
        
        return {
            "type": self._categorize_location(location),
            "scale": "medium",
            "architecture": self._determine_architecture(location),
            "vegetation": self._add_vegetation(location),
            "ambient_sound": self._suggest_ambient_sound(location)
        }
    
    def _create_atmosphere(self, scene: Dict) -> Dict[str, Any]:
        """Create atmospheric effects."""
        emotional_tone = scene.get("emotional_tone", "neutral")
        time_of_day = scene.get("time_of_day", "day")
        
        return {
            "mood": emotional_tone,
            "fog": self._calculate_fog(time_of_day, emotional_tone),
            "haze": self._calculate_haze(time_of_day),
            "god_rays": self._enable_god_rays(time_of_day),
            "ambient_occlusion": 0.6,
            "global_illumination": True
        }
    
    def _select_color_palette(self, scene: Dict) -> Dict[str, List[str]]:
        """Select color palette for scene."""
        time_of_day = scene.get("time_of_day", "day")
        emotional_tone = scene.get("emotional_tone", "neutral")
        
        palettes = {
            "dawn": ["#FFB6C1", "#FFD700", "#87CEEB", "#FFA07A"],
            "morning": ["#FFD700", "#87CEEB", "#90EE90", "#F0E68C"],
            "afternoon": ["#FFD700", "#FF8C00", "#87CEEB", "#F5DEB3"],
            "evening": ["#FF6347", "#FF8C00", "#4B0082", "#8B4513"],
            "night": ["#191970", "#483D8B", "#2F4F4F", "#000080"],
            "midnight": ["#000033", "#1C1C3C", "#2C2C54", "#0F0F3C"]
        }
        
        base_palette = palettes.get(time_of_day, palettes["afternoon"])
        
        return {
            "primary": base_palette,
            "accent": self._select_accent_colors(emotional_tone),
            "temperature": self._determine_temperature_palette(time_of_day)
        }
    
    def _place_props(self, scene: Dict) -> List[Dict[str, Any]]:
        """Place props in the scene."""
        location = scene.get("location", "")
        
        props = []
        if "urban" in location.lower() or "city" in location.lower():
            props = [
                {"type": "vehicle", "position": "background", "quantity": 3},
                {"type": "street_furniture", "position": "mid_ground", "quantity": 5},
                {"type": "signage", "position": "various", "quantity": 4}
            ]
        elif "interior" in location.lower() or "room" in location.lower():
            props = [
                {"type": "furniture", "position": "various", "quantity": 6},
                {"type": "decorations", "position": "walls", "quantity": 4},
                {"type": "lighting_fixtures", "position": "ceiling", "quantity": 2}
            ]
        else:
            props = [
                {"type": "natural_elements", "position": "scattered", "quantity": 8},
                {"type": "atmospheric_objects", "position": "various", "quantity": 4}
            ]
        
        return props
    
    def _generate_particle_effects(self, emotional_tone: str) -> List[Dict[str, Any]]:
        """Generate particle effect specifications."""
        if emotional_tone == "high_intensity":
            return [
                {
                    "type": "dust_debris",
                    "density": 0.7,
                    "size_range": [0.1, 0.5],
                    "velocity": "high"
                },
                {
                    "type": "sparks",
                    "density": 0.5,
                    "size_range": [0.05, 0.15],
                    "velocity": "very_high"
                }
            ]
        return []
    
    def _apply_post_processing(self, emotional_tone: str) -> Dict[str, Any]:
        """Apply post-processing effects."""
        return {
            "bloom": 0.3 if emotional_tone == "high_intensity" else 0.1,
            "chromatic_aberration": 0.2 if emotional_tone == "high_intensity" else 0.0,
            "vignette": 0.4,
            "film_grain": 0.15,
            "sharpening": 0.5
        }
    
    def _generate_sky(self, time_of_day: str) -> Dict[str, Any]:
        """Generate sky specifications."""
        skies = {
            "dawn": {"color": "#FFB6C1", "clouds": 0.4, "stars": 0.2},
            "morning": {"color": "#87CEEB", "clouds": 0.3, "stars": 0.0},
            "afternoon": {"color": "#87CEEB", "clouds": 0.5, "stars": 0.0},
            "evening": {"color": "#FF6347", "clouds": 0.6, "stars": 0.1},
            "night": {"color": "#191970", "clouds": 0.3, "stars": 0.8},
            "midnight": {"color": "#000033", "clouds": 0.2, "stars": 1.0}
        }
        
        return skies.get(time_of_day, skies["afternoon"])
    
    def _generate_ambient_lighting(self, scene: Dict) -> Dict[str, Any]:
        """Generate ambient lighting."""
        time_of_day = scene.get("time_of_day", "day")
        
        intensities = {
            "dawn": 0.4, "morning": 0.7, "afternoon": 0.9,
            "evening": 0.5, "night": 0.2, "midnight": 0.1
        }
        
        return {
            "intensity": intensities.get(time_of_day, 0.7),
            "color": self._get_ambient_color(time_of_day),
            "direction": "top_down",
            "bounce": 2
        }
    
    def _create_depth_layers(self, location: str) -> List[Dict[str, Any]]:
        """Create depth layers for parallax."""
        return [
            {"name": "far_background", "depth": 100, "parallax_factor": 0.1},
            {"name": "mid_background", "depth": 50, "parallax_factor": 0.3},
            {"name": "near_background", "depth": 25, "parallax_factor": 0.5},
            {"name": "action_plane", "depth": 0, "parallax_factor": 1.0},
            {"name": "foreground", "depth": -10, "parallax_factor": 1.5}
        ]
    
    def _add_environmental_details(self, location: str) -> List[str]:
        """Add environmental details."""
        if "urban" in location.lower():
            return ["buildings", "streets", "vehicles", "street_lights", "signage"]
        elif "nature" in location.lower() or "outdoor" in location.lower():
            return ["trees", "foliage", "terrain", "sky", "natural_features"]
        else:
            return ["walls", "floor", "ceiling", "furniture", "decorations"]
    
    def _determine_weather(self, scene: Dict) -> Dict[str, Any]:
        """Determine weather conditions."""
        return {
            "condition": "clear",
            "precipitation": 0.0,
            "wind": 0.3,
            "temperature_feel": "moderate"
        }
    
    def _gather_shot_elements(self, shot: Dict) -> List[str]:
        """Gather all elements needed for a shot."""
        return [
            "background",
            "characters",
            "props",
            "lighting",
            "effects",
            "camera"
        ]
    
    def _categorize_location(self, location: str) -> str:
        """Categorize the location type."""
        location_lower = location.lower()
        if any(word in location_lower for word in ["room", "interior", "office", "home"]):
            return "interior"
        elif any(word in location_lower for word in ["urban", "city", "street", "building"]):
            return "urban_exterior"
        else:
            return "natural_exterior"
    
    def _determine_architecture(self, location: str) -> str:
        """Determine architectural style."""
        if "modern" in location.lower() or "urban" in location.lower():
            return "contemporary"
        elif "ancient" in location.lower() or "temple" in location.lower():
            return "historical"
        else:
            return "generic"
    
    def _add_vegetation(self, location: str) -> Dict[str, Any]:
        """Add vegetation to the scene."""
        location_lower = location.lower()
        if any(word in location_lower for word in ["jungle", "forest", "nature"]):
            return {"density": 0.8, "types": ["trees", "bushes", "vines"]}
        elif any(word in location_lower for word in ["park", "garden"]):
            return {"density": 0.5, "types": ["trees", "grass", "flowers"]}
        else:
            return {"density": 0.1, "types": ["minimal_greenery"]}
    
    def _suggest_ambient_sound(self, location: str) -> List[str]:
        """Suggest ambient sounds for the location."""
        location_lower = location.lower()
        if "urban" in location_lower or "city" in location_lower:
            return ["traffic", "distant_voices", "urban_ambience"]
        elif "nature" in location_lower or "outdoor" in location_lower:
            return ["birds", "wind", "natural_ambience"]
        else:
            return ["room_tone", "subtle_ambience"]
    
    def _calculate_fog(self, time_of_day: str, emotional_tone: str) -> Dict[str, Any]:
        """Calculate fog parameters."""
        fog_density = 0.0
        if time_of_day in ["dawn", "night", "midnight"]:
            fog_density = 0.3
        if emotional_tone in ["building_tension", "high_intensity"]:
            fog_density += 0.2
        
        return {
            "density": min(fog_density, 0.7),
            "color": "#808080",
            "falloff": "exponential"
        }
    
    def _calculate_haze(self, time_of_day: str) -> float:
        """Calculate atmospheric haze."""
        haze_values = {
            "dawn": 0.3, "morning": 0.2, "afternoon": 0.4,
            "evening": 0.3, "night": 0.1, "midnight": 0.1
        }
        return haze_values.get(time_of_day, 0.2)
    
    def _enable_god_rays(self, time_of_day: str) -> bool:
        """Determine if god rays should be enabled."""
        return time_of_day in ["dawn", "morning", "evening"]
    
    def _select_accent_colors(self, emotional_tone: str) -> List[str]:
        """Select accent colors based on emotional tone."""
        accent_map = {
            "high_intensity": ["#FF0000", "#FF6600", "#FFFF00"],
            "building_tension": ["#FF6600", "#CC6600", "#996600"],
            "establishing": ["#6699CC", "#99CC99", "#CC9966"],
            "resolution": ["#99CCFF", "#99FF99", "#FFCC99"]
        }
        return accent_map.get(emotional_tone, accent_map["establishing"])
    
    def _determine_temperature_palette(self, time_of_day: str) -> str:
        """Determine color temperature."""
        temp_map = {
            "dawn": "cool_warm_mix",
            "morning": "warm",
            "afternoon": "neutral_warm",
            "evening": "warm_orange",
            "night": "cool",
            "midnight": "very_cool"
        }
        return temp_map.get(time_of_day, "neutral")
    
    def _get_ambient_color(self, time_of_day: str) -> str:
        """Get ambient light color."""
        colors = {
            "dawn": "#FFE4E1",
            "morning": "#FFFACD",
            "afternoon": "#FFFFFF",
            "evening": "#FFD700",
            "night": "#4169E1",
            "midnight": "#191970"
        }
        return colors.get(time_of_day, "#FFFFFF")
