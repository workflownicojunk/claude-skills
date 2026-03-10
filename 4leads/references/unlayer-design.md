# Unlayer Design JSON Structure

The Unlayer design JSON has this hierarchy for finding and modifying content:

```
{
  "counters": { "u_row": N, "u_column": N, "u_content_text": N, ... },
  "body": {
    "id": "...",
    "rows": [
      {
        "id": "...",
        "cells": [1],          // column count
        "columns": [
          {
            "id": "...",
            "contents": [
              {
                "id": "...",
                "type": "text",   // or "button", "image", "html", "divider", "social"
                "values": {
                  "text": "<p>HTML content with {{placeholders}}</p>",
                  // ... other type-specific values
                }
              }
            ]
          }
        ]
      }
    ]
  }
}
```

## Content Types

### Text Block
```json
{
  "type": "text",
  "values": {
    "text": "<p>Hey {{firstname}},</p><p>Dein Code: <strong>{{field_15306}}</strong></p>",
    "textAlign": "left",
    "lineHeight": "140%",
    "linkStyle": { ... },
    "containerPadding": "10px"
  }
}
```

### Button Block
```json
{
  "type": "button",
  "values": {
    "text": "<span>Jetzt kaufen</span>",
    "href": {
      "name": "web",
      "values": {
        "href": "https://buy.stripe.com/xxx?prefilled_promo_code={{field_15306}}"
      }
    },
    "buttonColors": { "color": "#FFFFFF", "backgroundColor": "#7A94CC" },
    "size": { "autoWidth": true, "width": "100%" },
    "padding": "10px 20px",
    "borderRadius": "100px"
  }
}
```

### Image Block
```json
{
  "type": "image",
  "values": {
    "src": { "url": "https://onecdn.io/...", "width": 800, "height": 600 },
    "alt": "Description",
    "action": { "name": "web", "values": { "href": "https://..." } }
  }
}
```

### Social Block
```json
{
  "type": "social",
  "values": {
    "icons": {
      "iconType": "custom",
      "icons": [
        { "url": "https://instagram.com/nicolstanzel/", "image": "https://..." },
        { "url": "https://youtube.com/@NicolStanzel", "image": "https://..." },
        { "url": "mailto:info@nicolstanzel.de", "image": "https://..." }
      ]
    }
  }
}
```

## Finding Content by Type

To find all text that contains a placeholder:

```python
import json

def find_placeholders(design, pattern):
    """Find all occurrences of a pattern in text/button content."""
    results = []
    design_str = json.dumps(design)

    if pattern in design_str:
        for row_idx, row in enumerate(design.get('body', {}).get('rows', [])):
            for col_idx, col in enumerate(row.get('columns', [])):
                for content_idx, content in enumerate(col.get('contents', [])):
                    values = content.get('values', {})
                    text = values.get('text', '')
                    if pattern in text:
                        results.append({
                            'path': f'body.rows[{row_idx}].columns[{col_idx}].contents[{content_idx}]',
                            'type': content.get('type'),
                            'text_snippet': text[:100]
                        })
                    # Also check button href
                    href = values.get('href', {}).get('values', {}).get('href', '')
                    if pattern in href:
                        results.append({
                            'path': f'body.rows[{row_idx}].columns[{col_idx}].contents[{content_idx}].values.href',
                            'type': 'button-href',
                            'text_snippet': href[:100]
                        })
    return results
```

## Safe Find-and-Replace

The simplest and most reliable way to modify content is string replacement on the
serialized JSON. This works because placeholders and URLs are unique strings:

```python
design_str = json.dumps(design)
design_str = design_str.replace('OLD_TEXT', 'NEW_TEXT')
design = json.loads(design_str)
```

This is preferred over navigating the tree structure because it catches placeholders
in all locations (text blocks, button hrefs, HTML blocks, etc.) in one pass.
