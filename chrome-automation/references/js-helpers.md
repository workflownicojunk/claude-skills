# Reusable JS Helpers for Chrome DevTools MCP

Inject these helpers via `evaluate_script` at the start of a workflow.
After injection, each subsequent call is ~50 tokens instead of ~300.

## Generic DOM Helper

Works on any website. Inject once, then use `_H.q()`, `_H.qAll()`, etc.

```js
() => {
  window._H = {
    // Query single element text
    q: (sel) => document.querySelector(sel)?.textContent?.trim(),

    // Query all matching elements, return text or attribute
    qAll: (sel, attr) => [...document.querySelectorAll(sel)].map(
      e => attr ? e.getAttribute(attr) : e.textContent?.trim()
    ),

    // Page status (replaces take_screenshot for orientation)
    status: () => ({
      url: location.href,
      title: document.title,
      h1: document.querySelector('h1')?.textContent?.trim(),
      ready: document.readyState
    }),

    // Wait for page load
    waitReady: () => new Promise(r => {
      const check = () => document.readyState === 'complete'
        ? r('ready') : setTimeout(check, 200);
      check();
    }),

    // Wait for specific selector
    waitFor: (sel, timeout = 10000) => new Promise((resolve, reject) => {
      const el = document.querySelector(sel);
      if (el) return resolve('found');
      const obs = new MutationObserver(() => {
        if (document.querySelector(sel)) { obs.disconnect(); resolve('found'); }
      });
      obs.observe(document.body, {childList: true, subtree: true});
      setTimeout(() => { obs.disconnect(); reject('timeout'); }, timeout);
    }),

    // Extract table data as JSON
    table: (sel) => {
      const t = document.querySelector(sel);
      if (!t) return null;
      const headers = [...t.querySelectorAll('th')].map(h => h.textContent.trim());
      return [...t.querySelectorAll('tbody tr')].map(row => {
        const cells = [...row.querySelectorAll('td')].map(c => c.textContent.trim());
        return headers.length
          ? Object.fromEntries(headers.map((h, i) => [h, cells[i]]))
          : cells;
      });
    },

    // Store/retrieve data across page navigations
    store: (key, data) => { sessionStorage.setItem(key, JSON.stringify(data)); return 'stored'; },
    load: (key) => JSON.parse(sessionStorage.getItem(key))
  };
  return 'helpers injected';
}
```

**Usage after injection:**
```js
() => _H.status()                          // page orientation
() => _H.q('.user-name')                   // single element
() => _H.qAll('table a', 'href')           // all links in table
() => _H.table('#data-table')              // full table as JSON
() => _H.store('myData', {foo: 'bar'})     // persist across navigation
() => _H.load('myData')                    // retrieve after navigation
```

## Unlayer Email Editor Helper (4leads)

For editing emails in the 4leads Unlayer editor.

```js
() => {
  window._U = {
    // Export current design, store it, return structure summary
    export: () => new Promise(r => unlayer.saveDesign(d => {
      sessionStorage.setItem('tpl', JSON.stringify(d));
      r({
        rows: d.body.rows.length,
        structure: d.body.rows.map((row, i) => ({
          i,
          cols: row.columns?.length,
          types: row.columns?.flatMap(c => c.contents?.map(x => x.type))
        })),
        len: JSON.stringify(d).length
      });
    })),

    // Load stored design with optional text replacements
    // mods: {rowIndex: "new HTML content"} for text content in that row
    load: (mods) => new Promise(r => {
      const d = JSON.parse(sessionStorage.getItem('tpl'));
      if (mods) Object.entries(mods).forEach(([i, html]) => {
        const txt = d.body.rows[+i]?.columns?.[0]?.contents?.find(c => c.type === 'text');
        if (txt) txt.values.text = html;
      });
      unlayer.loadDesign(d);
      r('design loaded');
    }),

    // Get text content of a specific row
    rowText: (rowIdx) => new Promise(r => unlayer.saveDesign(d => {
      const txt = d.body.rows[rowIdx]?.columns?.[0]?.contents?.find(c => c.type === 'text');
      r(txt?.values?.text || null);
    })),

    // Replace image in a specific row
    replaceImage: (rowIdx, newUrl) => new Promise(r => unlayer.saveDesign(d => {
      const img = d.body.rows[rowIdx]?.columns?.[0]?.contents?.find(c => c.type === 'image');
      if (img) img.values.src = { url: newUrl };
      unlayer.loadDesign(d);
      r('image replaced');
    })),

    // Get full design as JSON string (for saving to file)
    raw: () => new Promise(r => unlayer.saveDesign(d => r(JSON.stringify(d))))
  };
  return 'unlayer helpers injected';
}
```

**Typical workflow (4 calls total):**
```js
// 1. On source email: inject + export
() => { /* inject _U */ }
() => _U.export()

// 2. Navigate to target email
// navigate_page → target URL

// 3. On target: inject + load with modifications
() => { /* inject _U */ }
() => _U.load({1: '<p>New welcome text here</p>'})
```

Note: Helpers need to be re-injected after `navigate_page` because `window._U`
does not survive navigation. But `sessionStorage` does survive within the same
origin, so stored data persists.

## 4leads Automation Builder Helper

For building automations in the 4leads cockpit editor. The flow uses jQuery UI
drag/drop and custom DOM elements that are hard to find via standard selectors.

```js
() => {
  window._4A = {
    // Get current automation status and structure
    status: () => ({
      url: location.href,
      title: document.querySelector('.p-name')?.textContent?.trim(),
      status: document.querySelector('.p-status.active')?.textContent?.trim(),
      steps: [...document.querySelectorAll('.p-row')].map(r => ({
        text: r.textContent?.trim().substring(0, 60),
        type: r.querySelector('[class*="fa-"]')?.className
      }))
    }),

    // Click the + (add action) button in the flow
    clickPlus: () => {
      const plus = document.querySelector('.fa-plus.fa-lg');
      if (plus) { plus.closest('div').click(); return 'opened add-action panel'; }
      return 'plus not found';
    },

    // Select action from the right panel by name
    selectAction: (name) => {
      const panel = document.querySelector('.p-split-load');
      if (!panel) return 'panel not open';
      const items = panel.querySelectorAll('[class*="action"], div');
      for (const el of items) {
        if (el.textContent.trim() === name && el.offsetHeight > 0) {
          el.click();
          return 'selected: ' + name;
        }
      }
      return 'not found: ' + name;
    },

    // Set automation status (values: 1=Aktiv, 0=Deaktiviert, 20=Bearbeitung, 40=Auslaufend)
    setStatus: (targetText) => {
      const box = document.querySelector('.p-status-box');
      if (!box) return 'status box not found';
      const statuses = box.querySelectorAll('.p-status');
      for (const s of statuses) {
        s.style.display = 'block';
        s.style.visibility = 'visible';
        if (s.textContent.trim() === targetText) {
          s.click();
          return 'status change requested: ' + targetText;
        }
      }
      return 'status not found: ' + targetText;
    },

    // Confirm status change dialog
    confirmActivate: () => {
      const btns = document.querySelectorAll('button, a.btn, .btn');
      for (const btn of btns) {
        if (btn.textContent.includes('Ja, Automation aktivieren')) {
          btn.click();
          return 'confirmed activation';
        }
      }
      return 'confirm button not found';
    },

    // Click speichern button (works even if off-screen)
    save: () => {
      const btns = document.querySelectorAll('button');
      for (const btn of btns) {
        if (btn.textContent.trim() === 'speichern') {
          btn.click();
          return 'saved';
        }
      }
      return 'save button not found';
    },

    // Select dropdown option in condition/action panels
    // Works for typeahead dropdowns (e.g., field selection, email selection)
    selectDropdownItem: (containsText) => {
      const items = document.querySelectorAll('.p-split-load *');
      for (const el of items) {
        if (el.children.length === 0 && el.textContent.includes(containsText) && el.offsetHeight > 0) {
          el.click();
          return 'selected: ' + el.textContent.trim().substring(0, 50);
        }
      }
      return 'not found: ' + containsText;
    }
  };
  return '4leads automation helpers injected';
}
```

**Typical automation build workflow (8 calls):**
```
1. navigate_page → cockpit editor URL
2. evaluate_script → inject _4A + status check
3. evaluate_script → _4A.clickPlus() + _4A.selectAction('Bedingung')
4. evaluate_script → configure condition fields + _4A.save()
5. evaluate_script → _4A.clickPlus() on ja-branch
6. evaluate_script → selectAction('E-Mail senden') + select email + _4A.save()
7. evaluate_script → _4A.setStatus('Aktiv')
8. evaluate_script → _4A.confirmActivate()
```

## 4leads Newsletter Wizard Helper

For activating/managing newsletters in the 4leads Newsletter UI.

```js
() => {
  window._4N = {
    // Find newsletter by name and return its edit URL
    findByName: (name) => {
      const rows = document.querySelectorAll('tr, .list-group-item, [class*="row"]');
      for (const row of rows) {
        if (row.textContent.includes(name)) {
          const link = row.querySelector('a[href*="/newsletter/edit/"]')
            || row.closest('tr')?.querySelector('a[href*="/newsletter/edit/"]');
          return link ? link.href : 'name found but no edit link';
        }
      }
      return 'not found: ' + name;
    },

    // Navigate to Wizard step (1=Einstellungen, 2=Empfänger, 3=E-Mail, 4=Prüfen)
    // Steps are StaticText elements with icons, click triggers step change
    goStep: (n) => {
      const labels = ['Einstellungen', 'Empfänger', 'E-Mail', 'Prüfen'];
      const target = labels[n - 1];
      const els = document.querySelectorAll('*');
      for (const el of els) {
        if (el.children.length === 0 && el.textContent.trim().includes(target)
            && el.offsetHeight > 0 && el.closest('.wizard, .steps, nav, [class*="step"]')) {
          el.click();
          return 'navigated to step ' + n + ': ' + target;
        }
      }
      return 'step not found: ' + target;
    },

    // Activate newsletter (on Prüfen step)
    // Radio buttons: #aStatus1 = Aktiv, #aStatus2 = Entwurf
    activate: () => {
      const radio = document.getElementById('aStatus1');
      if (!radio) return 'aktiv radio not found';
      radio.click();
      return { activated: radio.checked };
    },

    // Save + finish (clicks speichern then fertig)
    saveAndFinish: () => {
      const btns = document.querySelectorAll('button');
      let saved = false, finished = false;
      for (const btn of btns) {
        const t = btn.textContent.trim();
        if (t === 'speichern' && !saved) { btn.click(); saved = true; }
      }
      // fertig button triggers after save
      setTimeout(() => {
        for (const btn of document.querySelectorAll('button')) {
          if (btn.textContent.trim() === 'fertig') { btn.click(); finished = true; }
        }
      }, 500);
      return { saved, willFinish: true };
    },

    // Get newsletter status on Prüfen step
    status: () => ({
      recipients: document.querySelector('[class*="count"], .badge')?.textContent?.trim(),
      entwurf: document.getElementById('aStatus2')?.checked,
      aktiv: document.getElementById('aStatus1')?.checked,
      sendTime: document.body.textContent.includes('Sofort nach der Aktivierung')
        ? 'sofort' : 'geplant'
    })
  };
  return '4leads newsletter helpers injected';
}
```

**Typical newsletter activation workflow (3 calls):**
```
1. navigate_page → /email-funnel/newsletter
2. evaluate_script → inject _4N + _4N.findByName('Newsletter Name') → get URL
3. navigate_page → edit URL
4. evaluate_script → inject _4N + _4N.activate() + _4N.saveAndFinish()
```

## SPA Admin Panel Helper

For React/Vue/Angular single-page applications with client-side routing.

```js
() => {
  window._S = {
    // React state (works with React DevTools fiber)
    reactState: (sel) => {
      const el = document.querySelector(sel);
      const key = Object.keys(el || {}).find(k => k.startsWith('__reactFiber'));
      return key ? el[key]?.memoizedState : null;
    },

    // Wait for SPA route change
    waitRoute: (pathContains) => new Promise(r => {
      const check = () => location.pathname.includes(pathContains)
        ? r(location.pathname) : setTimeout(check, 300);
      check();
    }),

    // Click and wait for navigation (SPA-safe)
    clickAndWait: (sel, waitSel) => new Promise(r => {
      document.querySelector(sel)?.click();
      const check = () => document.querySelector(waitSel)
        ? r('ready') : setTimeout(check, 200);
      setTimeout(check, 500);
    })
  };
  return 'spa helpers injected';
}
```
