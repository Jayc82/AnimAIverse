"""
Workflow Coordinator - Manages agent interactions and production pipeline.
Orchestrates the entire animation production process.
"""
import time
from typing import Dict, Any, List, Optional
from datetime import datetime


class WorkflowCoordinator:
    """Coordinates the multi-agent animation production workflow."""
    
    def __init__(self, config: Dict[str, Any], style_memory, continuous_learning):
        self.config = config
        self.style_memory = style_memory
        self.continuous_learning = continuous_learning
        self.agents = {}
        self.current_production = None
        
    def register_agent(self, agent_name: str, agent_instance):
        """Register an agent with the coordinator."""
        self.agents[agent_name] = agent_instance
        
    def execute_production(self, production_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a complete animation production.
        
        Args:
            production_request: Dictionary containing:
                - genre: Animation genre
                - theme: Story theme
                - characters: Character descriptions
                - duration: Target duration in minutes
                - style_preferences: Optional style preferences
                
        Returns:
            Complete production output with all agent results
        """
        start_time = time.time()
        
        print(f"\n{'='*60}")
        print(f"🎬 STARTING ANIMATION PRODUCTION")
        print(f"{'='*60}")
        print(f"Genre: {production_request.get('genre', 'action')}")
        print(f"Theme: {production_request.get('theme', 'N/A')}")
        print(f"Duration: {production_request.get('duration', 5)} minutes")
        print(f"{'='*60}\n")
        
        # Initialize production
        self.current_production = {
            "request": production_request,
            "status": "in_progress",
            "start_time": datetime.now().isoformat(),
            "results": {}
        }
        
        # Get style context
        print("📚 Loading style memory and preferences...")
        style_context = self._prepare_style_context(production_request)
        
        # Execute workflow stages
        try:
            # Stage 1: Writer Agent
            print("\n✍️  Stage 1/5: Script Generation (Writer Agent)")
            script_result = self._execute_writer_stage(production_request, style_context)
            self.current_production["results"]["script"] = script_result
            print("   ✓ Script generated successfully")
            
            # Stage 2: Director Agent
            print("\n🎥 Stage 2/5: Scene Direction (Director Agent)")
            direction_result = self._execute_director_stage(script_result, style_context)
            self.current_production["results"]["direction"] = direction_result
            print("   ✓ Scene direction completed")
            
            # Stage 3: Animator Agent
            print("\n🎨 Stage 3/5: Character Animation (Animator Agent)")
            animation_result = self._execute_animator_stage(
                script_result, direction_result, style_context
            )
            self.current_production["results"]["animation"] = animation_result
            print("   ✓ Animation created")
            
            # Stage 4: Scene Composer Agent
            print("\n🖼️  Stage 4/5: Scene Composition (Scene Composer Agent)")
            composition_result = self._execute_composer_stage(
                script_result, direction_result, animation_result, style_context
            )
            self.current_production["results"]["composition"] = composition_result
            print("   ✓ Scenes composed")
            
            # Stage 5: Editor Agent
            print("\n✂️  Stage 5/5: Final Editing (Editor Agent)")
            final_result = self._execute_editor_stage(
                composition_result, animation_result, style_context
            )
            self.current_production["results"]["final_edit"] = final_result
            print("   ✓ Final edit completed")
            
            # Finalize production
            duration = time.time() - start_time
            self.current_production["status"] = "completed"
            self.current_production["end_time"] = datetime.now().isoformat()
            self.current_production["duration_seconds"] = duration
            
            # Learning and memory updates
            print("\n🧠 Updating style memory and learning systems...")
            self._post_production_learning(self.current_production)
            
            print(f"\n{'='*60}")
            print(f"✅ PRODUCTION COMPLETED SUCCESSFULLY")
            print(f"{'='*60}")
            print(f"Total Duration: {duration:.2f} seconds")
            print(f"Quality Score: {final_result.get('quality_report', {}).get('metrics', {}).get('overall_score', 0):.2f}")
            print(f"{'='*60}\n")
            
            return self.current_production
            
        except Exception as e:
            print(f"\n❌ ERROR: Production failed - {str(e)}")
            self.current_production["status"] = "failed"
            self.current_production["error"] = str(e)
            return self.current_production
    
    def _prepare_style_context(self, production_request: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare style context from memory and preferences."""
        genre = production_request.get("genre", "action")
        
        # Get style context from memory
        memory_context = self.style_memory.get_style_context(genre)
        
        # Get recommendations from learning system
        learning_recommendations = self.continuous_learning.get_optimization_suggestions()
        
        # Merge with user preferences
        style_context = {
            **memory_context,
            **production_request.get("style_preferences", {}),
            "learning_insights": learning_recommendations
        }
        
        return style_context
    
    def _execute_writer_stage(self, request: Dict[str, Any], 
                              style_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute writer agent stage."""
        if "Writer" not in self.agents:
            raise ValueError("Writer agent not registered")
        
        writer = self.agents["Writer"]
        
        writer_input = {
            "genre": request.get("genre", "action"),
            "theme": request.get("theme", ""),
            "characters": request.get("characters", ["Hero", "Companion", "Antagonist"]),
            "duration": request.get("duration", 5),
            "style_context": style_context
        }
        
        result = writer.process(writer_input)
        
        # Record performance
        self.continuous_learning.record_agent_performance("Writer", {
            "quality": 0.9,  # Simulated quality score
            "processing_time": 1.0
        })
        
        return result
    
    def _execute_director_stage(self, script_result: Dict[str, Any],
                                style_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute director agent stage."""
        if "Director" not in self.agents:
            raise ValueError("Director agent not registered")
        
        director = self.agents["Director"]
        
        director_input = {
            "script": script_result.get("script", {}),
            "style_context": style_context,
            "genre": script_result.get("script", {}).get("genre", "action")
        }
        
        result = director.process(director_input)
        
        # Record performance
        self.continuous_learning.record_agent_performance("Director", {
            "quality": 0.88,
            "processing_time": 1.2
        })
        
        return result
    
    def _execute_animator_stage(self, script_result: Dict[str, Any],
                                direction_result: Dict[str, Any],
                                style_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute animator agent stage."""
        if "Animator" not in self.agents:
            raise ValueError("Animator agent not registered")
        
        animator = self.agents["Animator"]
        
        animator_input = {
            "shot_list": direction_result.get("shot_list", []),
            "script": script_result.get("script", {}),
            "style_context": style_context
        }
        
        result = animator.process(animator_input)
        
        # Record performance
        self.continuous_learning.record_agent_performance("Animator", {
            "quality": 0.91,
            "processing_time": 1.5
        })
        
        return result
    
    def _execute_composer_stage(self, script_result: Dict[str, Any],
                                direction_result: Dict[str, Any],
                                animation_result: Dict[str, Any],
                                style_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute scene composer agent stage."""
        if "SceneComposer" not in self.agents:
            raise ValueError("SceneComposer agent not registered")
        
        composer = self.agents["SceneComposer"]
        
        composer_input = {
            "script": script_result.get("script", {}),
            "shot_list": direction_result.get("shot_list", []),
            "character_animations": animation_result.get("character_animations", []),
            "style_context": style_context
        }
        
        result = composer.process(composer_input)
        
        # Record performance
        self.continuous_learning.record_agent_performance("SceneComposer", {
            "quality": 0.89,
            "processing_time": 1.3
        })
        
        return result
    
    def _execute_editor_stage(self, composition_result: Dict[str, Any],
                             animation_result: Dict[str, Any],
                             style_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute editor agent stage."""
        if "Editor" not in self.agents:
            raise ValueError("Editor agent not registered")
        
        editor = self.agents["Editor"]
        
        editor_input = {
            "composed_scenes": composition_result.get("composed_scenes", []),
            "timing_charts": animation_result.get("timing_charts", []),
            "style_context": style_context
        }
        
        result = editor.process(editor_input)
        
        # Record performance
        self.continuous_learning.record_agent_performance("Editor", {
            "quality": 0.92,
            "processing_time": 1.1
        })
        
        return result
    
    def _post_production_learning(self, production: Dict[str, Any]):
        """Update learning systems after production."""
        # Record production
        production_data = {
            "script": production["results"].get("script"),
            "final_edit": production["results"].get("final_edit"),
            "style_context": production["request"].get("style_preferences", {}),
            "quality_report": production["results"].get("final_edit", {}).get("quality_report", {})
        }
        
        self.continuous_learning.record_production(production_data)
        
        # Record workflow metrics
        self.continuous_learning.record_workflow_metrics({
            "duration": production.get("duration_seconds", 0),
            "agent_count": len(self.agents),
            "quality_score": production_data.get("quality_report", {}).get("metrics", {}).get("overall_score", 0)
        })
        
        # Update style memory
        self.style_memory.learn_from_production(production_data)
        
        # Generate improvement insights
        insights = self.continuous_learning.generate_improvement_insights()
        if insights:
            print(f"\n💡 Generated {len(insights)} improvement insights")
    
    def get_production_status(self) -> Dict[str, Any]:
        """Get current production status."""
        if not self.current_production:
            return {"status": "idle", "message": "No active production"}
        
        return {
            "status": self.current_production.get("status", "unknown"),
            "start_time": self.current_production.get("start_time"),
            "completed_stages": len(self.current_production.get("results", {}))
        }
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """Get learning system summary."""
        return self.continuous_learning.get_learning_summary()
    
    def get_style_recommendations(self, genre: str) -> Dict[str, Any]:
        """Get style recommendations for a genre."""
        context = {"genre": genre}
        return self.style_memory.get_recommendations(context)
    
    def export_production(self, production: Dict[str, Any], export_path: str):
        """Export production data to file."""
        import json
        with open(export_path, 'w') as f:
            json.dump(production, f, indent=2)
        print(f"✅ Production exported to {export_path}")
