# API Reference

Detailed documentation for the movie-character-skill Python API.

## Config Class

Configuration management for the skill.

### Initialization

```python
from scripts import Config

# Auto-detect skill directory
config = Config()

# Explicit skill directory
config = Config(skill_dir="/path/to/movie-character-skill")
```

### Methods

#### get_characters(use_defaults=True)

Get list of available characters.

```python
# Get all characters (defaults + custom)
all_chars = config.get_characters(use_defaults=True)

# Get only custom characters
custom_chars = config.get_characters(use_defaults=False)
```

**Returns:** List of character dictionaries with keys: `name`, `prompt`, `scene`

#### add_character(name, prompt, scene=None)

Add a custom character.

```python
config.add_character(
    name="Batman",
    prompt="Bruce Wayne as Batman in dark knight suit",
    scene="Gotham city at night"
)
```

**Returns:** The added character dictionary

#### get_temp_dir()

Get absolute path to temporary directory.

```python
temp_path = config.get_temp_dir()
# Returns: /path/to/movie-character-skill/temp
```

#### get_output_dir()

Get absolute path to output directory.

```python
output_path = config.get_output_dir()
# Returns: /path/to/movie-character-skill/output
```

#### get_logs_dir()

Get absolute path to logs directory.

```python
logs_path = config.get_logs_dir()
# Returns: /path/to/movie-character-skill/logs
```

#### update_setting(section, key, value)

Update a configuration setting.

```python
config.update_setting("generation", "default_image_count", 3)
```

**Returns:** `True` if updated successfully, `False` otherwise

### Properties

| Property | Description |
|----------|-------------|
| `skill_dir` | Path to skill directory |
| `temp_dir` | Alias for `get_temp_dir()` |
| `image_dir` | Path to output images directory |
| `video_dir` | Path to output videos directory |
| `default_characters` | List of default characters |
| `config` | Full configuration dictionary |

---

## ImageGenerator Class

Handles image generation via Seedream 4.5 API.

### Initialization

```python
from scripts import ImageGenerator, InteractionManager

# Get config instance
from scripts import config

# Create interaction manager (optional, for logging)
interaction = InteractionManager(config)

# Create image generator
image_gen = ImageGenerator(config, interaction)
```

### Methods

#### generate_single_image(user_photo, character, index=1)

Generate a single image with one character.

```python
character = {
    "name": "Iron Man",
    "prompt": "Tony Stark as Iron Man in Avengers suit",
    "scene": "movie film set"
}

result = image_gen.generate_single_image(
    user_photo="/path/to/photo.jpg",
    character=character,
    index=1
)

if result:
    print(f"Generated: {result}")
```

**Returns:** Path to generated image, or `None` on failure

#### generate_all_images(user_photo, characters, skip_review=False, max_workers=3)

Generate images for multiple characters.

```python
characters = config.get_characters()[:5]  # First 5 characters

results = image_gen.generate_all_images(
    user_photo="/path/to/photo.jpg",
    characters=characters,
    skip_review=True,  # Skip interactive review
    max_workers=3      # Parallel API calls
)

print(f"Successfully generated: {len(results)} images")
for img_path in results:
    print(f"  - {img_path}")
```

**Parameters:**
- `user_photo`: Path to user photo
- `characters`: List of character dictionaries
- `skip_review`: Skip interactive review step
- `max_workers`: Maximum parallel API calls

**Returns:** List of successful image paths

#### cleanup_temp_files()

Clean up temporary files.

```python
image_gen.cleanup_temp_files()
```

---

## InteractionManager Class

Handles user interaction during the generation process.

### Initialization

```python
from scripts import InteractionManager, config

interaction = InteractionManager(config)
```

### Methods

#### collect_inputs()

Collect user inputs interactively.

```python
inputs = interaction.collect_inputs()
# Returns: {'user_photo': '...', 'characters': [...], 'count': 5}
```

**Note:** This method requires user input via stdin.

#### confirm_generation(generated_images)

Confirm generation with user.

```python
confirmed = interaction.confirm_generation(generated_images)
if confirmed:
    print("Generation confirmed!")
```

**Returns:** `True` if confirmed, `False` otherwise

---

## Character Format

Characters are stored with the following structure:

```python
character = {
    "name": "Character Name",
    "prompt": "Detailed prompt for the AI to generate the character",
    "scene": "Background scene description"
}
```

### Example Character

```python
{
    "name": "Iron Man",
    "prompt": "Tony Stark as Iron Man in character on Avengers film set, taking break from shooting, high-tech suit",
    "scene": "movie film set with crew members, cameras, lighting equipment, behind-the-scenes atmosphere"
}
```

---

## Configuration File

The `config.json` file controls skill behavior:

```json
{
  "api": {
    "image_generation_url": "https://ark.cn-beijing.volces.com/api/v3/images/generations"
  },
  "paths": {
    "temp_dir": "temp",
    "output_dir": "output",
    "logs_dir": "logs"
  },
  "generation": {
    "default_image_count": 5,
    "image_width": 1024,
    "image_height": 1024,
    "image_model": "doubao-seedream-4.5"
  },
  "characters": []
}
```

### Environment Variables

- `ARK_API_KEY`: ByteDance ARK API key for image generation

---

## Error Handling

### API Key Errors

```python
from scripts import config

api_key = config.get_api_key()
if not api_key:
    raise ValueError("ARK_API_KEY environment variable not set")
```

### Image Generation Errors

```python
from scripts import ImageGenerator

image_gen = ImageGenerator(config, interaction)

try:
    result = image_gen.generate_single_image(photo, character)
    if result is None:
        print("Generation failed - check logs for details")
except Exception as e:
    print(f"Error: {e}")
```
