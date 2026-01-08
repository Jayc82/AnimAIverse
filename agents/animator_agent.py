"""
Animator Agent - Handles character animation, motion, and action sequences.
Creates dynamic movement and brings characters to life.
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent


class AnimatorAgent(BaseAgent):
    """Agent responsible for character animation and motion."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("Animator", config)
        self.animation_styles = {
            "realistic": "Natural, lifelike movement",
            "stylized": "Exaggerated, expressive movement",
            "fluid": "Smooth, flowing motion",
            "dynamic": "Fast-paced, energetic action"
        }
        
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create animation data from director's shot list.
        
        Args:
            input_data: Dictionary containing:
                - shot_list: Shot details from director
                - script: Original script for character actions
                - style_context: Animation style preferences
                
        Returns:
            Dictionary containing:
                - character_animations: Character movement data
                - action_sequences: Detailed action choreography
                - timing_charts: Animation timing information
                - motion_paths: Movement trajectories
        """
        shot_list = input_data.get("shot_list", [])
        script = input_data.get("script", {})
        style_context = input_data.get("style_context", {})
        
        character_animations = self._create_character_animations(shot_list, script)
        action_sequences = self._choreograph_actions(shot_list, script)
        timing_charts = self._generate_timing_charts(shot_list)
        motion_paths = self._define_motion_paths(shot_list, script)
        
        self.log_action("animation_creation", {
            "num_shots": len(shot_list),
            "num_characters": len(script.get("scenes", [{}])[0].get("characters_present", [])),
            "style": style_context.get("animation_style", "dynamic")
        })
        
        return {
            "character_animations": character_animations,
            "action_sequences": action_sequences,
            "timing_charts": timing_charts,
            "motion_paths": motion_paths,
            "metadata": {
                "animation_style": style_context.get("animation_style", "dynamic"),
                "fps": 30
            }
        }
    
    def _create_character_animations(self, shot_list: List[Dict], script: Dict) -> List[Dict[str, Any]]:
        """Create detailed character animations for each shot."""
        animations = []
        scenes = script.get("scenes", [])
        
        for shot in shot_list:
            scene_idx = shot.get("scene", 1) - 1
            if scene_idx < len(scenes):
                scene = scenes[scene_idx]
                characters = scene.get("characters_present", [])
                
                for character in characters:
                    animation = {
                        "shot_number": shot["shot_number"],
                        "character": character,
                        "pose_sequence": self._generate_pose_sequence(shot, scene),
                        "facial_expressions": self._generate_expressions(scene.get("emotional_tone", "neutral")),
                        "body_language": self._define_body_language(scene.get("emotional_tone", "neutral")),
                        "movements": self._define_movements(shot, scene),
                        "timing": {
                            "start_frame": 0,
                            "end_frame": shot.get("duration_seconds", 5) * 30,  # 30 fps
                            "keyframes": self._calculate_keyframes(shot.get("duration_seconds", 5))
                        }
                    }
                    animations.append(animation)
        
        return animations
    
    def _choreograph_actions(self, shot_list: List[Dict], script: Dict) -> List[Dict[str, Any]]:
        """Choreograph complex action sequences."""
        actions = []
        scenes = script.get("scenes", [])
        
        for shot in shot_list:
            scene_idx = shot.get("scene", 1) - 1
            if scene_idx < len(scenes):
                scene = scenes[scene_idx]
                action_beats = scene.get("action_beats", [])
                
                for i, beat in enumerate(action_beats):
                    action = {
                        "shot_number": shot["shot_number"],
                        "action_beat": beat,
                        "choreography": self._design_choreography(beat, scene),
                        "motion_blur": self._calculate_motion_blur(beat),
                        "impact_frames": self._define_impact_frames(beat),
                        "anticipation": self._add_anticipation(i, len(action_beats)),
                        "follow_through": self._add_follow_through(i, len(action_beats))
                    }
                    actions.append(action)
        
        return actions
    
    def _generate_timing_charts(self, shot_list: List[Dict]) -> List[Dict[str, Any]]:
        """Generate timing charts for animation."""
        timing_charts = []
        
        for shot in shot_list:
            duration_seconds = shot.get("duration_seconds", 5)
            total_frames = duration_seconds * 30
            
            chart = {
                "shot_number": shot["shot_number"],
                "total_frames": total_frames,
                "fps": 30,
                "ease_in": self._calculate_ease_in(total_frames),
                "ease_out": self._calculate_ease_out(total_frames),
                "holds": self._calculate_holds(shot["camera_angle"]),
                "spacing": self._calculate_frame_spacing(shot["camera_angle"])
            }
            timing_charts.append(chart)
        
        return timing_charts
    
    def _define_motion_paths(self, shot_list: List[Dict], script: Dict) -> List[Dict[str, Any]]:
        """Define motion paths for characters and objects."""
        motion_paths = []
        scenes = script.get("scenes", [])
        
        for shot in shot_list:
            scene_idx = shot.get("scene", 1) - 1
            if scene_idx < len(scenes):
                scene = scenes[scene_idx]
                characters = scene.get("characters_present", [])
                
                for character in characters:
                    path = {
                        "shot_number": shot["shot_number"],
                        "character": character,
                        "path_type": self._determine_path_type(shot["camera_angle"]),
                        "waypoints": self._generate_waypoints(shot),
                        "speed_curve": self._generate_speed_curve(shot.get("duration_seconds", 5)),
                        "arc_motion": self._apply_arc_motion(shot["camera_angle"])
                    }
                    motion_paths.append(path)
        
        return motion_paths
    
    def _generate_pose_sequence(self, shot: Dict, scene: Dict) -> List[Dict[str, Any]]:
        """Generate sequence of poses for animation."""
        emotional_tone = scene.get("emotional_tone", "neutral")
        duration = shot.get("duration_seconds", 5)
        
        poses = []
        num_poses = max(3, int(duration / 2))  # Pose every 2 seconds
        
        for i in range(num_poses):
            pose = {
                "pose_number": i + 1,
                "stance": self._determine_stance(emotional_tone, i, num_poses),
                "weight_distribution": self._calculate_weight(emotional_tone),
                "tension_level": self._calculate_tension(emotional_tone)
            }
            poses.append(pose)
        
        return poses
    
    def _generate_expressions(self, emotional_tone: str) -> List[Dict[str, Any]]:
        """Generate facial expressions."""
        expression_map = {
            "high_intensity": ["determined", "focused", "intense"],
            "building_tension": ["concerned", "alert", "anticipating"],
            "establishing": ["neutral", "observing", "calm"],
            "resolution": ["relieved", "satisfied", "peaceful"]
        }
        
        expressions = expression_map.get(emotional_tone, ["neutral"])
        
        return [
            {
                "expression": expr,
                "intensity": 0.8 if emotional_tone == "high_intensity" else 0.6,
                "transition_speed": "fast" if emotional_tone == "high_intensity" else "medium"
            }
            for expr in expressions
        ]
    
    def _define_body_language(self, emotional_tone: str) -> Dict[str, Any]:
        """Define body language based on emotional context."""
        body_language_map = {
            "high_intensity": {
                "posture": "aggressive_forward",
                "gestures": "sharp_decisive",
                "energy": "high"
            },
            "building_tension": {
                "posture": "alert_ready",
                "gestures": "controlled_precise",
                "energy": "medium_high"
            },
            "establishing": {
                "posture": "neutral_balanced",
                "gestures": "natural_flowing",
                "energy": "medium"
            },
            "resolution": {
                "posture": "relaxed_open",
                "gestures": "gentle_calm",
                "energy": "low_medium"
            }
        }
        
        return body_language_map.get(emotional_tone, body_language_map["establishing"])
    
    def _define_movements(self, shot: Dict, scene: Dict) -> List[str]:
        """Define specific movements for the shot."""
        emotional_tone = scene.get("emotional_tone", "neutral")
        
        if emotional_tone == "high_intensity":
            return ["quick_turn", "forward_lunge", "defensive_stance", "power_move"]
        elif emotional_tone == "building_tension":
            return ["cautious_step", "scan_environment", "ready_position", "subtle_shift"]
        else:
            return ["walk_forward", "gesture", "turn", "settle"]
    
    def _calculate_keyframes(self, duration: float) -> List[int]:
        """Calculate keyframe positions."""
        total_frames = int(duration * 30)
        num_keyframes = max(3, total_frames // 15)  # Keyframe every half second
        
        return [int(total_frames * i / (num_keyframes - 1)) for i in range(num_keyframes)]
    
    def _design_choreography(self, action_beat: str, scene: Dict) -> Dict[str, Any]:
        """Design choreography for action beat."""
        return {
            "action": action_beat,
            "phases": ["preparation", "execution", "recovery"],
            "timing": "2_frames_anticipation_6_frames_action_2_frames_recovery",
            "style": "dynamic_fluid"
        }
    
    def _calculate_motion_blur(self, action_beat: str) -> Dict[str, Any]:
        """Calculate motion blur settings."""
        if "action" in action_beat.lower() or "dynamic" in action_beat.lower():
            return {"enabled": True, "intensity": 0.7, "samples": 16}
        return {"enabled": True, "intensity": 0.3, "samples": 8}
    
    def _define_impact_frames(self, action_beat: str) -> List[int]:
        """Define frames where impacts occur."""
        if "action" in action_beat.lower():
            return [10, 25, 40]  # Example impact frames
        return []
    
    def _add_anticipation(self, beat_index: int, total_beats: int) -> Dict[str, Any]:
        """Add anticipation to movement."""
        return {
            "frames": 3,
            "direction": "opposite_to_action",
            "intensity": 0.6
        }
    
    def _add_follow_through(self, beat_index: int, total_beats: int) -> Dict[str, Any]:
        """Add follow-through to movement."""
        return {
            "frames": 4,
            "dampening": 0.7,
            "secondary_motion": "enabled"
        }
    
    def _calculate_ease_in(self, total_frames: int) -> Dict[str, Any]:
        """Calculate ease-in timing."""
        return {
            "frames": min(10, total_frames // 4),
            "curve": "quadratic"
        }
    
    def _calculate_ease_out(self, total_frames: int) -> Dict[str, Any]:
        """Calculate ease-out timing."""
        return {
            "frames": min(10, total_frames // 4),
            "curve": "quadratic"
        }
    
    def _calculate_holds(self, camera_angle: str) -> List[Dict[str, Any]]:
        """Calculate hold frames."""
        if camera_angle in ["close_up", "extreme_close_up"]:
            return [{"frame": 15, "duration": 5}]
        return []
    
    def _calculate_frame_spacing(self, camera_angle: str) -> str:
        """Calculate spacing between frames."""
        if camera_angle in ["tracking", "aerial"]:
            return "even_fast"
        return "ease_in_out"
    
    def _determine_path_type(self, camera_angle: str) -> str:
        """Determine type of motion path."""
        path_types = {
            "tracking": "linear_following",
            "aerial": "circular_arc",
            "wide_shot": "straight_line",
            "close_up": "minimal_subtle"
        }
        return path_types.get(camera_angle, "natural_curve")
    
    def _generate_waypoints(self, shot: Dict) -> List[Dict[str, float]]:
        """Generate waypoints for motion path."""
        return [
            {"x": 0.0, "y": 0.0, "z": 0.0, "time": 0.0},
            {"x": 0.5, "y": 0.2, "z": 0.3, "time": 0.5},
            {"x": 1.0, "y": 0.0, "z": 0.5, "time": 1.0}
        ]
    
    def _generate_speed_curve(self, duration: float) -> List[float]:
        """Generate speed curve for motion."""
        num_points = int(duration * 10)  # 10 points per second
        return [0.5 + 0.5 * (i / num_points) for i in range(num_points)]
    
    def _apply_arc_motion(self, camera_angle: str) -> bool:
        """Determine if arc motion should be applied."""
        return camera_angle in ["aerial", "tracking", "over_shoulder"]
    
    def _determine_stance(self, emotional_tone: str, pose_index: int, total_poses: int) -> str:
        """Determine character stance."""
        stances = {
            "high_intensity": "combat_ready",
            "building_tension": "alert_stance",
            "establishing": "neutral_standing",
            "resolution": "relaxed_standing"
        }
        return stances.get(emotional_tone, "neutral_standing")
    
    def _calculate_weight(self, emotional_tone: str) -> str:
        """Calculate weight distribution."""
        if emotional_tone == "high_intensity":
            return "forward_aggressive"
        elif emotional_tone == "building_tension":
            return "centered_balanced"
        return "natural_neutral"
    
    def _calculate_tension(self, emotional_tone: str) -> float:
        """Calculate tension level in pose."""
        tension_map = {
            "high_intensity": 0.9,
            "building_tension": 0.7,
            "establishing": 0.3,
            "resolution": 0.2
        }
        return tension_map.get(emotional_tone, 0.5)
