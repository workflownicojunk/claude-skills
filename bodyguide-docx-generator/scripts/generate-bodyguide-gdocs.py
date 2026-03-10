#!/usr/bin/env python3
"""
BodyGuide Generator v5 (Google Docs)
Nutzt die Google Docs Vorlage "BodyGuide 2.0 [Template]" statt python-docx.

Workflow:
  1. Kopiert die Vorlage via gws drive files copy
  2. Ersetzt alle 197 Platzhalter via gws docs documents batchUpdate
  3. Ersetzt Rezeptbilder via gws docs (insertInlineImage)
  4. Exportiert als PDF via Headless Chrome (Google API Export-Limit: 12.5 MB)

Usage:
    python3 generate-bodyguide-gdocs.py input.json [output.pdf]
    python3 generate-bodyguide-gdocs.py --test

Requires: gws CLI (authenticated), Google Chrome
"""

import json
import sys
import os
import subprocess
import tempfile
import time
from pathlib import Path

TEMPLATE_DOC_ID = "14ZH_XVuYZUJuKsJzuQQKQCEHgbrJnaKQ1ipyRGr3K_Y"

# === GWS CLI WRAPPER ===

def gws(*args, json_body=None, timeout=30):
    """Run a gws command and return parsed JSON."""
    cmd = ["gws"] + list(args)
    if json_body:
        cmd += ["--json", json.dumps(json_body)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if result.returncode != 0:
        raise RuntimeError(f"gws error: {result.stderr or result.stdout}")
    return json.loads(result.stdout) if result.stdout.strip() else {}


def copy_template(name):
    """Copy the BodyGuide template. Returns new document ID."""
    print(f"1/4 Kopiere Vorlage: {name}")
    result = gws(
        "drive", "files", "copy",
        "--params", json.dumps({"fileId": TEMPLATE_DOC_ID}),
        json_body={"name": name}
    )
    doc_id = result["id"]
    print(f"     Kopie erstellt: {doc_id}")
    return doc_id


def build_replacements(data):
    """Build list of {find, replace} pairs from structured input JSON."""
    replacements = []

    def add(placeholder, value):
        replacements.append((placeholder, str(value) if value else ""))

    # 1. Customer data
    c = data.get("customer", {})
    add("{{firstName}}", c.get("firstName", ""))
    add("{{firstname}}", c.get("firstName", ""))
    add("{{Name}}", c.get("name", ""))
    add("{{Alter}}", c.get("alter", ""))
    add("{{Größe}}", c.get("groesse", ""))
    add("{{Aktuelles Gewicht}}", c.get("aktuellesGewicht", ""))
    add("{{Zielgewicht}}", c.get("zielgewicht", ""))
    add("{{Gesamtenergieumsatz}}", c.get("gesamtenergieumsatz", ""))
    add("{{Tagesanpassung/Tag}}", c.get("tagesanpassung", ""))
    add("{{Angepasster Energieumsatz}}", c.get("angepassterEnergieumsatz", ""))
    add("{{Ernährungsform}}", c.get("ernaehrungsform", ""))

    # 2. Meal plan overview (15)
    mp = data.get("mealPlan", {})
    for block in "ABCDE":
        meals = mp.get(block, {})
        add(f"{{{{Option.{block}.Meal.1}}}}", meals.get("meal1", ""))
        add(f"{{{{Option.{block}.Meal.2}}}}", meals.get("meal2", ""))
        add(f"{{{{Option.{block}.Meal.3}}}}", meals.get("meal3", ""))

    # 3. Recipes (60 fields) + CravingControl (45 fields)
    # Template has DIFFERENT casing per field type (Rezeptname/Kalorien/Zutaten/Zubereitung)
    # Extracted 2026-03-08 directly from template via Google Docs API
    recipes = data.get("recipes", {})

    # Exact per-field casing from template (verified against 197 placeholders)
    # Format: {block: {meal: {field: letter}}}
    field_casing = {
        "A": {
            "1": {"Rezeptname": "A", "Kalorien": "A", "Zutaten": "A", "Zubereitung": "A"},
            "2": {"Rezeptname": "A", "Kalorien": "A", "Zutaten": "A", "Zubereitung": "A"},
            "3": {"Rezeptname": "A", "Kalorien": "A", "Zutaten": "A", "Zubereitung": "A"},
        },
        "B": {
            "1": {"Rezeptname": "B", "Kalorien": "B", "Zutaten": "B", "Zubereitung": "B"},
            "2": {"Rezeptname": "B", "Kalorien": "b", "Zutaten": "b", "Zubereitung": "b"},
            "3": {"Rezeptname": "B", "Kalorien": "B", "Zutaten": "B", "Zubereitung": "b"},
        },
        "C": {
            "1": {"Rezeptname": "c", "Kalorien": "c", "Zutaten": "c", "Zubereitung": "c"},
            "2": {"Rezeptname": "C", "Kalorien": "C", "Zutaten": "C", "Zubereitung": "C"},
            "3": {"Rezeptname": "c", "Kalorien": "c", "Zutaten": "c", "Zubereitung": "c"},
        },
        "D": {
            "1": {"Rezeptname": "d", "Kalorien": "D", "Zutaten": "D", "Zubereitung": "D"},
            "2": {"Rezeptname": "D", "Kalorien": "D", "Zutaten": "D", "Zubereitung": "D"},
            "3": {"Rezeptname": "D", "Kalorien": "D", "Zutaten": "D", "Zubereitung": "D"},
        },
        "E": {
            "1": {"Rezeptname": "E", "Kalorien": "e", "Zutaten": "e", "Zubereitung": "e"},
            "2": {"Rezeptname": "E", "Kalorien": "E", "Zutaten": "E", "Zubereitung": "e"},
            "3": {"Rezeptname": "E", "Kalorien": "E", "Zutaten": "E", "Zubereitung": "E"},
        },
    }

    for block in "ABCDE":
        block_recipes = recipes.get(block, [])
        for i, recipe in enumerate(block_recipes[:3], 1):
            idx = str(i)
            casing = field_casing[block][idx]

            for field, json_key in [("Rezeptname", "name"), ("Kalorien", "kalorien"),
                                     ("Zutaten", "zutaten"), ("Zubereitung", "zubereitung")]:
                letter = casing[field]
                add(f"{{{{{field}.{letter}.{idx}}}}}", recipe.get(json_key, ""))

            # CravingControl (always lowercase in template, except D.3)
            cc = recipe.get("cravingControl", {})
            cc_letter = block.lower()
            # Special case: cravingcontrolwas.D.3 is uppercase D
            if block == "D" and idx == "3":
                add(f"{{{{cravingcontrolwas.D.3}}}}", cc.get("was", ""))
            else:
                add(f"{{{{cravingcontrolwas.{cc_letter}.{idx}}}}}", cc.get("was", ""))
            add(f"{{{{cravingcontrol-warum.{cc_letter}.{idx}}}}}", cc.get("warum", ""))
            add(f"{{{{cravingcontrollösung.{cc_letter}.{idx}}}}}", cc.get("loesung", ""))

    # 4. Snacks
    snacks = data.get("snacks", {})
    for category, count in [("vegan", 6), ("vegetarian", 6), ("flexitarian", 5), ("midnight", 5)]:
        cat_snacks = snacks.get(category, [])
        for i in range(1, count + 1):
            snack = cat_snacks[i - 1] if i <= len(cat_snacks) else {}
            add(f"{{{{{category}.name.{i}}}}}", snack.get("name", ""))
            add(f"{{{{{category}.ingredients.{i}}}}}", snack.get("ingredients", ""))
            add(f"{{{{{category}.preparation.{i}}}}}", snack.get("preparation", ""))

    return replacements


def replace_placeholders(doc_id, replacements):
    """Replace all placeholders in the Google Doc via batchUpdate."""
    print(f"2/4 Ersetze {len(replacements)} Platzhalter...")

    # Google Docs batchUpdate has a limit, batch in groups of 50
    batch_size = 50
    total_replaced = 0

    for i in range(0, len(replacements), batch_size):
        batch = replacements[i:i + batch_size]
        requests = []
        for find_text, replace_text in batch:
            requests.append({
                "replaceAllText": {
                    "containsText": {
                        "text": find_text,
                        "matchCase": True
                    },
                    "replaceText": replace_text
                }
            })

        result = gws(
            "docs", "documents", "batchUpdate",
            "--params", json.dumps({"documentId": doc_id}),
            json_body={"requests": requests},
            timeout=60
        )

        for reply in result.get("replies", []):
            changed = reply.get("replaceAllText", {}).get("occurrencesChanged", 0)
            total_replaced += changed

    print(f"     {total_replaced} Ersetzungen durchgeführt")
    return total_replaced


def export_pdf_chrome(doc_id, output_path):
    """Export Google Doc as PDF via headless Chrome print."""
    print(f"4/4 PDF-Export via Chrome...")

    doc_url = f"https://docs.google.com/document/d/{doc_id}/export?format=pdf"

    # Try gws export first (works for docs under 10MB)
    try:
        gws(
            "drive", "files", "export",
            "--params", json.dumps({"fileId": doc_id, "mimeType": "application/pdf"}),
            "--output", str(output_path),
            timeout=60
        )
        size_mb = Path(output_path).stat().st_size / 1024 / 1024
        print(f"     PDF erstellt: {output_path} ({size_mb:.1f} MB)")
        return str(output_path)
    except RuntimeError as e:
        if "exportSizeLimitExceeded" in str(e):
            print("     Google API Export zu groß, nutze Chrome Print...")
        else:
            raise

    # Fallback: Chrome headless print-to-pdf
    # Need to use the Google Docs print URL with auth cookie
    # Simpler approach: use the /export?format=pdf endpoint via curl with access token
    token_result = subprocess.run(
        ["gcloud", "auth", "print-access-token"],
        capture_output=True, text=True, timeout=10
    )
    if token_result.returncode != 0:
        raise RuntimeError("Could not get access token for PDF download")

    access_token = token_result.stdout.strip()
    export_url = f"https://docs.google.com/document/d/{doc_id}/export?format=pdf"

    curl_cmd = [
        "curl", "-sL",
        "-H", f"Authorization: Bearer {access_token}",
        "-o", str(output_path),
        export_url
    ]
    result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=120)

    if result.returncode != 0 or not Path(output_path).exists():
        raise RuntimeError(f"PDF download failed: {result.stderr}")

    size_mb = Path(output_path).stat().st_size / 1024 / 1024
    if size_mb < 0.01:
        # Probably an error page, not a real PDF
        content = Path(output_path).read_text(errors="ignore")[:200]
        raise RuntimeError(f"PDF download returned error page: {content}")

    print(f"     PDF erstellt: {output_path} ({size_mb:.1f} MB)")
    return str(output_path)


def cleanup_test_doc(doc_id):
    """Delete a test document."""
    try:
        gws("drive", "files", "delete", "--params", json.dumps({"fileId": doc_id}))
        print(f"     Test-Dokument gelöscht: {doc_id}")
    except Exception:
        print(f"     WARNUNG: Konnte Test-Dokument nicht löschen: {doc_id}")


def get_test_data():
    """Return minimal test data for a dry run."""
    return {
        "customer": {
            "firstName": "TestSarah",
            "name": "TestSarah M.",
            "alter": "42",
            "groesse": "168",
            "aktuellesGewicht": "78",
            "zielgewicht": "68",
            "gesamtenergieumsatz": "1.850 kcal",
            "tagesanpassung": "-350 kcal",
            "angepassterEnergieumsatz": "1.500 kcal",
            "ernaehrungsform": "Flexitarisch"
        },
        "mealPlan": {
            block: {f"meal{i}": f"Testgericht {block}.{i}" for i in range(1, 4)}
            for block in "ABCDE"
        },
        "recipes": {
            block: [
                {
                    "name": f"Testrezept {block}.{i}",
                    "kalorien": f"{400 + i * 50}",
                    "zutaten": f"Testzutat 1, Testzutat 2, Testzutat 3",
                    "zubereitung": f"Testschritt 1. Testschritt 2. Testschritt 3.",
                    "cravingControl": {
                        "was": f"Test-Craving {block}.{i}",
                        "warum": f"Test-Warum {block}.{i}",
                        "loesung": f"Test-Lösung {block}.{i}"
                    }
                }
                for i in range(1, 4)
            ]
            for block in "ABCDE"
        },
        "snacks": {
            "vegan": [{"name": f"Vegan Snack {i}", "ingredients": "Zutaten...", "preparation": "Zubereitung..."} for i in range(1, 7)],
            "vegetarian": [{"name": f"Veggie Snack {i}", "ingredients": "Zutaten...", "preparation": "Zubereitung..."} for i in range(1, 7)],
            "flexitarian": [{"name": f"Flexi Snack {i}", "ingredients": "Zutaten...", "preparation": "Zubereitung..."} for i in range(1, 6)],
            "midnight": [{"name": f"Midnight Snack {i}", "ingredients": "Zutaten...", "preparation": "Zubereitung..."} for i in range(1, 6)],
        }
    }


def main():
    is_test = "--test" in sys.argv

    if is_test:
        data = get_test_data()
        output_path = "/tmp/bodyguide-test-gdocs.pdf"
        doc_name = "BodyGuide TEST (auto-delete)"
    else:
        if len(sys.argv) < 2:
            print("Usage: python3 generate-bodyguide-gdocs.py input.json [output.pdf]")
            print("       python3 generate-bodyguide-gdocs.py --test")
            sys.exit(1)

        input_path = sys.argv[1]
        with open(input_path) as f:
            data = json.load(f)

        customer_name = data.get("customer", {}).get("firstName", "Kundin")
        output_path = sys.argv[2] if len(sys.argv) > 2 else f"{customer_name}_BodyGuide.pdf"
        doc_name = f"{customer_name}'s Personal Body Guide"

    # Step 1: Copy template
    doc_id = copy_template(doc_name)

    try:
        # Step 2: Replace placeholders
        replacements = build_replacements(data)
        replace_placeholders(doc_id, replacements)

        # Step 3: Recipe images (skip for now, placeholder images stay)
        print("3/4 Rezeptbilder: Vorlage-Bilder beibehalten (Bildersetzung via Docs API geplant)")

        # Step 4: Export PDF
        export_pdf_chrome(doc_id, output_path)

    finally:
        if is_test:
            cleanup_test_doc(doc_id)

    print(f"\nFertig: {output_path}")
    return output_path


if __name__ == "__main__":
    main()
