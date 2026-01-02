---
name: photo-studio-skill
description: Generate portrait and group photos using Seedream 4.5 AI. Supports celebrity photos, personal portraits, couple photos, and family portraits with customizable poses, templates, and backgrounds. Use when users want to create professional AI-enhanced photos.
license: MIT
compatibility: Requires Python 3.8+, ByteDance ARK API key for image generation, internet access
allowed-tools: Bash(python:*) Read Write
metadata:
  author: AI Assistant
  version: "2.1"
  entrypoint: scripts/main.py
---

# Photo Studio

This skill generates professional portrait and group photos using ByteDance's Seedream 4.5 AI model. It supports multiple photo generation scenarios.

## Overview

The Photo Studio skill takes user photos and generates professional AI-enhanced portraits and group photos across multiple scenarios:
- **Celebrity Photos**: Take photos with movie characters
- **Personal Portraits**: Professional headshots in various styles
- **Couple Portraits**: Romantic or friendly couple photos
- **Family Portraits**: Professional family photos (3-6 people)

## When to Use This Skill

- User wants professional portrait photography
- User wants couple or family photos with consistent style
- User wants photos with movie characters
- User needs AI-enhanced portraits with specific styles
- User wants to create social media content with professional quality

## Prerequisites

### Software Dependencies
- Python 3.8+
- Python packages: `requests`, `pillow`, `opencv-python`, `numpy` (see `requirements.txt`)

## Quick Start

```bash
# Run the generation wizard
python scripts/main.py generate --photo path/to/your/photo.jpg
```

## Complete Workflow

### Step 1: Select Scenario
Choose from available scenarios:
1. **明星合影** (Celebrity) - Photos with movie characters
2. **个人写真** (Portrait) - Professional personal portraits
3. **双人合影** (Couple) - Couple or friend photos
4. **全家合影** (Family) - Family group photos (3-6 people)

### Step 2: Collect Inputs
Based on selected scenario, provide:
- **Photos**: Upload 1-6 photos as required
- **Styles/Characters/Templates**: Choose from available options
- **Background** (for couple/family): Select custom background (optional)
- **Count**: Specify number of images to generate

**Available Options:**
- **Portrait**: 15+ styles (Professional, Artistic, Lifestyle, Vintage, etc.)
- **Couple**: 12 poses + 6 backgrounds (Side by side, Hugging, etc.)
- **Family**: 8 templates + 6 backgrounds (Classic, Casual, Outdoor, etc.)
- **Celebrity**: 18+ characters (Iron Man, Wonder Woman, Spider-Man, etc.)

### Step 3: Generate Images
The skill will:
1. Preprocess user photos (resize to max 2048x2048)
2. Call Seedream 4.5 API with optimized prompts
3. Save generated images to `output/images/`

### Step 4: Review and Save
You can:
- View all generated images
- Reorder images
- Regenerate specific images if needed
- Confirm and save photos

## Agent Integration (Recommended: CLI)

Agents should use the CLI for integration. The skill supports a **non-interactive mode** for fully automated workflows.

### Basic Integration Pattern

```bash
# Celebrity photos with specific characters
python scripts/main.py generate --photo "$USER_PHOTO" \
    --scenario celebrity \
    --characters "Iron Man,Wonder Woman" \
    --non-interactive

# Personal portraits with specific style
python scripts/main.py generate --photo "$USER_PHOTO" \
    --scenario portrait \
    --style "职业商务照" \
    --non-interactive

# Couple photos with pose and background
python scripts/main.py generate --photos "$PHOTO1,$PHOTO2" \
    --scenario couple \
    --pose "手牵手面向镜头" \
    --background "海滩日落" \
    --non-interactive

# Family photos with template and background
python scripts/main.py generate --photos "$PHOTO1,$PHOTO2,$PHOTO3" \
    --scenario family \
    --template "温馨家庭聚会" \
    --background "户外公园" \
    --non-interactive
```

### List Available Options

```bash
# List all scenarios
python scripts/main.py list-scenarios

# List styles for portrait scenario
python scripts/main.py list-styles --scenario portrait

# List styles for couple scenario
python scripts/main.py list-styles --scenario couple

# List styles for family scenario
python scripts/main.py list-styles --scenario family

# List couple poses (12 options)
python scripts/main.py list-poses

# List family templates (8 options)
python scripts/main.py list-templates

# List backgrounds for couple scenario
python scripts/main.py list-backgrounds --scenario couple

# List backgrounds for family scenario
python scripts/main.py list-backgrounds --scenario family

# List available characters
python scripts/main.py list-characters
```

### Environment Setup

Ensure necessary dependencies are installed before running commands. The skill will check for required API credentials automatically.

Run generation with automatic confirmation:

```bash
python scripts/main.py generate --photo photo.jpg --non-interactive
```

### Output Parsing

Generated images are saved to `output/images/` directory. Agents can:
1. Check `output/images/` for generated files
2. Use `config --show` to view current settings
3. Check `logs/` directory for error details

## Command Reference

### Generate Command

```bash
python scripts/main.py generate [options]
```

**For Celebrity Scenario:**
- `--photo, -p` - Path to user photo
- `--characters, -ch` - Comma-separated character names
- `--count, -c` - Number of images (default: 5)

**For Portrait Scenario:**
- `--photo, -p` - Path to user photo
- `--style` - Specific style name
- `--count, -c` - Number of images

**For Couple Scenario:**
- `--photos` - Comma-separated photo paths (2 photos)
- `--pose` - Specific pose name (12 options available, default: 并肩站立)
- `--background` - Background name (6 options available, default: pose's built-in scene)
- `--count, -c` - Number of images

**For Family Scenario:**
- `--photos` - Comma-separated photo paths (1-6 photos)
- `--template` - Specific template name (8 options available, default: 经典全家福)
- `--background` - Background name (6 options available, default: template's built-in scene)
- `--count, -c` - Number of images

**Common Options:**
- `--scenario, -s` - Scenario type (celebrity, portrait, couple, family)
- `--skip-review` - Skip image review step
- `--non-interactive, -ni` - Run in non-interactive mode

### List Commands

```bash
# List available scenarios
python scripts/main.py list-scenarios

# List styles for a scenario
python scripts/main.py list-styles --scenario <scenario_id>

# List couple poses (12 options)
python scripts/main.py list-poses

# List family templates (8 options)
python scripts/main.py list-templates

# List backgrounds for a scenario (couple or family)
python scripts/main.py list-backgrounds --scenario <scenario_id>

# List available characters
python scripts/main.py list-characters
```

### Utility Commands

```bash
# Add custom character
python scripts/main.py add-character "Character Name" "Description prompt" --scene "Scene description"

# View configuration
python scripts/main.py config --show

# Update configuration
python scripts/main.py config --set generation.default_image_count=3

# Clean temporary files
python scripts/main.py cleanup
```

## File Structure

```
photo-studio-skill/
 ├── SKILL.md              # This file
 ├── scripts/              # Python scripts
 │   ├── __init__.py       # Python API exports
 │   ├── main.py           # CLI entry point
 │   ├── config.py         # Configuration management
 │   ├── interaction.py    # User interaction
 │   └── image_generator.py # Seedream 4.5 integration
 ├── data/                 # Scenario templates
 │   ├── scenarios.json         # Scenario configurations
 │   ├── default_characters.json # Movie characters (18+ options for celebrity scenario)
 │   ├── portrait_styles.json   # Portrait styles (15+ options with attire descriptions)
 │   ├── couple_poses.json    # Couple poses (12 options with attire + 6 backgrounds)
 │   └── family_templates.json # Family templates (8 options with attire + 6 backgrounds)
 ├── references/           # Additional documentation
 │   └── API.md            # Python API reference
 ├── temp/                 # Temporary files (auto-generated)
 ├── output/               # Generated content
 │   └── images/          # AI-generated photos
 └── logs/                 # Log files (auto-generated)
```

**Data Files Content:**
- `couple_poses.json`: 12 poses (并肩站立, 面对面, etc.) with attire + 6 backgrounds (城市街头, 公园自然, 海滩日落, etc.)
- `family_templates.json`: 8 templates (经典全家福, 温馨家庭聚会, etc.) with attire + 6 backgrounds (正式客厅, 温馨家庭内景, 专业摄影棚, etc.)

## Configuration

### Configuration File
Settings can be modified in `config.json`:
- `generation.image_width` - Image width (default: 2048)
- `generation.image_height` - Image height (default: 2048)
- `generation.default_image_count` - Default number of images (default: 5)
- `scenarios.default_scenario` - Default scenario (default: celebrity)
### API Credentials

The skill requires ByteDance ARK API access. Ensure API credentials are properly configured in the environment before running.

### Mock Mode for Testing

To enable mock mode for testing without API calls:

```bash
# Enable mock mode via environment variable
export MOCK_API=true

# Or configure in config.json
{
  "mock": {
    "enabled": true,
    "use_sample_images": false,
    "sample_images_dir": "mock_samples"
  }
}
```

**Benefits of Mock Mode:**
- No API costs (saves money)
- Fast testing (500ms instead of 10-20 seconds per image)
- No network dependency
- Consistent test results
- Can test all scenarios quickly

## Technical Details

### Image Generation (Seedream 4.5)
- Uses image-to-image generation with user photo(s) as reference
- Supports single or multiple reference images (up to 14)
- Resolution: 2048x2048 (configurable)
- Negative prompts exclude blurry faces, unnatural poses, watermarks
- Model: `doubao-seedream-4.5-251128`

### Multi-Photo Scenarios
- Couple and family scenarios use multi-reference image fusion
- API supports up to 14 reference photos
- Person count controlled through prompt descriptions

## Customization Options

### Couple Photos Customization

**12 Available Poses:**
1. 并肩站立 - Side by side
2. 面对面 - Facing each other
3. 揽肩拥抱 - Arm around shoulder
4. 背对背 - Back to back
5. 并肩而坐 - Seated together
6. 携手同行 - Walking together
7. 手牵手面向镜头 - Holding hands facing camera
8. 背背抱 - Piggyback
9. 拥抱姿势 - Hugging
10. 额头相抵 - Forehead touch
11. 坐地相拥 - Sitting on ground
12. 舞动时刻 - Dancing together

**6 Available Backgrounds:**
1. 城市街头 - Urban street
2. 公园自然 - Park nature
3. 海滩日落 - Beach sunset
4. 咖啡厅内 - Cafe interior
5. 屋顶天台 - Rooftop view
6. 摄影棚简约 - Simple studio

**Use:**
```bash
python scripts/main.py list-poses
python scripts/main.py list-backgrounds --scenario couple
```

### Family Photos Customization

**8 Available Templates:**
1. 经典全家福 - Classic family portrait
2. 温馨家庭聚会 - Casual family gathering
3. 户外家庭照 - Outdoor family photo
4. 多代同堂 - Multigenerational family
5. 活泼家庭照 - Playful family photo
6. 坐姿全家福 - Seated family portrait
7. 专业摄影棚全家福 - Professional studio family
8. 节日家庭照 - Holiday family photo

**6 Available Backgrounds:**
1. 正式客厅 - Formal living room
2. 温馨家庭内景 - Cozy home interior
3. 专业摄影棚 - Professional studio
4. 户外公园 - Outdoor park
5. 海滩风景 - Beach seaside
6. 花园花卉 - Garden floral

**Use:**
```bash
python scripts/main.py list-templates
python scripts/main.py list-backgrounds --scenario family
```

**Note:** All poses/templates include detailed attire descriptions to ensure generated images don't use original photo clothing.

## Examples

### Celebrity Photos Example

```bash
# Generate with default characters
python scripts/main.py generate --photo user.jpg --scenario celebrity

# Generate with specific characters
python scripts/main.py generate --photo user.jpg --scenario celebrity \
    --characters "Iron Man,Wonder Woman,Spider-Man"
```

### Portrait Example

```bash
# Generate portraits with all styles
python scripts/main.py generate --photo user.jpg --scenario portrait

# Generate with specific style
python scripts/main.py generate --photo user.jpg --scenario portrait --style "职业商务照"
```

### Couple Photos Example

```bash
# Generate couple photos with default pose
python scripts/main.py generate --photos "photo1.jpg,photo2.jpg" --scenario couple

# Generate couple photos with specific pose
python scripts/main.py generate --photos "photo1.jpg,photo2.jpg" --scenario couple \
    --pose "手牵手面向镜头"

# Generate couple photos with custom background
python scripts/main.py generate --photos "photo1.jpg,photo2.jpg" --scenario couple \
    --pose "手牵手面向镜头" --background "海滩日落"
```

### Family Photos Example

```bash
# Generate family photos with default template
python scripts/main.py generate --photos "photo1.jpg,photo2.jpg,photo3.jpg" --scenario family

# Generate family photos with specific template
python scripts/main.py generate --photos "photo1.jpg,photo2.jpg,photo3.jpg" --scenario family \
    --template "温馨家庭聚会"

# Generate family photos with custom background
python scripts/main.py generate --photos "photo1.jpg,photo2.jpg,photo3.jpg" --scenario family \
    --template "温馨家庭聚会" --background "户外公园"
```

### Non-Interactive Example (For Agent Integration)

```bash
# Fully automated generation
python scripts/main.py generate --photo user.jpg --scenario portrait \
    --style "职业商务照" --count 3 --non-interactive

# Couple photos with pose and background
python scripts/main.py generate --photos "photo1.jpg,photo2.jpg" --scenario couple \
    --pose "手牵手面向镜头" --background "海滩日落" --non-interactive

# Family photos with template and background
python scripts/main.py generate --photos "photo1.jpg,photo2.jpg,photo3.jpg" --scenario family \
    --template "温馨家庭聚会" --background "户外公园" --non-interactive
```

## Troubleshooting

### Common Issues

**Image Generation Fails**
- Check internet connection
- Ensure API credentials are properly configured
- Ensure photos are clear and well-lit (≥1024×1024 recommended)
- For multi-photo scenarios, ensure all photos are valid
- Check `logs/` directory for detailed error messages

### Logs
Check `logs/` directory for detailed error information.

## Performance Notes
- Image generation: ~10-20 seconds per image
- Total time for 5 images: ~1-2 minutes
- Storage: 500MB-1GB temporary space during processing

## Limitations
- Requires stable internet connection for API calls
- API rate limits may apply
- Large photos may require more processing time
- Person count in group photos is controlled via prompt (not precise)

## Support
For issues, check logs in `logs/` directory or review error messages in console.
