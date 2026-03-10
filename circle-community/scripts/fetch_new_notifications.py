#!/usr/bin/env python3
"""
Circle Notification Fetcher - Holt neue, unbeantwortete Notifications für Nico.
Speichert State in ~/Desktop/Area/Community/circle-notification-state.json

Gibt JSON aus mit allen neuen Notifications inkl. Kontext (Original-Kommentar,
Nicos vorherige Antwort, Reply-Text der Person).

Usage: python3 ~/.claude/skills/circle-community/scripts/fetch_new_notifications.py
"""

import json
import subprocess
import re
import time
import os
from pathlib import Path

STATE_FILE = os.path.expanduser("~/Desktop/Area/Community/circle-notification-state.json")
ENV_FILE = os.path.expanduser("~/Desktop/.env")

def load_env(key):
    with open(ENV_FILE) as f:
        for line in f:
            if line.startswith(f"{key}="):
                return line.strip().split("=", 1)[1]
    return None

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_notification_id": None, "answered_comment_ids": []}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def api_get_admin(endpoint, circle_key):
    result = subprocess.run(
        ["curl", "-s", f"https://app.circle.so/api/admin/v2{endpoint}",
         "-H", f"Authorization: Token {circle_key}"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

def get_jwt():
    nico_key = load_env("CIRCLE_HEADLESS_MEMBER_API_KEY_NICO")
    result = subprocess.run(
        ["curl", "-s", "-X", "POST", "https://app.circle.so/api/v1/headless/auth_token",
         "-H", f"Authorization: Bearer {nico_key}",
         "-H", "Content-Type: application/json",
         "-d", '{"email":"info@nicojunk.com"}'],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)["access_token"]

def get_notifications(jwt, per_page=50):
    result = subprocess.run(
        ["curl", "-s", f"https://app.circle.so/api/headless/v1/notifications?per_page={per_page}",
         "-H", f"Authorization: Bearer {jwt}"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout).get("records", [])

def strip_html(html):
    return re.sub(r"<[^>]+>", "", html).strip()

def main():
    state = load_state()
    circle_key = load_env("CIRCLE_ADMIN_API_KEY")
    jwt = get_jwt()

    notifications = get_notifications(jwt)

    # Filter: nur reply und mention
    relevant = [n for n in notifications if n["action"] in ("reply", "mention")]

    # Filter: nur neue (nach last_notification_id)
    if state["last_notification_id"]:
        new_notifications = []
        for n in relevant:
            if n["id"] == state["last_notification_id"]:
                break
            new_notifications.append(n)
        relevant = new_notifications

    # Filter: bereits beantwortete Comment-IDs ausschließen
    answered = set(state.get("answered_comment_ids", []))
    relevant = [n for n in relevant if n["notifiable_id"] not in answered]

    if not relevant:
        print(json.dumps({"status": "no_new", "message": "Keine neuen Notifications.", "count": 0}))
        return

    # Kontext laden für jede Notification
    output = []
    posts_cache = {}

    for n in relevant:
        notif = n.get("notifiable", {})
        post_id = notif.get("post_id")
        comment_id = n["notifiable_id"]
        parent_comment_id = notif.get("parent_comment_id")

        # Post-Kommentare laden (mit Cache)
        if post_id and post_id not in posts_cache:
            data = api_get_admin(f"/comments?post_id={post_id}&per_page=100", circle_key)
            posts_cache[post_id] = data.get("records", [])
            time.sleep(0.5)

        comments = posts_cache.get(post_id, [])

        # Den Notification-Kommentar finden
        target_comment = next((c for c in comments if c["id"] == comment_id), None)
        # Den Parent-Kommentar finden (Nicos Kommentar oder anderer)
        parent_comment = next((c for c in comments if c["id"] == parent_comment_id), None) if parent_comment_id else None

        # Kommentar-Text extrahieren
        target_text = ""
        target_user = {}
        if target_comment:
            body = target_comment.get("body", {})
            target_text = strip_html(body.get("body", "") if isinstance(body, dict) else str(body))
            target_user = target_comment.get("user", {})

        parent_text = ""
        parent_user = {}
        is_nico_parent = False
        if parent_comment:
            body = parent_comment.get("body", {})
            parent_text = strip_html(body.get("body", "") if isinstance(body, dict) else str(body))
            parent_user = parent_comment.get("user", {})
            is_nico_parent = parent_user.get("email") == "info@nicojunk.com"

        entry = {
            "notification_id": n["id"],
            "action": n["action"],
            "comment_id": comment_id,
            "parent_comment_id": parent_comment_id,
            "post_id": post_id,
            "post_title": n.get("notifiable_title", ""),
            "space": n.get("space_title", ""),
            "actor_name": n.get("actor_name", ""),
            "actor_email": target_user.get("email", ""),
            "comment_text": target_text[:500],
            "parent_author": parent_user.get("name", ""),
            "parent_is_nico": is_nico_parent,
            "parent_text": parent_text[:300],
            "url": n.get("action_web_url", ""),
        }
        output.append(entry)

    print(json.dumps({
        "status": "new_notifications",
        "count": len(output),
        "notifications": output
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
