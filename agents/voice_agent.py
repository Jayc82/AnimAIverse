"""
Voice Agent - Handles thousands of different voice types and voice acting.
Specializes in voice synthesis, character voices, and audio performance.
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent


class VoiceAgent(BaseAgent):
    """Agent responsible for voice synthesis and thousands of voice types."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("Voice", config)
        self.voice_library = self._initialize_voice_library()
        
    def _initialize_voice_library(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize comprehensive voice library."""
        return {
            "human_adult_male": self._create_voice_variants("adult_male", 500),
            "human_adult_female": self._create_voice_variants("adult_female", 500),
            "human_child_male": self._create_voice_variants("child_male", 200),
            "human_child_female": self._create_voice_variants("child_female", 200),
            "elderly_male": self._create_voice_variants("elderly_male", 150),
            "elderly_female": self._create_voice_variants("elderly_female", 150),
            "teen_male": self._create_voice_variants("teen_male", 200),
            "teen_female": self._create_voice_variants("teen_female", 200),
            "animal_cat": self._create_voice_variants("cat", 50),
            "animal_dog": self._create_voice_variants("dog", 100),
            "animal_bird": self._create_voice_variants("bird", 50),
            "creature_fantasy": self._create_voice_variants("fantasy_creature", 100),
            "robot_synthetic": self._create_voice_variants("robot", 80),
            "alien": self._create_voice_variants("alien", 70),
            "monster": self._create_voice_variants("monster", 60)
        }
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate voice profiles and audio direction.
        
        Args:
            input_data: Dictionary containing:
                - characters: Character list with voice requirements
                - dialogue: Dialogue lines to be voiced
                - language: Target language for voices
                - quality: Voice quality (standard, high, exceptional)
                
        Returns:
            Dictionary containing:
                - voice_assignments: Voice profiles for each character
                - voice_direction: Acting and performance notes
                - audio_samples: Voice sample specifications
                - language_variants: Multi-language voice options
        """
        characters = input_data.get("characters", [])
        dialogue = input_data.get("dialogue", {})
        language = input_data.get("language", "en")
        quality = input_data.get("quality", "exceptional")
        
        voice_assignments = self._assign_voices(characters, language, quality)
        voice_direction = self._create_voice_direction(characters, dialogue)
        audio_samples = self._generate_audio_samples(voice_assignments)
        language_variants = self._create_language_variants(voice_assignments, language)
        
        self.log_action("voice_generation", {
            "num_characters": len(characters),
            "language": language,
            "quality": quality,
            "total_voices_available": self._count_total_voices()
        })
        
        return {
            "voice_assignments": voice_assignments,
            "voice_direction": voice_direction,
            "audio_samples": audio_samples,
            "language_variants": language_variants,
            "metadata": {
                "language": language,
                "quality": quality,
                "voice_library_size": self._count_total_voices()
            }
        }
    
    def _create_voice_variants(self, base_type: str, count: int) -> List[Dict[str, Any]]:
        """Create voice variants for a base type."""
        variants = []
        
        for i in range(count):
            variant = {
                "id": f"{base_type}_{i:04d}",
                "base_type": base_type,
                "pitch": self._vary_pitch(base_type, i),
                "tone": self._vary_tone(i),
                "accent": self._assign_accent(base_type, i),
                "speech_rate": self._vary_speech_rate(i),
                "emotion_range": self._define_emotion_range(base_type),
                "vocal_characteristics": self._define_vocal_traits(base_type, i),
                "language_support": ["en", "es", "fr", "ja", "zh", "de"],  # Multi-language
                "age_sound": self._determine_age_sound(base_type, i),
                "distinctiveness": self._calculate_distinctiveness(i)
            }
            variants.append(variant)
        
        return variants
    
    def _assign_voices(self, characters: List[str], language: str, quality: str) -> List[Dict[str, Any]]:
        """Assign specific voices to characters."""
        assignments = []
        
        for char in characters:
            char_str = str(char).lower()
            
            # Determine character type from name/description
            voice_type = self._determine_voice_type(char_str)
            
            assignment = {
                "character": char,
                "voice_profile": self._select_optimal_voice(voice_type, quality),
                "language": language,
                "performance_style": self._determine_performance_style(char_str),
                "emotional_palette": self._create_emotional_palette(char_str),
                "special_effects": self._add_voice_effects(voice_type),
                "lip_sync_data": "phoneme_timing_data",
                "prosody_control": self._define_prosody(char_str)
            }
            assignments.append(assignment)
        
        return assignments
    
    def _create_voice_direction(self, characters: List[str], dialogue: Dict) -> List[Dict[str, Any]]:
        """Create detailed voice acting direction."""
        directions = []
        
        for char in characters:
            direction = {
                "character": char,
                "overall_approach": "natural_and_expressive",
                "key_emotions": ["primary_emotion", "secondary_emotion", "nuanced_feelings"],
                "pacing_notes": "varied_for_dramatic_effect",
                "emphasis_points": "key_dialogue_moments",
                "breath_control": "natural_breathing_patterns",
                "interaction_style": "responsive_to_scene_partners",
                "character_voice_consistency": "maintain_throughout",
                "ad_lib_guidelines": "appropriate_character_moments"
            }
            directions.append(direction)
        
        return directions
    
    def _generate_audio_samples(self, voice_assignments: List[Dict]) -> List[Dict[str, Any]]:
        """Generate audio sample specifications."""
        samples = []
        
        for assignment in voice_assignments:
            sample = {
                "character": assignment["character"],
                "sample_type": "voice_test",
                "sample_lines": [
                    "neutral_tone_sample",
                    "emotional_range_sample",
                    "character_specific_line"
                ],
                "technical_specs": {
                    "sample_rate": "48kHz",
                    "bit_depth": "24-bit",
                    "format": "WAV_uncompressed",
                    "channels": "mono"
                },
                "processing": self._define_audio_processing(assignment["voice_profile"])
            }
            samples.append(sample)
        
        return samples
    
    def _create_language_variants(self, voice_assignments: List[Dict], primary_language: str) -> Dict[str, List[Dict]]:
        """Create multi-language variants for voices."""
        variants = {
            "primary": voice_assignments,
            "alternates": {}
        }
        
        supported_languages = ["en", "es", "fr", "de", "ja", "zh", "pt", "ko", "ru", "ar", "hi", "it"]
        
        for lang in supported_languages:
            if lang != primary_language:
                variants["alternates"][lang] = self._adapt_voices_for_language(voice_assignments, lang)
        
        return variants
    
    def _count_total_voices(self) -> int:
        """Count total voices in library."""
        total = 0
        for category, voices in self.voice_library.items():
            total += len(voices)
        return total
    
    def _vary_pitch(self, base_type: str, index: int) -> str:
        """Vary pitch for voice variant."""
        pitch_values = ["very_low", "low", "medium_low", "medium", "medium_high", "high", "very_high"]
        return pitch_values[index % len(pitch_values)]
    
    def _vary_tone(self, index: int) -> str:
        """Vary tone for voice variant."""
        tones = ["warm", "cold", "bright", "dark", "rich", "thin", "gravelly", "smooth"]
        return tones[index % len(tones)]
    
    def _assign_accent(self, base_type: str, index: int) -> str:
        """Assign accent to voice."""
        accents = [
            "neutral", "british", "american_south", "australian", "irish", "scottish",
            "new_york", "california", "midwest", "boston", "texas", "international"
        ]
        return accents[index % len(accents)]
    
    def _vary_speech_rate(self, index: int) -> str:
        """Vary speech rate."""
        rates = ["very_slow", "slow", "moderate", "fast", "very_fast"]
        return rates[index % len(rates)]
    
    def _define_emotion_range(self, base_type: str) -> List[str]:
        """Define emotional range for voice type."""
        if "child" in base_type:
            return ["happy", "sad", "excited", "scared", "curious", "playful"]
        elif "animal" in base_type:
            return ["content", "alert", "distressed", "playful", "aggressive"]
        else:
            return ["neutral", "happy", "sad", "angry", "surprised", "fearful", "disgusted", "excited"]
    
    def _define_vocal_traits(self, base_type: str, index: int) -> Dict[str, str]:
        """Define specific vocal characteristics."""
        return {
            "resonance": "characteristic_resonance",
            "breathiness": "controlled_breathiness",
            "rasp": "appropriate_rasp_level",
            "clarity": "crystal_clear" if index % 3 == 0 else "natural",
            "power": "strong" if "adult" in base_type else "moderate"
        }
    
    def _determine_age_sound(self, base_type: str, index: int) -> str:
        """Determine age sound of voice."""
        if "child" in base_type:
            return f"child_age_{5 + (index % 10)}"
        elif "elderly" in base_type:
            return f"elderly_age_{60 + (index % 30)}"
        elif "teen" in base_type:
            return f"teen_age_{13 + (index % 7)}"
        else:
            return f"adult_age_{20 + (index % 50)}"
    
    def _calculate_distinctiveness(self, index: int) -> float:
        """Calculate voice distinctiveness score."""
        return 0.5 + (index % 50) / 100.0
    
    def _determine_voice_type(self, character_desc: str) -> str:
        """Determine voice type from character description."""
        if any(word in character_desc for word in ["child", "kid", "young"]):
            return "human_child_male" if "boy" in character_desc else "human_child_female"
        elif any(word in character_desc for word in ["cat", "feline", "kitty"]):
            return "animal_cat"
        elif any(word in character_desc for word in ["dog", "canine", "puppy"]):
            return "animal_dog"
        elif any(word in character_desc for word in ["old", "elderly", "aged"]):
            return "elderly_male" if "man" in character_desc or "male" in character_desc else "elderly_female"
        elif any(word in character_desc for word in ["teen", "adolescent"]):
            return "teen_male" if any(w in character_desc for w in ["boy", "male"]) else "teen_female"
        elif any(word in character_desc for word in ["robot", "android", "ai"]):
            return "robot_synthetic"
        elif any(word in character_desc for word in ["alien", "extraterrestrial"]):
            return "alien"
        elif any(word in character_desc for word in ["monster", "creature", "beast"]):
            return "monster"
        else:
            return "human_adult_male"
    
    def _select_optimal_voice(self, voice_type: str, quality: str) -> Dict[str, Any]:
        """Select optimal voice from library."""
        voices = self.voice_library.get(voice_type, [])
        if voices:
            # Select a high-quality voice based on distinctiveness
            optimal = max(voices, key=lambda v: v.get("distinctiveness", 0))
            return optimal
        return {"id": "default_voice", "base_type": voice_type}
    
    def _determine_performance_style(self, character_desc: str) -> str:
        """Determine voice performance style."""
        if "hero" in character_desc:
            return "confident_and_heroic"
        elif "villain" in character_desc:
            return "menacing_or_cunning"
        elif "comic" in character_desc or "funny" in character_desc:
            return "comedic_timing"
        else:
            return "natural_conversational"
    
    def _create_emotional_palette(self, character_desc: str) -> List[str]:
        """Create emotional range for character."""
        return [
            "primary_emotion",
            "secondary_emotion",
            "conflicted_states",
            "peak_moments",
            "subtle_nuances"
        ]
    
    def _add_voice_effects(self, voice_type: str) -> List[str]:
        """Add special voice effects."""
        effects = []
        
        if "robot" in voice_type:
            effects.extend(["vocoder", "digital_processing", "mechanical_undertone"])
        elif "alien" in voice_type:
            effects.extend(["pitch_shift", "reverb", "otherworldly_processing"])
        elif "monster" in voice_type:
            effects.extend(["distortion", "sub_harmonic", "growl_enhancement"])
        else:
            effects.append("natural_enhancement")
        
        return effects
    
    def _define_prosody(self, character_desc: str) -> Dict[str, str]:
        """Define prosodic features."""
        return {
            "intonation": "character_appropriate",
            "stress_patterns": "natural_emphasis",
            "rhythm": "conversational_flow",
            "timing": "dramatic_appropriate"
        }
    
    def _define_audio_processing(self, voice_profile: Dict) -> List[str]:
        """Define audio processing chain."""
        return [
            "noise_reduction",
            "equalization",
            "compression",
            "de_essing",
            "reverb_subtle",
            "final_limiting"
        ]
    
    def _adapt_voices_for_language(self, assignments: List[Dict], language: str) -> List[Dict[str, Any]]:
        """Adapt voice assignments for different language."""
        adapted = []
        
        for assignment in assignments:
            adapted_assignment = assignment.copy()
            adapted_assignment["language"] = language
            adapted_assignment["phoneme_set"] = f"{language}_phonemes"
            adapted_assignment["cultural_adaptation"] = f"{language}_cultural_context"
            adapted.append(adapted_assignment)
        
        return adapted
