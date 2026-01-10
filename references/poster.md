# Poster Design

Create professional posters with 3 poster templates.

## Overview

Design professional posters for movies, events, or products using 3 poster templates: movie poster, event poster, or product poster.

## Use Cases

- User wants to create movie promotional poster
- User wants to create event marketing poster
- User wants to create product marketing poster

## Available Templates

### 1. Movie Poster (电影海报)

Create cinematic movie promotional poster.

**Required Photos:** 0-1 (optional - character, scene, or element)

**Fields:**
| Parameter | Type | Options | Default |
|-----------|-------|----------|---------|
| `--title` | text | Movie title | Required |
| `--genre` | select | 动作, 科幻, 奇幻, 爱情, 喜剧, 惊悚, 犯罪, 战争, 动画 | 动作 |
| `--style` | select | 好莱坞大片, 亚洲电影, 独立电影, 复古海报, 现代极简, 漫画风格 | 好莱坞大片 |
| `--mood` | select | 史诗震撼, 紧张悬疑, 温馨浪漫, 欢乐轻松, 黑暗压抑, 热血励志 | 史诗震撼 |
| `--additional-info` | text | Additional text (e.g., release date, tagline) | Optional |

**Genre Examples:**
- 动作 - Action
- 科幻 - Sci-Fi
- 奇幻 - Fantasy
- 爱情 - Romance
- 喜剧 - Comedy
- 惊悚 - Thriller
- 犯罪 - Crime
- 战争 - War
- 动画 - Animation

**Style Examples:**
- 好莱坞大片 - Hollywood blockbuster
- 亚洲电影 - Asian cinema
- 独立电影 - Indie film
- 复古海报 - Retro poster
- 现代极简 - Modern minimalist
- 漫画风格 - Manga style

**Mood Examples:**
- 史诗震撼 - Epic,震撼
- 紧张悬疑 - Suspenseful, mysterious
- 温馨浪漫 - Warm, romantic
- 欢乐轻松 - Cheerful, lighthearted
- 黑暗压抑 - Dark, oppressive
- 热血励志 - Inspiring, motivational

**Example:**
```bash
python scripts/main.py generate --photo "me.jpg" --scenario poster \
    --template movie-poster \
    --title "银河守护者3" \
    --genre "科幻" \
    --style "好莱坞大片" \
    --mood "史诗震撼" \
    --additional-info "2025.05.02 全球上映" \
    --non-interactive
```

---

### 2. Event Poster (活动海报)

Create promotional event poster.

**Required Photos:** 1 (event representative, speaker, or visual element)

**Fields:**
| Parameter | Type | Options | Default |
|-----------|-------|----------|---------|
| `--event-name` | text | Event name | Required |
| `--event-type` | select | 音乐节, 演唱会, 会议, 展览, 比赛, 市集, 讲座, 派对 | 音乐节 |
| `--style` | select | 潮流时尚, 简约现代, 复古怀旧, 科技未来, 艺术创意, 专业商务 | 潮流时尚 |
| `--date` | text | Event date | Required |
| `--location` | text | Event location | Required |
| `--mood` | select | 热闹欢快, 神秘酷炫, 温馨亲切, 专业正式, 活力四射, 文艺清新 | 热闹欢快 |

**Event Type Examples:**
- 音乐节 - Music festival
- 演唱会 - Concert
- 会议 - Conference
- 展览 - Exhibition
- 比赛 - Competition
- 市集 - Market/Fair
- 讲座 - Lecture
- 派对 - Party

**Style Examples:**
- 潮流时尚 - Trendy, fashionable
- 简约现代 - Minimalist, modern
- 复古怀旧 - Retro, nostalgic
- 科技未来 - Futuristic
- 艺术创意 - Artistic, creative
- 专业商务 - Professional, business

**Mood Examples:**
- 热闹欢快 - Lively, cheerful
- 神秘酷炫 - Mysterious, cool
- 温馨亲切 - Warm, friendly
- 专业正式 - Professional, formal
- 活力四射 - Energetic, dynamic
- 文艺清新 - Artistic, fresh

**Example:**
```bash
python scripts/main.py generate --photo "me.jpg" --scenario poster \
    --template event-poster \
    --event-name "夏日音乐节" \
    --event-type "音乐节" \
    --style "潮流时尚" \
    --date "2025.07.20" \
    --location "北京工人体育场" \
    --mood "热闹欢快" \
    --non-interactive
```

---

### 3. Product Poster (产品海报)

Create product marketing poster.

**Required Photos:** 1 (product photo)

**Fields:**
| Parameter | Type | Options | Default |
|-----------|-------|----------|---------|
| `--product-name` | text | Product name | Required |
| `--product-type` | select | 科技产品, 食品饮料, 服装时尚, 美妆护肤, 家居用品, 运动健身, 图书文创 | 科技产品 |
| `--style` | select | 科技感, 时尚潮流, 简约高级, 温馨亲切, 运动活力, 自然清新 | 科技感 |
| `--mood` | select | 专业高端, 亲切温暖, 创新前沿, 活力四射, 优雅精致, 科技未来 | 专业高端 |
| `--features` | text | Comma-separated product features | Optional |
| `--additional-info` | text | Additional text (e.g., price, tagline) | Optional |

**Product Type Examples:**
- 科技产品 - Tech products
- 服装鞋帽 - Clothing and footwear
- 食品饮料 - Food and beverages
- 家居用品 - Home goods
- 化妆品 - Cosmetics
- 书籍文具 - Books and stationery

**Style Examples:**
- 科技感 - Tech-oriented
- 时尚潮流 - Fashionable, trendy
- 简约高级 - Minimalist, premium
- 复古怀旧 - Retro, nostalgic
- 温馨生活 - Warm, lifestyle
- 商务专业 - Business, professional

**Mood Examples:**
- 专业高端 - Professional, premium
- 亲民实惠 - Affordable, accessible
- 创新前卫 - Innovative, cutting-edge
- 温馨舒适 - Warm, comfortable
- 时尚潮流 - Fashionable, trendy

**Example:**
```bash
python scripts/main.py generate --photo "product.jpg" --scenario poster \
    --template product-poster \
    --product-name "智能手表Pro" \
    --product-type "科技产品" \
    --style "科技感" \
    --mood "专业高端" \
    --features "高性能,轻薄便携,长续航" \
    --additional-info "¥2999 首发优惠" \
    --non-interactive
```

## Command Examples

```bash
# Movie poster
python scripts/main.py generate --photo "me.jpg" --scenario poster \
    --template movie-poster \
    --title "银河守护者3" \
    --genre "科幻" \
    --style "好莱坞大片" \
    --mood "史诗震撼" \
    --additional-info "2025.05.02 全球上映" \
    --non-interactive

# Event poster
python scripts/main.py generate --photo "me.jpg" --scenario poster \
    --template event-poster \
    --event-name "夏日音乐节" \
    --event-type "音乐节" \
    --style "潮流时尚" \
    --date "2025.07.20" \
    --location "北京工人体育场" \
    --mood "热闹欢快" \
    --non-interactive

# Product poster
python scripts/main.py generate --photo "product.jpg" --scenario poster \
    --template product-poster \
    --product-name "智能手表Pro" \
    --product-type "科技产品" \
    --style "科技感" \
    --mood "专业高端" \
    --features "高性能,轻薄便携,长续航" \
    --additional-info "¥2999 首发优惠" \
    --non-interactive
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|-------|-----------|-------------|
| `--photo, -p` | path | Yes | Path to reference photo |
| `--template` | string | Yes | Template ID |
| Template-specific | varies | Varies | See template-specific fields above |
| `--scenario, -s` | string | Yes | Scenario type: `poster` |
| `--non-interactive, -ni` | flag | No | Run in non-interactive mode |

## Best Practices

### Movie Poster
1. **Compelling title**: Choose memorable, attention-grabbing title
2. **Match genre to style**: Ensure genre and style are compatible
3. **Create mood impact**: Choose mood that matches movie tone
4. **Use additional info**: Add release date or tagline for completeness
5. **Strong visual**: Use photo with good composition and lighting

### Event Poster
1. **Clear event name**: Make event name prominent and memorable
2. **Appropriate event type**: Match type to actual event format
3. **Include details**: Add date and location for clarity
4. **Match style to audience**: Choose style that appeals to target audience
5. **Set right mood**: Mood should reflect event atmosphere

### Product Poster
1. **Clear product name**: Make product name prominent and readable
2. **Highlight features**: List key features in concise format
3. **Pricing information**: Include price or promotional info if relevant
4. **Match style to brand**: Choose style that aligns with brand identity
5. **Appropriate mood**: Mood should match product positioning

## Template Comparison

| Template | Use Case | Key Fields |
|----------|-----------|------------|
| Movie Poster | Movie promotion | title, genre, style, mood |
| Event Poster | Event promotion | event-name, event-type, date, location |
| Product Poster | Product marketing | product-name, product-type, features |

## Photo Guidelines

### Photo Requirements
- **All templates**: 1 reference photo
- **Resolution**: ≥1024×1024 for best results
- **Composition**: Clear subject with good framing
- **Lighting**: Professional lighting for best results

### Photo Quality Tips
- **Movie poster**: Character photo with dramatic pose works best
- **Event poster**: Speaker or representative photo with good lighting
- **Product poster**: Clear product photo showing features clearly

## Text Guidelines

### Movie Poster Text
- **Title**: Large, bold, eye-catching
- **Additional info**: Release date, tagline, or credits
- **Keep it concise**: Limit text to essential information

### Event Poster Text
- **Event name**: Largest text element
- **Date and location**: Clear and readable
- **Additional info**: Speakers, schedule, or other details

### Product Poster Text
- **Product name**: Prominent and clear
- **Features**: Short, benefit-focused descriptions
- **Additional info**: Price, tagline, or promotional offer

## Common Issues & Solutions

### Movie Poster Issues
- **Title unclear**: Use shorter, more memorable title
- **Genre mismatch**: Adjust style to match genre better
- **Mood doesn't match**: Choose mood that aligns with movie tone
- **Weak visual impact**: Use more dramatic reference photo

### Event Poster Issues
- **Event details unclear**: Add specific date and time
- **Location unclear**: Include clear location details
- **Style mismatch**: Choose style appropriate for target audience
- **Mood doesn't match**: Adjust mood to reflect event atmosphere

### Product Poster Issues
- **Product unclear**: Use clearer product photo
- **Features not compelling**: Focus on user benefits
- **Price positioning unclear**: Adjust mood to match price point
- **Style mismatch**: Choose style that aligns with brand identity

## Design Tips

### Visual Hierarchy
1. **Primary text**: Make title/product name largest
2. **Secondary text**: Key information (date, features) medium size
3. **Tertiary text**: Additional info smallest

### Color Selection
1. **Contrast**: Ensure text is readable against background
2. **Consistency**: Use consistent color palette
3. **Brand alignment**: Match colors to brand identity

### Layout
1. **Balance**: Distribute elements evenly
2. **Focus**: Keep main subject prominent
3. **Simplicity**: Avoid cluttering with too much text
