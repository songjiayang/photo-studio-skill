# Multi-Photo Fusion

Merge multiple photos with 4 fusion templates.

## Overview

Combine multiple photos (1-6 images) using 4 fusion templates: outfit fusion, person-scenery fusion, brand visual design, or multi-person composite.

## Use Cases

- User wants to merge person photo with clothing for outfit visualization
- User wants to merge person with scenery for natural scene photos
- User wants to design brand visual kit based on LOGO
- User wants to merge multiple people into one group photo

## Available Templates

### 1. Outfit Fusion (穿搭融合)

Merge person photo with clothing photo for natural outfit visualization.

**Required Photos:**
1. Person photo (reference for facial features, gender, age, posture)
2. Clothing photo (reference for outfit style, color, material)

**Fields:**
| Parameter | Type | Options |
|-----------|-------|---------|
| `--style` | select | 时尚街拍, 商务休闲, 运动休闲, 文艺清新, 复古风, 韩系风 |

**Example:**
```bash
python scripts/main.py generate --photos "me.jpg,clothing.jpg" --scenario fusion \
    --template outfit-fusion \
    --style "时尚街拍" \
    --non-interactive
```

---

### 2. Person-Scenery Fusion (人景融合)

Merge person photo with scenery photo for natural scene composition.

**Required Photos:**
1. Person photo (reference for facial features, gender, age, posture)
2. Scenery photo (reference for scene, tone, atmosphere, composition)

**Fields:**
| Parameter | Type | Options | Default |
|-----------|-------|----------|---------|
| `--mood` | select | 宁静致远, 活力四射, 浪漫温馨, 神秘奇幻, 怀旧温暖 | 宁静致远 |
| `--clothing` | text | Clothing description (optional) | None |
| `--composition` | text | Composition suggestion (optional) | None |

**Clothing Examples:**
- "白色运动外套"
- "连衣裙"
- "西装"
- "休闲T恤"

**Composition Examples:**
- "人物位于画面左侧三分之一处"
- "人物位于画面中央"
- "人物位于画面右侧"

**Example:**
```bash
python scripts/main.py generate --photos "me.jpg,scenery.jpg" --scenario fusion \
    --template person-scenery-fusion \
    --mood "宁静致远" \
    --clothing "白色运动外套" \
    --composition "人物位于画面左侧三分之一处" \
    --non-interactive
```

---

### 3. Brand Visual Design (品牌视觉设计)

Design brand visual kit based on LOGO.

**Required Photos:**
1. Brand LOGO photo

**Fields:**
| Parameter | Type | Description |
|-----------|-------|-------------|
| `--brand-name` | text | Brand name |
| `--color` | text | Primary color (e.g., 绿色, 蓝色, 红色) |
| `--style` | select | 简约现代, 复古风, 科技感, 文艺风, 极简主义 | 简约现代 |
| `--items` | text | Comma-separated items (e.g., 包装袋,帽子,卡片,挂绳) |

**Common Items:**
- 包装袋 - Packaging bags
- 帽子 - Hats
- 卡片 - Cards
- 挂绳 - Lanyards
- 徽章 - Badges
- 服装 - Clothing
- 马克杯 - Mugs

**Example:**
```bash
python scripts/main.py generate --photo "logo.jpg" --scenario fusion \
    --template brand-design \
    --brand-name "MyBrand" \
    --color "绿色" \
    --style "简约现代" \
    --items "包装袋,帽子,卡片,挂绳" \
    --non-interactive
```

---

### 4. Multi-Person Composite (多人合成)

Merge multiple people into one group photo.

**Required Photos:**
1-6 photos (one per person)

**Fields:**
| Parameter | Type | Description |
|-----------|-------|-------------|
| `--scene` | text | Scene description (e.g., 户外公园, 咖啡厅, 办公室) |
| `--atmosphere` | text | Atmosphere (e.g., 温馨轻松, 专业严肃, 活泼欢快) |

**Scene Examples:**
- 户外公园 - Outdoor park
- 咖啡厅 - Cafe
- 办公室 - Office
- 海滩 - Beach
- 餐厅 - Restaurant
- 屋顶 - Rooftop

**Atmosphere Examples:**
- 温馨轻松 - Warm and relaxed
- 专业严肃 - Professional and serious
- 活泼欢快 - Playful and cheerful
- 浪漫温馨 - Romantic and warm
- 友好亲切 - Friendly and warm

**Example:**
```bash
python scripts/main.py generate --photos "p1.jpg,p2.jpg,p3.jpg" --scenario fusion \
    --template multi-person-composite \
    --scene "户外公园" \
    --atmosphere "温馨轻松" \
    --non-interactive
```

## Command Examples

```bash
# Outfit fusion
python scripts/main.py generate --photos "me.jpg,clothing.jpg" --scenario fusion \
    --template outfit-fusion \
    --style "时尚街拍" \
    --non-interactive

# Person-scenery fusion
python scripts/main.py generate --photos "me.jpg,scenery.jpg" --scenario fusion \
    --template person-scenery-fusion \
    --mood "宁静致远" \
    --clothing "白色运动外套" \
    --composition "人物位于画面左侧三分之一处" \
    --non-interactive

# Brand design
python scripts/main.py generate --photo "logo.jpg" --scenario fusion \
    --template brand-design \
    --brand-name "MyBrand" \
    --color "绿色" \
    --style "简约现代" \
    --items "包装袋,帽子,卡片,挂绳" \
    --non-interactive

# Multi-person composite
python scripts/main.py generate --photos "p1.jpg,p2.jpg,p3.jpg" --scenario fusion \
    --template multi-person-composite \
    --scene "户外公园" \
    --atmosphere "温馨轻松" \
    --non-interactive
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|-------|-----------|-------------|
| `--photo` or `--photos` | paths | Yes | Path(s) to photos (1-6 photos) |
| `--template` | string | Yes | Template ID |
| Template-specific | varies | Varies | See template-specific fields above |
| `--scenario, -s` | string | Yes | Scenario type: `fusion` |
| `--non-interactive, -ni` | flag | No | Run in non-interactive mode |

## Best Practices

### Outfit Fusion
1. **Clear person photo**: Front-facing photo with visible posture
2. **Clear clothing photo**: Isolated clothing image with visible details
3. **Match style**: Choose style that matches clothing type
4. **Consistent lighting**: Photos with similar lighting work best

### Person-Scenery Fusion
1. **Person photo clarity**: Clear facial features and posture
2. **Scenery photo quality**: High-resolution scenery with clear details
3. **Appropriate mood**: Choose mood that matches scenery type
4. **Clothing matching**: Optional clothing parameter to change outfit
5. **Consider composition**: Specify positioning for better results

### Brand Design
1. **Clear LOGO**: High-resolution LOGO with visible details
2. **Consistent color**: Choose color that matches brand identity
3. **Appropriate style**: Match style to brand personality
4. **Specific items**: List items clearly for better generation

### Multi-Person Composite
1. **Individual photos**: Use individual photos for each person (1-6 photos)
2. **Clear faces**: Photos with visible facial features work best
3. **Appropriate scene**: Choose scene that fits desired atmosphere
4. **Consistent style**: Photos with similar styles produce better results

## Template Comparison

| Template | Photos Required | Use Case |
|----------|----------------|-----------|
| Outfit Fusion | 2 | Visualize outfit on person |
| Person-Scenery Fusion | 2 | Place person in scene |
| Brand Design | 1 | Design brand visual kit |
| Multi-Person Composite | 1-6 | Create group photo |

## Photo Guidelines

### Photo Requirements
- **Outfit Fusion**: 2 photos (1 person, 1 clothing)
- **Person-Scenery Fusion**: 2 photos (1 person, 1 scenery)
- **Brand Design**: 1 photo (LOGO)
- **Multi-Person Composite**: 1-6 photos (one per person)
- **Resolution**: ≥1024×1024 for best results

### Photo Quality
- Clear, well-lit photos produce best fusion results
- Consistent lighting across photos improves blending
- Sharp focus on key elements (faces, clothing, LOGO)
- Avoid photos with complex backgrounds for brand design

## Common Issues & Solutions

### Outfit Fusion Issues
- **Outfit doesn't fit**: Provide clearer person photo showing body posture
- **Unnatural look**: Choose style that matches clothing type
- **Poor blending**: Ensure photos have consistent lighting

### Person-Scenery Fusion Issues
- **Person looks out of place**: Adjust mood and composition settings
- **Lighting mismatch**: Choose scenery with compatible lighting
- **Scale issues**: Ensure person and scenery have compatible proportions
- **Clothing doesn't match**: Adjust clothing parameter to match scenery style

### Brand Design Issues
- **Unclear design**: Provide clearer, higher-resolution LOGO
- **Inconsistent style**: Match style to brand personality
- **Missing items**: List items specifically in correct format

### Multi-Person Composite Issues
- **Faces look different**: Use consistent photo quality and lighting
- **Unnatural grouping**: Choose appropriate scene and atmosphere
- **Scale mismatch**: Use photos with consistent scale and angle
