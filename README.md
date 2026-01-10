# Photo Studio

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Compatible-green.svg)

A powerful AI photo generation skill for Claude Code/Agent Skills ecosystem that generates professional portrait and group photos using ByteDance's Seedream 4.5 AI.

## Features

 - **Multiple Photo Scenarios**: Support for 9 generation types
    - 明星合影 (Celebrity Photos) - Take photos with movie characters
    - 个人写真 (Personal Portraits) - Professional headshots with standard poses (15+ styles)
    - 双人合影 (Couple Photos) - Romantic or friendly couple portraits with gender detection (12 poses, 6 backgrounds)
    - 全家合影 (Family Photos) - Professional family group photos with person count control (3-6 people, 8 templates, 6 backgrounds)
    - 图像编辑 (Image Edit) - Edit images (clothing, material, background, style, enhance)
    - 图像融合 (Image Fusion) - Merge multiple photos (outfit, person-scenery, brand, composite)
    - 系列创作 (Series Creation) - Create related image series (seasons, brand kit, character states, story)
    - 海报设计 (Poster Design) - Design posters (movie, event, product)
    - 自由模式 (Free Mode) - Custom prompt generation with 1-14 reference photos
- **AI Image Generation**: Use ByteDance's Seedream 4.5 for high-quality image-to-image transformations
- **Multi-Photo Support**: Process up to 6 reference photos for group scenarios with unique preprocessing
- **Non-interactive Mode**: Full automation for agent integration via CLI
- **Extensible Configuration**: Easy to add custom styles, poses, and templates
- **Smart Preprocessing**: Auto-resize photos to max 2048x2048 with unique filenames
- **Gender Detection**: Automatic gender detection from input photos for couple and family scenarios
- **Standard Poses**: All portrait styles include professional standard pose descriptions

## Architecture

```
photo-studio-skill/
├── SKILL.md              # Skill documentation with YAML frontmatter
├── README.md             # This file
├── config.json           # Configuration settings
├── requirements.txt      # Python dependencies
├── LICENSE               # MIT License
├── scripts/              # Core Python scripts
│   ├── main.py           # CLI entry point with subcommands
│   ├── config.py         # Configuration management
│   ├── interaction.py    # User interaction handling
│   └── image_generator.py # Seedream 4.5 API integration
├── data/                 # Scenario templates
│   ├── scenarios.json         # Scenario configurations
│   ├── portrait_styles.json   # Portrait styles (15+ options)
│   ├── couple_poses.json    # Couple poses (12 options)
│   ├── family_templates.json # Family templates (8 options)
│   └── default_characters.json # Movie characters (for celebrity scenario)
├── references/           # Additional documentation
│   └── API.md            # Python API reference
├── temp/                 # Temporary files (auto-generated)
├── output/               # Generated content
│   └── images/           # AI-generated photos
└── logs/                 # Log files (auto-generated)
```

## Quick Start

### Prerequisites

- **Python 3.8+** with pip
- **ByteDance ARK API Key**: Get from [Volcano Engine Console](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey)

### Installation

```bash
cd photo-studio-skill
pip install -r requirements.txt
```

### Claude Skill Installation

To install this skill for use with Claude Code, copy the `photo-studio-skill` directory to Claude's skills folder:

```bash
# Copy the skill to Claude Code's skills directory
cp -r photo-studio-skill ~/.claude/skills/photo-studio-skill
```

After installation, the skill will be available in Claude Code as `photo-studio-skill`.

### Configure API Credentials

```bash
# Set API key for image generation
# API key environment variable name: ARK_API_KEY
# API will return error if key is not properly configured
```

### Run the Skill

```bash
# Interactive generation wizard
python scripts/main.py generate --photo path/to/your/photo.jpg
```

## Usage

### List Available Options

```bash
# List all scenarios
python scripts/main.py list-scenarios

# List styles for portrait scenario (15 options)
python scripts/main.py list-styles --scenario portrait

# List poses for couple scenario (12 options)
python scripts/main.py list-poses

# List templates for family scenario (8 options)
python scripts/main.py list-templates

# List backgrounds for couple scenario (6 options)
python scripts/main.py list-backgrounds --scenario couple

# List backgrounds for family scenario (6 options)
python scripts/main.py list-backgrounds --scenario family

# List available characters
python scripts/main.py list-characters
```

### Generate Photos

**Celebrity Photos:**
```bash
# Generate with movie characters
python scripts/main.py generate --photo photo.jpg --scenario celebrity

# Generate with specific characters
python scripts/main.py generate --photo photo.jpg --scenario celebrity \
    --characters "Iron Man,Wonder Woman,Spider-Man"
```

**Personal Portraits:**
```bash
# Generate portraits with all available styles
python scripts/main.py generate --photo photo.jpg --scenario portrait

# Generate with specific style
python scripts/main.py generate --photo photo.jpg --scenario portrait --style "职业商务照"

# Generate multiple images with the same style
python scripts/main.py generate --photo photo.jpg --scenario portrait \
    --style "时尚杂志" --count 3
```

**Couple Photos:**
```bash
# Generate couple photos (requires 2 photos)
python scripts/main.py generate --photos "photo1.jpg,photo2.jpg" --scenario couple

# Generate with specific pose
python scripts/main.py generate --photos "photo1.jpg,photo2.jpg" --scenario couple \
    --pose "手牵手面向镜头"

# Generate with custom background
python scripts/main.py generate --photos "photo1.jpg,photo2.jpg" --scenario couple \
    --pose "并肩站立" --background "海滩日落"

# Generate with multiple images
python scripts/main.py generate --photos "photo1.jpg,photo2.jpg" --scenario couple \
    --pose "揽肩拥抱" --count 2
```

**Family Photos:**
```bash
# Generate family photos (1-6 photos)
python scripts/main.py generate --photos "photo1.jpg,photo2.jpg,photo3.jpg" --scenario family

# Generate with specific template
python scripts/main.py generate --photos "photo1.jpg,photo2.jpg,photo3.jpg" --scenario family \
    --template "温馨家庭聚会"

# Generate with custom background
python scripts/main.py generate --photos "photo1.jpg,photo2.jpg,photo3.jpg" --scenario family \
    --template "经典全家福" --background "正式客厅"

# Generate 4-person family photo
python scripts/main.py generate --photos "photo1.jpg,photo2.jpg,photo3.jpg,photo4.jpg" \
    --scenario family --template "多代同堂"

# Generate multiple family photos
python scripts/main.py generate --photos "photo1.jpg,photo2.jpg,photo3.jpg" --scenario family \
    --template "户外家庭照" --count 2
```

### Non-interactive Mode

```bash
# Non-interactive mode (for agents)
python scripts/main.py generate --photo photo.jpg --scenario portrait --non-interactive

# Generate multiple images
python scripts/main.py generate --photo photo.jpg --count 3 --skip-review
```

### Configuration Management

```bash
# View configuration
python scripts/main.py config --show

# Update settings
python scripts/main.py config --set generation.default_image_count=3

# Clean temporary files
python scripts/main.py cleanup
```

## Scenarios

### 1. 明星合影 (Celebrity Photos)

Take photos with movie characters from popular films.

**Features:**
- 18+ pre-defined characters (Iron Man, Wonder Woman, Spider-Man, etc.)
- 3 background styles (Movie set, Premiere, Fan meet-and-greet)
- Character selection from list or custom input

**Example:**
```bash
python scripts/main.py generate --photo user.jpg --scenario celebrity \
    --characters "Iron Man,Wonder Woman,Spider-Man"
```

### 2. 个人写真 (Personal Portraits)

Generate professional personal portraits in various styles.

**Features:**
- 15+ portrait styles including:
  - Professional Headshot (职业商务照)
  - Artistic Portrait (艺术肖像)
  - Lifestyle (生活写真)
  - Vintage Style (复古风格)
  - Fashion Editorial (时尚杂志)
  - Black & White (黑白经典)
  - And more...
- Multiple style selection
- High-quality studio lighting simulation

**Example:**
```bash
python scripts/main.py generate --photo user.jpg --scenario portrait --style "职业商务照"
```

### 3. 双人合影 (Couple Photos)

Generate romantic or friendly couple portraits.

**Features:**
- Support for 2 photos (couple or friends)
- 12+ pose options (Side by side, Hugging, Walking together, etc.)
- 6 background options (Urban street, Park, Beach, Cafe, etc.)
- Automatic gender detection from input photos
- Person 1 and Person 2 positioning based on input order
- Couple type selection (Romantic vs. Friends)
- Standard attire descriptions (no gender assumptions)

**Example:**
```bash
python scripts/main.py generate --photos "photo1.jpg,photo2.jpg" --scenario couple
```

### 4. 全家合影 (Family Photos)

Generate professional family group photos.

**Features:**
- Support for 1-6 family photos
- 8+ family templates (Classic, Casual, Outdoor, etc.)
- 4 arrangement options (Standing, Seated, Front/Back, Circular)
- 6 background options
- Family size specification (3-6 people)
- Automatic gender detection from each input photo
- Exact person count control (matches input photos)
- Person 1, 2, 3... positioning based on input order
- Standard family attire descriptions

**Example:**
```bash
python scripts/main.py generate --photos "photo1.jpg,photo2.jpg,photo3.jpg" --scenario family
```

### 5. 自由模式 (Free Mode)

Generate images with custom prompts and full control.

**Features:**
- Support for 1-14 reference photos
- Completely custom prompt input
- Optional negative prompt
- No template restrictions
- Full creative control

**Example:**
```bash
# Single photo with custom prompt
python scripts/main.py generate --photo "photo.jpg" --scenario free \
    --prompt "A futuristic cyberpunk portrait with neon lights"

# Multiple photos with custom prompt
python scripts/main.py generate --photos "photo1.jpg,photo2.jpg" --scenario free \
    --prompt "A group photo on the surface of Mars, wearing space suits"

# Multiple images with negative prompt
python scripts/main.py generate --photo "photo.jpg" --scenario free \
    --prompt "Renaissance art style portrait" \
    --negative-prompt "modern, digital, low quality" \
    --count 3

# Many reference photos for complex scene
python scripts/main.py generate --photos "p1.jpg,p2.jpg,p3.jpg,p4.jpg,p5.jpg" \
    --scenario free \
    --prompt "A dinner party scene with all characters around a table, candlelight atmosphere"
```

## Agent Integration

For Claude Code agent integration, use CLI commands with `--non-interactive` flag:

### Basic Integration Pattern

```bash
# Generate portrait photos
python scripts/main.py generate --photo "$USER_PHOTO" \
    --scenario portrait \
    --style "职业商务照" \
    --non-interactive

# Generate couple photos
python scripts/main.py generate --photos "$PHOTO1,$PHOTO2" \
    --scenario couple \
    --pose "手牵手面向镜头" \
    --non-interactive

# Generate family photos
python scripts/main.py generate --photos "$PHOTO1,$PHOTO2,$PHOTO3" \
    --scenario family \
    --template "温馨家庭聚会" \
    --non-interactive

# Generate free mode photos
python scripts/main.py generate --photo "$USER_PHOTO" \
    --scenario free \
    --prompt "A futuristic cyberpunk portrait with neon lighting" \
    --non-interactive
```

Recommended tools for agent skills:
- `Bash(python:*)` - Execute Python commands
- `Read` - Read generated images
- `Write` - Save output files

## Configuration

### Environment Variables

- `ARK_API_KEY`: ByteDance ARK API key for image generation (required, API will error if not set)

### Configuration File (`config.json`)

Key settings:
- `api.image_generation_url`: Volcano Engine image API endpoint
- `paths.temp_dir`: Temporary files directory
- `paths.output_dir`: Generated content directory
- `paths.logs_dir`: Log files directory
- `generation.default_image_count`: Default number of images to generate (default: 5)
- `generation.image_width` / `generation.image_height`: Image dimensions (default: 2048x2048)
- `generation.image_model`: AI model to use (default: doubao-seedream-4.5-251128)
- `scenarios.config_file`: Scenarios configuration file (default: scenarios.json)
- `scenarios.default_scenario`: Default scenario type (default: celebrity)

### Scenario Data Files

**Portrait Styles** (`data/portrait_styles.json`):
- Each style includes: name, category, prompt, lighting, background, mood
- Easy to extend with custom styles

**Couple Poses** (`data/couple_poses.json`):
- Each pose includes: name, prompt, scene, atmosphere, attire
- 12+ pose options for different moods and settings
- 6 background options for independent environment control
- Gender-neutral attire descriptions
- Automatic gender detection from input photos
- Person 1 and Person 2 positioning based on input order

**Family Templates** (`data/family_templates.json`):
- Each template includes: name, prompt, scene, atmosphere, person_count
- Arrangement options for different family sizes

## Technical Details

### Image Generation (Seedream 4.5)

- **Model**: `doubao-seedream-4.5-251128`
- **Method**: Image-to-image generation
- **Resolution**: 2048x2048 (configurable, supports multiple aspect ratios)
- **Multi-photo support**: Up to 14 reference images for fusion
- **Negative prompts**: Exclude blurry faces, unnatural poses, watermarks
- **Response format**: Base64 JSON or URL (configurable)

### Performance

- Image generation: ~10-20 seconds per image
- Total time for 5 images: ~1-2 minutes
- Temporary storage: 200-500MB during processing

## API Integration

This skill integrates with ByteDance's Volcano Engine ARK platform:

- **Image Generation API**: `POST https://ark.cn-beijing.volces.com/api/v3/images/generations`
- **Multi-reference fusion**: Support for combining multiple reference photos
- **Sequential generation**: Optional for related image series

Detailed API documentation is available in `docs/api/`.

## Troubleshooting

### Missing API Credentials

```bash
# Configure API credentials before running
# Set environment variable: ARK_API_KEY
# API will return error if key is not properly configured
```

### Image Generation Fails

- Check internet connection
- Verify API key validity
- Ensure photos are clear and well-lit (≥1024×1024 recommended)
- Check `logs/` directory for detailed errors

### Logs

Detailed error information is available in `logs/` directory.

## Documentation

- **`photo-studio-skill/SKILL.md`**: Complete skill documentation with usage examples
- **`photo-studio-skill/references/API.md`**: Python API reference
- **`docs/skill-spec.md`**: Agent Skills format specification
- **`docs/api/`**: Volcano Engine API documentation (Chinese)
- **`CLAUDE.md`**: Guidance for Claude Code instances

## Customization

### Adding Custom Styles (Portrait Scenario)

Edit `data/portrait_styles.json`:

```json
{
  "styles": [
    {
      "id": "my_custom_style",
      "name": "我的风格",
      "category": "Custom",
      "prompt": "Your custom prompt here",
      "lighting": "lighting description",
      "background": "background description",
      "mood": "mood description"
    }
  ]
}
```

### Adding Custom Poses (Couple Scenario)

Edit `data/couple_poses.json`:

```json
{
  "poses": [
    {
      "id": "my_custom_pose",
      "name": "Custom Pose",
      "prompt": "Pose description",
      "scene": "Scene description",
      "atmosphere": "Atmosphere description"
    }
  ]
}
```

### Adding Custom Characters (Celebrity Scenario)

```bash
# Add via CLI
python scripts/main.py add-character "Character Name" "Description prompt" --scene "Scene description"

# Or edit data/default_characters.json directly
```


## Recent Improvements

### Enhanced Gender Detection & Person Count Control

**Multiple Photo Scenarios (Couple/Family):**
- ✅ Automatic gender detection from each input photo
- ✅ Person 1, 2, 3... positioning based on input order
- ✅ No default "male/female" assumption - matches actual input photos
- ✅ Supports same-gender couples (male-male, female-female)
- ✅ Supports mixed-gender couples (male-female)

**Family Photos:**
- ✅ Exact person count control (matches input photos exactly)
- ✅ Repeated person count requirements (at least 3x in prompt)
- ✅ Uppercase "EXACTLY" and "MUST" for emphasis
- ✅ "NO MORE, NO FEWER" negative constraints
- ✅ Clear person matching instructions for each person
- ✅ Supports 2-6 person families

### Standard Pose System

**Portrait Styles (15+ options):**
- ✅ Each style includes standard pose description
- ✅ Professional headshot poses for business styles
- ✅ Artistic three-quarter poses for creative styles
- ✅ Natural casual poses for lifestyle styles
- ✅ All poses ensure consistent, professional positioning

**Enhanced Photo Preprocessing:**
- ✅ Unique filenames for each input photo
- ✅ Format: `processed_user_photo_00.jpg`, `01.jpg`, `02.jpg`...
- ✅ Fixes photo overwriting in multi-photo scenarios
- ✅ Each photo independently preprocessed with unique ID

### Background & Attire Control

**Couple Poses (12 options):**
- ✅ 6 independent background options
- ✅ Gender-neutral attire descriptions
- ✅ Backgrounds: Urban street, Park nature, Beach sunset, Cafe interior, Rooftop, Studio simple

**Family Templates (8 options):**
- ✅ 6 independent background options
- ✅ Standard family attire descriptions
- ✅ Backgrounds: Formal living room, Cozy home, Professional studio, Outdoor park, Beach seaside, Garden floral

### Technical Enhancements

**Prompt Optimization:**
- ✅ Explicit "Use ONLY facial features" instructions
- ✅ "Generate completely new body positions, poses, and backgrounds"
- ✅ Separate Person 1, 2, 3... identification for each input photo
- ✅ Gender detection from each reference photo
- ✅ Age and appearance extraction for family scenarios

**Examples:**

```bash
# Couple photos with pose and background
MOCK_API=true python scripts/main.py generate     --photos "photo1.jpg,photo2.jpg"     --scenario couple     --pose "手牵手面向镜头"     --background "海滩日落"     --non-interactive

# Family photos with template and background
MOCK_API=true python scripts/main.py generate     --photos "photo1.jpg,photo2.jpg,photo3.jpg"     --scenario family     --template "温馨家庭聚会"     --background "户外公园"     --non-interactive

# Portrait with specific style
MOCK_API=true python scripts/main.py generate     --photo photo.jpg     --scenario portrait     --style "职业商务照"     --count 3     --non-interactive
```

### Key Benefits

1. ✅ No photo overwriting in multi-photo scenarios
2. ✅ Accurate gender detection from input photos
3. ✅ Exact person count matching in family portraits
4. ✅ Standard professional poses for all portrait styles
5. ✅ Independent background control for couple/family
6. ✅ Enhanced attire descriptions (no original clothing usage)
7. ✅ Clear Person 1, 2, 3... positioning
8. ✅ Supports all gender combinations (MM, MF, FM, FF)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **ByteDance** for providing the Seedream 4.5 API through Volcano Engine
- **Claude Code** ecosystem for the Agent Skills framework
- All open-source libraries used in this project

---

**Note**: This skill requires a ByteDance ARK API key. Usage of the APIs may incur costs according to ByteDance's pricing policies.
