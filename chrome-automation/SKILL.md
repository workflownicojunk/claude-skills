---
name: chrome-automation
description: >
  Token-efficient Chrome DevTools MCP automation. Reduces token consumption by 60-70%
  through bundled evaluate_script calls, script injection patterns, and avoiding
  screenshots/snapshots for orientation. Use this skill whenever working with the
  Chrome DevTools MCP server, browser automation, web scraping, DOM interaction,
  form filling, or any task involving navigate_page, evaluate_script, take_screenshot,
  take_snapshot, or click. Also use when the user mentions 4leads email editor, Unlayer,
  or any web-based admin panel. Even simple browser tasks benefit from these patterns
  because every unnecessary tool call wastes tokens and time.
---

# Chrome DevTools MCP: Token-Efficient Automation

Every Chrome DevTools MCP tool call costs tokens: the request, the response, and the
reasoning text between calls. A typical browser workflow burns 12k-15k tokens when done
naively. The same workflow costs 3k-5k tokens when done right. The difference is not
about doing less work, it is about doing the same work in fewer round-trips.

## Prerequisite

Chrome must run with remote debugging enabled:
```bash
open -a 'Google Chrome' --args --remote-debugging-port=9222
```
If Chrome is already open, quit it completely, then restart with the flag.

## The 3 Principles

### 1. Bundle operations into single calls

Each tool call has overhead: the function source in the request (~200 tokens), the
response payload (~100-500 tokens), and reasoning text the model writes between calls
(~200-500 tokens). Three separate calls easily cost 1500+ tokens. One bundled call
costs ~500 tokens for the same result.

The key insight: if you need to read data, store it, AND inspect its structure, do
all three in the same `evaluate_script` call. Return a compact JSON summary.

**Bad** (3 calls, ~1500 tokens):
```
evaluate_script → export design → read response
evaluate_script → store in sessionStorage → read confirmation
evaluate_script → inspect structure → read structure
```

**Good** (1 call, ~500 tokens):
```js
() => new Promise(r => {
  unlayer.saveDesign(d => {
    sessionStorage.setItem('tpl', JSON.stringify(d));
    r(JSON.stringify({
      rows: d.body.rows.length,
      types: d.body.rows.map((row, i) => ({
        i, contents: row.columns?.flatMap(c => c.contents?.map(x => x.type))
      })),
      len: JSON.stringify(d).length
    }));
  });
});
```

Same result. One third the tokens. Apply this to every multi-step operation:
login checks, data extraction, state verification.

### 2. Never use screenshots for orientation

Screenshots encode as base64 images and cost ~2000 tokens each. They tell you
what the page looks like, but for automation you almost always need structured
data (URL, title, element presence), not visual appearance.

**Bad** (~2000 tokens): `take_screenshot` to check which page you are on

**Good** (~150 tokens):
```js
() => ({
  url: location.href,
  title: document.title,
  h1: document.querySelector('h1')?.textContent,
  form: !!document.querySelector('form'),
  ready: document.readyState
})
```

Use screenshots only for:
- Visual debugging when a layout problem is suspected
- Final verification after a visual change (once, never in loops)
- When the user explicitly asks to see what the page looks like

### 3. Inject helpers for multi-step workflows

When a workflow requires more than 3 evaluate_script calls, inject a helper object
once, then make short function calls. The injection costs ~300 tokens upfront but
each subsequent call drops to ~50 tokens instead of ~300.

```js
// Call 1: Inject helpers (~300 tokens, one-time cost)
() => {
  window._H = {
    q: (sel) => document.querySelector(sel)?.textContent?.trim(),
    qAll: (sel, attr) => [...document.querySelectorAll(sel)].map(
      e => attr ? e.getAttribute(attr) : e.textContent?.trim()
    ),
    waitReady: () => new Promise(r => {
      const check = () => document.readyState === 'complete'
        ? r('ready') : setTimeout(check, 200);
      check();
    })
  };
  return 'helpers injected';
}

// Call 2+: Short calls (~50 tokens each)
() => _H.q('h1')
() => _H.qAll('table td', 'data-id')
```

For domain-specific helpers (Unlayer, 4leads, etc.), see `references/js-helpers.md`.

## Tool Cost Matrix

| Tool | ~Tokens | When to use |
|------|---------|-------------|
| `evaluate_script` | 100-500 | Default choice. Read data, manipulate DOM, check state |
| `navigate_page` | 100 | URL navigation |
| `click` | 100 | Click a known CSS selector |
| `fill_form` | 150 | Fill multiple fields at once |
| `wait_for` | 100 | Wait for element/condition (instead of sleep) |
| `fill` | 100 | Single field (prefer fill_form for multiple) |
| `press_key` | 100 | Simulate keypress |
| `type_text` | 100 | Type into focused element |
| `take_screenshot` | 2000 | Visual debugging only, never in loops |
| `list_network_requests` | 500 | Intercept API responses |
| `get_network_request` | 500 | Read response body |
| `take_snapshot` | 5k-50k | Last resort for unknown DOM. Never in loops |
| `lighthouse_audit` | 30k | Performance audits |

## Workflow Patterns

### Pattern A: Data extraction (3 calls max)

```
1. navigate_page → target URL
2. wait_for → selector of target element
3. evaluate_script → collect data as JSON, return compact summary
```

### Pattern B: Form submission (3 calls max)

```
1. navigate_page → form URL
2. fill_form → all fields at once
3. click → submit button
```

### Pattern C: Copy state across page navigation (4 calls)

Use sessionStorage to persist data across navigations.

```
1. evaluate_script → export state + store in sessionStorage + return structure summary
2. navigate_page → target page
3. wait_for → editor/target element loaded
4. evaluate_script → load from sessionStorage, apply modifications, execute
```

### Pattern D: Multi-page scraping (2 + N calls)

```
1. evaluate_script → collect all URLs/links as JSON array
2. Per page:
   a. navigate_page → URL
   b. evaluate_script → extract data (never take_snapshot in the loop)
```

### Pattern E: API interception instead of DOM scraping

Many modern web apps use REST APIs. Reading the API response directly is often
10x more efficient than parsing the DOM.

```
1. navigate_page → load page (triggers API calls)
2. list_network_requests → find relevant API endpoints
3. get_network_request → read response body directly
```

### Pattern F: Admin panel automation (inject + call pattern)

For complex admin UIs (4leads automation builder, CMS editors, etc.) where
multiple interactions are needed, inject a domain-specific helper first.

```
1. navigate_page → admin panel URL
2. evaluate_script → inject domain helper (e.g., _4A) + get current status
3. evaluate_script → perform action + save (bundle action chains)
4. evaluate_script → verify result
```

See `references/js-helpers.md` for ready-made helpers: `_U` (Unlayer), `_4A` (4leads Automation), `_S` (SPA).

### Pattern G: 4leads Newsletter activation (4 calls)

```
1. navigate_page → /email-funnel/newsletter
2. evaluate_script → inject _4N helper + find newsletter by name → returns edit URL
3. navigate_page → edit URL (lands on Einstellungen step)
4. evaluate_script → go to step 4 (Prüfen) + set #aStatus1 (Aktiv) + click speichern + click fertig
```

Key selectors:
- Radio `#aStatus1` = Aktiv, `#aStatus2` = Entwurf (on Prüfen step)
- Wizard steps: StaticText elements containing "Einstellungen", "Empfänger", "E-Mail", "Prüfen"
- Empfänger count visible on Prüfen step

IMPORTANT: Do NOT use `take_snapshot` to read the newsletter list. Use `evaluate_script`
to query the DOM directly for the newsletter name and its edit link.

## Anti-Patterns

These patterns waste tokens. Recognizing them is key to staying efficient.

| Anti-pattern | Cost | Fix |
|-------------|------|-----|
| `take_snapshot` in loops | 50k+ per call | Use `evaluate_script` |
| Screenshot after every step | 2k per image | Only on errors or final check |
| Exploratory JS calls ("let me check...") | 500+ per call | Bundle into one call that returns everything needed |
| Verbose reasoning between tool calls | 200-500 per block | Proceed directly to next call, skip narration |
| Individual `fill` per form field | 100 per field | Use `fill_form` with all fields |
| Export, inspect, re-save as separate calls | 3 calls | Combine into 1 call |
| Checking sessionStorage survival as separate call | 200+ | Integrate check into the load call |
| `take_snapshot` to read a list page | 5k-50k | `evaluate_script` with targeted selector for the item you need |
| `take_snapshot` + `Read` (file) to parse UI | 5k+2k | Single `evaluate_script` returning only needed data |
| Sequential click(save) then click(finish) | 200+ each | Bundle in one `evaluate_script` with setTimeout for chaining |

## Reasoning Efficiency

This is the most commonly overlooked source of token waste. Between Chrome tool
calls, the model often writes explanatory paragraphs like "I can see the editor
is loaded. The page shows a form with 4 fields. Now I will export the design..."

Every word costs tokens. For Chrome workflows, proceed directly from one tool call
to the next. Only write text when communicating something the user needs to know
(errors, decisions, results).

**Bad** (~400 tokens of narration):
```
"Good, I can see the editor for email #51894 is loaded. The page shows the Unlayer
editor with the header image. Now I'll export the design and store it in
sessionStorage so it survives the navigation. After that, I'll navigate to the
target email."
→ evaluate_script(...)
```

**Good** (0 tokens of narration):
```
→ evaluate_script(...)
```

## Subagent Instructions

When delegating a Chrome task to a subagent:

1. **Specific goal**: "Export the Unlayer design from email #51894 as JSON" not "Take a look at the page"
2. **Max 10 tool calls** per subagent task. More suggests a missing strategy.
3. **Return structured JSON**, not screenshots or prose
4. **Inject helpers** when more than 3 evaluate_script calls are needed
5. **Health check**: Use `list_pages` as first call to verify Chrome connection

## Cost Benchmarks

| Task type | Expected calls | Token budget |
|-----------|---------------|-------------|
| Simple data extraction | 3-4 | ~3k |
| Login + read data | 4-6 | ~5k |
| Copy design between pages | 4-5 | ~4k |
| Multi-page scraping (5 pages) | 7-12 | ~8k |
| Form fill + submit | 3 | ~2k |

## Self-Improvement Protocol

See `~/.claude/rules/self-improvement.md` (global rule, applies to all skills).

## References

Reusable JS helpers for common platforms: `references/js-helpers.md`
