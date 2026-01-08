"""
Language Manager - Handles multi-language support for AnimAIverse.
Manages translations, language settings, and localization.
"""
import os
import yaml
from typing import Dict, Any, Optional, List


class LanguageManager:
    """Manages multi-language support for the animation system."""
    
    def __init__(self, config_path: str = "config/languages.yaml"):
        self.config_path = config_path
        self.language_config = self._load_language_config()
        self.default_language = self.language_config.get("languages", {}).get("default", "en")
        self.current_language = self.default_language
        
    def _load_language_config(self) -> Dict[str, Any]:
        """Load language configuration."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default language configuration."""
        return {
            "languages": {
                "default": "en",
                "supported": ["en", "es", "fr", "de", "it", "pt", "ja", "ko", "zh", "ar", "ru", "hi"]
            },
            "language_settings": {
                "en": {"name": "English", "text_direction": "ltr", "font_preference": "latin"}
            }
        }
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported language codes."""
        return self.language_config.get("languages", {}).get("supported", ["en"])
    
    def get_language_info(self, language_code: str) -> Dict[str, Any]:
        """Get information about a specific language."""
        settings = self.language_config.get("language_settings", {})
        return settings.get(language_code, settings.get("en", {}))
    
    def is_language_supported(self, language_code: str) -> bool:
        """Check if a language is supported."""
        return language_code in self.get_supported_languages()
    
    def set_language(self, language_code: str) -> bool:
        """
        Set the current language.
        
        Args:
            language_code: ISO 639-1 language code (e.g., 'en', 'es', 'ja')
            
        Returns:
            True if language was set successfully, False otherwise
        """
        if self.is_language_supported(language_code):
            self.current_language = language_code
            return True
        else:
            print(f"⚠️  Warning: Language '{language_code}' not supported. Using default: {self.default_language}")
            return False
    
    def get_current_language(self) -> str:
        """Get the current language code."""
        return self.current_language
    
    def get_language_name(self, language_code: str = None) -> str:
        """Get the display name of a language."""
        if language_code is None:
            language_code = self.current_language
        
        info = self.get_language_info(language_code)
        return info.get("name", language_code)
    
    def get_text_direction(self, language_code: str = None) -> str:
        """Get text direction for a language (ltr or rtl)."""
        if language_code is None:
            language_code = self.current_language
        
        info = self.get_language_info(language_code)
        return info.get("text_direction", "ltr")
    
    def get_font_preference(self, language_code: str = None) -> str:
        """Get font preference for a language."""
        if language_code is None:
            language_code = self.current_language
        
        info = self.get_language_info(language_code)
        return info.get("font_preference", "latin")
    
    def format_agent_input(self, input_data: Dict[str, Any], language_code: str = None) -> Dict[str, Any]:
        """
        Format agent input with language context.
        
        Args:
            input_data: Original input data
            language_code: Target language code
            
        Returns:
            Input data with language context added
        """
        if language_code is None:
            language_code = self.current_language
        
        # Add language context to input
        input_data["language"] = language_code
        input_data["language_info"] = self.get_language_info(language_code)
        
        # Add language instruction for AI models
        input_data["language_instruction"] = self._get_language_instruction(language_code)
        
        return input_data
    
    def _get_language_instruction(self, language_code: str) -> str:
        """Get instruction text for AI models about language."""
        language_name = self.get_language_name(language_code)
        
        if language_code == "en":
            return "Generate all content in English."
        else:
            return f"Generate all content in {language_name} ({language_code}). Ensure proper grammar, idioms, and cultural context."
    
    def get_ui_text(self, key: str, language_code: str = None) -> str:
        """
        Get UI text in the specified language.
        
        Args:
            key: Text key identifier
            language_code: Language code (uses current if not specified)
            
        Returns:
            Localized text string
        """
        if language_code is None:
            language_code = self.current_language
        
        # UI text translations
        translations = {
            "en": {
                "production_starting": "STARTING ANIMATION PRODUCTION",
                "production_completed": "PRODUCTION COMPLETED SUCCESSFULLY",
                "production_failed": "ERROR: Production failed",
                "stage_writer": "Script Generation (Writer Agent)",
                "stage_director": "Scene Direction (Director Agent)",
                "stage_animator": "Character Animation (Animator Agent)",
                "stage_composer": "Scene Composition (Scene Composer Agent)",
                "stage_editor": "Final Editing (Editor Agent)",
                "loading_memory": "Loading style memory and preferences...",
                "updating_learning": "Updating style memory and learning systems...",
                "genre": "Genre",
                "theme": "Theme",
                "duration": "Duration",
                "quality_score": "Quality Score",
                "total_duration": "Total Duration"
            },
            "es": {
                "production_starting": "INICIANDO PRODUCCIÓN DE ANIMACIÓN",
                "production_completed": "PRODUCCIÓN COMPLETADA EXITOSAMENTE",
                "production_failed": "ERROR: Producción fallida",
                "stage_writer": "Generación de Guión (Agente Escritor)",
                "stage_director": "Dirección de Escena (Agente Director)",
                "stage_animator": "Animación de Personajes (Agente Animador)",
                "stage_composer": "Composición de Escena (Agente Compositor)",
                "stage_editor": "Edición Final (Agente Editor)",
                "loading_memory": "Cargando memoria de estilo y preferencias...",
                "updating_learning": "Actualizando memoria de estilo y sistemas de aprendizaje...",
                "genre": "Género",
                "theme": "Tema",
                "duration": "Duración",
                "quality_score": "Puntuación de Calidad",
                "total_duration": "Duración Total"
            },
            "fr": {
                "production_starting": "DÉMARRAGE DE LA PRODUCTION D'ANIMATION",
                "production_completed": "PRODUCTION TERMINÉE AVEC SUCCÈS",
                "production_failed": "ERREUR: Production échouée",
                "stage_writer": "Génération de Scénario (Agent Écrivain)",
                "stage_director": "Direction de Scène (Agent Réalisateur)",
                "stage_animator": "Animation de Personnages (Agent Animateur)",
                "stage_composer": "Composition de Scène (Agent Compositeur)",
                "stage_editor": "Montage Final (Agent Monteur)",
                "loading_memory": "Chargement de la mémoire de style et des préférences...",
                "updating_learning": "Mise à jour de la mémoire de style et des systèmes d'apprentissage...",
                "genre": "Genre",
                "theme": "Thème",
                "duration": "Durée",
                "quality_score": "Score de Qualité",
                "total_duration": "Durée Totale"
            },
            "ja": {
                "production_starting": "アニメーション制作を開始",
                "production_completed": "制作が正常に完了しました",
                "production_failed": "エラー：制作が失敗しました",
                "stage_writer": "脚本生成（ライターエージェント）",
                "stage_director": "シーン演出（ディレクターエージェント）",
                "stage_animator": "キャラクターアニメーション（アニメーターエージェント）",
                "stage_composer": "シーン構成（コンポーザーエージェント）",
                "stage_editor": "最終編集（エディターエージェント）",
                "loading_memory": "スタイルメモリと設定を読み込んでいます...",
                "updating_learning": "スタイルメモリと学習システムを更新しています...",
                "genre": "ジャンル",
                "theme": "テーマ",
                "duration": "長さ",
                "quality_score": "品質スコア",
                "total_duration": "総時間"
            },
            "zh": {
                "production_starting": "开始动画制作",
                "production_completed": "制作成功完成",
                "production_failed": "错误：制作失败",
                "stage_writer": "剧本生成（编剧代理）",
                "stage_director": "场景导演（导演代理）",
                "stage_animator": "角色动画（动画师代理）",
                "stage_composer": "场景合成（合成师代理）",
                "stage_editor": "最终编辑（编辑代理）",
                "loading_memory": "加载风格记忆和偏好...",
                "updating_learning": "更新风格记忆和学习系统...",
                "genre": "类型",
                "theme": "主题",
                "duration": "时长",
                "quality_score": "质量评分",
                "total_duration": "总时长"
            }
        }
        
        # Get translation for the language, fallback to English
        lang_translations = translations.get(language_code, translations["en"])
        return lang_translations.get(key, translations["en"].get(key, key))
    
    def list_available_languages(self) -> Dict[str, str]:
        """
        Get a dictionary of available languages with their display names.
        
        Returns:
            Dictionary mapping language codes to display names
        """
        languages = {}
        for lang_code in self.get_supported_languages():
            languages[lang_code] = self.get_language_name(lang_code)
        return languages
    
    def validate_content_language(self, content: str, expected_language: str) -> Dict[str, Any]:
        """
        Validate that content is in the expected language.
        
        Args:
            content: Text content to validate
            expected_language: Expected language code
            
        Returns:
            Dictionary with validation results
        """
        # Simple validation - in production, use language detection library
        return {
            "is_valid": True,
            "expected_language": expected_language,
            "confidence": 0.95,
            "note": "Language validation is simplified in this version"
        }
