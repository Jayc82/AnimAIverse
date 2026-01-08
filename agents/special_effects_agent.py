"""
Special Effects Agent - Handles visual effects, music, and sound design.
Specializes in VFX, audio effects, music composition, and sound engineering.
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent


class SpecialEffectsAgent(BaseAgent):
    """Agent responsible for special effects, music, and sounds."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("SpecialEffects", config)
        self.vfx_library = self._initialize_vfx_library()
        self.music_library = self._initialize_music_library()
        self.sound_library = self._initialize_sound_library()
        
    def _initialize_vfx_library(self) -> Dict[str, List[str]]:
        """Initialize VFX effects library."""
        return {
            "particles": ["fire", "smoke", "sparks", "dust", "magic", "energy", "water", "snow"],
            "lighting": ["lens_flare", "god_rays", "lightning", "glow", "aurora", "neon"],
            "explosions": ["small", "medium", "large", "massive", "controlled", "chain_reaction"],
            "magical": ["spell_cast", "teleport", "transformation", "barrier", "aura", "portal"],
            "environmental": ["wind", "rain", "storm", "fog", "mist", "heatwave"],
            "energy": ["laser", "plasma", "electricity", "force_field", "shockwave"],
            "destruction": ["impact", "shattering", "disintegration", "collapse"],
            "atmospheric": ["lens_distortion", "color_aberration", "motion_blur", "depth_of_field"]
        }
    
    def _initialize_music_library(self) -> Dict[str, Dict[str, Any]]:
        """Initialize music composition library."""
        return {
            "orchestral": {
                "styles": ["epic", "dramatic", "heroic", "mysterious", "romantic"],
                "instruments": ["strings", "brass", "woodwinds", "percussion", "choir"],
                "tempo_range": [60, 180]
            },
            "electronic": {
                "styles": ["synthwave", "ambient", "techno", "dubstep", "chillwave"],
                "instruments": ["synthesizers", "drum_machines", "samples", "effects"],
                "tempo_range": [80, 160]
            },
            "rock": {
                "styles": ["hard_rock", "indie", "alternative", "punk", "metal"],
                "instruments": ["electric_guitar", "bass", "drums", "keyboards"],
                "tempo_range": [90, 180]
            },
            "cinematic": {
                "styles": ["trailer", "ambient", "tension", "action", "emotional"],
                "instruments": ["hybrid_orchestra", "synths", "percussion", "processed"],
                "tempo_range": [40, 200]
            }
        }
    
    def _initialize_sound_library(self) -> Dict[str, List[str]]:
        """Initialize sound effects library."""
        return {
            "impacts": ["punch", "kick", "crash", "explosion", "slam", "thud"],
            "movements": ["footsteps", "cloth_rustle", "weapon_swish", "door_open", "vehicle"],
            "ambience": ["city", "nature", "indoor", "crowd", "machinery", "weather"],
            "creatures": ["roar", "growl", "chirp", "howl", "screech", "hiss"],
            "technology": ["beep", "whir", "hum", "click", "scan", "power_up", "glitch"],
            "magic": ["whoosh", "shimmer", "sparkle", "rumble", "echo", "pulse"],
            "weapons": ["gunshot", "sword_clash", "arrow_release", "reload", "ricochet"],
            "environment": ["wind", "water", "fire", "earth", "metal", "wood"]
        }
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create special effects, music, and sound design.
        
        Args:
            input_data: Dictionary containing:
                - scenes: Scene information for effects
                - action_sequences: Action scenes requiring VFX
                - mood_profile: Emotional/mood requirements
                - genre: Genre for appropriate effects
                
        Returns:
            Dictionary containing:
                - visual_effects: VFX specifications
                - music_score: Music composition details
                - sound_design: Sound effect specifications
                - audio_mix: Final audio mixing guide
        """
        scenes = input_data.get("scenes", [])
        action_sequences = input_data.get("action_sequences", [])
        mood_profile = input_data.get("mood_profile", {})
        genre = input_data.get("genre", "action")
        
        visual_effects = self._create_visual_effects(scenes, action_sequences, genre)
        music_score = self._compose_music(scenes, mood_profile, genre)
        sound_design = self._design_sound_effects(scenes, action_sequences, genre)
        audio_mix = self._create_audio_mix(music_score, sound_design)
        
        self.log_action("special_effects_creation", {
            "num_scenes": len(scenes),
            "num_vfx": len(visual_effects),
            "genre": genre
        })
        
        return {
            "visual_effects": visual_effects,
            "music_score": music_score,
            "sound_design": sound_design,
            "audio_mix": audio_mix,
            "metadata": {
                "genre": genre,
                "vfx_count": len(visual_effects),
                "music_cues": len(music_score.get("cues", [])),
                "sound_effects_count": sum(len(s.get("effects", [])) for s in sound_design)
            }
        }
    
    def _create_visual_effects(self, scenes: List[Dict], action_sequences: List[Dict], 
                               genre: str) -> List[Dict[str, Any]]:
        """Create comprehensive visual effects."""
        vfx_shots = []
        
        for i, scene in enumerate(scenes):
            scene_num = scene.get("scene_number", i + 1)
            emotional_tone = scene.get("emotional_tone", "neutral")
            
            # Determine VFX needs based on scene
            vfx_requirements = self._analyze_vfx_needs(scene, genre)
            
            for vfx_type in vfx_requirements:
                vfx_shot = {
                    "scene": scene_num,
                    "effect_type": vfx_type,
                    "complexity": self._determine_vfx_complexity(vfx_type, emotional_tone),
                    "layers": self._create_vfx_layers(vfx_type),
                    "timing": self._calculate_vfx_timing(vfx_type, scene),
                    "integration": "seamless_blend_with_footage",
                    "rendering": {
                        "quality": "exceptional",
                        "samples": 512 if vfx_type in ["particles", "explosions"] else 256,
                        "motion_blur": True,
                        "depth_of_field": True
                    },
                    "color_grading": self._match_scene_color(scene),
                    "compositing_notes": self._add_compositing_notes(vfx_type)
                }
                vfx_shots.append(vfx_shot)
        
        return vfx_shots
    
    def _compose_music(self, scenes: List[Dict], mood_profile: Dict, genre: str) -> Dict[str, Any]:
        """Compose original music score."""
        return {
            "main_theme": self._create_main_theme(genre, mood_profile),
            "character_themes": self._create_character_themes(genre),
            "scene_cues": self._create_scene_cues(scenes, mood_profile),
            "emotional_beats": self._compose_emotional_moments(scenes),
            "action_music": self._compose_action_sequences(genre),
            "ambient_tracks": self._create_ambient_music(scenes),
            "instrumentation": self._define_instrumentation(genre),
            "mixing_notes": {
                "overall_level": "-14_LUFS",
                "dynamic_range": "wide",
                "mastering": "theatrical_standard"
            }
        }
    
    def _design_sound_effects(self, scenes: List[Dict], action_sequences: List[Dict], 
                             genre: str) -> List[Dict[str, Any]]:
        """Design comprehensive sound effects."""
        sound_design = []
        
        for scene in scenes:
            scene_num = scene.get("scene_number", 1)
            location = scene.get("location", "")
            
            design = {
                "scene": scene_num,
                "ambience": self._design_ambience(location, scene),
                "effects": self._select_sound_effects(scene, genre),
                "foley": self._create_foley_list(scene),
                "dialogue_treatment": self._process_dialogue(scene),
                "spatial_audio": self._design_spatial_audio(scene),
                "layering": {
                    "background": "ambient_layer",
                    "midground": "action_effects",
                    "foreground": "dialogue_and_key_sounds"
                }
            }
            sound_design.append(design)
        
        return sound_design
    
    def _create_audio_mix(self, music: Dict, sound_design: List[Dict]) -> Dict[str, Any]:
        """Create final audio mixing specifications."""
        return {
            "mix_type": "5.1_surround",
            "channels": {
                "dialogue": {"level": "0dB", "priority": "highest"},
                "music": {"level": "-6dB", "priority": "high"},
                "effects": {"level": "-3dB", "priority": "medium"},
                "ambience": {"level": "-12dB", "priority": "low"}
            },
            "dynamics": {
                "compression": "gentle_multi_band",
                "limiting": "transparent_brick_wall",
                "expansion": "on_ambience_only"
            },
            "effects_processing": [
                "reverb_for_space",
                "eq_for_clarity",
                "stereo_enhancement",
                "surround_panning"
            ],
            "master_output": {
                "format": "24bit_48kHz",
                "loudness": "-16_LUFS_with_-1dB_true_peak",
                "delivery": "multiple_stems_plus_master"
            }
        }
    
    def _analyze_vfx_needs(self, scene: Dict, genre: str) -> List[str]:
        """Analyze VFX needs for scene."""
        vfx_needs = []
        
        emotional_tone = scene.get("emotional_tone", "neutral")
        
        if genre == "action":
            vfx_needs.extend(["explosions", "particles", "energy", "destruction"])
        
        if emotional_tone == "high_intensity":
            vfx_needs.extend(["motion_blur", "lens_distortion", "impact"])
        
        # Add atmospheric effects
        vfx_needs.extend(["lighting", "atmospheric"])
        
        return vfx_needs
    
    def _determine_vfx_complexity(self, vfx_type: str, emotional_tone: str) -> str:
        """Determine VFX complexity level."""
        complex_types = ["explosions", "magical", "destruction"]
        
        if vfx_type in complex_types or emotional_tone == "high_intensity":
            return "high"
        return "medium"
    
    def _create_vfx_layers(self, vfx_type: str) -> List[Dict[str, str]]:
        """Create VFX composition layers."""
        return [
            {"layer": "base_effect", "blend_mode": "add"},
            {"layer": "secondary_details", "blend_mode": "screen"},
            {"layer": "lighting_interaction", "blend_mode": "multiply"},
            {"layer": "final_touches", "blend_mode": "normal"}
        ]
    
    def _calculate_vfx_timing(self, vfx_type: str, scene: Dict) -> Dict[str, Any]:
        """Calculate VFX timing."""
        return {
            "start_frame": 0,
            "duration_frames": scene.get("duration_seconds", 5) * 30,
            "peak_frame": "calculated_impact_moment",
            "fade_in": 5,
            "fade_out": 10
        }
    
    def _match_scene_color(self, scene: Dict) -> Dict[str, Any]:
        """Match VFX to scene color."""
        return {
            "color_match": "scene_palette",
            "contrast": "enhanced",
            "saturation": "slightly_boosted"
        }
    
    def _add_compositing_notes(self, vfx_type: str) -> List[str]:
        """Add compositing notes for VFX."""
        return [
            "blend_naturally_with_footage",
            "match_lighting_direction",
            "apply_camera_motion",
            "add_subtle_imperfections"
        ]
    
    def _create_main_theme(self, genre: str, mood: Dict) -> Dict[str, Any]:
        """Create main musical theme."""
        music_style = self.music_library.get("orchestral" if genre == "action" else "cinematic", {})
        
        return {
            "title": "Main_Theme",
            "style": music_style.get("styles", ["epic"])[0],
            "tempo": 120,
            "key": "C_minor",
            "time_signature": "4/4",
            "duration": "2_minutes_30_seconds",
            "instrumentation": music_style.get("instruments", []),
            "motifs": ["heroic_melody", "emotional_undertone", "rhythmic_drive"]
        }
    
    def _create_character_themes(self, genre: str) -> List[Dict[str, str]]:
        """Create themes for main characters."""
        return [
            {"character": "protagonist", "theme": "heroic_inspiring"},
            {"character": "antagonist", "theme": "menacing_complex"},
            {"character": "mentor", "theme": "wise_supportive"}
        ]
    
    def _create_scene_cues(self, scenes: List[Dict], mood: Dict) -> List[Dict[str, Any]]:
        """Create music cues for scenes."""
        cues = []
        
        for scene in scenes:
            cue = {
                "scene": scene.get("scene_number", 1),
                "cue_type": "underscore",
                "mood": scene.get("emotional_tone", "neutral"),
                "intensity": self._calculate_music_intensity(scene),
                "duration": scene.get("duration_seconds", 30),
                "fade_in": 2.0,
                "fade_out": 3.0
            }
            cues.append(cue)
        
        return cues
    
    def _compose_emotional_moments(self, scenes: List[Dict]) -> List[Dict[str, Any]]:
        """Compose music for emotional moments."""
        return [
            {"moment": "climax", "style": "intense_emotional", "instruments": ["full_orchestra"]},
            {"moment": "resolution", "style": "peaceful_uplifting", "instruments": ["strings", "piano"]}
        ]
    
    def _compose_action_sequences(self, genre: str) -> Dict[str, Any]:
        """Compose music for action sequences."""
        return {
            "style": "high_energy_driving",
            "tempo": 140,
            "instrumentation": ["percussion", "brass", "electronic_elements"],
            "dynamics": "very_dynamic_with_builds"
        }
    
    def _create_ambient_music(self, scenes: List[Dict]) -> List[Dict[str, str]]:
        """Create ambient background music."""
        return [
            {"type": "exploration", "mood": "mysterious"},
            {"type": "tension", "mood": "suspenseful"},
            {"type": "calm", "mood": "peaceful"}
        ]
    
    def _define_instrumentation(self, genre: str) -> Dict[str, List[str]]:
        """Define overall instrumentation."""
        return {
            "primary": ["orchestra", "choir", "percussion"],
            "secondary": ["synthesizers", "ethnic_instruments"],
            "special": ["sound_design_elements", "processed_effects"]
        }
    
    def _design_ambience(self, location: str, scene: Dict) -> Dict[str, Any]:
        """Design ambient soundscape."""
        return {
            "location_type": location,
            "layers": [
                "distant_background",
                "mid_range_activity",
                "near_field_details"
            ],
            "density": "rich_and_immersive",
            "variation": "evolving_over_time"
        }
    
    def _select_sound_effects(self, scene: Dict, genre: str) -> List[Dict[str, Any]]:
        """Select appropriate sound effects."""
        effects = []
        
        # Add action sounds for action genre
        if genre == "action":
            effects.extend([
                {"type": "impacts", "count": 10, "variety": "high"},
                {"type": "movements", "count": 20, "variety": "medium"},
                {"type": "weapons", "count": 5, "variety": "high"}
            ])
        
        # Add ambient sounds
        effects.append({"type": "ambience", "continuous": True})
        
        return effects
    
    def _create_foley_list(self, scene: Dict) -> List[Dict[str, str]]:
        """Create foley sound list."""
        return [
            {"action": "footsteps", "surface": "appropriate_material"},
            {"action": "cloth_movement", "intensity": "subtle"},
            {"action": "object_handling", "detail": "precise"}
        ]
    
    def _process_dialogue(self, scene: Dict) -> Dict[str, Any]:
        """Process dialogue audio."""
        return {
            "eq": "voice_clarity_enhancement",
            "compression": "gentle_dynamics",
            "de_essing": "sibilance_control",
            "reverb": "room_appropriate",
            "noise_reduction": "subtle_cleaning"
        }
    
    def _design_spatial_audio(self, scene: Dict) -> Dict[str, str]:
        """Design spatial audio positioning."""
        return {
            "format": "5.1_surround",
            "panning": "scene_appropriate",
            "depth": "front_to_back_positioning",
            "movement": "dynamic_following_action"
        }
    
    def _calculate_music_intensity(self, scene: Dict) -> float:
        """Calculate music intensity for scene."""
        emotional_tone = scene.get("emotional_tone", "neutral")
        
        intensity_map = {
            "high_intensity": 1.0,
            "building_tension": 0.7,
            "establishing": 0.3,
            "resolution": 0.5
        }
        
        return intensity_map.get(emotional_tone, 0.5)
