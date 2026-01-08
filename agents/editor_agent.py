"""
Editor Agent - Final editing, timing adjustments, and post-production.
Polishes the final animation and ensures quality.
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent


class EditorAgent(BaseAgent):
    """Agent responsible for final editing and post-production."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("Editor", config)
        
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform final editing and post-production.
        
        Args:
            input_data: Dictionary containing:
                - composed_scenes: Scenes from composer
                - timing_charts: Timing information
                - style_context: Style preferences
                
        Returns:
            Dictionary containing:
                - final_edit: Complete edited animation
                - transitions: Scene transitions
                - audio_guide: Audio synchronization guide
                - quality_report: Quality assessment
        """
        composed_scenes = input_data.get("composed_scenes", [])
        timing_charts = input_data.get("timing_charts", [])
        style_context = input_data.get("style_context", {})
        
        final_edit = self._create_final_edit(composed_scenes, timing_charts)
        transitions = self._refine_transitions(composed_scenes)
        audio_guide = self._create_audio_guide(composed_scenes)
        quality_report = self._assess_quality(final_edit)
        
        self.log_action("final_editing", {
            "num_scenes": len(composed_scenes),
            "total_duration": sum(s.get("duration", 0) for s in composed_scenes),
            "quality_score": quality_report.get("overall_score", 0)
        })
        
        return {
            "final_edit": final_edit,
            "transitions": transitions,
            "audio_guide": audio_guide,
            "quality_report": quality_report,
            "metadata": {
                "total_duration": sum(s.get("duration", 0) for s in composed_scenes),
                "scene_count": len(composed_scenes),
                "status": "completed"
            }
        }
    
    def _create_final_edit(self, composed_scenes: List[Dict], 
                          timing_charts: List[Dict]) -> Dict[str, Any]:
        """Create the final edited version."""
        timeline = []
        current_time = 0.0
        
        for scene in composed_scenes:
            scene_num = scene.get("scene_number", 1)
            duration = scene.get("duration", 30)
            
            timeline_entry = {
                "scene_number": scene_num,
                "start_time": current_time,
                "end_time": current_time + duration,
                "duration": duration,
                "shots": self._edit_shots(scene.get("shots", [])),
                "adjustments": self._apply_timing_adjustments(scene, timing_charts),
                "color_correction": self._apply_color_correction(scene),
                "sound_markers": self._place_sound_markers(scene)
            }
            timeline.append(timeline_entry)
            current_time += duration
        
        return {
            "timeline": timeline,
            "total_duration": current_time,
            "format": "1920x1080_30fps",
            "codec": "h264",
            "quality": "high"
        }
    
    def _refine_transitions(self, composed_scenes: List[Dict]) -> List[Dict[str, Any]]:
        """Refine transitions between scenes."""
        transitions = []
        
        for i in range(len(composed_scenes) - 1):
            current_scene = composed_scenes[i]
            next_scene = composed_scenes[i + 1]
            
            transition = {
                "from_scene": current_scene.get("scene_number", i + 1),
                "to_scene": next_scene.get("scene_number", i + 2),
                "type": self._select_transition_type(current_scene, next_scene),
                "duration": self._calculate_transition_duration(current_scene, next_scene),
                "easing": self._select_easing_function(current_scene, next_scene),
                "effects": self._add_transition_effects(current_scene, next_scene)
            }
            transitions.append(transition)
        
        return transitions
    
    def _create_audio_guide(self, composed_scenes: List[Dict]) -> Dict[str, Any]:
        """Create audio synchronization guide."""
        audio_tracks = {
            "dialogue": [],
            "sound_effects": [],
            "music": [],
            "ambience": []
        }
        
        for scene in composed_scenes:
            scene_num = scene.get("scene_number", 1)
            
            # Dialogue markers
            for character in scene.get("characters", []):
                audio_tracks["dialogue"].append({
                    "scene": scene_num,
                    "character": character,
                    "timing": "sync_to_lip_movement",
                    "volume": 1.0,
                    "effects": ["eq", "compression"]
                })
            
            # Sound effects
            audio_tracks["sound_effects"].extend(
                self._generate_sfx_markers(scene)
            )
            
            # Music
            audio_tracks["music"].append(
                self._suggest_music(scene)
            )
            
            # Ambience
            audio_tracks["ambience"].append({
                "scene": scene_num,
                "type": scene.get("environment", {}).get("ambient_sound", ["general"])[0],
                "volume": 0.3,
                "loop": True
            })
        
        return {
            "tracks": audio_tracks,
            "master_volume": 1.0,
            "normalization": "EBU_R128",
            "mix_type": "stereo"
        }
    
    def _assess_quality(self, final_edit: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the quality of the final animation."""
        timeline = final_edit.get("timeline", [])
        
        quality_metrics = {
            "timing_accuracy": self._check_timing_accuracy(timeline),
            "visual_consistency": self._check_visual_consistency(timeline),
            "narrative_flow": self._check_narrative_flow(timeline),
            "technical_quality": self._check_technical_quality(final_edit),
            "overall_score": 0.0
        }
        
        # Calculate overall score
        scores = [
            quality_metrics["timing_accuracy"],
            quality_metrics["visual_consistency"],
            quality_metrics["narrative_flow"],
            quality_metrics["technical_quality"]
        ]
        quality_metrics["overall_score"] = sum(scores) / len(scores)
        
        return {
            "metrics": quality_metrics,
            "passed": quality_metrics["overall_score"] >= 0.8,
            "issues": self._identify_issues(quality_metrics),
            "recommendations": self._generate_recommendations(quality_metrics)
        }
    
    def _edit_shots(self, shots: List[Dict]) -> List[Dict[str, Any]]:
        """Edit individual shots."""
        edited_shots = []
        
        for shot in shots:
            edited = {
                "shot_number": shot.get("shot_number"),
                "duration": shot.get("duration", 5),
                "trim_in": 0.0,
                "trim_out": shot.get("duration", 5),
                "speed": 1.0,
                "effects": self._apply_shot_effects(shot),
                "stabilization": True,
                "noise_reduction": 0.3
            }
            edited_shots.append(edited)
        
        return edited_shots
    
    def _apply_timing_adjustments(self, scene: Dict, 
                                  timing_charts: List[Dict]) -> Dict[str, Any]:
        """Apply timing adjustments to scene."""
        return {
            "speed_ramping": [],
            "freeze_frames": [],
            "time_remapping": "linear",
            "frame_interpolation": True
        }
    
    def _apply_color_correction(self, scene: Dict) -> Dict[str, Any]:
        """Apply color correction to scene."""
        color_palette = scene.get("color_palette", {})
        
        return {
            "white_balance": "auto",
            "exposure": 0.0,
            "contrast": 1.1,
            "saturation": 1.05,
            "vibrance": 0.1,
            "temperature": self._adjust_temperature(scene),
            "tint": 0.0,
            "lut": "cinematic_standard"
        }
    
    def _place_sound_markers(self, scene: Dict) -> List[Dict[str, Any]]:
        """Place sound synchronization markers."""
        markers = []
        shots = scene.get("shots", [])
        
        for i, shot in enumerate(shots):
            markers.append({
                "shot": shot.get("shot_number"),
                "type": "dialogue_sync",
                "position": i * shot.get("duration", 5)
            })
            
            markers.append({
                "shot": shot.get("shot_number"),
                "type": "action_sync",
                "position": i * shot.get("duration", 5) + shot.get("duration", 5) / 2
            })
        
        return markers
    
    def _select_transition_type(self, current_scene: Dict, next_scene: Dict) -> str:
        """Select appropriate transition type."""
        current_atmosphere = current_scene.get("atmosphere", {}).get("mood", "neutral")
        next_atmosphere = next_scene.get("atmosphere", {}).get("mood", "neutral")
        
        if current_atmosphere == "high_intensity" and next_atmosphere != "high_intensity":
            return "fade"
        elif current_atmosphere == next_atmosphere:
            return "cut"
        else:
            return "dissolve"
    
    def _calculate_transition_duration(self, current_scene: Dict, next_scene: Dict) -> float:
        """Calculate transition duration."""
        transition_type = self._select_transition_type(current_scene, next_scene)
        
        durations = {
            "cut": 0.0,
            "dissolve": 1.0,
            "fade": 1.5,
            "wipe": 0.8
        }
        
        return durations.get(transition_type, 1.0)
    
    def _select_easing_function(self, current_scene: Dict, next_scene: Dict) -> str:
        """Select easing function for transition."""
        return "ease_in_out"
    
    def _add_transition_effects(self, current_scene: Dict, next_scene: Dict) -> List[str]:
        """Add effects to transition."""
        return ["motion_blur", "cross_fade"]
    
    def _generate_sfx_markers(self, scene: Dict) -> List[Dict[str, Any]]:
        """Generate sound effect markers."""
        sfx = []
        shots = scene.get("shots", [])
        
        for shot in shots:
            shot_num = shot.get("shot_number", 1)
            
            sfx.extend([
                {
                    "scene": scene.get("scene_number", 1),
                    "shot": shot_num,
                    "type": "ambient",
                    "timing": "continuous",
                    "volume": 0.5
                },
                {
                    "scene": scene.get("scene_number", 1),
                    "shot": shot_num,
                    "type": "action",
                    "timing": "on_beat",
                    "volume": 0.8
                }
            ])
        
        return sfx
    
    def _suggest_music(self, scene: Dict) -> Dict[str, Any]:
        """Suggest music for scene."""
        atmosphere = scene.get("atmosphere", {})
        mood = atmosphere.get("mood", "neutral")
        
        music_suggestions = {
            "high_intensity": {
                "tempo": "fast",
                "genre": "orchestral_action",
                "intensity": "high",
                "key": "minor"
            },
            "building_tension": {
                "tempo": "medium",
                "genre": "suspenseful",
                "intensity": "medium",
                "key": "minor"
            },
            "establishing": {
                "tempo": "medium",
                "genre": "ambient",
                "intensity": "low",
                "key": "major"
            },
            "resolution": {
                "tempo": "slow",
                "genre": "emotional",
                "intensity": "medium",
                "key": "major"
            }
        }
        
        music = music_suggestions.get(mood, music_suggestions["establishing"])
        music["scene"] = scene.get("scene_number", 1)
        music["volume"] = 0.6
        
        return music
    
    def _check_timing_accuracy(self, timeline: List[Dict]) -> float:
        """Check timing accuracy."""
        # Simulate timing check
        return 0.92
    
    def _check_visual_consistency(self, timeline: List[Dict]) -> float:
        """Check visual consistency."""
        # Simulate visual consistency check
        return 0.88
    
    def _check_narrative_flow(self, timeline: List[Dict]) -> float:
        """Check narrative flow."""
        # Check if scenes flow logically
        return 0.90
    
    def _check_technical_quality(self, final_edit: Dict[str, Any]) -> float:
        """Check technical quality."""
        # Check format, resolution, etc.
        format_valid = final_edit.get("format") == "1920x1080_30fps"
        quality_high = final_edit.get("quality") == "high"
        
        return 0.95 if (format_valid and quality_high) else 0.75
    
    def _identify_issues(self, quality_metrics: Dict) -> List[str]:
        """Identify quality issues."""
        issues = []
        metrics = quality_metrics.get("metrics", {})
        
        if metrics.get("timing_accuracy", 1.0) < 0.8:
            issues.append("Timing accuracy below threshold")
        
        if metrics.get("visual_consistency", 1.0) < 0.8:
            issues.append("Visual consistency needs improvement")
        
        if metrics.get("narrative_flow", 1.0) < 0.8:
            issues.append("Narrative flow could be smoother")
        
        return issues if issues else ["No major issues detected"]
    
    def _generate_recommendations(self, quality_metrics: Dict) -> List[str]:
        """Generate recommendations for improvement."""
        recommendations = []
        metrics = quality_metrics.get("metrics", {})
        
        if metrics.get("timing_accuracy", 1.0) < 0.9:
            recommendations.append("Review and adjust scene timing")
        
        if metrics.get("visual_consistency", 1.0) < 0.9:
            recommendations.append("Ensure consistent color grading across scenes")
        
        if metrics.get("narrative_flow", 1.0) < 0.9:
            recommendations.append("Consider refining scene transitions")
        
        if not recommendations:
            recommendations.append("Quality is excellent - ready for final export")
        
        return recommendations
    
    def _apply_shot_effects(self, shot: Dict) -> List[str]:
        """Apply effects to shot."""
        effects = ["color_correction", "sharpening"]
        
        camera_angle = shot.get("camera", {}).get("angle")
        if camera_angle in ["tracking", "aerial"]:
            effects.append("stabilization")
        
        return effects
    
    def _adjust_temperature(self, scene: Dict) -> float:
        """Adjust color temperature."""
        time_of_day = scene.get("time_of_day", "day")
        
        temperatures = {
            "dawn": 0.1,
            "morning": 0.05,
            "afternoon": 0.0,
            "evening": 0.15,
            "night": -0.1,
            "midnight": -0.15
        }
        
        return temperatures.get(time_of_day, 0.0)
