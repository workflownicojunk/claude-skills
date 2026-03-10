# Video Analysis Pipeline

Analyze Instagram videos (Stories, Reels, competitor content) using Google Gemini's
multimodal API. Four specialized modes extract different information types, each with
optimized prompts that enforce structured JSON output.

## Table of Contents

1. [Model Selection](#model-selection)
2. [Upload Strategy](#upload-strategy)
3. [Analysis Modes](#analysis-modes)
4. [Prompt Templates](#prompt-templates)
5. [CLI Reference](#cli-reference)
6. [Output Schemas](#output-schemas)

---

## Model Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Design extraction (colors, timing, layout) | `gemini-2.5-pro` | Highest accuracy for HEX values, frame timing, layout proportions. Quality over cost. |
| Content analysis (hooks, pacing, structure) | `gemini-2.5-flash` | Good structural understanding, best price-performance ratio |
| Competitor analysis (patterns, benchmarks) | `gemini-2.5-flash` | Sufficient for categorical analysis |
| Transcription with timestamps | `gemini-2.5-flash` | Millisecond-precise timestamps, best price-performance |
| Thumbnail/still analysis | `gemini-2.5-flash` | Sufficient for single-frame evaluation |

**Key insight:** `gemini-2.5-flash` delivers good but approximate results for design extraction.
HEX values are estimated ("~#F8EDE6"), animation timing is approximated ("~0.3s"). For design
replication where exact values are needed, `gemini-2.5-pro` is the better choice.

---

## Upload Strategy

| File Size | Method | Implementation |
|-----------|--------|---------------|
| < 20MB | Inline (base64) | `types.Part.from_bytes(data=bytes, mime_type=mime)` |
| 20MB - 2GB | Files API | `client.files.upload(file=path)` then reference in call |

Most Instagram videos (Stories, Reels) are under 20MB. Files API is only needed for
long raw/uncompressed videos.

---

## Analysis Modes

### Mode 1: Design Extraction (`--mode design`)

**Purpose:** Extract exact design tokens for replication in Remotion templates.

**Extracts:**
- Exact color values (HEX, not "warm beige")
- Font identification (family, weight, style)
- Layout proportions (margins, padding, element sizes as % of frame)
- Animation types and frame-accurate timing
- Element hierarchy and z-ordering
- Spacing between elements (px values)

**Output:** Structured JSON with design tokens, directly usable in code.

**Default model:** `gemini-2.5-pro` (exact values required)

### Mode 2: Content Analysis (`--mode content`)

**Purpose:** Evaluate video content structure for performance scoring.

**Extracts:**
- Hook identification (first 3 seconds: type, text, visual technique)
- Cut rhythm and scene transitions (timestamps, transition types)
- Text overlays and their timing (appear/disappear timestamps)
- Audio usage (music, voiceover, silence segments)
- Watch-time prediction based on structural elements
- Pacing score (cuts per minute, information density)

**Output:** Structured JSON with scoring-relevant metrics.

**Default model:** `gemini-2.5-flash`

### Mode 3: Competitor Analysis (`--mode competitor`)

**Purpose:** Categorize competitor content patterns for benchmarking.

**Extracts:**
- Hook category (Correction, Identity, Bold Claim, Curiosity, Pain)
- Format pattern (Talking Head, B-Roll, Text-on-Screen, Split-Screen, etc.)
- CTA type and placement (timestamp, visual style, text)
- Production quality indicators (lighting, audio quality, editing complexity)
- Estimated engagement drivers (controversy, relatability, education, entertainment)

**Output:** Structured JSON with benchmark data.

**Default model:** `gemini-2.5-flash`

### Mode 4: Transcription (`--mode transcribe`)

**Purpose:** Full text transcription with precise timestamps.

**Extracts:**
- Word-level or segment-level timestamps
- Speaker identification where possible
- Non-speech audio events (music, sound effects)
- Language detection

**Output:** JSON with timestamped segments.

**Default model:** `gemini-2.5-flash`

---

## Prompt Templates

Each mode uses a specific prompt that enforces JSON output. The prompt quality directly
determines result quality. Specific measurement points outperform generic "analyze this video"
instructions by a large margin.

### Design Extraction Prompt

```
Analyze this video frame-by-frame and extract the exact design system. Respond in JSON only.

Extract these 10 specific data points:
1. background_color: Exact HEX value of the primary background
2. colors: Array of all distinct colors used, each as {hex, usage, area_percentage}
3. typography: Array of text elements, each as {text, font_family_guess, weight, style, size_relative_to_frame, color_hex}
4. layout: {padding_top_pct, padding_bottom_pct, padding_left_pct, padding_right_pct, content_alignment}
5. elements: Ordered array of visual elements from top to bottom, each as {type, position_y_pct, width_pct, description}
6. animations: Array of {element_index, type, direction, duration_seconds, delay_seconds, easing}
7. spacing: Array of gaps between consecutive elements in pixels (estimated for 1080x1920)
8. images: Array of {position, size_pct, shape, has_shadow, description}
9. text_content: All readable text in the video, in order of appearance
10. duration_seconds: Total video duration
```

### Content Analysis Prompt

```
Analysiere dieses Video und bewerte die Content-Struktur. Antworte ausschließlich in JSON.

Analysiere diese 8 spezifischen Datenpunkte:
1. hook: {type, text_if_any, visual_technique, duration_seconds, attention_score_1_to_10}
2. scenes: Array von {start_seconds, end_seconds, description, transition_type}
3. text_overlays: Array von {text, appear_seconds, disappear_seconds, position, style}
4. audio: {has_music, has_voiceover, silence_segments, music_energy}
5. pacing: {cuts_per_minute, information_density, rhythm_consistency}
6. cta: {text, timestamp_seconds, type, visual_style} oder null
7. watch_time_prediction: {predicted_retention_pct, reasoning, strongest_element, weakest_element}
8. format_category: einer von [talking_head, b_roll, text_on_screen, split_screen, slideshow, mixed]
```

### Competitor Analysis Prompt

```
Analysiere dieses Instagram-Video eines Competitors. Antworte ausschließlich in JSON.

Analysiere diese 7 spezifischen Datenpunkte:
1. hook_category: einer von [correction, identity_trigger, bold_claim, curiosity_gap, pain_point, other]
2. hook_details: {opening_text, visual_technique, estimated_stop_scroll_power_1_to_10}
3. format: {primary_format, secondary_elements, production_complexity_1_to_5}
4. content_pillars: Array von Themen die angesprochen werden
5. cta: {type, placement_seconds, text, visual_integration}
6. differentiators: Array von {element, description, replicable_boolean}
7. benchmark_signals: {estimated_save_worthiness_1_to_10, estimated_share_worthiness_1_to_10, controversy_level_1_to_5}
```

### Transcription Prompt

```
Transcribe this video with precise timestamps. Respond in JSON only.

Return:
1. language: detected language code (e.g., "de", "en")
2. segments: Array of {start_seconds, end_seconds, text, speaker_id}
3. non_speech: Array of {start_seconds, end_seconds, type, description}
   (type: one of [music, sound_effect, silence, ambient])
4. full_text: Complete transcription as a single string
```

---

## CLI Reference

```bash
# Design extraction for Remotion template creation
GEMINI_API_KEY=$(grep ^GOOGLE_API_KEY ~/Desktop/.env | cut -d'=' -f2-) \
  python3 ~/.claude/skills/ig/scripts/analyze_video.py \
  --mode design --file video.mp4 --output /tmp/design.json --model gemini-2.5-pro

# Content analysis for Reel scoring
GEMINI_API_KEY=$(grep ^GOOGLE_API_KEY ~/Desktop/.env | cut -d'=' -f2-) \
  python3 ~/.claude/skills/ig/scripts/analyze_video.py \
  --mode content --file video.mp4 --output /tmp/analysis.json

# Competitor analysis
GEMINI_API_KEY=$(grep ^GOOGLE_API_KEY ~/Desktop/.env | cut -d'=' -f2-) \
  python3 ~/.claude/skills/ig/scripts/analyze_video.py \
  --mode competitor --file video.mp4 --output /tmp/competitor.json

# Transcription
GEMINI_API_KEY=$(grep ^GOOGLE_API_KEY ~/Desktop/.env | cut -d'=' -f2-) \
  python3 ~/.claude/skills/ig/scripts/analyze_video.py \
  --mode transcribe --file video.mp4 --output /tmp/transcript.json

# Dry run (show prompt without API call)
python3 ~/.claude/skills/ig/scripts/analyze_video.py \
  --mode content --file video.mp4 --dry-run
```

**API Key:** The key in `~/Desktop/.env` is named `GOOGLE_API_KEY`, NOT `GEMINI_API_KEY`.
Always pass it as: `GEMINI_API_KEY=$(grep ^GOOGLE_API_KEY ~/Desktop/.env | cut -d'=' -f2-)`.
NEVER use `source .env` (breaks in subshells and background tasks).

---

## Output Schemas

All modes output JSON. The `response_mime_type: "application/json"` parameter in the Gemini
API call enforces structured output. Never accept freeform Markdown for machine processing.
