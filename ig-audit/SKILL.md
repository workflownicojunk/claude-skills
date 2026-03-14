---
name: ig-audit
description: >
  Full Instagram content audit with parallel subagent delegation. Fetches
  recent posts via Facebook Graph API, spawns specialized analysis agents in parallel,
  aggregates results into a unified report with an IG Health Score (0-100).
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
---

# IG Audit -- Full Instagram content audit with parallel agent delegation

**Key references:**
- `references/scoring-system.md` -- metric definitions, scoring thresholds
- `references/account-baseline.md` -- current benchmarks, historical averages
- `references/format-specs.md` -- format requirements, dimension specs

---

## API Authentication

Instagram data is accessed via the **Facebook Graph API** at `https://graph.facebook.com/v21.0`.
Do NOT use `graph.instagram.com` (that endpoint rejects Page Tokens).

**Environment variables** (load with `source ~/Desktop/.env`):
- `INSTAGRAM_ACCESS_TOKEN` -- Long-Lived User Token
- `META_PAGE_TOKEN` -- Page Token (required for Instagram content endpoints)
- `INSTAGRAM_BUSINESS_ACCOUNT_ID` -- IG Business Account ID (e.g. 17841408804651544)
- `META_PAGE_ID` -- Facebook Page ID (e.g. 489648017568050)

**Token derivation:** If `META_PAGE_TOKEN` fails or is stale, derive a fresh one:
```bash
source ~/Desktop/.env
PT=$(curl -s "https://graph.facebook.com/v21.0/$META_PAGE_ID?fields=access_token&access_token=$INSTAGRAM_ACCESS_TOKEN" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
```

## Phase 1: Data Collection

Write a Python script that collects all data in one pass. Use the Page Token for all Instagram endpoints.

### Endpoints

1. **Account info:**
   `GET /{IG_ID}?fields=id,username,followers_count,follows_count,media_count,biography,website,profile_picture_url`

2. **Recent posts (50):**
   `GET /{IG_ID}/media?fields=id,caption,media_type,thumbnail_url,timestamp,like_count,comments_count,permalink&limit=50`
   Paginate with `after` cursor if needed.

3. **Post insights (per post):**
   `GET /{media_id}/insights?metric=reach,saved,shares,likes,comments,total_interactions`
   **IMPORTANT:** Do NOT request `impressions` or `plays` (deprecated for Reels in v22+).

4. **Account insights (time-series, 30 days):**
   `GET /{IG_ID}/insights?metric=reach,follower_count,profile_views&period=day&since={30d_ago}&until={now}`

5. **Account insights (totals, 30 days):**
   `GET /{IG_ID}/insights?metric=accounts_engaged,total_interactions,likes,comments,shares,saves,replies&metric_type=total_value&period=day&since={30d_ago}&until={now}`
   Note: `accounts_engaged` requires `metric_type=total_value`.

6. **Stories:**
   `GET /{IG_ID}/stories?fields=id,media_type,timestamp`

Save all raw data to `/tmp/ig-audit-data.json` before spawning analysis agents.

**CRITICAL:** All analysis must be based on actual API data. If an API call fails, report the failure and reduce scope accordingly. Never fabricate data.

## Phase 2: Agent Delegation

Spawn **6 analysis agents in parallel**, each focused on a specific audit dimension. Each agent receives the collected data and its specific analysis brief.

### Agent 1: Content Analysis (ig-content)
- Content pillar distribution (what topics are covered, frequency)
- Caption quality (length, hook presence, CTA inclusion)
- Content type mix (educational, entertaining, promotional, personal)
- Topic gaps and oversaturation

### Agent 2: Engagement Analysis (ig-engagement)
- Engagement rate by format, topic, and posting time
- Save rate and share rate trends
- Comment sentiment overview (positive, neutral, negative, questions)
- DM generation potential (share rate as proxy)

### Agent 3: Creative Analysis (ig-creative)
- Visual consistency (brand colors, fonts, style)
- Cover/thumbnail quality assessment
- Video production quality indicators (completion rate as proxy)
- Hook effectiveness by category

### Agent 4: Growth Analysis (ig-growth)
- Follower growth rate and trajectory
- Reach-to-follower ratio trend
- Viral content identification (reach >> follower count)
- Audience growth sources (if available from insights)

### Agent 5: Competitor Benchmark (ig-competitor)
- Compare key metrics against account-baseline.md benchmarks
- Identify format or content gaps vs industry standards
- Note any emerging trends the account is missing

### Agent 6: Compliance Check (ig-compliance)
- Affiliate disclosure compliance (Kennzeichnungspflicht)
- Content rule violations (check against content-rules.md)
- Posting frequency consistency
- Bio optimization status

Each agent writes its findings to a temporary file. Collect all results before proceeding.

## Phase 3: Result Aggregation

Collect outputs from all 6 agents and merge into a unified dataset:

1. Read all agent output files.
2. Identify conflicting assessments between agents and resolve.
3. Rank findings by impact (high, medium, low).
4. Group related findings across agents into themes.

## Phase 4: IG Health Score

Calculate the IG Health Score (0-100) using weighted dimensions:

| Dimension | Weight | Score Range | Source Agent |
|-----------|--------|-------------|-------------|
| Content Quality | 20% | 0-100 | ig-content |
| Engagement Performance | 25% | 0-100 | ig-engagement |
| Creative Quality | 15% | 0-100 | ig-creative |
| Growth Trajectory | 20% | 0-100 | ig-growth |
| Competitive Position | 10% | 0-100 | ig-competitor |
| Compliance | 10% | 0-100 | ig-compliance |

### Scoring Guide
- **90-100:** Elite. Top 5% of accounts in this niche.
- **75-89:** Strong. Performing above average with clear strengths.
- **60-74:** Average. Solid foundation but significant optimization potential.
- **40-59:** Underperforming. Multiple areas need immediate attention.
- **0-39:** Critical. Fundamental strategy overhaul required.

Calculate each dimension score based on the agent findings, then compute the weighted total.

## Phase 5: Prioritized Action Plan

Create a prioritized list of improvements:

### Immediate (This Week)
- Max 3 high-impact, low-effort actions
- Each must reference a specific finding from the audit

### Short-Term (Next 30 Days)
- 3-5 strategic changes
- Include expected impact on specific metrics

### Long-Term (60-90 Days)
- 2-3 structural improvements
- May require new content types, tools, or workflows

## Phase 6: Quality Check

Before delivering the report, verify:

- [ ] All 6 agent dimensions are represented in the final report
- [ ] IG Health Score is calculated correctly (weights sum to 100%)
- [ ] Every recommendation is tied to a specific data point
- [ ] No fabricated data (all numbers trace back to API responses)
- [ ] Action plan items are specific and actionable (not vague advice)
- [ ] Report is readable without prior context

## Phase 7: Delivery

Output as a comprehensive Markdown report:

```
## Instagram Audit Report

**Account:** [handle]
**Period:** [date range]
**Posts Analyzed:** [count]
**IG Health Score:** [XX / 100] -- [rating label]

### Score Breakdown
| Dimension | Score | Status |
|-----------|-------|--------|
| Content Quality | XX | [label] |
| Engagement | XX | [label] |
| Creative | XX | [label] |
| Growth | XX | [label] |
| Competitive Position | XX | [label] |
| Compliance | XX | [label] |

### Key Findings
1. [finding with data]
2. [finding with data]
3. [finding with data]

### Strengths
- [strength 1]
- [strength 2]

### Critical Issues
- [issue 1 with impact]
- [issue 2 with impact]

### Action Plan

#### Immediate (This Week)
1. [action] -- Expected impact: [metric improvement]

#### Short-Term (30 Days)
1. [action] -- Expected impact: [metric improvement]

#### Long-Term (60-90 Days)
1. [action] -- Expected impact: [metric improvement]
```

Save the report to the location specified by the user, or to `/tmp/ig-audit-report.md` by default.
