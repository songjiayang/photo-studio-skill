#!/usr/bin/env python3
"""
Scenario handlers for main.py
Extracted to reduce command_generate function complexity
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def validate_photo_path(photo_path: Optional[str]) -> Tuple[bool, str]:
    """Validate single photo path exists"""
    if not photo_path or not Path(photo_path).exists():
        return False, f"❌ Photo not found: {photo_path}"
    return True, ""


def validate_photo_paths(photos_arg: Optional[str], min_count: int = 1, max_count: int = 14) -> Tuple[bool, str, List[str]]:
    """Validate and parse comma-separated photo paths"""
    if not photos_arg:
        return False, "❌ --photos parameter is required.", []
    
    photo_paths = [p.strip() for p in photos_arg.split(',')]
    if len(photo_paths) < min_count:
        return False, f"❌ At least {min_count} photo(s) required.", []
    if len(photo_paths) > max_count:
        return False, f"⚠️ Maximum {max_count} photos allowed, using first {max_count}", photo_paths[:max_count]

    for p in photo_paths:
        if not Path(p).exists():
            return False, f"❌ Photo not found: {p}", []
    
    return True, "", photo_paths


def find_item_by_name_or_id(items: List[Dict], name: str, item_type: str = "item") -> Tuple[Optional[Dict], str]:
    """Find item by name or id in list"""
    for item in items:
        if item.get('name') == name or item.get('id') == name:
            return item, ""
    return None, f"❌ {item_type.capitalize()} '{name}' not found."


def get_count_with_default(args, default: int = 1) -> int:
    """Get count from args with fallback to default"""
    return getattr(args, 'count', default) or default


def handle_portrait_scenario(args, config, image_gen) -> Tuple[bool, List[str]]:
    """Handle portrait scenario"""
    photo_path = getattr(args, 'photo', None)
    valid, error = validate_photo_path(photo_path)
    if not valid:
        print(error)
        return False, []

    style_name = getattr(args, 'style', None)
    if not style_name:
        print("❌ Style is required for portrait scenario. Use --style parameter.")
        print("Available styles:")
        styles = config.get_scenario_data('portrait')
        if styles:
            for s in styles[:5]:
                print(f"  - {s['name']}")
        return False, []

    styles = config.get_scenario_data('portrait')
    if not styles:
        print("❌ Failed to load portrait styles.")
        return False, []

    selected_style, error = find_item_by_name_or_id(styles, style_name, "style")
    if not selected_style:
        print(error)
        print("Available styles:")
        for s in styles[:5]:
            print(f"  - {s['name']}")
        return False, []

    count = get_count_with_default(args, 1)
    result = image_gen.generate_portrait_images(photo_path, [selected_style], count)
    return True, result if result else []


def handle_couple_scenario(args, config, image_gen) -> Tuple[bool, List[str]]:
    """Handle couple scenario"""
    photos_arg = getattr(args, 'photos', None)
    valid, error, photo_paths = validate_photo_paths(photos_arg, min_count=2)
    if not valid:
        print(error)
        return False, []

    count = get_count_with_default(args, 1)

    couple_poses = config.get_scenario_data('couple')
    if not couple_poses:
        print("❌ Failed to load couple poses.")
        return False, []

    pose_name = getattr(args, 'pose', None)
    if pose_name:
        selected_pose, error = find_item_by_name_or_id(couple_poses, pose_name, "pose")
        if not selected_pose:
            print(error)
            print("Available poses:")
            for p in couple_poses[:5]:
                print(f"  - {p['name']}")
            return False, []
    else:
        selected_pose = couple_poses[0]

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
                return False, []

    result = image_gen.generate_couple_images(photo_paths, selected_pose, count, background)
    return True, result if result else []


def handle_family_scenario(args, config, image_gen) -> Tuple[bool, List[str]]:
    """Handle family scenario"""
    photos_arg = getattr(args, 'photos', None)
    valid, error, photo_paths = validate_photo_paths(photos_arg, min_count=1, max_count=6)
    if not valid:
        print(error)
        return False, []

    count = get_count_with_default(args, 1)

    family_templates = config.get_scenario_data('family')
    if not family_templates:
        print("❌ Failed to load family templates.")
        return False, []

    template_name = getattr(args, 'template', None)
    if template_name:
        selected_template, error = find_item_by_name_or_id(family_templates, template_name, "template")
        if not selected_template:
            print(error)
            print("Available templates:")
            for t in family_templates[:5]:
                print(f"  - {t['name']}")
            return False, []
    else:
        selected_template = family_templates[0]

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
                return False, []

    result = image_gen.generate_family_images(
        photo_paths, len(photo_paths), count, selected_template, background
    )
    return True, result if result else []


def handle_free_scenario(args, config, image_gen) -> Tuple[bool, List[str]]:
    """Handle free mode scenario"""
    photos_arg = getattr(args, 'photos', None)
    photo_paths = None

    if photos_arg:
        valid, error, photo_paths = validate_photo_paths(photos_arg, min_count=1, max_count=14)
        if not valid:
            print(error)
            return False, []
    elif hasattr(args, 'photo') and args.photo:
        valid, error = validate_photo_path(args.photo)
        if not valid:
            print(error)
            return False, []
        photo_paths = [args.photo]
    else:
        print("❌ --photos or --photo parameter is required for free mode.")
        return False, []

    custom_prompt = getattr(args, 'prompt', None)
    if not custom_prompt:
        print("❌ --prompt parameter is required for free mode.")
        return False, []

    count = get_count_with_default(args, 1)
    negative_prompt = getattr(args, 'negative_prompt', "")

    result = image_gen.generate_free_mode_images(photo_paths, custom_prompt, count, negative_prompt)
    return True, result if result else []


def handle_edit_scenario(args, config, image_gen) -> Tuple[bool, List[str]]:
    """Handle edit scenario"""
    photo_path = getattr(args, 'photo', None)
    valid, error = validate_photo_path(photo_path)
    if not valid:
        print(error)
        return False, []

    return handle_template_based_common(args, config, image_gen, 'edit', photo_path, None)


def handle_fusion_scenario(args, config, image_gen) -> Tuple[bool, List[str]]:
    """Handle fusion scenario"""
    photos_arg = getattr(args, 'photos', None)
    if not photos_arg:
        print("❌ --photos parameter is required for fusion scenario.")
        return False, []
    
    valid, error, photo_paths = validate_photo_paths(photos_arg, min_count=1, max_count=6)
    if not valid:
        print(error)
        return False, []

    return handle_template_based_common(args, config, image_gen, 'fusion', None, photo_paths)


def handle_series_scenario(args, config, image_gen) -> Tuple[bool, List[str]]:
    """Handle series scenario"""
    photo_path = getattr(args, 'photo', None)
    valid, error = validate_photo_path(photo_path)
    if not valid:
        print(error)
        return False, []

    return handle_template_based_common(args, config, image_gen, 'series', photo_path, None)


def handle_poster_scenario(args, config, image_gen) -> Tuple[bool, List[str]]:
    """Handle poster scenario"""
    photo_path = getattr(args, 'photo', None)
    if photo_path:
        valid, error = validate_photo_path(photo_path)
        if not valid:
            print(error)
            return False, []

    return handle_template_based_common(args, config, image_gen, 'poster', photo_path, None)


def handle_template_based_common(args, config, image_gen, scenario_id: str, 
                                photo_path: Optional[str], photo_paths: Optional[List[str]]) -> Tuple[bool, List[str]]:
    """Common handler for template-based scenarios (edit, fusion, series, poster)"""
    templates = config.get_scenario_data(scenario_id)
    if not templates:
        print(f"❌ Failed to load {scenario_id} templates")
        return False, []

    template_name = getattr(args, 'template', None)
    if template_name:
        selected_template, error = find_item_by_name_or_id(templates, template_name, "template")
        if not selected_template:
            print(error)
            print("Available templates:")
            for t in templates[:5]:
                print(f"  - {t['name']}")
            return False, []
    else:
        selected_template = templates[0] if templates else None

    if not selected_template:
        print("❌ No templates available")
        return False, []

    field_values = {}
    template_fields = selected_template.get('fields', [])

    for field in template_fields:
        field_name = field['name']
        
        value = None
        
        if hasattr(args, 'template_fields') and field_name in args.template_fields:
            value = args.template_fields[field_name]
        elif hasattr(args, field_name):
            value = getattr(args, field_name)
        
        if value is not None:
            if field['type'] == 'multiselect' and isinstance(value, str):
                value = value.replace(',', ', ')
            field_values[field_name] = value
        elif field.get('default'):
            field_values[field_name] = field['default']
        elif not field.get('required', False):
            field_values[field_name] = ""

    if scenario_id == 'edit':
        result = image_gen.generate_edit_images(photo_path, selected_template, field_values)
    elif scenario_id == 'fusion':
        result = image_gen.generate_fusion_images(photo_paths, selected_template, field_values)
    elif scenario_id == 'series':
        result = image_gen.generate_series_images(photo_path, selected_template, field_values)
    elif scenario_id == 'poster':
        result = image_gen.generate_poster_images(photo_path, selected_template, field_values)
    else:
        return False, []

    return True, result if result else []


def handle_celebrity_scenario(args, config, image_gen) -> Tuple[bool, List[str]]:
    """Handle celebrity scenario"""
    photo_path = getattr(args, 'photo', None)
    valid, error = validate_photo_path(photo_path)
    if not valid:
        print(error)
        return False, []

    all_chars = config.get_characters()

    if hasattr(args, 'characters') and args.characters:
        selected_chars = []
        char_names = [c.strip() for c in args.characters.split(',')]
        for char in all_chars:
            if char['name'] in char_names:
                selected_chars.append(char)
        characters_to_generate = selected_chars
    else:
        default_count = config.config["generation"]["default_image_count"]
        count = getattr(args, 'count', default_count)
        characters_to_generate = all_chars[:count]

    generated_images = []
    for i, character in enumerate(characters_to_generate):
        print(f"\nGenerating image {i+1}/{len(characters_to_generate)}: {character['name']}")

        image_path = image_gen.generate_single_image(photo_path, character, i)

        if image_path:
            generated_images.append(image_path)

    return True, generated_images
