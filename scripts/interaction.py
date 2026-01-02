"""
Interaction module for collecting user input and managing the generation process
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Optional

class InteractionManager:
    """Manages user interaction for the generation process"""

    def __init__(self, config):
        self.config = config
        self.state_file = Path(config.skill_dir) / "temp" / "generation_state.json"
        self.current_state = self._load_state()

    def _load_state(self):
        """Load current generation state"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
        return {
            "step": "initial",
            "user_photo": None,
            "selected_characters": [],
            "image_count": 5,
            "generated_images": [],
            "image_order": [],
            "confirmed": False
        }

    def _save_state(self):
        """Save current generation state"""
        self.state_file.parent.mkdir(exist_ok=True)
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.current_state, f, indent=2, ensure_ascii=False)

    def collect_scenario_selection(self):
        """
        Let user select which scenario to use
        Returns: selected scenario dict
        """
        print("\n" + "=" * 60)
        print("📷 Photo Studio - Scenario Selection")
        print("=" * 60)

        scenarios = self.config.get_all_scenarios()

        if not scenarios:
            print("No scenarios available. Using default celebrity scenario.")
            return {
                "id": "celebrity",
                "name": "明星合影",
                "description": "与电影明星拍照留念",
                "input_type": "single_photo",
                "required_photos": 1,
                "max_photos": 1,
                "data_file": "default_characters.json"
            }

        print("\nAvailable Scenarios:")
        for i, scenario in enumerate(scenarios, 1):
            print(f"{i}. {scenario['name']}")
            print(f"   {scenario['description']}")
            print()

        print("Select a scenario by number:")
        try:
            choice = int(input("> ").strip())
            if 1 <= choice <= len(scenarios):
                selected = scenarios[choice - 1]
                print(f"\n✓ Selected: {selected['name']}")
                return selected
            else:
                print("Invalid choice. Using first scenario.")
                return scenarios[0]
        except ValueError:
            print("Invalid input. Using first scenario.")
            return scenarios[0]

    def collect_photos_for_scenario(self, scenario):
        """
        Collect photo paths based on scenario requirements
        Returns: list of photo paths
        """
        photos = []
        required = scenario.get("required_photos", 1)
        max_photos = scenario.get("max_photos", 1)

        print(f"\n{'=' * 60}")
        print(f"📸 Photo Upload - {scenario['name']}")
        print(f"{'=' * 60}")
        print(f"Required photos: {required}")
        print(f"Maximum photos: {max_photos}")
        print()

        num_photos = required
        if max_photos > required:
            print(f"You may upload up to {max_photos} photos (default: {required})")
            try:
                custom_count = input(f"How many photos? (Press Enter for {required}): ").strip()
                if custom_count:
                    num_photos = int(custom_count)
                    if num_photos < required:
                        print(f"Minimum {required} photos required. Using {required}.")
                        num_photos = required
                    elif num_photos > max_photos:
                        print(f"Maximum {max_photos} photos allowed. Using {max_photos}.")
                        num_photos = max_photos
            except ValueError:
                print(f"Invalid number. Using default: {required}")

        for i in range(num_photos):
            while True:
                photo_path = input(f"Photo {i+1}/{num_photos}: Enter photo path: ").strip()
                if Path(photo_path).exists():
                    photos.append(photo_path)
                    print(f"  ✓ Added: {Path(photo_path).name}")
                    break
                else:
                    print(f"  ✗ File not found: {photo_path}")

        print(f"\n✓ Collected {len(photos)} photo(s)")
        return photos

    def collect_portrait_inputs(self, scenario, inputs):
        """
        Collect inputs for portrait scenario
        """
        print("\n" + "=" * 60)
        print("🎨 Portrait Photography Setup")
        print("=" * 60)

        # Get photo
        photos = self.collect_photos_for_scenario(scenario)
        inputs["user_photo"] = photos[0] if photos else None

        # Get styles
        styles = self.config.get_scenario_data(scenario["id"])
        if styles and len(styles) > 1:
            print("\nAvailable Portrait Styles:")
            for i, style in enumerate(styles, 1):
                print(f"{i}. {style['name']} ({style.get('category', 'Portrait')})")
                print(f"   {style['prompt'][:80]}...")
                print()

            print("Select styles (comma-separated numbers, or 'all' for all):")
            try:
                style_input = input("> ").strip().lower()
                if style_input == "all":
                    selected_styles = styles
                else:
                    indices = [int(idx.strip()) - 1 for idx in style_input.split(",")]
                    selected_styles = [styles[i] for i in indices if 0 <= i < len(styles)]
                print(f"  ✓ Selected {len(selected_styles)} style(s)")
            except ValueError:
                print("  Invalid selection. Using first style.")
                selected_styles = [styles[0]]
        else:
            selected_styles = styles if styles else []

        inputs["selected_styles"] = selected_styles

        # Get image count
        inputs["image_count"] = min(len(selected_styles), self.config.get_global_settings().get("max_image_count", 10))
        if len(selected_styles) > inputs["image_count"]:
            print(f"Note: Will generate first {inputs['image_count']} styles")

        return inputs

    def collect_couple_inputs(self, scenario, inputs):
        """
        Collect inputs for couple scenario
        """
        print("\n" + "=" * 60)
        print("👫 Couple Portrait Setup")
        print("=" * 60)

        # Get photos
        photos = self.collect_photos_for_scenario(scenario)
        inputs["user_photos"] = photos

        # Select couple type
        types = scenario.get("types", [{"name": "情侣合影", "prompt": "romantic"}])
        if len(types) > 1:
            print("\nCouple Type:")
            for i, t in enumerate(types, 1):
                print(f"{i}. {t['name']}")
            print()
            try:
                type_idx = int(input("Select type: ").strip()) - 1
                if 0 <= type_idx < len(types):
                    inputs["couple_type"] = types[type_idx]
                else:
                    inputs["couple_type"] = types[0]
            except ValueError:
                inputs["couple_type"] = types[0]
        else:
            inputs["couple_type"] = types[0]

        # Get poses
        poses = self.config.get_scenario_data(scenario["id"])
        if poses:
            print(f"\n✓ Available: {len(poses)} poses")

        # Get image count
        print(f"\nHow many photos to generate? (default: 5, max: 10)")
        try:
            count_input = input("> ").strip()
            count = int(count_input) if count_input else 5
            inputs["image_count"] = max(1, min(count, 10))
        except ValueError:
            inputs["image_count"] = 5

        return inputs

    def collect_family_inputs(self, scenario, inputs):
        """
        Collect inputs for family scenario
        """
        print("\n" + "=" * 60)
        print("👨‍👩‍👧‍👦 Family Portrait Setup")
        print("=" * 60)

        # Get photos
        photos = self.collect_photos_for_scenario(scenario)
        inputs["user_photos"] = photos

        # Get person count
        print(f"\nHow many family members in total? (min: {len(photos)}, max: 6)")
        try:
            person_count_input = input("> ").strip()
            person_count = int(person_count_input) if person_count_input else len(photos)
            if person_count < len(photos):
                print(f"Minimum {len(photos)} required. Using {len(photos)}.")
                person_count = len(photos)
            elif person_count > 6:
                print(f"Maximum 6 allowed. Using 6.")
                person_count = 6
        except ValueError:
            person_count = len(photos)

        inputs["person_count"] = person_count

        # Get templates
        templates = self.config.get_scenario_data(scenario["id"])
        if templates:
            print(f"\n✓ Available: {len(templates)} templates")

        # Get image count
        print(f"\nHow many photos to generate? (default: 5, max: 10)")
        try:
            count_input = input("> ").strip()
            count = int(count_input) if count_input else 5
            inputs["image_count"] = max(1, min(count, 10))
        except ValueError:
            inputs["image_count"] = 5

        return inputs

    def collect_user_inputs(self):
        """
        Collect all necessary inputs from user through interactive prompts
        Returns: dictionary with collected inputs
        """
        print("=" * 60)
        print("Movie Character Generation Wizard")
        print("=" * 60)

        inputs = {}

        # Get user photo path
        if not self.current_state["user_photo"]:
            print("\n📷 Step 1: User Photo")
            print("-" * 40)
            photo_path = input("Please enter the path to your photo: ").strip()
            if not Path(photo_path).exists():
                print(f"Error: File '{photo_path}' does not exist.")
                return None
            inputs["user_photo"] = photo_path
            self.current_state["user_photo"] = photo_path
        else:
            inputs["user_photo"] = self.current_state["user_photo"]
            print(f"Using previously selected photo: {inputs['user_photo']}")

        # Get number of images to generate
        if not self.current_state["image_count"]:
            print("\n🎬 Step 2: Number of Movie Characters")
            print("-" * 40)
            print(f"Default is {self.config.config['generation']['default_image_count']} characters.")
            count_input = input("How many movie characters would you like to be with? (Press Enter for default): ").strip()
            if count_input:
                try:
                    count = int(count_input)
                    if count < 1 or count > 10:
                        print("Please enter a number between 1 and 10. Using default.")
                        count = self.config.config['generation']['default_image_count']
                except ValueError:
                    print("Invalid number. Using default.")
                    count = self.config.config['generation']['default_image_count']
            else:
                count = self.config.config['generation']['default_image_count']
            inputs["image_count"] = count
            self.current_state["image_count"] = count
        else:
            inputs["image_count"] = self.current_state["image_count"]
            print(f"Using {inputs['image_count']} characters as previously selected.")

        # Select characters
        if not self.current_state["selected_characters"]:
            print("\n🌟 Step 3: Select Movie Characters")
            print("-" * 40)
            characters = self.config.get_characters()
            print(f"Found {len(characters)} available characters.")

            # Show character list
            for i, char in enumerate(characters, 1):
                print(f"{i}. {char['name']}")

            print("\nOptions:")
            print("1. Use all available characters")
            print("2. Select specific characters")
            print("3. Let AI suggest characters based on your photo")
            print("4. Enter custom movie characters")

            choice = input("\nEnter your choice (1-4): ").strip()

            selected_chars = []
            if choice == "1":
                # Use all characters (up to image_count)
                selected_chars = characters[:inputs["image_count"]]
                print(f"Selected first {len(selected_chars)} characters.")

            elif choice == "2":
                # Select specific characters
                print("Enter the numbers of characters you want (comma-separated):")
                char_indices = input("> ").strip()
                try:
                    indices = [int(idx.strip()) - 1 for idx in char_indices.split(",")]
                    indices = [idx for idx in indices if 0 <= idx < len(characters)]
                    selected_chars = [characters[idx] for idx in indices[:inputs["image_count"]]]
                except ValueError:
                    print("Invalid input. Using first few characters.")
                    selected_chars = characters[:inputs["image_count"]]

            elif choice == "3":
                # AI suggested characters
                print("AI will suggest characters based on your photo...")
                # For now, use default characters
                selected_chars = characters[:inputs["image_count"]]
                print(f"Selected: {', '.join([c['name'] for c in selected_chars])}")

            elif choice == "4":
                # Custom characters
                print("Enter custom movie characters:")
                print("Options:")
                print("  1. Interactive input (one per line, format: Name|Description|Scene)")
                print("  2. JSON input (paste JSON array)")
                print("  3. Load from JSON file")

                input_choice = input("\nChoose input method (1-3): ").strip()

                custom_chars = []

                if input_choice == "1":
                    # Interactive input
                    print("\nEnter characters (one per line, format: Name|Description|Scene)")
                    print("Example: Batman|Bruce Wayne as Batman in dark knight suit|Gotham city at night")
                    print("Scene is optional. Press Enter twice when done.")

                    while len(custom_chars) < inputs["image_count"]:
                        line = input(f"Character {len(custom_chars) + 1}: ").strip()
                        if not line:
                            if custom_chars:
                                break
                            else:
                                continue

                        # Parse line
                        parts = line.split("|")
                        if len(parts) >= 2:
                            name = parts[0].strip()
                            prompt = parts[1].strip()
                            scene = parts[2].strip() if len(parts) >= 3 else "movie set with crew members working, cameras and equipment visible"
                            custom_chars.append({
                                "name": name,
                                "prompt": prompt,
                                "scene": scene
                            })
                        else:
                            # Just name provided
                            custom_chars.append({
                                "name": line.strip(),
                                "prompt": f"{line.strip()} on film set, between takes, cinematic lighting",
                                "scene": "movie set with crew members working, cameras and equipment visible"
                            })

                elif input_choice == "2":
                    # JSON input
                    print("\nPaste JSON array of characters (format: [{\"name\": \"...\", \"prompt\": \"...\", \"scene\": \"...\"}, ...])")
                    print("Press Ctrl+D (Unix) or Ctrl+Z (Windows) then Enter when done:")

                    import sys
                    json_input = ""
                    try:
                        while True:
                            line = sys.stdin.readline()
                            if not line:
                                break
                            json_input += line
                    except KeyboardInterrupt:
                        pass

                    if json_input.strip():
                        try:
                            import json
                            chars_from_json = json.loads(json_input)
                            if isinstance(chars_from_json, list):
                                for char in chars_from_json:
                                    if isinstance(char, dict) and "name" in char:
                                        custom_chars.append({
                                            "name": char["name"],
                                            "prompt": char.get("prompt", f"{char['name']} on film set"),
                                            "scene": char.get("scene", "movie set with crew members working, cameras and equipment visible")
                                        })
                                print(f"✓ Loaded {len(custom_chars)} characters from JSON")
                            else:
                                print("❌ JSON should be an array of objects")
                        except json.JSONDecodeError as e:
                            print(f"❌ Invalid JSON: {e}")

                elif input_choice == "3":
                    # Load from JSON file
                    file_path = input("\nEnter path to JSON file: ").strip()
                    if Path(file_path).exists():
                        try:
                            import json
                            with open(file_path, 'r', encoding='utf-8') as f:
                                chars_from_file = json.load(f)
                            if isinstance(chars_from_file, list):
                                for char in chars_from_file:
                                    if isinstance(char, dict) and "name" in char:
                                        custom_chars.append({
                                            "name": char["name"],
                                            "prompt": char.get("prompt", f"{char['name']} on film set"),
                                            "scene": char.get("scene", "movie set with crew members working, cameras and equipment visible")
                                        })
                                print(f"✓ Loaded {len(custom_chars)} characters from file")
                            else:
                                print("❌ JSON should be an array of objects")
                        except json.JSONDecodeError as e:
                            print(f"❌ Invalid JSON in file: {e}")
                        except Exception as e:
                            print(f"❌ Error reading file: {e}")
                    else:
                        print(f"❌ File not found: {file_path}")


                else:
                    print("Invalid choice. Using interactive input.")
                    # Fallback to simple input
                    print("\nEnter characters (one per line, format: Name|Description):")
                    while len(custom_chars) < inputs["image_count"]:
                        line = input(f"Character {len(custom_chars) + 1}: ").strip()
                        if not line:
                            if custom_chars:
                                break
                            else:
                                continue
                        if "|" in line:
                            name, prompt = line.split("|", 1)
                            custom_chars.append({
                                "name": name.strip(),
                                "prompt": prompt.strip(),
                                "scene": "movie set with crew members working, cameras and equipment visible"
                            })
                        else:
                            custom_chars.append({
                                "name": line.strip(),
                                "prompt": f"{line.strip()} on film set, between takes, cinematic lighting",
                                "scene": "movie set with crew members working, cameras and equipment visible"
                            })

                if not custom_chars:
                    print("No characters provided. Using default characters.")
                    selected_chars = characters[:inputs["image_count"]]
                else:
                    selected_chars = custom_chars[:inputs["image_count"]]

            else:
                print("Invalid choice. Using default selection.")
                selected_chars = characters[:inputs["image_count"]]

            inputs["selected_characters"] = selected_chars
            self.current_state["selected_characters"] = selected_chars
        else:
            inputs["selected_characters"] = self.current_state["selected_characters"]
            print(f"Using previously selected {len(inputs['selected_characters'])} characters.")

        # Save state
        self.current_state["step"] = "inputs_collected"
        self._save_state()

        print("\n✅ Input collection complete!")
        return inputs

    def show_generated_images(self, image_paths: List[str]):
        """
        Display generated images and allow user to review
        """
        print("\n" + "=" * 60)
        print("📸 Generated Images Review")
        print("=" * 60)

        if not image_paths:
            print("No images generated yet.")
            return False

        print(f"\nGenerated {len(image_paths)} images:")
        for i, img_path in enumerate(image_paths, 1):
            print(f"{i}. {Path(img_path).name}")

        print("\nOptions:")
        print("1. View image details")
        print("2. Reorder images")
        print("3. Regenerate specific image")
        print("4. Confirm and save photos")
        print("5. Cancel generation")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            self._view_image_details(image_paths)
            return False

        elif choice == "2":
            new_order = self._reorder_images(image_paths)
            if new_order:
                self.current_state["image_order"] = new_order
                self._save_state()
                print("Image order updated.")
            return False

        elif choice == "3":
            self._regenerate_image(image_paths)
            return False

        elif choice == "4":
            self.current_state["confirmed"] = True
            self.current_state["step"] = "images_confirmed"
            self._save_state()
            print("✅ Images confirmed! Photos saved.")
            return True

        elif choice == "5":
            print("Generation cancelled.")
            sys.exit(0)

        else:
            print("Invalid choice. Please try again.")
            return False

    def _view_image_details(self, image_paths: List[str]):
        """Show detailed information about each image"""
        for i, img_path in enumerate(image_paths, 1):
            print(f"\n--- Image {i} ---")
            print(f"Path: {img_path}")
            print(f"Size: {Path(img_path).stat().st_size / 1024:.1f} KB")
            # Here we could add image analysis or metadata display

    def _reorder_images(self, image_paths: List[str]) -> List[str]:
        """Allow user to reorder images"""
        print("\nCurrent order:")
        for i, img_path in enumerate(image_paths, 1):
            print(f"{i}. {Path(img_path).name}")

        print("\nEnter new order (comma-separated numbers):")
        order_input = input("> ").strip()
        try:
            new_indices = [int(idx.strip()) - 1 for idx in order_input.split(",")]
            # Validate indices
            valid_indices = [idx for idx in new_indices if 0 <= idx < len(image_paths)]
            if len(valid_indices) != len(image_paths):
                print("Invalid order. Must include all images.")
                return image_paths

            new_order = [image_paths[idx] for idx in valid_indices]
            print("New order:")
            for i, img_path in enumerate(new_order, 1):
                print(f"{i}. {Path(img_path).name}")

            confirm = input("\nConfirm new order? (y/n): ").strip().lower()
            if confirm == 'y':
                return new_order
            else:
                return image_paths

        except ValueError:
            print("Invalid input. Order unchanged.")
            return image_paths

    def _regenerate_image(self, image_paths: List[str]):
        """Regenerate a specific image"""
        print("Enter the number of the image to regenerate:")
        for i, img_path in enumerate(image_paths, 1):
            print(f"{i}. {Path(img_path).name}")

        try:
            idx = int(input("> ").strip()) - 1
            if 0 <= idx < len(image_paths):
                print(f"Image {idx + 1} selected for regeneration.")
                # In a real implementation, this would trigger re-generation
                # For now, just mark it in state
                self.current_state["regenerate_index"] = idx
                self._save_state()
            else:
                print("Invalid index.")
        except ValueError:
            print("Invalid input.")

    def get_confirmation(self, message: str) -> bool:
        """Get user confirmation for an action"""
        response = input(f"{message} (y/n): ").strip().lower()
        return response == 'y'

    def show_progress(self, step: str, current: int, total: int):
        """Show progress for a generation step"""
        percentage = (current / total) * 100
        bar_length = 40
        filled_length = int(bar_length * current // total)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        print(f"\r{step}: [{bar}] {current}/{total} ({percentage:.1f}%)", end='')
        if current == total:
            print()

    def update_state(self, key, value):
        """Update a specific state value"""
        self.current_state[key] = value
        self._save_state()