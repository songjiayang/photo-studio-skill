"""
Configuration module for movie character skill
"""

import os
import json
from pathlib import Path

# Default directory names (relative to skill directory)
DEFAULT_DATA_DIR = "data"
DEFAULT_TEMP_DIR = "temp"
DEFAULT_OUTPUT_DIR = "output"
DEFAULT_LOGS_DIR = "logs"


class Config:
    """Configuration manager for the skill

    This class manages configuration with portable relative paths.
    Paths in config.json can be either:
    - Relative paths (recommended): "temp", "output", "logs"
    - Absolute paths: "/full/path/to/directory"

    The class resolves paths relative to the skill directory.
    """

    def __init__(self, skill_dir=None):
        """
        Initialize configuration manager.

        Args:
            skill_dir: Path to the skill directory. If None, auto-detected from script location.
        """
        self.skill_dir = Path(skill_dir) if skill_dir else Path(__file__).resolve().parent.parent
        self.config_file = self.skill_dir / "config.json"
        self.default_characters_file = self.skill_dir / DEFAULT_DATA_DIR / "default_characters.json"

        # Ensure directories exist
        self._ensure_directories()

        # Load or create config
        self.config = self._load_config()

        # Load default characters
        self.default_characters = self._load_default_characters()

    def _ensure_directories(self):
        """Ensure all required directories exist"""
        for dir_name in [DEFAULT_DATA_DIR, DEFAULT_TEMP_DIR, DEFAULT_OUTPUT_DIR, DEFAULT_LOGS_DIR]:
            (self.skill_dir / dir_name).mkdir(exist_ok=True)

    def _resolve_path(self, path_value):
        """
        Resolve a path value to absolute path.

        Args:
            path_value: Either a relative path (str) or absolute path (str starting with /)

        Returns:
            Path: Resolved absolute path
        """
        if not path_value:
            return self.skill_dir

        path = Path(path_value)

        # If it's an absolute path, use it directly
        if path.is_absolute():
            return path

        # If it's a relative path, resolve from skill directory
        return (self.skill_dir / path).resolve()

    def get_temp_dir(self):
        """Get the absolute path to temp directory"""
        path_value = self.config.get("paths", {}).get("temp_dir", DEFAULT_TEMP_DIR)
        return self._resolve_path(path_value)

    def get_output_dir(self):
        """Get the absolute path to output directory"""
        path_value = self.config.get("paths", {}).get("output_dir", DEFAULT_OUTPUT_DIR)
        return self._resolve_path(path_value)

    def get_logs_dir(self):
        """Get the absolute path to logs directory"""
        path_value = self.config.get("paths", {}).get("logs_dir", DEFAULT_LOGS_DIR)
        return self._resolve_path(path_value)

    @property
    def temp_dir(self):
        """Property for temp directory (backward compatibility)"""
        return self.get_temp_dir()

    @property
    def image_dir(self):
        """Get the absolute path to images output directory"""
        return self.get_output_dir() / "images"

    @property
    def video_dir(self):
        """Get the absolute path to video output directory (for future use)"""
        return self.get_output_dir() / "videos"

    def _load_config(self):
        """Load configuration from file or create default with relative paths"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                # Ensure required fields exist
                if "characters" not in config:
                    config["characters"] = []
                if "paths" not in config:
                    config["paths"] = {
                        "temp_dir": DEFAULT_TEMP_DIR,
                        "output_dir": DEFAULT_OUTPUT_DIR,
                        "logs_dir": DEFAULT_LOGS_DIR
                    }
                if "generation" not in config:
                    config["generation"] = {
                        "default_image_count": 5,
                        "image_width": 1024,
                        "image_height": 1024,
                        "image_model": "doubao-seedream-4.5"
                    }

                # Save updated config if fields were added
                self._save_config(config)
                return config

            except json.JSONDecodeError:
                print(f"Warning: Config file {self.config_file} is corrupted. Using defaults.")

        # Default configuration with RELATIVE paths (portable)
        default_config = {
            "api": {
                "image_generation_url": "https://ark.cn-beijing.volces.com/api/v3/images/generations"
            },
            "paths": {
                # Use RELATIVE paths for portability
                "temp_dir": DEFAULT_TEMP_DIR,
                "output_dir": DEFAULT_OUTPUT_DIR,
                "logs_dir": DEFAULT_LOGS_DIR
            },
            "generation": {
                "default_image_count": 5,
                "image_width": 1024,
                "image_height": 1024,
                "image_model": "doubao-seedream-4.5"
            },
            "characters": []
        }

        # Save default config
        self._save_config(default_config)
        return default_config

    def _load_default_characters(self):
        """Load default movie characters"""
        default_chars = [
            {
                "name": "Iron Man",
                "prompt": "Tony Stark as Iron Man in character on Avengers film set, taking break from shooting, high-tech suit",
                "scene": "movie film set with crew members, cameras, lighting equipment, behind-the-scenes atmosphere"
            },
            {
                "name": "Wonder Woman",
                "prompt": "Diana Prince as Wonder Woman on Justice League film set, between takes, golden armor",
                "scene": "epic film set with director's chairs, camera cranes, production crew working"
            },
            {
                "name": "Spider-Man",
                "prompt": "Peter Parker as Spider-Man on Marvel film set, friendly neighborhood hero pose",
                "scene": "urban film set with green screens, stunt coordinators, special effects equipment"
            },
            {
                "name": "Harry Potter",
                "prompt": "Harry Potter on Hogwarts film set, holding wand, magical atmosphere between scenes",
                "scene": "fantasy film set with magical props, special effects team, cinematic lighting"
            },
            {
                "name": "Neo (Matrix)",
                "prompt": "Neo from The Matrix on film set, wearing sunglasses and black coat, between bullet time shots",
                "scene": "futuristic film set with green code rain screens, wire rigging, special effects"
            },
            {
                "name": "Star-Lord (Guardians of the Galaxy)",
                "prompt": "Peter Quill as Star-Lord on Guardians of the Galaxy film set, wearing leather jacket and helmet, holding blasters",
                "scene": "space film set with alien props, starship models, cosmic background visuals"
            },
            {
                "name": "Gamora (Guardians of the Galaxy)",
                "prompt": "Gamora on Guardians of the Galaxy film set, green-skinned assassin, holding sword, fierce expression",
                "scene": "alien planet film set with exotic flora, spaceship wreckage, otherworldly lighting"
            },
            {
                "name": "Drax the Destroyer (Guardians of the Galaxy)",
                "prompt": "Drax the Destroyer on Guardians of the Galaxy film set, heavily muscled, covered in tattoos, holding knives",
                "scene": "prison ship film set with metal corridors, alien prisoners, sci-fi security systems"
            },
            {
                "name": "Rocket Raccoon (Guardians of the Galaxy)",
                "prompt": "Rocket Raccoon on Guardians of the Galaxy film set, genetically engineered raccoon, holding oversized gun, annoyed expression",
                "scene": "spaceship cockpit film set with control panels, navigation screens, futuristic technology"
            },
            {
                "name": "Groot (Guardians of the Galaxy)",
                "prompt": "Groot on Guardians of the Galaxy film set, sentient tree-like creature, peaceful expression, wooden texture",
                "scene": "alien forest film set with bioluminescent plants, floating rocks, mystical atmosphere"
            },
            {
                "name": "Captain America",
                "prompt": "Steve Rogers as Captain America on Avengers film set, holding iconic shield, patriotic suit",
                "scene": "WWII-era film set with period costumes, military vehicles, historical props"
            },
            {
                "name": "Thor",
                "prompt": "Thor on Marvel film set, holding Mjolnir hammer, flowing red cape, Asgardian armor",
                "scene": "Asgardian palace film set with golden architecture, mystical runes, divine lighting"
            },
            {
                "name": "Black Widow",
                "prompt": "Natasha Romanoff as Black Widow on Avengers film set, black tactical suit, martial arts pose",
                "scene": "spy headquarters film set with high-tech computers, weapon displays, surveillance monitors"
            },
            {
                "name": "Hulk",
                "prompt": "Bruce Banner as Hulk on Avengers film set, massive green creature, roaring expression, torn purple pants",
                "scene": "laboratory film set with broken equipment, scientific instruments, emergency lighting"
            },
            {
                "name": "Black Panther",
                "prompt": "T'Challa as Black Panther on Marvel film set, vibranium suit, cat-like helmet, regal pose",
                "scene": "Wakandan throne room film set with African-inspired decor, advanced technology, tribal patterns"
            },
            {
                "name": "Doctor Strange",
                "prompt": "Stephen Strange as Doctor Strange on Marvel film set, Cloak of Levitation, magical gestures, mystical aura",
                "scene": "Sanctum Sanctorum film set with ancient artifacts, floating books, magical portals"
            },
            {
                "name": "Captain Marvel",
                "prompt": "Carol Danvers as Captain Marvel on Marvel film set, glowing with cosmic energy, flight pose, Kree suit",
                "scene": "space station film set with starfield views, alien technology, zero-gravity effects"
            },
            {
                "name": "Thanos",
                "prompt": "Thanos on Avengers film set, purple-skinned titan, wearing golden armor, Infinity Gauntlet on hand",
                "scene": "Titan planet film set with alien ruins, desolate landscape, cosmic destruction"
            }
        ]

        # Save default characters if file doesn't exist
        if not self.default_characters_file.exists():
            self.default_characters_file.parent.mkdir(exist_ok=True)
            with open(self.default_characters_file, 'w', encoding='utf-8') as f:
                json.dump(default_chars, f, indent=2, ensure_ascii=False)

        return default_chars

    def get_all_scenarios(self):
        """Get all available scenarios from scenarios.json"""
        scenarios_config_file = self.skill_dir / "data" / self.config.get("scenarios", {}).get("config_file", "scenarios.json")

        if not scenarios_config_file.exists():
            # Fallback to old format (single celebrity scenario)
            return [{
                "id": "celebrity",
                "name": "明星合影",
                "description": "与电影明星拍照留念",
                "input_type": "single_photo",
                "required_photos": 1,
                "max_photos": 1,
                "data_file": "default_characters.json"
            }]

        try:
            with open(scenarios_config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                return config_data.get("scenarios", [])
        except (json.JSONDecodeError, IOError):
            # Fallback to old format
            return [{
                "id": "celebrity",
                "name": "明星合影",
                "description": "与电影明星拍照留念",
                "input_type": "single_photo",
                "required_photos": 1,
                "max_photos": 1,
                "data_file": "default_characters.json"
            }]

    def get_scenario(self, scenario_id):
        """Get a specific scenario by ID"""
        scenarios = self.get_all_scenarios()
        for scenario in scenarios:
            if scenario.get("id") == scenario_id:
                return scenario
        return None

    def get_scenario_data(self, scenario_id):
        """Get scenario data file content (styles, poses, templates, or characters)"""
        scenario = self.get_scenario(scenario_id)
        if not scenario:
            return None

        data_file = scenario.get("data_file")
        if not data_file:
            return None

        data_file_path = self.skill_dir / "data" / data_file

        if not data_file_path.exists():
            return None

        try:
            with open(data_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Extract styles, poses, templates, or characters based on file type
            if "styles" in data:
                return data["styles"]
            elif "poses" in data:
                return data["poses"]
            elif "templates" in data:
                return data["templates"]
            else:
                # Assume it's a characters list (backward compatible)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError):
            return None

    def get_backgrounds(self, scenario_id):
        """Get background options for a scenario"""
        data_file = None
        if scenario_id == 'couple':
            data_file = self.skill_dir / "data" / "couple_poses.json"
        elif scenario_id == 'family':
            data_file = self.skill_dir / "data" / "family_templates.json"
        else:
            return None

        if not data_file or not data_file.exists():
            return None

        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("backgrounds", [])
        except (json.JSONDecodeError, IOError):
            return None

    def get_global_settings(self):
        """Get global settings from scenarios config"""
        scenarios_config_file = self.skill_dir / "data" / self.config.get("scenarios", {}).get("config_file", "scenarios.json")

        if not scenarios_config_file.exists():
            return {
                "default_image_count": 5,
                "max_image_count": 10,
                "default_width": 2048,
                "default_height": 2048
            }

        try:
            with open(scenarios_config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                return config_data.get("global_settings", {})
        except (json.JSONDecodeError, IOError):
            return {
                "default_image_count": 5,
                "max_image_count": 10,
                "default_width": 2048,
                "default_height": 2048
            }

    def _save_config(self, config=None):
        """Save configuration to file"""
        config = config or self.config
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def get_api_key(self, api_name=None):
        """
        Get API credentials from environment variable
        Retrieves API key for image generation service
        """
        return os.getenv("ARK_API_KEY")


    def add_character(self, name, prompt, scene=None):
        """Add a custom character"""
        character = {
            "name": name,
            "prompt": prompt,
            "scene": scene or "movie theater setting, cinematic photo"
        }

        self.config["characters"].append(character)
        self._save_config()
        return character

    def get_characters(self, use_defaults=True):
        """Get list of characters (custom + defaults)"""
        characters = self.config["characters"].copy()
        if use_defaults:
            characters.extend(self.default_characters)
        return characters

    def update_setting(self, section, key, value):
        """Update a configuration setting"""
        if section in self.config and key in self.config[section]:
            self.config[section][key] = value
            self._save_config()
            return True
        return False

# Global configuration instance
config = Config()