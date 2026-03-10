# Remotion Story Templates: Animated Instagram Story Slides

Comprehensive reference for building animated 9:16 Instagram Story slides using Remotion.
These templates transform static Story concepts into polished, animated video clips
that outperform static image slides in watch time and tap-through rate.

## Table of Contents

1. [Project Setup](#project-setup)
2. [Design System](#design-system)
3. [Template Library](#template-library)
4. [Animation Patterns](#animation-patterns)
5. [Rendering Pipeline](#rendering-pipeline)
6. [Quality Checklist](#quality-checklist)

---

## Project Setup

### Remotion Project Location

```
~/Desktop/remotion-stories/
├── public/              # Static assets (product images, logos, backgrounds)
├── src/
│   ├── Root.tsx          # Composition registry (all templates registered here)
│   ├── index.ts          # Entry point
│   ├── components/
│   │   └── animations/
│   │       └── FadeSlideIn.tsx  # Shared animation primitive (spring fade + slide)
│   └── templates/
│       └── slides/
│           └── ProductCTASlide.tsx  # Product CTA template (first template)
├── package.json
└── remotion.config.ts
```

### Base Composition Config

Every Story composition uses these exact settings:

```tsx
<Composition
  id="TemplateName"
  component={TemplateComponent}
  durationInFrames={N}    // Calculate: seconds * 30
  fps={30}
  width={1080}
  height={1920}
/>
```

| Property | Value | Why |
|----------|-------|-----|
| Width | 1080px | Instagram Story standard |
| Height | 1920px | 9:16 aspect ratio |
| FPS | 30 | Smooth animation, Instagram standard |
| Codec | H.264 | Universal compatibility |
| CRF | 10 | High quality, reasonable file size |

### Required Packages

```bash
npx remotion add @remotion/google-fonts
```

### Duration Guidelines

| Content Density | Duration | Frames (30fps) |
|----------------|----------|----------------|
| Simple CTA (2-3 elements) | 8-10s | 240-300 |
| Product showcase (4-6 elements) | 10-13s | 300-390 |
| Educational (6-8 elements) | 12-15s | 360-450 |

Instagram Stories auto-advance after 15 seconds. Stay under 15s for single slides.

---

## Design System

### StrongerYou / Nicol Stanzel Brand Tokens

These tokens match the established brand from Canva templates and previous Story designs.

#### Colors

| Token | HEX | Usage |
|-------|-----|-------|
| `background` | `#F8EDE3` | Slide background (warm cream) |
| `title` | `#2C1810` | Headlines, bold text, product names |
| `subtitle` | `#5C4A42` | Body text, descriptions, supporting copy |
| `label` | `#96827D` | Captions, footnotes, "Anzeige" label |
| `accent` | `#7A94CC` | "Anzeige" text, CTA highlights, benefit lines |
| `ctaBg` | `#FFFFFF` | Button backgrounds |
| `divider` | `#D4C4B8` | Thin separator lines |

**Forbidden colors:** `#000000` (use `#2C1810`), any saturated neon, pure blue/red backgrounds.

#### Typography

| Role | Font | Weight | Style | Import |
|------|------|--------|-------|--------|
| Headlines | Playfair Display | 700 | Italic | `@remotion/google-fonts/PlayfairDisplay` |
| Body | Noto Sans | 400, 600, 700 | Normal | `@remotion/google-fonts/NotoSans` |

Font loading pattern:
```tsx
import { loadFont as loadPlayfair } from "@remotion/google-fonts/PlayfairDisplay";
import { loadFont as loadNotoSans } from "@remotion/google-fonts/NotoSans";

const { fontFamily: playfairFamily } = loadPlayfair("normal", {
  weights: ["700"], subsets: ["latin"],
});
const { fontFamily: notoFamily } = loadNotoSans("normal", {
  weights: ["400", "600", "700"], subsets: ["latin"],
});
```

#### Sizing Reference

| Element | Font Size | Line Height |
|---------|-----------|-------------|
| Main headline (Playfair) | 68-78px | 1.2 |
| Product name | 36-38px | 1.3 |
| Product description | 28-30px | 1.4 |
| Pain-hook text | 36px | 1.5 |
| Pain-hook emphasis | 36px bold | 1.5 |
| CTA text | 28-34px | 1.4 |
| Benefit line | 30px italic | 1.4 |
| "Anzeige" label | 26px | 1.0 |
| Button text (SUNDAY etc.) | 36-38px | 1.0 |
| Rabattcode | 42-44px bold | 1.2 |

#### Layout Spacing

| Between | Margin |
|---------|--------|
| Top edge to "Anzeige" | 55px |
| "Anzeige" to first content | 120px from top |
| Between major sections | 40-55px |
| Product images gap | 50px |
| Divider line to next section | 40px top + 40px bottom |
| Horizontal padding | 70-80px left/right |

---

## Template Library

### Template 1: Product CTA with Pain-Hook

**Use case:** Affiliate/Sponsored Stories, product recommendations, link-sticker slides.

**Structure:**
```
1. "Anzeige" (oben rechts)
2. Pain-Hook (2 Zeilen: Problem + Verstärker)
3. Headline (Playfair, "Mein System" / "Meine Routine")
4. Produktbilder (2 nebeneinander oder 3 in Reihe)
5. Produktnamen + Kurzbeschreibung
6. Benefit-Line (kursiv, Accent-Farbe)
7. Trennlinie
8. Rabattcode
9. CTA ("Kommentiere X" + Button + Subtext)
```

**Animation Timeline:**
| Delay (s) | Element | Animation |
|-----------|---------|-----------|
| 0.2 | "Anzeige" | Fade-in + slide down |
| 0.3 | Pain line 1 | Fade-in + slide up |
| 0.9 | Pain line 2 (emphasis) | Fade-in + slide up |
| 1.6 | Headline | Fade-in + slide up |
| 2.2 | Product images | Fade-in + slide up |
| 3.0-4.2 | Product names + descriptions | Staggered fade-in (0.4s apart) |
| 4.8 | Benefit line | Fade-in + slide up |
| 5.2 | Divider | Fade-in |
| 5.5 | Rabattcode | Fade-in + slide up |
| 6.2-6.9 | CTA elements | Staggered fade-in |

**Duration:** 13s (390 frames)

**Reference Implementation:** `~/Desktop/remotion-stories/src/Slide4CTA.tsx`

### Template 2: Educational Reveal

**Use case:** "Wusstest du...?", Mythbusting, Quick Tips.

**Structure:**
```
1. Hook-Frage (gross, zentriert)
2. Pause (0.8s, nur Frage sichtbar)
3. Antwort-Block (Fade-in)
4. Visual (Icon/Illustration oder Produktbild)
5. Takeaway (1 Satz, bold)
6. CTA ("Mehr dazu im Reel" / "Speichern!")
```

**Animation Timeline:**
| Delay (s) | Element | Animation |
|-----------|---------|-----------|
| 0.3 | Hook-Frage | Fade-in + slide up |
| 1.5 | Antwort Block | Fade-in + slide up |
| 2.5 | Visual | Scale from 0.8 to 1.0 + fade |
| 4.0 | Takeaway | Fade-in + slide up |
| 5.5 | CTA | Fade-in + subtle pulse |

**Duration:** 10s (300 frames)

### Template 3: Testimonial / Social Proof

**Use case:** Kundenstimmen, Vorher/Nachher, Ergebnisse.

**Structure:**
```
1. Headline ("Das sagen unsere Kundinnen")
2. Zitat-Block (mit Anführungszeichen, leicht eingerückt)
3. Name + Kontext ("Sandra, 34 | 8 Wochen Connect")
4. Ergebnis-Visual (Vorher/Nachher oder Kennzahl)
5. CTA
```

### Template 4: Countdown / Urgency

**Use case:** Launch, Deadline, Sale.

**Structure:**
```
1. Headline ("Noch 3 Tage")
2. Grosse Zahl (animiert, spring bounce)
3. Was endet / startet
4. Benefit-Reminder
5. CTA + Code
```

---

## Animation Patterns

### Core: FadeSlideIn Component

The universal animation primitive for Story slides. Every element uses this.

```tsx
const FadeSlideIn: React.FC<{
  children: React.ReactNode;
  delay: number;        // In seconds
  direction?: "up" | "down";
  distance?: number;    // Pixels, default 25
}> = ({ children, delay, direction = "up", distance = 25 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame,
    fps,
    delay: Math.round(delay * fps),
    config: { damping: 200 },           // Smooth, no bounce
    durationInFrames: Math.round(0.45 * fps),  // 0.45s per element
  });

  const translateY = interpolate(
    progress,
    [0, 1],
    [direction === "up" ? distance : -distance, 0]
  );

  return (
    <div style={{ opacity: progress, transform: `translateY(${translateY}px)` }}>
      {children}
    </div>
  );
};
```

**Design rationale:** `damping: 200` creates a smooth reveal without bounce. Stories are
informational, not playful. The 0.45s duration matches the reference InnoNature Story
cadence (rapid enough to hold attention, slow enough to feel deliberate).

### Stagger Pattern

Elements appear in sequence with consistent intervals. The interval between elements
creates a reading rhythm that guides the viewer's eye.

| Content density | Interval between elements |
|----------------|--------------------------|
| Dense (8+ elements) | 0.3-0.4s |
| Medium (5-7 elements) | 0.4-0.6s |
| Sparse (3-4 elements) | 0.6-0.8s |

Group related elements (e.g., product name + description) with tighter intervals (0.3s)
and separate groups with wider gaps (0.6s+).

### CTA Pulse

Subtle scale pulse on the main action element after all content is visible:

```tsx
const pulseProgress = interpolate(
  frame,
  [8.5 * fps, 9 * fps, 9.5 * fps, 10 * fps, 10.5 * fps],
  [1, 1.035, 1, 1.035, 1],
  { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
);

<div style={{ transform: `scale(${pulseProgress})` }}>
  {/* CTA Button */}
</div>
```

### Forbidden Animations

| Animation | Why forbidden |
|-----------|--------------|
| CSS transitions / keyframes | Will not render in Remotion |
| Tailwind animate classes | Will not render in Remotion |
| Bouncy springs (`damping < 10`) | Stories are informational, not playful |
| Horizontal slides | Conflicts with Story swipe gesture mental model |
| Rotation | Disorienting on mobile, reduces readability |
| Scale > 1.1x on text | Blurs text during animation |

---

## Rendering Pipeline

### Preview (during development)

```bash
cd ~/Desktop/remotion-stories
npx remotion studio
# Opens http://localhost:3000 with live preview
```

### Render Still (for approval)

```bash
npx remotion still src/index.ts CompositionId /tmp/preview.png --frame=FRAME_NUMBER
```

Pick a frame where all elements are visible (usually 70% of total frames).

### Render Video (final output)

```bash
npx remotion render src/index.ts CompositionId ~/Desktop/YYMMDD-story-name.mp4 \
  --crf=10 --codec=h264
```

| Setting | Value | Why |
|---------|-------|-----|
| CRF | 10 | High quality, ~1.5MB for 13s |
| Codec | H.264 | Universal Instagram compatibility |
| Output format | .mp4 | Required by Instagram |

### File Naming

Follow PARA convention: `YYMMDD-story-description.mp4`

Example: `260310-slide4-cta-story.mp4`

### Asset Preparation

Product images go in `~/Desktop/remotion-stories/public/`:
- Copy images: `cp source.jpeg public/product-name.jpeg`
- Use `<Img src={staticFile("product-name.jpeg")} />` in code
- White/transparent background images work best on cream background
- No preprocessing needed for properly lit product shots

---

## Quality Checklist

Before delivering any Remotion Story slide:

| # | Check | Pass Criteria |
|---|-------|--------------|
| 1 | Dimensions | 1080x1920 (9:16) |
| 2 | Duration | Under 15 seconds |
| 3 | Safe zones | No important content in top 15% or bottom 20% |
| 4 | Font readability | All text readable at arm's length on phone |
| 5 | Color compliance | Only brand tokens used, no `#000000`, no neon |
| 6 | Animation smoothness | No janky transitions, consistent stagger rhythm |
| 7 | Pain/Context | Slide stands alone, understandable without previous slides |
| 8 | "Anzeige" | Present for all sponsored/affiliate content |
| 9 | CTA clarity | Clear next action (comment keyword, link sticker, save) |
| 10 | File size | Under 4MB for Instagram upload |
| 11 | Still preview | Rendered preview reviewed before final video |
| 12 | Em dashes | Zero em dashes in any text |
