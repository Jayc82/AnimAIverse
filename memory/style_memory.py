"""
Style Memory System - Maintains consistency across episodes and learns from past productions.
Stores and retrieves style preferences and patterns.
"""
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime


class StyleMemory:
    """Manages style memory for consistent animation production."""
    
    def __init__(self, memory_path: str = "memory/style_memory.json"):
        self.memory_path = memory_path
        self.memory = self._load_memory()
        
    def _load_memory(self) -> Dict[str, Any]:
        """Load style memory from disk."""
        if os.path.exists(self.memory_path):
            try:
                with open(self.memory_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return self._initialize_memory()
        return self._initialize_memory()
    
    def _initialize_memory(self) -> Dict[str, Any]:
        """Initialize empty style memory."""
        return {
            "visual_styles": {},
            "color_palettes": {},
            "animation_patterns": {},
            "character_styles": {},
            "composition_preferences": {},
            "narrative_patterns": {},
            "successful_combinations": [],
            "metadata": {
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "version": "1.0"
            }
        }
    
    def save_memory(self):
        """Save style memory to disk."""
        os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)
        self.memory["metadata"]["last_updated"] = datetime.now().isoformat()
        
        with open(self.memory_path, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def store_style(self, style_type: str, style_name: str, style_data: Dict[str, Any]):
        """Store a style in memory."""
        if style_type not in self.memory:
            self.memory[style_type] = {}
        
        self.memory[style_type][style_name] = {
            "data": style_data,
            "timestamp": datetime.now().isoformat(),
            "usage_count": self.memory[style_type].get(style_name, {}).get("usage_count", 0) + 1
        }
        
        self.save_memory()
    
    def retrieve_style(self, style_type: str, style_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve a style from memory."""
        if style_type in self.memory and style_name in self.memory[style_type]:
            style_entry = self.memory[style_type][style_name]
            style_entry["usage_count"] = style_entry.get("usage_count", 0) + 1
            self.save_memory()
            return style_entry["data"]
        return None
    
    def get_popular_styles(self, style_type: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get most popular styles of a given type."""
        if style_type not in self.memory:
            return []
        
        styles = self.memory[style_type]
        sorted_styles = sorted(
            styles.items(),
            key=lambda x: x[1].get("usage_count", 0),
            reverse=True
        )
        
        return [
            {"name": name, "data": entry["data"], "usage_count": entry.get("usage_count", 0)}
            for name, entry in sorted_styles[:limit]
        ]
    
    def store_successful_combination(self, combination: Dict[str, Any]):
        """Store a successful style combination."""
        combination_entry = {
            "combination": combination,
            "timestamp": datetime.now().isoformat(),
            "success_score": combination.get("success_score", 0.8)
        }
        
        self.memory["successful_combinations"].append(combination_entry)
        
        # Keep only the best 100 combinations
        if len(self.memory["successful_combinations"]) > 100:
            self.memory["successful_combinations"].sort(
                key=lambda x: x["success_score"],
                reverse=True
            )
            self.memory["successful_combinations"] = self.memory["successful_combinations"][:100]
        
        self.save_memory()
    
    def get_style_context(self, genre: str = None) -> Dict[str, Any]:
        """Get style context for production."""
        context = {
            "visual_style": "cinematic",
            "animation_style": "dynamic",
            "composition_style": "rule_of_thirds",
            "preferred_palettes": [],
            "narrative_preferences": {}
        }
        
        # Get popular styles
        if "visual_styles" in self.memory:
            popular_visual = self.get_popular_styles("visual_styles", 1)
            if popular_visual:
                context["visual_style"] = popular_visual[0]["name"]
        
        if "animation_patterns" in self.memory:
            popular_animation = self.get_popular_styles("animation_patterns", 1)
            if popular_animation:
                context["animation_style"] = popular_animation[0]["name"]
        
        # Get color palettes
        if "color_palettes" in self.memory:
            context["preferred_palettes"] = self.get_popular_styles("color_palettes", 3)
        
        return context
    
    def learn_from_production(self, production_data: Dict[str, Any]):
        """Learn from a completed production."""
        # Extract and store successful patterns
        if "script" in production_data:
            script = production_data["script"]
            self.store_style("narrative_patterns", script.get("genre", "general"), {
                "structure": "extracted_structure",
                "pacing": "extracted_pacing"
            })
        
        if "final_edit" in production_data:
            final_edit = production_data["final_edit"]
            quality_score = final_edit.get("quality_report", {}).get("metrics", {}).get("overall_score", 0.8)
            
            if quality_score >= 0.85:
                # Store successful combination
                self.store_successful_combination({
                    "visual_style": production_data.get("style_context", {}).get("visual_style"),
                    "animation_style": production_data.get("style_context", {}).get("animation_style"),
                    "success_score": quality_score
                })
    
    def get_recommendations(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get style recommendations based on context."""
        genre = context.get("genre", "action")
        
        recommendations = {
            "visual_style": "cinematic",
            "animation_style": "dynamic",
            "color_palette": "high_contrast",
            "composition": "rule_of_thirds",
            "confidence": 0.7
        }
        
        # Find similar successful combinations
        similar_combos = [
            combo for combo in self.memory.get("successful_combinations", [])
            if combo.get("combination", {}).get("genre") == genre
        ]
        
        if similar_combos:
            best_combo = max(similar_combos, key=lambda x: x.get("success_score", 0))
            recommendations.update(best_combo.get("combination", {}))
            recommendations["confidence"] = 0.9
        
        return recommendations
    
    def clear_old_entries(self, days: int = 90):
        """Clear entries older than specified days."""
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        for style_type in ["visual_styles", "color_palettes", "animation_patterns"]:
            if style_type in self.memory:
                self.memory[style_type] = {
                    name: entry
                    for name, entry in self.memory[style_type].items()
                    if datetime.fromisoformat(entry.get("timestamp", datetime.now().isoformat())).timestamp() > cutoff_date
                }
        
        self.save_memory()
    
    def export_memory(self, export_path: str):
        """Export memory to a file."""
        with open(export_path, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def import_memory(self, import_path: str):
        """Import memory from a file."""
        with open(import_path, 'r') as f:
            imported_memory = json.load(f)
            
        # Merge with existing memory
        for key, value in imported_memory.items():
            if key in self.memory and isinstance(value, dict):
                self.memory[key].update(value)
            else:
                self.memory[key] = value
        
        self.save_memory()
