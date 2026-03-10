---
name: ig-analyze
description: >
  API-driven Instagram post and account performance analysis. Pulls live data
  via Facebook Graph API, calculates engagement metrics, detects performance
  patterns, and benchmarks against account baselines.
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
---

# IG Analyze -- API-driven Instagram performance analysis

**Key references:**
- `references/account-baseline.md` -- current benchmarks, follower count, historical averages
- `references/scoring-system.md` -- metric definitions, scoring thresholds, weighted formulas

**CRITICAL RULE:** This skill MUST use live API data. Never guess, estimate, or fabricate metrics. If an API call fails, report the failure. Do not fill in placeholder numbers.

---

## API Authentication

Instagram data is accessed via the **Facebook Graph API** (NOT graph.instagram.com).

**Environment variables** (load with `source ~/Desktop/.env`):
- `INSTAGRAM_ACCESS_TOKEN` -- Long-Lived User Token (for ads, user-level queries)
- `META_PAGE_TOKEN` -- Page Token (for all Instagram content endpoints)
- `INSTAGRAM_BUSINESS_ACCOUNT_ID` -- Instagram Business Account ID (17841408804651544)
- `META_PAGE_ID` -- Facebook Page ID (489648017568050)

**Token selection:**
- Instagram content endpoints (media, insights, stories) require the **Page Token**
- If `META_PAGE_TOKEN` is not set or fails, derive it dynamically:
  ```bash
  source ~/Desktop/.env
  PAGE_TOKEN=$(curl -s "https://graph.facebook.com/v21.0/$META_PAGE_ID?fields=access_token&access_token=$INSTAGRAM_ACCESS_TOKEN" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
  ```
- Ad account endpoints use the User Token (`INSTAGRAM_ACCESS_TOKEN`) directly

**Base URL:** `https://graph.facebook.com/v21.0`

---

## Phase 1: Data Collection

Pull data using curl against the Facebook Graph API. Write a Python script for efficiency.

1. **Account overview:**
   ```
   GET /17841408804651544?fields=id,username,followers_count,follows_count,media_count,biography,website,profile_picture_url
   ```
   Auth: Page Token

2. **Recent media:**
   ```
   GET /17841408804651544/media?fields=id,caption,media_type,thumbnail_url,timestamp,like_count,comments_count,permalink&limit=50
   ```
   Auth: Page Token. Paginate with `after` cursor if needed.

3. **Post-level insights** (for each post):
   ```
   GET /{media-id}/insights?metric=reach,saved,shares,likes,comments,total_interactions
   ```
   Auth: Page Token.
   **IMPORTANT:** Do NOT request `impressions` or `plays` (deprecated/unsupported for Reels).
   For Reels, optionally add `ig_reels_avg_watch_time` but be prepared for it to fail.

4. **Account-level insights (time-series):**
   ```
   GET /17841408804651544/insights?metric=reach,follower_count,profile_views&period=day&since={unix}&until={unix}
   ```
   Auth: Page Token.

5. **Account-level insights (totals):**
   ```
   GET /17841408804651544/insights?metric=accounts_engaged,total_interactions,likes,comments,shares,saves,replies&metric_type=total_value&period=day&since={unix}&until={unix}
   ```
   Auth: Page Token. Note: `accounts_engaged` requires `metric_type=total_value`.

6. **Stories:**
   ```
   GET /17841408804651544/stories?fields=id,media_type,timestamp
   ```
   Auth: Page Token. Only returns currently active stories (24h window).

Bundle independent API calls where possible. Save all raw data to `/tmp/ig-analyze-data.json`.

## Phase 2: Metric Calculation

Calculate the following metrics from the collected data:

### Per-Post Metrics
| Metric | Formula |
|--------|---------|
| Engagement Rate | (likes + comments + saves + shares) / reach * 100 |
| Save Rate | saves / reach * 100 |
| DM-Send Rate | shares / reach * 100 |
| Completion Rate (Reels) | avg_watch_time / duration * 100 (requires ig_reels_avg_watch_time, may not be available) |
| Reach-to-Follower Ratio | reach / follower_count * 100 |

### Account-Level Metrics
| Metric | Formula |
|--------|---------|
| Average Engagement Rate | mean of per-post engagement rates |
| Save Rate Trend | save rate comparison: last 7 posts vs prior 7 |
| Reach Growth | (current period reach - prior period reach) / prior * 100 |
| Content Mix | % reels vs % carousels vs % single images |

Round all percentages to 2 decimal places.

## Phase 3: Pattern Detection

Analyze the calculated metrics to identify patterns:

1. **Best performers:** Top 3 posts by engagement rate. Note format, hook category, posting day/time.
2. **Worst performers:** Bottom 3 posts. Note format, hook category, posting day/time.
3. **Format comparison:** Average engagement rate per format (reel, carousel, image).
4. **Hook category analysis:** If hook-library.md categories are identifiable in captions, group performance by category.
5. **Posting time analysis:** Group by day of week and hour. Identify best and worst windows.
6. **Save rate leaders:** Top 3 posts by save rate (these indicate high-value content).

## Phase 4: Benchmark Comparison

Load `references/account-baseline.md` and compare current metrics:

| Metric | Baseline | Current | Delta | Status |
|--------|----------|---------|-------|--------|
| Engagement Rate | X% | Y% | +/-Z% | Above/Below |
| Save Rate | X% | Y% | +/-Z% | Above/Below |
| Reach-to-Follower | X% | Y% | +/-Z% | Above/Below |
| Reel Completion | X% | Y% | +/-Z% | Above/Below |

Flag any metric that is more than 20% below baseline as a warning.

## Phase 5: Quality Check

Before delivering the report, verify:

- [ ] All metrics are based on actual API data (no estimates)
- [ ] Per-post and account-level metrics are both included
- [ ] At least one actionable insight per pattern detected
- [ ] Benchmark comparison uses current account-baseline.md values
- [ ] Numbers are internally consistent (engagement rate matches component metrics)

## Phase 6: Report Output

Deliver as a structured Markdown report:

```
## Instagram Performance Report

**Period:** [date range]
**Posts analyzed:** [count]
**Follower count:** [current]

### Key Metrics (Account Average)
| Metric | Value | vs Baseline |
|--------|-------|-------------|
| Engagement Rate | X% | +/-Y% |
| Save Rate | X% | +/-Y% |
| Reach-to-Follower | X% | +/-Y% |

### Top Performers
1. [Post description] -- [engagement rate] -- [why it worked]
2. ...
3. ...

### Format Breakdown
| Format | Avg Engagement | Avg Save Rate | Count |
|--------|---------------|---------------|-------|

### Patterns Detected
- [pattern 1 with actionable recommendation]
- [pattern 2 with actionable recommendation]

### Warnings
- [any metric >20% below baseline]

### Recommendations
1. [specific, actionable recommendation]
2. [specific, actionable recommendation]
3. [specific, actionable recommendation]
```

If the user requests a specific post analysis (single post), skip account-level metrics and deliver only per-post analysis with benchmark comparison.
