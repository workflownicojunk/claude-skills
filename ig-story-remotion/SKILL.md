---
name: ig-story-remotion
description: "Animated Instagram Story slides via Remotion: 9:16 MP4 with brand-compliant animations."
user-invocable: false
license: MIT
compatibility: Requires Remotion project at ~/Desktop/remotion-stories/. Node.js 20+.
metadata:
  author: NicoJunk
  version: "1.0.0"
  parent-skill: ig
---

# IG Story Remotion: Animated Story Slide Production

Produces animated 9:16 Instagram Story video clips using Remotion. Each slide is a
React component with frame-accurate animations, brand-compliant design, and automatic
MP4 rendering.

## When to Use

Use this sub-skill instead of static ig-story when:
- The slide needs animated text reveals (product CTAs, countdowns, educational reveals)
- Sponsored/affiliate content (animated slides get 20-40% more watch time)
- The user explicitly asks for animation, video, or "bewegte" Story content
- Multi-product showcases where staggered reveals guide the viewer's eye

Stay with static ig-story when:
- Behind-the-scenes content (raw/candid is the point)
- Simple polls or question stickers
- Quick reposts or shares

## Execution Flow

### Step 1: Content Architecture

Before touching code, determine the slide's information architecture:

1. **Context check:** Does the slide work standalone? If someone taps into this single
   slide without seeing previous slides, do they understand what it's about and why
   they should care? If not, add a pain-hook or context line at the top.

2. **Template selection:** Load `references/remotion-story-templates.md` and pick the
   matching template from the Template Library:
   - Product CTA with Pain-Hook (affiliate/sponsored)
   - Educational Reveal (tips, mythbusting)
   - Testimonial / Social Proof (Kundenstimmen)
   - Countdown / Urgency (launch, deadline)

3. **Element inventory:** List every element the slide needs, in reading order.
   This becomes the animation sequence.

### Step 2: Asset Preparation

1. Check what images/assets are needed
2. Copy product images to `~/Desktop/remotion-stories/public/`:
   ```bash
   cp "/path/to/product.jpeg" ~/Desktop/remotion-stories/public/product-name.jpeg
   ```
3. If a reference video exists, use `scripts/analyze_video.py --mode design` for exact
   design token extraction (see `references/video-analysis-pipeline.md` for details):
   ```bash
   GEMINI_API_KEY=$(grep ^GOOGLE_API_KEY ~/Desktop/.env | cut -d'=' -f2-) \
     python3 ~/.claude/skills/ig/scripts/analyze_video.py \
     --mode design --file reference.mp4 --output /tmp/design-tokens.json
   ```
   For screenshots, use the ai-multimodal skill with Gemini 2.5 Flash instead.

### Step 3: Build the Composition

1. Create a new `.tsx` file in `~/Desktop/remotion-stories/src/`
2. Import design tokens and fonts from `references/remotion-story-templates.md`
3. Use the `FadeSlideIn` component for all animations (documented in the reference)
4. Register the composition in `Root.tsx` with correct dimensions:
   ```tsx
   <Composition
     id="DescriptiveName"
     component={ComponentName}
     durationInFrames={SECONDS * 30}
     fps={30}
     width={1080}
     height={1920}
   />
   ```

### Step 4: Preview and Iterate

1. Render a still at ~70% of total frames (where all elements are visible):
   ```bash
   npx remotion still src/index.ts CompositionId /tmp/preview.png --frame=FRAME
   ```
2. Show the preview to the user (Read the PNG)
3. Iterate on layout, sizing, spacing based on feedback
4. Compare with reference screenshot if one was provided

### Step 5: Render Final Video

```bash
npx remotion render src/index.ts CompositionId ~/Desktop/YYMMDD-story-name.mp4 \
  --crf=10 --codec=h264
```

Output: MP4 file on Desktop, ready for Instagram upload.

## Design Rules

These rules are non-negotiable. They come from the StrongerYou brand system and
the specific visual language established across Nicol's Instagram Stories.

1. **Background:** Always `#F8EDE3` (warm cream). Never white, never dark.
2. **Typography:** Playfair Display Bold Italic for headlines, Noto Sans for body.
   Never Georgia, never Arial.
3. **"Anzeige":** Required on all sponsored/affiliate content. Position: top right,
   color: `#7A94CC` (accent blue), font size 26px.
4. **Animations:** Only `FadeSlideIn` with `damping: 200`. No bounce, no horizontal
   slides, no rotation. Stories are informational, not playful.
5. **Duration:** Maximum 15 seconds (Instagram auto-advance limit).
6. **Safe zones:** No content in top 15% (username area) or bottom 20% (reply bar).
   The "Anzeige" label is an exception (it mirrors Instagram's native ad labeling).
7. **Em dashes:** Forbidden. Use comma, period, or sentence restructuring.
8. **Black (#000000):** Forbidden. Use `#2C1810` for dark text.

## Reference Files

| Reference | When to load |
|-----------|-------------|
| `references/remotion-story-templates.md` | Always. Contains design tokens, template library, animation patterns, rendering pipeline |
| `references/story-strategy.md` | When deciding story type, slide flow, retention strategy |
| `references/format-specs.md` | When checking safe zones and technical specs |
| `references/affiliate-compliance.md` | When creating sponsored/affiliate content |
| `references/tone-of-voice.md` | When writing the text content for slides |
| `references/video-analysis-pipeline.md` | When analyzing reference videos for design token extraction |

## Remotion Skills (Agent Rules)

The Remotion project includes agent skills at
`~/Desktop/remotion-stories/.claude/skills/remotion-best-practices/`.
Load specific rule files as needed:

| Rule File | When to load |
|-----------|-------------|
| `rules/animations.md` | When writing animation code |
| `rules/timing.md` | When configuring spring/interpolate curves |
| `rules/images.md` | When embedding product images |
| `rules/fonts.md` | When loading fonts |
| `rules/sequencing.md` | When orchestrating multi-scene compositions |

## Quality Gates

Before delivering any animated Story slide:

| Gate | Check |
|------|-------|
| G1 | Dimensions are 1080x1920 at 30fps |
| G2 | Duration under 15 seconds |
| G3 | Still preview rendered and reviewed |
| G4 | Safe zones respected |
| G5 | All brand tokens used (no #000000, no neon) |
| G6 | "Anzeige" present for sponsored content |
| G7 | Slide stands alone without previous slides |
| G8 | No em dashes |
| G9 | File under 4MB |

## Anti-Patterns

| Anti-Pattern | Why |
|-------------|-----|
| Bouncy spring animations | Stories are informational, not playful |
| CSS transitions or Tailwind animate | Will not render in Remotion |
| Text in bottom 20% | Gets covered by Instagram reply bar |
| Rendering without preview first | Always still-frame check before full render |
| Hardcoded pixel positions | Use relative layout (flex, margin) for maintainability |
| More than 15 seconds | Instagram cuts off at 15s, content is lost |
| Skipping the pain-hook on standalone slides | Without context, viewers swipe past immediately |
