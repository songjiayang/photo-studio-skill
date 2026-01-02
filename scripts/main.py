#!/usr/bin/env python3
"""
Main entry point for Photo Studio
"""

import sys
import os
import time
import argparse
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import config
from interaction import InteractionManager
from image_generator import ImageGenerator

def check_api_keys():
    """Check if required API credentials are configured"""
    api_key = config.get_api_key()
    if api_key:
        return True

    print("❌ API credentials not configured. Please configure API credentials before running.")
    return False

def setup_argparse():
    """Set up command line argument parsing"""
    parser = argparse.ArgumentParser(
        description="Photo Studio - Generate portrait and group photos using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py generate --photo path/to/photo.jpg --scenario portrait
  python main.py generate --photos photo1.jpg,photo2.jpg --scenario couple
  python main.py list-scenarios
  python main.py list-styles --scenario portrait
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Start the generation process")
    generate_parser.add_argument("--photo", "-p", help="Path to user photo (for single photo scenarios)")
    generate_parser.add_argument("--photos", help="Comma-separated photo paths (for multi-photo scenarios)")
    generate_parser.add_argument("--scenario", "-s", help="Scenario type (celebrity, portrait, couple, family)")
    generate_parser.add_argument("--style", help="Style name (for portrait scenario)")
    generate_parser.add_argument("--pose", help="Pose name (for couple scenario)")
    generate_parser.add_argument("--template", help="Template name (for family scenario)")
    generate_parser.add_argument("--background", help="Background name (for couple/family scenarios)")
    generate_parser.add_argument("--count", "-c", type=int, help="Number of images to generate")
    generate_parser.add_argument("--characters", "-ch", help="Comma-separated character names (for celebrity scenario)")
    generate_parser.add_argument("--skip-review", action="store_true", help="Skip image review step")
    generate_parser.add_argument("--non-interactive", "-ni", action="store_true",
                                 help="Run in non-interactive mode (for agent integration)")

    # List scenarios command
    subparsers.add_parser("list-scenarios", help="List available photo scenarios")

    # List styles command
    list_styles_parser = subparsers.add_parser("list-styles", help="List available styles for a scenario")
    list_styles_parser.add_argument("--scenario", "-s", help="Scenario type (portrait, couple, family)")

    # List poses command (for couple scenario)
    subparsers.add_parser("list-poses", help="List available couple poses")

    # List templates command (for family scenario)
    subparsers.add_parser("list-templates", help="List available family templates")

    # List backgrounds command
    list_backgrounds_parser = subparsers.add_parser("list-backgrounds", help="List available backgrounds for a scenario")
    list_backgrounds_parser.add_argument("--scenario", "-s", help="Scenario type (couple, family)")

    # List characters command
    subparsers.add_parser("list-characters", help="List available movie characters")

    # Add character command
    add_parser = subparsers.add_parser("add-character", help="Add a custom movie character")
    add_parser.add_argument("name", help="Character name")
    add_parser.add_argument("prompt", help="Character description prompt")
    add_parser.add_argument("--scene", help="Scene description (optional)")

    # Config command
    config_parser = subparsers.add_parser("config", help="View or update configuration")
    config_parser.add_argument("--show", action="store_true", help="Show current configuration")
    config_parser.add_argument("--set", help="Set configuration value (format: section.key=value)")

    # Cleanup command
    subparsers.add_parser("cleanup", help="Clean up temporary files")

    return parser

def command_generate(args):
    """Handle generate command"""
    print("\n📷 Photo Studio")
    print("=" * 60)

    # Check API keys
    if not check_api_keys():
        return 1

    # Initialize managers
    interaction = InteractionManager(config)
    image_gen = ImageGenerator(config, interaction)

    # Non-interactive mode (for agent integration)
    if getattr(args, 'non_interactive', False):
        print("\n🤖 Running in non-interactive mode...")

        # Get scenario type
        scenario_id = getattr(args, 'scenario', 'celebrity')
        generated_images = []

        # Handle different scenarios
        if scenario_id == 'portrait':
            # Portrait scenario - validate photo first
            photo_path = args.photo
            if not photo_path or not Path(photo_path).exists():
                print(f"❌ Photo not found: {photo_path}")
                return 1

            # Portrait scenario - generate portrait photos with styles
            style_name = getattr(args, 'style', None)
            if not style_name:
                print("❌ Style is required for portrait scenario. Use --style parameter.")
                print("Available styles:")
                styles = config.get_scenario_data('portrait')
                if styles:
                    for s in styles[:5]:
                        print(f"  - {s['name']}")
                return 1

            # Find the style
            styles = config.get_scenario_data('portrait')
            if not styles:
                print("❌ Failed to load portrait styles.")
                return 1

            selected_style = None
            for style in styles:
                if style['name'] == style_name or style.get('id') == style_name:
                    selected_style = style
                    break

            if not selected_style:
                print(f"❌ Style '{style_name}' not found.")
                return 1

            # Get count (default to 1 for portrait)
            count = getattr(args, 'count', 1)

            # Generate portrait images
            result = image_gen.generate_portrait_images(
                photo_path,
                [selected_style],
                count
            )
            generated_images = result if result else []

        elif scenario_id == 'couple':
            # Couple scenario
            photos_arg = getattr(args, 'photos', None)
            if not photos_arg:
                print("❌ --photos parameter is required for couple scenario.")
                return 1

            photo_paths = [p.strip() for p in photos_arg.split(',')]
            if len(photo_paths) < 2:
                print("❌ At least 2 photos required for couple scenario.")
                return 1

            # Validate all photos exist
            for p in photo_paths:
                if not Path(p).exists():
                    print(f"❌ Photo not found: {p}")
                    return 1

            count = getattr(args, 'count', 1)

            # Get couple pose (default to first one)
            couple_poses = config.get_scenario_data('couple')
            if not couple_poses:
                print("❌ Failed to load couple poses.")
                return 1

            # Filter by specified pose if provided
            pose_name = getattr(args, 'pose', None)
            if pose_name:
                selected_pose = None
                for pose in couple_poses:
                    if pose['name'] == pose_name or pose.get('id') == pose_name:
                        selected_pose = pose
                        break
                if not selected_pose:
                    print(f"❌ Pose '{pose_name}' not found.")
                    print("Available poses:")
                    for p in couple_poses[:5]:
                        print(f"  - {p['name']}")
                    return 1
                couple_type = selected_pose
            else:
                couple_type = couple_poses[0]

            # Get background (optional)
            background = None
            background_name = getattr(args, 'background', None)
            if background_name:
                backgrounds = config.get_backgrounds('couple')
                if backgrounds:
                    for bg in backgrounds:
                        if bg['name'] == background_name or bg.get('id') == background_name:
                            background = bg
                            break
                    if not background:
                        print(f"❌ Background '{background_name}' not found.")
                        print("Available backgrounds:")
                        for b in backgrounds[:5]:
                            print(f"  - {b['name']}")
                        return 1

            # Generate couple images
            result = image_gen.generate_couple_images(
                photo_paths,
                couple_type,
                count,
                background
            )
            generated_images = result if result else []

        elif scenario_id == 'family':
            # Family scenario
            photos_arg = getattr(args, 'photos', None)
            if not photos_arg:
                print("❌ --photos parameter is required for family scenario.")
                return 1

            photo_paths = [p.strip() for p in photos_arg.split(',')]
            if len(photo_paths) < 1:
                print("❌ At least 1 photo required for family scenario.")
                return 1

            # Validate all photos exist
            for p in photo_paths:
                if not Path(p).exists():
                    print(f"❌ Photo not found: {p}")
                    return 1

            count = getattr(args, 'count', 1)

            # Get family template
            family_templates = config.get_scenario_data('family')
            if not family_templates:
                print("❌ Failed to load family templates.")
                return 1

            # Filter by specified template if provided
            template_name = getattr(args, 'template', None)
            if template_name:
                selected_template = None
                for template in family_templates:
                    if template['name'] == template_name or template.get('id') == template_name:
                        selected_template = template
                        break
                if not selected_template:
                    print(f"❌ Template '{template_name}' not found.")
                    print("Available templates:")
                    for t in family_templates[:5]:
                        print(f"  - {t['name']}")
                    return 1
                family_template = selected_template
            else:
                family_template = family_templates[0]

            # Get background (optional)
            background = None
            background_name = getattr(args, 'background', None)
            if background_name:
                backgrounds = config.get_backgrounds('family')
                if backgrounds:
                    for bg in backgrounds:
                        if bg['name'] == background_name or bg.get('id') == background_name:
                            background = bg
                            break
                    if not background:
                        print(f"❌ Background '{background_name}' not found.")
                        print("Available backgrounds:")
                        for b in backgrounds[:5]:
                            print(f"  - {b['name']}")
                        return 1

            # Generate family images
            result = image_gen.generate_family_images(
                photo_paths,
                len(photo_paths),
                count,
                family_template,
                background
            )
            generated_images = result if result else []

        else:
            # Celebrity scenario (default) - validate photo first
            photo_path = args.photo
            if not photo_path or not Path(photo_path).exists():
                print(f"❌ Photo not found: {photo_path}")
                return 1

            # Get characters
            all_chars = config.get_characters()

            # Filter by specified characters if provided
            if hasattr(args, 'characters') and args.characters:
                selected_chars = []
                char_names = [c.strip() for c in args.characters.split(',')]
                for char in all_chars:
                    if char['name'] in char_names:
                        selected_chars.append(char)
                characters_to_generate = selected_chars
            else:
                # Use first N characters
                count = getattr(args, 'count', config.config["generation"]["default_image_count"])
                characters_to_generate = all_chars[:count]

            # Generate images
            for i, character in enumerate(characters_to_generate):
                print(f"\nGenerating image {i+1}/{len(characters_to_generate)}: {character['name']}")

                image_path = image_gen.generate_single_image(
                    photo_path,
                    character,
                    i
                )

                if image_path:
                    generated_images.append(image_path)
                # Rate limiting - wait between requests
                if i < len(characters_to_generate) - 1:
                    time.sleep(2)

        # Summary
        print("\n" + "=" * 60)
        print("📊 Generation Summary")
        print("=" * 60)
        print(f"✅ Successfully generated: {len(generated_images)} images")

        # Generation complete
        print("\n" + "=" * 60)
        print("✅ Photo Generation Complete!")
        print("=" * 60)
        print(f"\nGenerated {len(generated_images)} photos:")
        for i, img_path in enumerate(generated_images, 1):
            print(f"  {i}. {Path(img_path).name}")
        print(f"\nImages saved in: {image_gen.image_dir}")

        # Cleanup
        image_gen.cleanup_temp_files()

        return 0

    # Interactive mode
    print("\n📷 Photo Studio Generation Wizard")
    print("=" * 60)

    # Step 1: Photo selection
    if not interaction.current_state.get("user_photo"):
        print("\n📷 Step 1: User Photo")
        print("-" * 40)
        photo_input = input("Please enter path to your photo: ").strip()
        if not Path(photo_input).exists():
            print(f"❌ Photo not found: {photo_input}")
            return 1
        photo_path = photo_input
        interaction.update_state("user_photo", photo_path)
    else:
        photo_path = interaction.current_state["user_photo"]
        print(f"\nUsing previously selected photo: {photo_path}")

    # Step 2: Character/Style/Type selection
    # Get scenario to determine what to select
    scenario_id = getattr(args, 'scenario', None) or config.config.get("scenarios", {}).get("default_scenario", "celebrity")

    # For celebrity scenario, select characters
    if scenario_id == "celebrity":
        all_chars = config.get_characters()

        if not interaction.current_state.get("selected_characters"):
            print("\n🌟 Step 2: Select Movie Characters")
            print("-" * 40)
            print(f"Found {len(all_chars)} available characters.")

            # Show character list
            for i, char in enumerate(all_chars, 1):
                print(f"{i}. {char['name']}")

            print("\nOptions:")
            print("1. Use first few characters (recommended)")
            print("2. Use all available characters")
            print("3. Let AI suggest characters based on your photo")
            print("4. Enter custom movie characters")

            choice = input("\nEnter your choice (1-4): ").strip()

            selected_chars = []
            if choice == "1":
                # Use first few
                count = getattr(args, 'count', config.config["generation"]["default_image_count"])
                selected_chars = all_chars[:count]
                print(f"Selected first {len(selected_chars)} characters.")
            elif choice == "2":
                selected_chars = all_chars
                print(f"Selected all {len(selected_chars)} characters.")
            elif choice == "3":
                # AI suggested
                count = getattr(args, 'count', config.config["generation"]["default_image_count"])
                selected_chars = all_chars[:count]
                print(f"AI suggested: {', '.join([c['name'] for c in selected_chars])}")
            elif choice == "4":
                # Custom characters - simplified
                print("\nEnter custom characters:")
                print("Format: Name|Prompt|Scene")
                print("Example: Batman|Bruce Wayne as Batman|Gotham city at night")
                print("Press Enter twice when done.")

                while len(selected_chars) < 5:
                    line = input(f"Character {len(selected_chars) + 1}: ").strip()
                    if not line:
                        if selected_chars:
                            break
                        else:
                            continue

                    # Parse line
                    parts = line.split("|")
                    if len(parts) >= 2:
                        name = parts[0].strip()
                        prompt = parts[1].strip()
                        scene = parts[2].strip() if len(parts) >= 3 else "movie set with crew members working, cameras and equipment visible"
                        selected_chars.append({
                            "name": name,
                            "prompt": prompt,
                            "scene": scene
                        })
                    else:
                        # Just name provided
                        selected_chars.append({
                            "name": line.strip(),
                            "prompt": f"{line.strip()} on film set, between takes, cinematic lighting",
                            "scene": "movie set with crew members working, cameras and equipment visible"
                        })

            interaction.update_state("selected_characters", selected_chars)
        else:
            selected_chars = interaction.current_state["selected_characters"]
            print(f"\nUsing previously selected {len(selected_chars)} characters.")

        # Step 3: Number of images
        if not interaction.current_state.get("image_count"):
            print("\n🎬 Step 3: Number of Images")
            print("-" * 40)
            count_input = input(f"How many characters would you like to be with? (default: {len(selected_chars)}): ").strip()
            if count_input:
                try:
                    count = int(count_input)
                    if count < 1 or count > 10:
                        print("Please enter a number between 1 and 10. Using default.")
                        count = len(selected_chars)
                except ValueError:
                    print("Invalid number. Using default.")
                    count = len(selected_chars)
            else:
                count = len(selected_chars)

            interaction.update_state("image_count", count)
        else:
            count = interaction.current_state["image_count"]
            print(f"\nUsing {count} images as previously selected.")

        # Limit to requested count
        selected_chars = selected_chars[:count]

        # Generate images
        print("\n" + "=" * 60)
        print("🖼️  Image Generation Started")
        print("=" * 60)

        generated_images = []
        failed_characters = []

        for i, character in enumerate(selected_chars):
            print(f"\nGenerating image {i+1}/{len(selected_chars)}: {character['name']}")

            image_path = image_gen.generate_single_image(
                photo_path,
                character,
                i
            )

            if image_path:
                generated_images.append(image_path)
                interaction.update_state("generated_images", generated_images)
            else:
                failed_characters.append(character['name'])

            # Rate limiting - wait between requests
            if i < len(selected_chars) - 1:
                time.sleep(2)

        # Summary
        print("\n" + "=" * 60)
        print("📊 Generation Summary")
        print("=" * 60)
        print(f"✅ Successfully generated: {len(generated_images)} images")
        if failed_characters:
            print(f"❌ Failed for: {', '.join(failed_characters)}")

        interaction.current_state["image_order"] = generated_images.copy()
        interaction._save_state()

        # Show generated images
        interaction.show_generated_images(generated_images)

        return 0
    else:
        # For new scenarios (portrait, couple, family), not yet fully implemented
        print(f"\n⚠️ Scenario '{scenario_id}' interactive mode not yet implemented.")
        print("Use non-interactive mode for now.")
        print("\nExample:")
        print(f"  python scripts/main.py generate --photo your_photo.jpg --scenario {scenario_id} --non-interactive")
        return 1

def command_list_scenarios(args):
    """Handle list-scenarios command"""
    scenarios = config.get_all_scenarios()

    print("\n" + "=" * 60)
    print("📷 Available Photo Scenarios")
    print("=" * 60)

    if not scenarios:
        print("No scenarios found. Check configuration.")
        return 1

    print("\nAvailable Scenarios:\n")
    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario['name']}")
        print(f"   ID: {scenario['id']}")
        print(f"   Description: {scenario['description']}")
        print(f"   Input Type: {scenario.get('input_type', 'unknown')}")
        print(f"   Required Photos: {scenario.get('required_photos', 'N/A')}")
        print(f"   Max Photos: {scenario.get('max_photos', 'N/A')}")
        print()

    print(f"Total: {len(scenarios)} scenarios")
    print(f"Default: {config.config.get('scenarios', {}).get('default_scenario', 'celebrity')}")
    return 0

def command_list_styles(args):
    """Handle list-styles command"""
    scenario_id = args.scenario

    if not scenario_id:
        print("❌ Scenario ID is required. Use --scenario parameter.")
        print("\nUsage: python main.py list-styles --scenario <scenario_id>")
        print("\nAvailable scenarios:")
        scenarios = config.get_all_scenarios()
        for s in scenarios:
            print(f"  - {s['id']}: {s['name']}")
        return 1

    scenario = config.get_scenario(scenario_id)
    if not scenario:
        print(f"❌ Scenario '{scenario_id}' not found.")
        return 1

    data_file = scenario.get("data_file")
    if not data_file:
        print(f"❌ Data file not configured for scenario '{scenario_id}'.")
        return 1

    styles = config.get_scenario_data(scenario_id)
    if not styles:
        print(f"❌ No styles found for scenario '{scenario_id}'.")
        return 1

    print("\n" + "=" * 60)
    print(f"🎨 Styles for Scenario: {scenario['name']}")
    print("=" * 60)

    print(f"\nTotal: {len(styles)} styles")
    print()

    if isinstance(styles, list):
        for i, style in enumerate(styles, 1):
            category = style.get('category', 'General')
            print(f"{i}. {style['name']} ({category})")
            print(f"   ID: {style.get('id', 'N/A')}")
            print(f"   Prompt: {style.get('prompt', '')[:60]}...")
            if style.get('lighting'):
                print(f"   Lighting: {style.get('lighting', '')[:60]}...")
            if style.get('background'):
                print(f"   Background: {style.get('background', '')[:60]}...")
            if style.get('mood'):
                print(f"   Mood: {style.get('mood', '')[:60]}...")
            if style.get('attire'):
                print(f"   Attire: {style['attire'][:60]}...")
            if style.get('scene'):
                print(f"   Scene: {style['scene'][:60]}...")
            if style.get('atmosphere'):
                print(f"   Atmosphere: {style['atmosphere'][:60]}...")
            print()
    else:
        print(f"Data type: {type(styles)}")
        print(f"Keys: {list(styles.keys()) if isinstance(styles, dict) else 'N/A'}")

    print(f"\nScenario Data File: {data_file}")
    print("=" * 60)
    return 0

def command_list_backgrounds(args):
    """Handle list-backgrounds command"""
    scenario_id = args.scenario

    if not scenario_id:
        print("❌ Scenario ID is required. Use --scenario parameter.")
        print("\nUsage: python main.py list-backgrounds --scenario <scenario_id>")
        print("\nAvailable scenarios:")
        print("  - couple: 双人合影")
        print("  - family: 全家合影")
        return 1

    if scenario_id not in ['couple', 'family']:
        print(f"❌ Scenario '{scenario_id}' does not have background options.")
        return 1

    backgrounds = config.get_backgrounds(scenario_id)
    if not backgrounds:
        print(f"❌ No backgrounds found for scenario '{scenario_id}'.")
        return 1

    scenario_name = "双人合影" if scenario_id == 'couple' else "全家合影"
    print("\n" + "=" * 60)
    print(f"🎨 Backgrounds for Scenario: {scenario_name}")
    print("=" * 60)

    print(f"\nTotal: {len(backgrounds)} backgrounds\n")

    for i, bg in enumerate(backgrounds, 1):
        print(f"{i}. {bg['name']}")
        print(f"   ID: {bg.get('id', 'N/A')}")
        print(f"   Description: {bg.get('prompt', '')[:80]}...")

    print("\n" + "=" * 60)
    return 0

def command_list_poses(args):
    """Handle list-poses command"""
    poses = config.get_scenario_data('couple')
    if not poses:
        print("❌ No poses found for couple scenario.")
        return 1

    print("\n" + "=" * 60)
    print("👫 Available Couple Poses")
    print("=" * 60)

    print(f"\nTotal: {len(poses)} poses\n")

    for i, pose in enumerate(poses, 1):
        print(f"{i}. {pose['name']}")
        print(f"   ID: {pose.get('id', 'N/A')}")
        print(f"   Pose: {pose.get('prompt', '')[:80]}...")
        print(f"   Scene: {pose.get('scene', '')[:80]}...")
        print(f"   Atmosphere: {pose.get('atmosphere', '')[:80]}...")
        if pose.get('attire'):
            print(f"   Attire: {pose['attire'][:80]}...")
        print()

    print("=" * 60)
    return 0

def command_list_templates(args):
    """Handle list-templates command"""
    templates = config.get_scenario_data('family')
    if not templates:
        print("❌ No templates found for family scenario.")
        return 1

    print("\n" + "=" * 60)
    print("👨‍👩‍👧‍👦 Available Family Templates")
    print("=" * 60)

    print(f"\nTotal: {len(templates)} templates\n")

    for i, template in enumerate(templates, 1):
        print(f"{i}. {template['name']}")
        print(f"   ID: {template.get('id', 'N/A')}")
        print(f"   Prompt: {template.get('prompt', '')[:80]}...")
        print(f"   Scene: {template.get('scene', '')[:80]}...")
        print(f"   Atmosphere: {template.get('atmosphere', '')[:80]}...")
        print(f"   Person Count: {template.get('person_count', 'N/A')}")
        if template.get('attire'):
            print(f"   Attire: {template['attire'][:80]}...")
        print()

    print("=" * 60)
    return 0

def command_list_characters(args):
    """Handle list-characters command"""
    characters = config.get_characters()
    custom_chars = config.config["characters"]

    print("🎭 Available Movie Characters")
    print("=" * 60)

    if custom_chars:
        print("\n📝 Custom Characters:")
        for i, char in enumerate(custom_chars, 1):
            print(f"  {i}. {char['name']}")
            print(f"     Prompt: {char['prompt'][:80]}...")
            if char.get('scene'):
                print(f"     Scene: {char['scene'][:80]}...")
            print()

    print("\n🌟 Default Characters:")
    default_chars = [c for c in characters if c not in custom_chars]
    for i, char in enumerate(default_chars, 1):
        print(f"  {i}. {char['name']}")
        print(f"     Prompt: {char['prompt'][:80]}...")
        if char.get('scene'):
            print(f"     Scene: {char['scene'][:80]}...")
        print()

    print(f"Total: {len(characters)} characters")
    return 0

def command_add_character(args):
    """Handle add-character command"""
    print("➕ Adding Custom Character")
    print("=" * 60)

    character = config.add_character(args.name, args.prompt, args.scene)

    print(f"✅ Added character: {character['name']}")
    print(f"   Prompt: {character['prompt']}")
    if character.get('scene'):
        print(f"   Scene: {character['scene']}")

    return 0

def command_config(args):
    """Handle config command"""
    if args.show:
        print("⚙️ Current Configuration")
        print("=" * 60)
        print(json.dumps(config.config, indent=2, ensure_ascii=False))
    elif args.set:
        try:
            section_key, value = args.set.split('=', 1)
            section, key = section_key.split('.', 1)
            if config.update_setting(section, key, value):
                print(f"✅ Updated {section}.{key} = {value}")
            else:
                print(f"❌ Failed to update {section}.{key}")
        except ValueError:
            print("❌ Invalid format. Use: section.key=value")
            return 1
    else:
        print("Configuration file:", config.config_file)
        print("\nUse --show to view config or --set to update")
    return 0

def command_cleanup(args):
    """Handle cleanup command"""
    print("🧹 Cleaning up temporary files...")
    temp_dir = Path(config.config["paths"]["temp_dir"])
    if temp_dir.exists():
        for item in temp_dir.iterdir():
            try:
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    import shutil
                    shutil.rmtree(item)
            except Exception as e:
                print(f"⚠️ Could not delete {item}: {e}")
        print(f"✅ Cleaned up {temp_dir}")
    else:
        print("⚠️ Temp directory does not exist")
    return 0

def main():
    """Main entry point"""
    parser = setup_argparse()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        if args.command == "generate":
            return command_generate(args)
        elif args.command == "list-scenarios":
            return command_list_scenarios(args)
        elif args.command == "list-styles":
            return command_list_styles(args)
        elif args.command == "list-poses":
            return command_list_poses(args)
        elif args.command == "list-templates":
            return command_list_templates(args)
        elif args.command == "list-backgrounds":
            return command_list_backgrounds(args)
        elif args.command == "list-characters":
            return command_list_characters(args)
        elif args.command == "add-character":
            return command_add_character(args)
        elif args.command == "config":
            return command_config(args)
        elif args.command == "cleanup":
            return command_cleanup(args)
        else:
            print(f"❌ Unknown command: {args.command}")
            return 1

    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        return 130
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    # Import json here to avoid circular imports
    import json
    sys.exit(main())