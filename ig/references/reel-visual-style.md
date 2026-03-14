# Reel Visual Style: @nicolstanzel

Based on Gemini 2.5 Pro frame-by-frame analysis of 9 published Reels (Feb 2026).
This is the ground truth. When in doubt, match these patterns, not brand guidelines.

## Core Principle

Nicol's Reels are intentionally simple. The authority comes from her presence, voice,
and content, not from visual effects. Overengineering the visuals actively hurts
authenticity because it makes the content look "produced" instead of "real".

## Visual Parameters (extracted from published Reels)

### Layout
- **Aspect ratio:** 9:16 vertical, fullscreen
- **Crop:** center_crop, object-fit: cover
- **Blur:** NEVER. No background blur, no gaussian, no bokeh fakes
- **Black bars:** NEVER. Always fullscreen video
- **Zoom effects:** NONE. No dynamic zoom, no ken burns, no scale animations

### Text Styling
- **Font:** Sans-serif bold (Arial, Helvetica). Weight 700.
- **Font NOT used in Reels:** Playfair Display, Lato, Georgia (these are for documents/presentations only)
- **Color:** White (#FFFFFF) primary
- **Shadow:** 2-8px blur, rgba(0,0,0,0.5-0.9). Always present for readability.
- **Size range:** 22px (stats/subtitles) to 64px (main hooks)
- **Alignment:** Center

### Text Background Variants (two patterns, both valid)

**Pattern A: Naked text (most common, 3 of 5 analyzed Reels)**
- White text directly on video
- Shadow only for readability
- No background box, no padding

**Pattern B: Colored background box (used in recipe/tutorial Reels)**
- White text on red (#FF0000) or dark (#000000 at 70% opacity) background
- Border radius ~5-8px
- Drop shadow on the box: 2px offset, 4px blur, rgba(0,0,0,0.4)
- Padding ~12-16px

### What is NOT in Nicol's published Reels
- No word-by-word caption highlighting
- No progress bars
- No gradient overlays (top/bottom darkening)
- No animated text entrances (no spring, no slide-in, no scale-up)
- No TikTok-style karaoke captions as default
- No background music overlay (music comes from Instagram's audio picker, not embedded)
- No watermarks or logos
- No CTA end cards with colored backgrounds

## Caption/Subtitle Display

### Default: Phrase-Level Static Text
Most Reels use **static text overlays** that appear and disappear with cuts. Not animated.

When subtitles are needed (Talk-to-Camera >30s), use **phrase-level segments**:
- 2-5 words per segment
- Follow natural speech rhythm and pauses
- Simple cut transition (instant appear/disappear, 0ms animation)
- Centered at ~50% Y position
- Same text styling as above (white, bold, shadow)

### When word-by-word IS appropriate
Only for Talk-to-Camera Reels >45s where the spoken content IS the content (no B-roll, no demos).
One Reel in the analysis (62s) used this pattern. It's the exception.

## Reel Duration Patterns (from published content)

| Duration | Format | When |
|----------|--------|------|
| 7-15s | Quick-Tip, POV Meme, Single Exercise Demo | One point, maximum impact |
| 15-30s | Exercise Demo with Stats, Recipe Quick-Version | Show + explain |
| 30-60s | Talk-to-Camera, Detailed Explanation, Myth-Bust | Deep value, phrase-level captions |

There is NO fixed 60-second template. Duration follows content, not a formula.

### Timing per format type

**Quick-Tip (7-15s):**
- 0-2s: Hook text (static overlay)
- 2-12s: Demo/content
- 12-15s: Optional closing text

**Demo (15-30s):**
- 0-1s: Hook text + stats overlay (age, muscle mass, body fat)
- 1-25s: Exercise demonstration with persistent label
- 25-30s: Closing tip or CTA text

**Talk-to-Camera (30-60s):**
- 0-3s: Visual hook (text overlay or spoken)
- 3-55s: Content with phrase-level captions
- 55-60s: Spoken CTA ("Folge mir" / "Speicher dir das")

## Stats Overlay Pattern

Nicol frequently shows her stats as credibility markers:
- "53 Jahre | 22kg Muskelmasse | 11% Koerperfett"
- Position: top-left or right-center
- Size: small (22-28px)
- Duration: first 3-5 seconds, then fades or persists
- White text, no background

## Production Checklist

Before delivering any Reel concept, verify:
- [ ] No blur effects specified
- [ ] No animated text entrances
- [ ] No progress bar
- [ ] No gradient overlay
- [ ] Font is sans-serif bold (not Playfair)
- [ ] Duration matches content type (not forced to 60s)
- [ ] Caption display is phrase-level or static (not word-by-word unless >45s talk-to-camera)
- [ ] Text styling matches Pattern A or Pattern B above
