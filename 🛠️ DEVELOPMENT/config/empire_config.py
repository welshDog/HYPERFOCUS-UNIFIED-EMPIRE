"""
🚀💎 HYPERFOCUS UNIFIED EMPIRE 💎🚀
Unified Configuration Management System

This module provides a centralized configuration system for the entire empire,
supporting environment-specific configs, validation, and ADHD-friendly defaults.
"""

import os
import json
import yaml
from pathlib import Path
from typing import Any, Dict, Optional, Union
from dataclasses import dataclass, field
from dotenv import load_dotenv


@dataclass
class EmpireConfig:
    """
    🏰 Unified Empire Configuration

    ADHD-friendly configuration management with:
    - Clear defaults
    - Environment-specific overrides
    - Validation and type conversion
    - Neurodivergent-optimized settings
    """

    # 🚀 Core Empire Settings
    name: str = "HYPERFOCUS-UNIFIED-EMPIRE"
    version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"

    # 🌐 Network Configuration
    host: str = "localhost"
    port: int = 8000
    api_base_url: str = "http://localhost:8000/api/empire/v1"

    # 🗄️ Database Configuration
    database_url: str = "sqlite:///🛠️ DEVELOPMENT/data/empire.db"
    database_pool_size: int = 10
    database_echo: bool = False

    # 🚀 Redis Configuration
    redis_url: str = "redis://localhost:6379/0"
    redis_password: str = ""
    redis_max_connections: int = 10

    # 🔐 Security Configuration
    secret_key: str = "legendary-empire-secret-change-this"
    jwt_secret: str = "legendary-jwt-secret-change-this"
    jwt_expiry_hours: int = 24
    api_rate_limit: str = "1000/hour"

    # 🤖 AI Agents Configuration
    agents_enabled: bool = True
    agents_message_bus_type: str = "redis"
    agents_heartbeat_interval: int = 30
    agents_max_retries: int = 3

    # 🧠 Neurodivergent Features
    focus_session_duration: int = 25  # Pomodoro minutes
    focus_break_duration: int = 5
    focus_long_break_duration: int = 15
    focus_notifications_enabled: bool = True
    focus_sound_enabled: bool = True

    # 🎨 UI/UX Configuration
    theme: str = "legendary"
    emoji_navigation: bool = True
    reduced_motion: bool = False
    high_contrast: bool = False

    # 🔧 Development Configuration
    dev_mode: bool = True
    hot_reload: bool = True
    auto_restart: bool = True
    dev_tools_port: int = 8081

    # 📊 Monitoring Configuration
    monitoring_enabled: bool = True
    metrics_port: int = 8080
    health_check_interval: int = 60
    log_retention_days: int = 30

    # 🎮 Component Ports
    chaos_genius_port: int = 3000
    hyperfocus_hub_ts_port: int = 3001
    hyperfocus_hub_legacy_port: int = 3002
    filter_zone_port: int = 3003
    neighbor_work_port: int = 3004

    # 🤖 Component Enablement
    broski_bot_enabled: bool = True
    discord_bot_enabled: bool = True
    chaos_genius_enabled: bool = True

    # 📁 Paths
    data_directory: Path = field(default_factory=lambda: Path("🛠️ DEVELOPMENT/data"))
    logs_directory: Path = field(default_factory=lambda: Path("🛠️ DEVELOPMENT/logs"))
    config_directory: Path = field(default_factory=lambda: Path("🛠️ DEVELOPMENT/config"))

    # 🎯 Feature Flags
    experimental_features: bool = False
    beta_features: bool = False
    legendary_mode: bool = True

    @classmethod
    def load(
        cls,
        config_file: Optional[Union[str, Path]] = None,
        env_file: Optional[Union[str, Path]] = None,
    ) -> "EmpireConfig":
        """
        🔄 Load configuration from multiple sources

        Priority order:
        1. Environment variables (highest)
        2. Config file (YAML/JSON)
        3. .env file
        4. Default values (lowest)
        """

        # Load .env file if specified or default
        if env_file:
            load_dotenv(env_file)
        else:
            # Try multiple .env file locations
            env_locations = [
                Path(".env"),
                Path("🛠️ DEVELOPMENT/config/.env"),
                Path("🛠️ DEVELOPMENT/.env"),
            ]
            for env_path in env_locations:
                if env_path.exists():
                    load_dotenv(env_path)
                    break

        # Load config file if specified
        config_data = {}
        if config_file:
            config_path = Path(config_file)
            if config_path.exists():
                if config_path.suffix.lower() in [".yaml", ".yml"]:
                    with open(config_path, "r") as f:
                        config_data = yaml.safe_load(f) or {}
                elif config_path.suffix.lower() == ".json":
                    with open(config_path, "r") as f:
                        config_data = json.load(f)

        # Create config instance with merged data
        config = cls()

        # Apply config file data
        for key, value in config_data.items():
            if hasattr(config, key):
                setattr(config, key, value)

        # Apply environment variables (highest priority)
        config._load_from_environment()

        # Validate and post-process
        config._validate_and_setup()

        return config

    def _load_from_environment(self):
        """🔄 Load configuration from environment variables"""

        # Core settings
        self.name = os.getenv("EMPIRE_NAME", self.name)
        self.version = os.getenv("EMPIRE_VERSION", self.version)
        self.environment = os.getenv("EMPIRE_ENV", self.environment)
        self.debug = self._get_bool_env("EMPIRE_DEBUG", self.debug)
        self.log_level = os.getenv("EMPIRE_LOG_LEVEL", self.log_level)

        # Network settings
        self.host = os.getenv("EMPIRE_HOST", self.host)
        self.port = self._get_int_env("EMPIRE_PORT", self.port)
        self.api_base_url = os.getenv("EMPIRE_API_BASE_URL", self.api_base_url)

        # Database settings
        self.database_url = os.getenv("EMPIRE_DATABASE_URL", self.database_url)
        self.database_pool_size = self._get_int_env(
            "EMPIRE_DATABASE_POOL_SIZE", self.database_pool_size
        )
        self.database_echo = self._get_bool_env(
            "EMPIRE_DATABASE_ECHO", self.database_echo
        )

        # Redis settings
        self.redis_url = os.getenv("EMPIRE_REDIS_URL", self.redis_url)
        self.redis_password = os.getenv("EMPIRE_REDIS_PASSWORD", self.redis_password)
        self.redis_max_connections = self._get_int_env(
            "EMPIRE_REDIS_MAX_CONNECTIONS", self.redis_max_connections
        )

        # Security settings
        self.secret_key = os.getenv("EMPIRE_SECRET_KEY", self.secret_key)
        self.jwt_secret = os.getenv("EMPIRE_JWT_SECRET", self.jwt_secret)
        self.jwt_expiry_hours = self._get_int_env(
            "EMPIRE_JWT_EXPIRY_HOURS", self.jwt_expiry_hours
        )
        self.api_rate_limit = os.getenv("EMPIRE_API_RATE_LIMIT", self.api_rate_limit)

        # AI Agents settings
        self.agents_enabled = self._get_bool_env(
            "EMPIRE_AGENTS_ENABLED", self.agents_enabled
        )
        self.agents_message_bus_type = os.getenv(
            "EMPIRE_AGENTS_MESSAGE_BUS_TYPE", self.agents_message_bus_type
        )
        self.agents_heartbeat_interval = self._get_int_env(
            "EMPIRE_AGENTS_HEARTBEAT_INTERVAL", self.agents_heartbeat_interval
        )
        self.agents_max_retries = self._get_int_env(
            "EMPIRE_AGENTS_MAX_RETRIES", self.agents_max_retries
        )

        # Neurodivergent features
        self.focus_session_duration = self._get_int_env(
            "FOCUS_SESSION_DEFAULT_DURATION", self.focus_session_duration
        )
        self.focus_break_duration = self._get_int_env(
            "FOCUS_BREAK_DURATION", self.focus_break_duration
        )
        self.focus_long_break_duration = self._get_int_env(
            "FOCUS_LONG_BREAK_DURATION", self.focus_long_break_duration
        )
        self.focus_notifications_enabled = self._get_bool_env(
            "FOCUS_NOTIFICATIONS_ENABLED", self.focus_notifications_enabled
        )
        self.focus_sound_enabled = self._get_bool_env(
            "FOCUS_SOUND_ENABLED", self.focus_sound_enabled
        )

        # UI/UX settings
        self.theme = os.getenv("EMPIRE_THEME", self.theme)
        self.emoji_navigation = self._get_bool_env(
            "EMPIRE_EMOJI_NAVIGATION", self.emoji_navigation
        )
        self.reduced_motion = self._get_bool_env(
            "EMPIRE_REDUCED_MOTION", self.reduced_motion
        )
        self.high_contrast = self._get_bool_env(
            "EMPIRE_HIGH_CONTRAST", self.high_contrast
        )

        # Development settings
        self.dev_mode = self._get_bool_env("EMPIRE_DEV_MODE", self.dev_mode)
        self.hot_reload = self._get_bool_env("EMPIRE_HOT_RELOAD", self.hot_reload)
        self.auto_restart = self._get_bool_env("EMPIRE_AUTO_RESTART", self.auto_restart)
        self.dev_tools_port = self._get_int_env(
            "EMPIRE_DEV_TOOLS_PORT", self.dev_tools_port
        )

        # Monitoring settings
        self.monitoring_enabled = self._get_bool_env(
            "EMPIRE_MONITORING_ENABLED", self.monitoring_enabled
        )
        self.metrics_port = self._get_int_env("EMPIRE_METRICS_PORT", self.metrics_port)
        self.health_check_interval = self._get_int_env(
            "EMPIRE_HEALTH_CHECK_INTERVAL", self.health_check_interval
        )
        self.log_retention_days = self._get_int_env(
            "EMPIRE_LOG_RETENTION_DAYS", self.log_retention_days
        )

        # Component ports
        self.chaos_genius_port = self._get_int_env(
            "CHAOS_GENIUS_PORT", self.chaos_genius_port
        )
        self.hyperfocus_hub_ts_port = self._get_int_env(
            "HYPERFOCUS_HUB_TS_PORT", self.hyperfocus_hub_ts_port
        )
        self.hyperfocus_hub_legacy_port = self._get_int_env(
            "HYPERFOCUS_HUB_LEGACY_PORT", self.hyperfocus_hub_legacy_port
        )
        self.filter_zone_port = self._get_int_env(
            "FILTER_ZONE_PORT", self.filter_zone_port
        )
        self.neighbor_work_port = self._get_int_env(
            "NEIGHBOR_WORK_PORT", self.neighbor_work_port
        )

        # Component enablement
        self.broski_bot_enabled = self._get_bool_env(
            "BROSKI_BOT_ENABLED", self.broski_bot_enabled
        )
        self.discord_bot_enabled = self._get_bool_env(
            "DISCORD_BOT_TOKEN", self.discord_bot_enabled
        )  # Enabled if token exists
        self.chaos_genius_enabled = self._get_bool_env(
            "CHAOS_GENIUS_ENABLED", self.chaos_genius_enabled
        )

        # Feature flags
        self.experimental_features = self._get_bool_env(
            "EMPIRE_EXPERIMENTAL_FEATURES", self.experimental_features
        )
        self.beta_features = self._get_bool_env(
            "EMPIRE_BETA_FEATURES", self.beta_features
        )
        self.legendary_mode = self._get_bool_env(
            "EMPIRE_LEGENDARY_MODE", self.legendary_mode
        )

    def _get_bool_env(self, key: str, default: bool) -> bool:
        """🔄 Get boolean from environment variable"""
        value = os.getenv(key)
        if value is None:
            return default
        return value.lower() in ("true", "1", "yes", "on", "enabled")

    def _get_int_env(self, key: str, default: int) -> int:
        """🔄 Get integer from environment variable"""
        value = os.getenv(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            return default

    def _validate_and_setup(self):
        """✅ Validate configuration and setup derived values"""

        # Ensure directories exist
        self.data_directory.mkdir(parents=True, exist_ok=True)
        self.logs_directory.mkdir(parents=True, exist_ok=True)
        self.config_directory.mkdir(parents=True, exist_ok=True)

        # Validate required settings
        if self.environment not in ["development", "staging", "production"]:
            raise ValueError(f"Invalid environment: {self.environment}")

        if self.log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError(f"Invalid log level: {self.log_level}")

        # Setup environment-specific defaults
        if self.environment == "production":
            self.debug = False
            self.dev_mode = False
            self.hot_reload = False
            self.log_level = "WARNING" if self.log_level == "DEBUG" else self.log_level

        # ADHD-friendly validation
        if self.focus_session_duration < 5 or self.focus_session_duration > 60:
            raise ValueError(
                "Focus session duration should be between 5-60 minutes for optimal ADHD experience"
            )

    def get_component_config(self, component: str) -> Dict[str, Any]:
        """
        🎯 Get configuration specific to a component

        Args:
            component: Component name (e.g., 'broski-bot', 'chaos-genius')

        Returns:
            Dictionary of component-specific configuration
        """

        component_configs = {
            "broski-bot": {
                "enabled": self.broski_bot_enabled,
                "api_key": os.getenv("BROSKI_BOT_API_KEY", ""),
                "api_secret": os.getenv("BROSKI_BOT_API_SECRET", ""),
                "sandbox_mode": self._get_bool_env("BROSKI_BOT_SANDBOX_MODE", True),
                "risk_level": os.getenv("BROSKI_BOT_RISK_LEVEL", "low"),
                "max_position_size": self._get_int_env(
                    "BROSKI_BOT_MAX_POSITION_SIZE", 1000
                ),
            },
            "discord-manager": {
                "enabled": self.discord_bot_enabled,
                "token": os.getenv("DISCORD_BOT_TOKEN", ""),
                "guild_id": os.getenv("DISCORD_GUILD_ID", ""),
                "command_prefix": os.getenv("DISCORD_COMMAND_PREFIX", "!"),
                "admin_roles": os.getenv(
                    "DISCORD_ADMIN_ROLES", "admin,moderator"
                ).split(","),
                "notifications_enabled": self._get_bool_env(
                    "DISCORD_NOTIFICATIONS_ENABLED", True
                ),
            },
            "chaos-genius": {
                "enabled": self.chaos_genius_enabled,
                "port": self.chaos_genius_port,
                "database_url": os.getenv(
                    "CHAOS_GENIUS_DATABASE_URL",
                    "sqlite:///🛠️ DEVELOPMENT/data/chaos_genius.db",
                ),
                "cache_ttl": self._get_int_env("CHAOS_GENIUS_CACHE_TTL", 300),
            },
            "hyperfocus-hub-ts": {
                "port": self.hyperfocus_hub_ts_port,
                "api_url": f"{self.api_base_url}",
                "theme": self.theme,
                "emoji_navigation": self.emoji_navigation,
            },
            "focus-tools": {
                "session_duration": self.focus_session_duration,
                "break_duration": self.focus_break_duration,
                "long_break_duration": self.focus_long_break_duration,
                "notifications_enabled": self.focus_notifications_enabled,
                "sound_enabled": self.focus_sound_enabled,
                "audio_volume": float(os.getenv("EMPIRE_AUDIO_VOLUME", "0.5")),
            },
        }

        return component_configs.get(component, {})

    def to_dict(self) -> Dict[str, Any]:
        """📊 Convert configuration to dictionary"""
        return {
            field.name: getattr(self, field.name)
            for field in self.__dataclass_fields__.values()
        }

    def save_to_file(self, file_path: Union[str, Path], format: str = "yaml"):
        """💾 Save configuration to file"""
        file_path = Path(file_path)
        config_dict = self.to_dict()

        # Convert Path objects to strings for serialization
        for key, value in config_dict.items():
            if isinstance(value, Path):
                config_dict[key] = str(value)

        if format.lower() == "yaml":
            with open(file_path, "w") as f:
                yaml.dump(config_dict, f, default_flow_style=False, indent=2)
        elif format.lower() == "json":
            with open(file_path, "w") as f:
                json.dump(config_dict, f, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def __str__(self) -> str:
        """🎨 String representation"""
        return f"EmpireConfig(name={self.name}, env={self.environment}, legendary_mode={self.legendary_mode})"

    def __repr__(self) -> str:
        """🔍 Debug representation"""
        return self.__str__()


# 🏰 Global empire configuration instance
empire_config: Optional[EmpireConfig] = None


def get_empire_config() -> EmpireConfig:
    """
    🏰 Get the global empire configuration instance

    Returns:
        EmpireConfig: The global configuration instance
    """
    global empire_config
    if empire_config is None:
        empire_config = EmpireConfig.load()
    return empire_config


def reload_empire_config() -> EmpireConfig:
    """
    🔄 Reload the global empire configuration

    Returns:
        EmpireConfig: The reloaded configuration instance
    """
    global empire_config
    empire_config = EmpireConfig.load()
    return empire_config


# 🎯 Convenience functions for common configuration access
def get_database_url() -> str:
    """🗄️ Get database URL"""
    return get_empire_config().database_url


def get_redis_url() -> str:
    """🚀 Get Redis URL"""
    return get_empire_config().redis_url


def get_api_base_url() -> str:
    """🌐 Get API base URL"""
    return get_empire_config().api_base_url


def is_development() -> bool:
    """🔧 Check if running in development mode"""
    return get_empire_config().environment == "development"


def is_production() -> bool:
    """🚀 Check if running in production mode"""
    return get_empire_config().environment == "production"


def is_legendary_mode() -> bool:
    """⚡ Check if legendary mode is enabled"""
    return get_empire_config().legendary_mode


if __name__ == "__main__":
    # 🧪 Test the configuration system
    print("🚀💎 HYPERFOCUS UNIFIED EMPIRE - Configuration Test 💎🚀")

    config = EmpireConfig.load()
    print(f"\n📊 Configuration loaded: {config}")
    print(f"\n🏰 Empire Name: {config.name}")
    print(f"🌍 Environment: {config.environment}")
    print(f"⚡ Legendary Mode: {config.legendary_mode}")
    print(f"🧠 Focus Session: {config.focus_session_duration} minutes")

    # Test component-specific config
    print(f"\n🤖 BROski Bot Config: {config.get_component_config('broski-bot')}")
    print(f"\n🎯 Focus Tools Config: {config.get_component_config('focus-tools')}")

    print(f"\n✅ Configuration system is LEGENDARY! ⚡❤️‍🔥")
