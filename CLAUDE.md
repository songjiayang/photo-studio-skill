# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Python-based AI Photo Studio skill** for the Claude Code/Agent Skills ecosystem. It generates professional portrait and group photos using ByteDance's Seedream 4.5 AI across multiple scenarios.

**Important Documentation Constraints:**
- `docs/api/` contains Volcano Engine service API documentation (Chinese)
- `docs/skill-spec.md` contains the Claude Agent Skills specification (English)
- All API integrations must follow the official Volcano Engine API documentation in `docs/api/`
- Skill implementation must adhere to the Agent Skills format specified in `docs/skill-spec.md`

## Architecture

### Core Components

1. **Main CLI (`scripts/main.py`)**: Entry point with subcommands:
   - `generate`: Main generation workflow (supports 4 scenarios)
   - `list-scenarios`: Show available photo scenarios
   - `list-styles`: Show available styles for a scenario
   - `list-characters`: Show available movie characters
   - `add-character`: Add custom character
   - `config`: View/update configuration
   - `cleanup`: Clean temporary files

2. **Interaction Manager (`scripts/interaction.py`)**: Handles user input collection, image review, and workflow state management
   - Scenario selection
   - Multi-photo input handling
   - Style/pose/template selection
   - State persistence

3. **Image Generator (`scripts/image_generator.py`)**: Integrates with Seedream 4.5 API for image generation
   - Single-photo generation (celebrity, portrait scenarios)
   - Multi-photo generation (couple, family scenarios)
   - Multi-reference image fusion
   - API request handling

4. **Configuration Manager (`scripts/config.py`)**: Manages settings, scenario data, and API key resolution
   - Scenario configuration from `data/scenarios.json`
   - Style/pose/template data loading
   - Global settings management
   - Backward compatibility

### Workflow

The skill follows a 4-scenario workflow:
1. **Scenario Selection**: User chooses from 4 scenarios (celebrity, portrait, couple, family)
2. **Input Collection**: Collect photos and scenario-specific options
3. **Image Generation**: Generate AI images using Seedream 4.5
4. **Review & Save**: User reviews and saves photos

### File Structure

```
photo-studio-skill/
├── SKILL.md              # Comprehensive user guide with YAML frontmatter
├── README.md             # This file
├── config.json           # Configuration settings (API endpoints, paths, generation settings)
├── requirements.txt      # Python dependencies
├── LICENSE               # MIT License
├── scripts/              # Core Python scripts
│   ├── main.py           # CLI entry point
│   ├── config.py         # Configuration management
│   ├── interaction.py    # User interaction handling
│   └── image_generator.py # Seedream 4.5 integration
├── data/                 # Scenario templates and data
│   ├── scenarios.json         # Unified scenario configurations
│   ├── default_characters.json # Movie characters (for celebrity scenario)
│   ├── portrait_styles.json   # Portrait styles (for portrait scenario)
│   ├── couple_poses.json    # Couple poses (for couple scenario)
│   └── family_templates.json # Family templates (for family scenario)
├── references/           # Additional documentation
│   └── API.md            # Python API reference
├── temp/                 # Temporary files (auto-generated)
├── output/               # Generated content
│   └── images/          # AI-generated photos
└── logs/                 # Log files (auto-generated)
```

## Development Commands

### Setup and Installation

```bash
# Install Python dependencies
cd photo-studio-skill
pip install -r requirements.txt

# Set API key for image generation
export ARK_API_KEY="your_ark_api_key_here"
```

### Running the Skill

```bash
# List available scenarios
python scripts/main.py list-scenarios

# Generate photos with specific scenario
python scripts/main.py generate --photo photo.jpg --scenario portrait --style "职业商务照"

# Generate couple photos
python scripts/main.py generate --photos "photo1.jpg,photo2.jpg" --scenario couple

# Non-interactive mode (for agents)
python scripts/main.py generate --photo photo.jpg --scenario portrait --non-interactive

# Add custom character
python scripts/main.py add-character "My Character" "Description prompt" --scene "Scene description"

# View configuration
python scripts/main.py config --show

# Update configuration
python scripts/main.py config --set generation.default_image_count=3

# Clean temporary files
python scripts/main.py cleanup
```

### Testing and Debugging

```bash
# Check logs for errors
ls photo-studio-skill/logs/

# Verify API key configuration
python scripts/main.py config --show | grep -i api

# Test scenario listing
python scripts/main.py list-scenarios

# Test style listing
python scripts/main.py list-styles --scenario portrait
```

## Configuration

### Environment Variables

- `ARK_API_KEY`: ByteDance ARK API key for image generation

### Configuration File (`config.json`)

Key settings:
- `api.image_generation_url`: Volcano Engine image API endpoint
- `paths.temp_dir`: Temporary files directory
- `paths.output_dir`: Generated content directory
- `generation.default_image_count`: Default number of images (default: 5)
- `generation.image_width`/`image_height`: Image dimensions (default: 2048x2048)
- `generation.image_model`: AI model to use (default: doubao-seedream-4.5-251128)
- `scenarios.config_file`: Scenarios configuration file (default: scenarios.json)
- `scenarios.default_scenario`: Default scenario type (default: celebrity)

### Scenario Configuration (`data/scenarios.json`)

Unified configuration for all scenarios:

```json
{
  "scenarios": [
    {
      "id": "celebrity",
      "name": "明星合影",
      "description": "与电影明星拍照留念",
      "input_type": "single_photo",
      "required_photos": 1,
      "max_photos": 1,
      "data_file": "default_characters.json"
    },
    {
      "id": "portrait",
      "name": "个人写真",
      "description": "专业个人肖像摄影",
      "input_type": "single_photo",
      "required_photos": 1,
      "max_photos": 1,
      "data_file": "portrait_styles.json"
    },
    {
      "id": "couple",
      "name": "双人合影",
      "description": "情侣或朋友合影",
      "input_type": "multiple_photos",
      "required_photos": 2,
      "max_photos": 2,
      "data_file": "couple_poses.json"
    },
    {
      "id": "family",
      "name": "全家合影",
      "description": "家庭合照（3-6人）",
      "input_type": "multiple_photos",
      "required_photos": 1,
      "max_photos": 6,
      "data_file": "family_templates.json"
    }
  ]
}
```

## Key Implementation Details

### API Integration

- **Image Generation**: Uses Seedream 4.5's image-to-image generation
- **Multi-photo fusion**: Supports up to 14 reference images for couple/family scenarios
- **Error Handling**: Comprehensive API key validation and error messaging in logs

### State Management

- `InteractionManager` maintains workflow state across steps
- Temporary files are managed in `temp/` directory with automatic cleanup
- Generated content organized in `output/images/`

### Scenario System

- **Unified Configuration**: All scenarios defined in single `scenarios.json` file
- **Flexible Data Loading**: Each scenario loads its data from separate JSON file
- **Extensible**: Easy to add new scenarios or modify existing ones
- **Backward Compatible**: Original celebrity scenario behavior preserved

### Input Handling

- **Single Photo**: Celebrity and portrait scenarios
- **Multiple Photos**: Couple and family scenarios (supports 1-6 photos)
- **Style Selection**: Portrait scenario offers style picker
- **Character/Selection**: Celebrity scenario offers character picker
- **Non-interactive Mode**: Full automation for agent integration

## Performance Characteristics

- Image generation: ~10-20 seconds per image
- Total time for 5 images: ~1-2 minutes
- Storage: 500MB-1GB temporary space during processing

## Common Issues and Solutions

### Missing API Keys

```bash
# Set ARK API key
export ARK_API_KEY="your_key"
```

### Image Generation Fails

- Check internet connection
- Verify API key validity
- Ensure photo is clear and well-lit (≥1024×1024 recommended)
- Check `logs/` directory for detailed errors

### Scenario Data Not Found

- Ensure `data/scenarios.json` exists
- Verify `data_file` paths in scenarios point to existing JSON files
- Check JSON format is valid

## External Dependencies

### Required System Tools

- Python 3.8+
- Internet connectivity for API calls

### Python Dependencies

- `requests`: HTTP client for API calls
- `Pillow`: Image processing
- `opencv-python`: Computer vision for image manipulation
- `numpy`: Numerical operations

### External APIs

- ByteDance ARK Platform (Seedream 4.5)
- Requires API key from ByteDance Developer Account

## Development Notes

- Entry point is always `scripts/main.py`
- Use unified `ARK_API_KEY` when possible (simplifies configuration)
- Scenario data can be extended by editing JSON files or via CLI
- All paths are configurable in `config.json`
- Logs provide detailed error information in `logs/` directory
- Temporary files auto-cleanup available via `cleanup` command

### Adding New Scenarios

1. Add scenario definition to `data/scenarios.json`
2. Create data file in `data/` directory
3. Add scenario handling in `scripts/interaction.py`
4. Add generation method in `scripts/image_generator.py`
5. Update documentation

### Extending Styles/Templates

Edit respective JSON files:
- `data/portrait_styles.json`: Add new portrait styles
- `data/couple_poses.json`: Add new couple poses
- `data/family_templates.json`: Add new family templates

Each entry should follow the established format with prompt, scene, and metadata.

## Security Considerations

- API credentials are loaded from environment variables
- No hardcoded API keys in source code
- Error messages avoid exposing specific environment variable names
- Temporary files cleaned up automatically
- Logs may contain sensitive info - secure logs directory appropriately
