---
name: ig-produce
description: "Autonomous end-to-end Instagram content production from raw video to publish-ready post."
user-invocable: false
license: MIT
compatibility: Requires Claude Code. Instagram Graph API credentials in .env. google-genai for video analysis.
metadata:
  author: NicoJunk
  version: "1.0.0"
  parent-skill: ig
---

# IG Produce: Autonomous Content Production

Fully autonomous content pipeline. Claude acts as the social media manager who looks at
the account data, understands what's performing and what's missing, analyzes available
material, and produces the right content to grow the account.

The user's only job is to provide raw material (video files, images) or nothing at all.
Every creative and strategic decision is made by Claude, backed by data.

## Philosophy

This sub-skill exists because the other sub-skills are tools that require the user to
know what they want. `ig-produce` is different: it figures out what the account needs
and delivers it. The user trusts Claude to make the right call, and Claude earns that
trust by basing every decision on data, not assumptions.

When in doubt about a creative choice, choose the option that optimizes for saves and
DM-sends (the two strongest algorithm signals in 2026). When two options score equally,
pick the one that's most different from the last 5 posts (content variety prevents
audience fatigue).

## Execution Flow

The flow has 5 phases. Each phase produces a concrete artifact that feeds the next.
No phase is optional. Skipping the account analysis means guessing, and guessing
violates Quality Gate G6.

### Phase 1: Account Intelligence (60 seconds)

Pull live data to understand the account's current state. This is not optional because
the right content depends entirely on what's already been posted and how it performed.

1. **Load credentials:**
   ```bash
   source ~/Desktop/.env
   ```

2. **Fetch last 25 posts** via Instagram Graph API:
   ```bash
   curl -s "https://graph.facebook.com/v21.0/$INSTAGRAM_BUSINESS_ACCOUNT_ID/media?fields=id,caption,media_type,thumbnail_url,timestamp,like_count,comments_count,permalink&limit=25&access_token=$META_PAGE_TOKEN"
   ```

3. **Fetch insights for the top 5 posts** (by like_count) to get saves, shares, reach:
   ```bash
   curl -s "https://graph.facebook.com/v21.0/{media-id}/insights?metric=reach,saved,shares,likes,comments,total_interactions&access_token=$META_PAGE_TOKEN"
   ```

4. **Compile the Account Snapshot:**
   - Last post date and time (posting recency)
   - Content mix of last 10 posts (how many Reels, Carousels, Stories, Feed posts)
   - Top 3 posts by save rate (saves / reach)
   - Bottom 3 posts by save rate
   - Average engagement rate (total_interactions / reach)
   - Hook patterns used in last 5 posts (to avoid repetition)
   - Days since last affiliate post (for spacing compliance)
   - Any content type not posted in 7+ days (content gap)

5. **Graceful degradation:** If API fails or tokens are expired, fall back to
   `references/account-baseline.md`. Clearly mark all decisions as "based on cached
   data" and warn the user.

**Artifact:** Account Snapshot (internal, not shown to user unless requested)

### Phase 2: Material Analysis (90 seconds)

If the user provided video files, analyze them with Gemini to understand what's available.
If no files were provided, skip to Phase 3 and produce a text-based concept instead.

1. **Analyze each video** using the content mode to understand what each clip shows:
   ```bash
   GEMINI_API_KEY=$(grep ^GOOGLE_API_KEY ~/Desktop/.env | cut -d'=' -f2-) \
     python3 ~/.claude/skills/ig/scripts/analyze_video.py \
     --mode content --file VIDEO_PATH --output /tmp/material-analysis-N.json
   ```

2. **For each video, extract:**
   - What's shown (talking head, B-roll, product shot, workout demo, etc.)
   - Duration and usable segments
   - Audio quality (has voiceover? music? silence?)
   - Text overlays already present
   - Overall energy level and mood
   - Technical quality (resolution, lighting, stability)

3. **Material Assessment:** Decide which clips are usable, which combine well,
   and what kind of content they naturally support. A talking head clip with good
   audio suggests a Correction or Bold Claim Reel. Silent B-roll suggests a
   text-on-screen or voiceover approach. Product close-ups suggest affiliate content.

**Artifact:** Material Report (internal)

### Phase 3: Strategic Decision (30 seconds)

This is where Claude acts as the social media manager. Combine the Account Snapshot
and Material Report to make three decisions:

#### Decision 1: Topic

Based on:
- Content gaps from Phase 1 (what hasn't been posted recently)
- Top-performing content patterns (what gets saves)
- Available material (what the videos actually show)
- Current date context (seasonal relevance, trending topics in the niche)

If the material clearly shows a product (visible brand, packaging), check whether an
affiliate partnership exists. Load `references/affiliate-compliance.md` if relevant.

#### Decision 2: Format

| Material Available | Account Needs | Decision |
|-------------------|---------------|----------|
| Talking head + good audio | Correction hook gap | Reel (talking head, 15-30s) |
| Multiple short clips | Educational content gap | Reel (montage/b-roll, 15-30s) |
| Product shots only | Affiliate content due | Carousel or Story (animated via Remotion) |
| No material provided | Any gap | Carousel concept or text-based Reel script |
| Mixed clips (talking head + b-roll) | Entertainment gap | Reel (mixed format, 30-60s) |

#### Decision 3: Hook Category

Select from the hook library based on:
- Which hook categories performed best (Phase 1 top posts)
- Which categories were used in the last 5 posts (avoid repetition)
- Which category fits the chosen topic most naturally

Strongly prefer CORRECTION hooks (proven #1 performer with 5.0-5.3% save rate)
unless the last 2 posts already used Correction. In that case, rotate to Identity
Trigger or Bold Claim.

**Artifact:** Creative Brief (shown to user for confirmation before proceeding)

```
CREATIVE BRIEF
━━━━━━━━━━━━━━
Thema:       [topic in one sentence]
Format:      [Reel / Carousel / Story] ([duration] / [slides])
Hook:        [hook category] - "[exact opening line]"
Material:    [which clips, with timestamps if segments]
CTA:         [Link in Bio / Kommentar-Keyword / Save / DM]
Begründung:  [2-3 sentences why THIS content for THIS account right now]
Affiliate:   [Ja (Partner, Code, Zeitraum) / Nein]
━━━━━━━━━━━━━━
Einverstanden? Oder soll ich eine andere Richtung gehen?
```

Wait for user confirmation before proceeding to Phase 4. This is the single
checkpoint where the user can redirect. Everything before was autonomous analysis,
everything after is autonomous production.

### Phase 4: Content Production

Based on the confirmed Creative Brief, produce the complete content package.
Route to the appropriate production logic:

#### If Reel:

Follow the standard `/ig reel` execution flow (SKILL.md lines 254-263):

1. **Load references:** format-specs.md + hook-library.md + content-rules.md
2. **Generate 3 hook variants** from the chosen category, score each, select best
3. **Write the script** with segment timing:
   - 0-3s: Hook (attention capture)
   - 3-15s: Problem/context (why this matters)
   - 15-25s: Solution/insight (the value)
   - 25-30s: CTA (what to do next)
4. **Write the caption** (500+ chars, save CTA, hook variation opener)
5. **Describe thumbnail concept**
6. **If affiliate:** Add "Werbung" as first word of caption, check spacing rule

#### If Carousel:

Follow standard carousel logic:
1. Cover slide with hook text
2. 5-8 content slides with one clear point each
3. CTA slide (save/share/comment)
4. Caption with hook variation opener

#### If Story (animated):

Route to `ig-story-remotion` sub-skill for animated production, or standard
`ig-story` for static sequences.

### Phase 5: Quality Gate + Delivery

1. **Score the content** using the full 5-category Content Quality Score
   (scoring-system.md). Every production must be scored before delivery.

2. **Quality Gate checklist:**
   - [ ] Score >= 80 (if below, auto-revise before delivering)
   - [ ] No em dashes anywhere
   - [ ] Affiliate disclosure present if applicable (first word: "Werbung")
   - [ ] No controversial opinion bait
   - [ ] Caption >= 500 characters
   - [ ] Hook uses a documented category
   - [ ] CTA matches the strategic goal

3. **If score < 80:** Identify the weakest category, revise that section,
   re-score. Repeat until >= 80 or 3 revision rounds (then deliver with
   revision notes explaining what's holding the score back).

4. **Deliver the complete package:**

```
REEL PACKAGE
━━━━━━━━━━━━

HOOK (Score: X/25)
[Opening line]

SCRIPT (Score: X/25)
[Full timed script]

CAPTION (Score: X/20)
[Complete caption with hashtags]

THUMBNAIL
[Concept description]

FORMAT COMPLIANCE (Score: X/15)
[Specs check]

ALGORITHM SIGNALS (Score: X/15)
[Save/DM optimization notes]

━━━━━━━━━━━━
TOTAL SCORE: XX/100 (Grade: X)

POSTING RECOMMENDATION
Beste Zeit: [day, time window based on account data]
Nächster Schritt: [concrete action for the user]
```

5. **Posting time recommendation:** Based on Phase 1 data, identify when the
   top-performing posts were published. Recommend a time window (not an exact
   minute). If no data is available, default to the general fitness niche
   sweet spots: Tue/Thu 7-9am, Wed/Sat 11am-1pm.

## Reference Files

| Reference | When to load |
|-----------|-------------|
| `references/account-baseline.md` | Phase 1 fallback if API fails |
| `references/algorithm-2026.md` | Phase 3 for signal priority decisions |
| `references/format-specs.md` | Phase 4 for format compliance |
| `references/hook-library.md` | Phase 3+4 for hook selection and generation |
| `references/content-rules.md` | Phase 4 for caption and CTA rules |
| `references/scoring-system.md` | Phase 5 for Content Quality Score |
| `references/affiliate-compliance.md` | Phase 3+4 if affiliate content detected |
| `references/conversion-pipeline.md` | Phase 3 for CTA strategy |
| `references/video-analysis-pipeline.md` | Phase 2 for Gemini video analysis |

## Quality Gates

| Gate | Check |
|------|-------|
| G1 | Score before delivery (mandatory, no exceptions) |
| G2 | No em dashes in any output |
| G3 | Affiliate disclosure if applicable |
| G4 | No controversial opinion hooks |
| G5 | Affiliate spacing (not within 1 day of last affiliate post) |
| G6 | No guessed metrics (API data or stated as unavailable) |
| G7 | Creative Brief shown to user before production |
| G8 | Score >= 80 or 3 revision attempts documented |

## Anti-Patterns

| Anti-Pattern | Why |
|-------------|-----|
| Asking the user what topic to post | Defeats the purpose. Use data to decide. |
| Skipping Phase 1 (account analysis) | Every decision depends on account context. Without data, you're guessing. |
| Producing without the Creative Brief checkpoint | The user needs one moment to redirect. Respect their authority. |
| Recommending the same hook category 3x in a row | Audience fatigue. Rotate categories. |
| Ignoring material analysis | If the user gave you videos, use them. Don't write a script that ignores what the clips show. |
| Optimizing for likes | Likes are the weakest signal. Optimize for saves and DM-sends. |
| Generic posting time | Use the account's actual performance data for timing. |
