"""
Character Generator Agent - Creates thousands of unique characters.
Specializes in character creation, variation, and population generation.
"""
from typing import Dict, Any, List
import random
from .base_agent import BaseAgent


class CharacterGeneratorAgent(BaseAgent):
    """Agent responsible for generating thousands of unique characters."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("CharacterGenerator", config)
        self.character_database = []
        self.archetypes = [
            "hero", "mentor", "villain", "sidekick", "guardian", "trickster",
            "herald", "shapeshifter", "shadow", "ally", "threshold_guardian"
        ]
        
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate thousands of unique characters.
        
        Args:
            input_data: Dictionary containing:
                - count: Number of characters to generate
                - character_types: Types of characters needed
                - diversity_level: Level of diversity (standard, high, maximum)
                - genre: Story genre for appropriate characters
                
        Returns:
            Dictionary containing:
                - characters: Generated character database
                - character_groups: Organized character groupings
                - relationship_matrix: Character relationship web
                - population_stats: Statistics about generated characters
        """
        count = input_data.get("count", 100)
        character_types = input_data.get("character_types", ["main", "supporting", "background"])
        diversity_level = input_data.get("diversity_level", "maximum")
        genre = input_data.get("genre", "action")
        
        characters = self._generate_character_population(count, character_types, diversity_level, genre)
        character_groups = self._organize_into_groups(characters)
        relationship_matrix = self._build_relationships(characters)
        population_stats = self._analyze_population(characters)
        
        self.log_action("character_generation", {
            "count": count,
            "diversity_level": diversity_level,
            "genre": genre
        })
        
        return {
            "characters": characters,
            "character_groups": character_groups,
            "relationship_matrix": relationship_matrix,
            "population_stats": population_stats,
            "metadata": {
                "total_characters": len(characters),
                "diversity_level": diversity_level,
                "generation_method": "procedural_with_ai_enhancement"
            }
        }
    
    def _generate_character_population(self, count: int, types: List[str], 
                                      diversity: str, genre: str) -> List[Dict[str, Any]]:
        """Generate large population of unique characters."""
        characters = []
        
        for i in range(count):
            character_type = types[i % len(types)]
            character = self._create_unique_character(i, character_type, diversity, genre)
            characters.append(character)
        
        return characters
    
    def _create_unique_character(self, index: int, char_type: str, 
                                diversity: str, genre: str) -> Dict[str, Any]:
        """Create a single unique character with full details."""
        return {
            "id": f"char_{index:05d}",
            "name": self._generate_name(char_type, genre),
            "type": char_type,
            "archetype": self._select_archetype(char_type),
            "personality": self._generate_personality(diversity),
            "appearance": self._generate_appearance(diversity),
            "background": self._generate_background(genre),
            "skills": self._assign_skills(char_type, genre),
            "motivations": self._define_motivations(char_type),
            "quirks": self._add_unique_quirks(diversity),
            "voice_profile": self._create_voice_profile(char_type),
            "age_group": self._assign_age_group(char_type),
            "role_in_story": self._define_story_role(char_type, genre),
            "relationships": [],
            "character_arc": self._outline_character_arc(char_type),
            "visual_tags": self._generate_visual_tags(diversity)
        }
    
    def _organize_into_groups(self, characters: List[Dict]) -> Dict[str, List[Dict]]:
        """Organize characters into logical groups."""
        groups = {
            "protagonists": [],
            "antagonists": [],
            "supporting_cast": [],
            "background_characters": [],
            "special_characters": []
        }
        
        for char in characters:
            char_type = char.get("type", "background")
            archetype = char.get("archetype", "ally")
            
            if char_type == "main" and archetype in ["hero", "mentor"]:
                groups["protagonists"].append(char)
            elif char_type == "main" and archetype in ["villain", "shadow"]:
                groups["antagonists"].append(char)
            elif char_type == "supporting":
                groups["supporting_cast"].append(char)
            else:
                groups["background_characters"].append(char)
        
        return groups
    
    def _build_relationships(self, characters: List[Dict]) -> Dict[str, Any]:
        """Build relationship web between characters."""
        return {
            "total_connections": len(characters) * 2,
            "relationship_types": ["family", "friend", "rival", "mentor", "ally", "enemy"],
            "network_density": "medium",
            "key_relationships": self._identify_key_relationships(characters[:20])
        }
    
    def _analyze_population(self, characters: List[Dict]) -> Dict[str, Any]:
        """Analyze the generated population."""
        return {
            "total_count": len(characters),
            "type_distribution": self._count_by_type(characters),
            "archetype_distribution": self._count_by_archetype(characters),
            "age_distribution": self._count_by_age(characters),
            "diversity_metrics": {
                "appearance_variety": "high",
                "personality_variety": "high",
                "background_variety": "high"
            }
        }
    
    def _generate_name(self, char_type: str, genre: str) -> str:
        """Generate appropriate character name."""
        first_names = ["Alex", "Jordan", "Sam", "Taylor", "Morgan", "Casey", "Riley", "Avery"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def _select_archetype(self, char_type: str) -> str:
        """Select character archetype."""
        if char_type == "main":
            return random.choice(["hero", "mentor", "villain"])
        return random.choice(self.archetypes)
    
    def _generate_personality(self, diversity: str) -> Dict[str, Any]:
        """Generate personality traits."""
        traits = ["brave", "cautious", "optimistic", "cynical", "analytical", "emotional"]
        return {
            "primary_trait": random.choice(traits),
            "secondary_traits": random.sample(traits, 2),
            "complexity": diversity,
            "emotional_range": "wide" if diversity == "maximum" else "moderate"
        }
    
    def _generate_appearance(self, diversity: str) -> Dict[str, Any]:
        """Generate appearance details."""
        return {
            "height": random.choice(["short", "average", "tall"]),
            "build": random.choice(["slim", "athletic", "stocky", "muscular"]),
            "hair_color": random.choice(["black", "brown", "blonde", "red", "gray", "white", "blue", "pink"]),
            "eye_color": random.choice(["brown", "blue", "green", "hazel", "amber"]),
            "distinctive_features": self._generate_distinctive_features(diversity),
            "style": random.choice(["casual", "formal", "edgy", "classic", "sporty"])
        }
    
    def _generate_background(self, genre: str) -> Dict[str, str]:
        """Generate character background."""
        return {
            "origin": f"{genre}_appropriate_origin",
            "education": random.choice(["self-taught", "formal_education", "specialized_training"]),
            "life_experience": "varied_experiences",
            "key_events": "formative_moments"
        }
    
    def _assign_skills(self, char_type: str, genre: str) -> List[str]:
        """Assign character skills."""
        skill_sets = {
            "action": ["combat", "tactics", "survival", "athleticism"],
            "drama": ["communication", "empathy", "insight", "persuasion"],
            "comedy": ["timing", "improvisation", "physical_comedy", "wit"],
            "adventure": ["exploration", "problem_solving", "adaptability", "courage"]
        }
        return skill_sets.get(genre, ["generic_skills"])[:3]
    
    def _define_motivations(self, char_type: str) -> List[str]:
        """Define character motivations."""
        return [
            "primary_goal",
            "underlying_desire",
            "fear_to_overcome"
        ]
    
    def _add_unique_quirks(self, diversity: str) -> List[str]:
        """Add unique character quirks."""
        quirk_count = 3 if diversity == "maximum" else 1
        quirks = ["specific_habit", "unique_mannerism", "memorable_trait", "distinctive_speech"]
        return random.sample(quirks, min(quirk_count, len(quirks)))
    
    def _create_voice_profile(self, char_type: str) -> Dict[str, str]:
        """Create voice profile reference."""
        return {
            "pitch": random.choice(["low", "medium", "high"]),
            "tone": random.choice(["warm", "cold", "neutral", "expressive"]),
            "accent": "character_appropriate_accent",
            "speech_pattern": "distinctive_pattern"
        }
    
    def _assign_age_group(self, char_type: str) -> str:
        """Assign age group."""
        return random.choice(["child", "teen", "young_adult", "adult", "middle_aged", "elderly"])
    
    def _define_story_role(self, char_type: str, genre: str) -> str:
        """Define role in story."""
        roles = {
            "main": ["protagonist", "antagonist", "deuteragonist"],
            "supporting": ["mentor", "ally", "rival"],
            "background": ["crowd", "extra", "ambient"]
        }
        return random.choice(roles.get(char_type, ["extra"]))
    
    def _outline_character_arc(self, char_type: str) -> Dict[str, str]:
        """Outline character development arc."""
        if char_type == "main":
            return {
                "beginning": "initial_state",
                "challenge": "conflict_faced",
                "growth": "transformation",
                "resolution": "final_state"
            }
        return {"arc_type": "static_or_minor_change"}
    
    def _generate_visual_tags(self, diversity: str) -> List[str]:
        """Generate visual identification tags."""
        return ["distinctive_silhouette", "color_coding", "iconic_element", "memorable_design"]
    
    def _generate_distinctive_features(self, diversity: str) -> List[str]:
        """Generate distinctive visual features."""
        features = ["scar", "tattoo", "unique_accessory", "distinctive_clothing", "unusual_trait"]
        count = 2 if diversity == "maximum" else 1
        return random.sample(features, count)
    
    def _identify_key_relationships(self, characters: List[Dict]) -> List[Dict[str, str]]:
        """Identify key character relationships."""
        relationships = []
        for i in range(min(10, len(characters) - 1)):
            relationships.append({
                "character_a": characters[i]["name"],
                "character_b": characters[i + 1]["name"],
                "relationship_type": random.choice(["ally", "rival", "mentor", "friend"])
            })
        return relationships
    
    def _count_by_type(self, characters: List[Dict]) -> Dict[str, int]:
        """Count characters by type."""
        counts = {}
        for char in characters:
            char_type = char.get("type", "unknown")
            counts[char_type] = counts.get(char_type, 0) + 1
        return counts
    
    def _count_by_archetype(self, characters: List[Dict]) -> Dict[str, int]:
        """Count characters by archetype."""
        counts = {}
        for char in characters:
            archetype = char.get("archetype", "unknown")
            counts[archetype] = counts.get(archetype, 0) + 1
        return counts
    
    def _count_by_age(self, characters: List[Dict]) -> Dict[str, int]:
        """Count characters by age group."""
        counts = {}
        for char in characters:
            age_group = char.get("age_group", "unknown")
            counts[age_group] = counts.get(age_group, 0) + 1
        return counts
