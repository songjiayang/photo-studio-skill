"""
Movie Character Skill - Python API

This module provides a Python API for the movie character photo generation skill.
It can be imported and used directly by agents or other Python code.

Example usage:
    from scripts import Config, config, ImageGenerator

    # Get characters
    characters = config.get_characters()

    # Generate photos
    image_gen = ImageGenerator(config, interaction_manager)
    results = image_gen.generate_all_images(user_photo, characters)
"""

from .config import Config, config
from .image_generator import ImageGenerator
from .interaction import InteractionManager

__all__ = ['Config', 'config', 'ImageGenerator', 'InteractionManager']
