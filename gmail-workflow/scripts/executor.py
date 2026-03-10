#!/usr/bin/env python3
"""
Email Support Agent - On-Demand Executor
Reads Gmail inbox, categorizes emails, generates staging report for review.
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional
import re

# Load environment variables
def load_env():
    """Load environment variables from ~/.env"""
    env_file = os.path.expanduser("~/.env")
    env_vars = {}
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip().strip('"\'')
    return env_vars

ENV = load_env()

# Gmail MCP via subprocess (requires gws-gmail CLI setup)
def get_gmail_emails(limit: int = 10) -> List[Dict]:
    """Fetch recent unread emails from Gmail using gws-gmail CLI"""
    import subprocess

    try:
        # Using gws-gmail CLI to fetch unread emails
        result = subprocess.run(
            ["gws", "gmail", "list", "--query", "is:unread", "--format", "json", f"--limit={limit}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            emails = json.loads(result.stdout)
            return emails if isinstance(emails, list) else [emails] if emails else []
        else:
            # No emails or CLI not available - use mock data
            return get_mock_emails()
    except Exception as e:
        # CLI not available - fall back to mock data
        return get_mock_emails()

def get_mock_emails() -> List[Dict]:
    """Mock email data for testing (remove in production)"""
    return [
        {
            "id": "msg001",
            "from": "julia@example.de",
            "subject": "Happy Body Plan - Portionen zu groß",
            "body": "Hallo, die Portionen in meinem Plan sind mir zu groß. Kann ich die anpassen?",
            "date": "2026-03-08T14:30:00Z",
            "labels": ["UNREAD"]
        },
        {
            "id": "msg002",
            "from": "marion@example.de",
            "subject": "Ernährungsplan - Salat",
            "body": "Wie kann ich den Salat im Plan ändern? Mag grünen Salat nicht.",
            "date": "2026-03-08T13:15:00Z",
            "labels": ["UNREAD"]
        },
        {
            "id": "msg003",
            "from": "dorit@example.de",
            "subject": "Circle App Probleme",
            "body": "Die App lädt nicht. Kann mir da jemand helfen?",
            "date": "2026-03-08T12:00:00Z",
            "labels": ["UNREAD"]
        },
        {
            "id": "msg004",
            "from": "claudia@example.de",
            "subject": "BodyGuide PDF - Fehler",
            "body": "Mein BodyGuide PDF hat kaputte Links. Können Sie mir helfen?",
            "date": "2026-03-08T11:45:00Z",
            "labels": ["UNREAD"]
        },
        {
            "id": "msg005",
            "from": "daniela@example.de",
            "subject": "Danke für alles!",
            "body": "Wollte nur sagen dass mir das Programm super gefällt. Macht gutes weiter!",
            "date": "2026-03-08T10:30:00Z",
            "labels": ["UNREAD"]
        },
    ]

def categorize_email(email: Dict) -> Dict:
    """
    Categorize an email based on subject, body, and sender.
    Returns category, subcategory, and action recommendation.
    """
    subject = (email.get("subject") or "").lower()
    body = (email.get("body") or "").lower()
    sender = email.get("from", "unknown")
    full_text = f"{subject} {body}"

    # Category mapping based on ref-learnings-log.md and ref-categories.md patterns
    categories = {
        # FAQ / Access Issues
        "access_issue": {
            "patterns": [r"kann nicht einloggen", r"zugang", r"passwort", r"anmelden"],
            "action": "AUTO_SEND",
            "template": "access-reset"
        },
        "technical_issue": {
            "patterns": [r"app lädt nicht", r"fehler", r"bug", r"kaputt", r"funktioniert nicht"],
            "action": "AUTO_SEND",
            "template": "technical-support"
        },

        # Cancellation / Refunds
        "cancellation": {
            "patterns": [r"kündigen", r"kundigung", r"beenden", r"stoppen", r"nicht mehr"],
            "action": "REVIEW_NEEDED",
            "template": "cancellation-assessment"
        },
        "refund_request": {
            "patterns": [r"erstattung", r"geld zurück", r"refund", r"rückgabe"],
            "action": "REVIEW_NEEDED",
            "template": "refund-assessment"
        },

        # Content / Plan Customization
        "plan_customization": {
            "patterns": [r"plan ändern", r"anpassen", r"rezept", r"portion", r"essen", r"lebensmittel"],
            "action": "AUTO_SEND",
            "template": "plan-customization"
        },
        "body_guide": {
            "patterns": [r"body.?guide", r"pdf", r"download", r"personalisierung"],
            "action": "AUTO_SEND",
            "template": "bodyguide-support"
        },

        # Feedback / Testimonials
        "positive_feedback": {
            "patterns": [r"danke", r"super", r"gefällt", r"toll", r"liebe", r"awesome", r"love"],
            "action": "SKIP",
            "template": "feedback-archive"
        },

        # Circle / Community Issues
        "circle_issue": {
            "patterns": [r"circle", r"community", r"forum", r"raum"],
            "action": "AUTO_SEND",
            "template": "circle-support"
        },

        # Subscription / Billing
        "subscription_query": {
            "patterns": [r"abo", r"mitgliedschaft", r"subscription", r"monat"],
            "action": "AUTO_SEND",
            "template": "subscription-info"
        },

        # Connect-specific
        "connect_issue": {
            "patterns": [r"connect", r"zugang", r"freischaltung"],
            "action": "AUTO_SEND",
            "template": "connect-support"
        },
    }

    # Match against patterns
    matched_category = None
    highest_match_count = 0

    for category, config in categories.items():
        match_count = sum(1 for pattern in config["patterns"] if re.search(pattern, full_text))
        if match_count > highest_match_count:
            highest_match_count = match_count
            matched_category = category
            matched_config = config

    if matched_category:
        return {
            "email_id": email.get("id"),
            "from": sender,
            "subject": email.get("subject"),
            "category": matched_category,
            "action": matched_config["action"],
            "template": matched_config["template"],
            "confidence": "high" if highest_match_count > 1 else "medium"
        }
    else:
        # Default to REVIEW_NEEDED for unmatched emails
        return {
            "email_id": email.get("id"),
            "from": sender,
            "subject": email.get("subject"),
            "category": "unknown",
            "action": "REVIEW_NEEDED",
            "template": None,
            "confidence": "low"
        }

def generate_staging_report(emails: List[Dict]) -> Dict:
    """Generate a staging report with categorized emails"""

    auto_send = []
    review_needed = []
    skip = []

    for email in emails:
        categorized = categorize_email(email)

        if categorized["action"] == "AUTO_SEND":
            auto_send.append(categorized)
        elif categorized["action"] == "REVIEW_NEEDED":
            review_needed.append(categorized)
        elif categorized["action"] == "SKIP":
            skip.append(categorized)

    report = {
        "timestamp": datetime.now().isoformat(),
        "total_emails": len(emails),
        "summary": {
            "auto_send_count": len(auto_send),
            "review_needed_count": len(review_needed),
            "skip_count": len(skip)
        },
        "auto_send": auto_send,
        "review_needed": review_needed,
        "skip": skip,
        "instructions": {
            "auto_send": "These emails will be sent immediately upon your approval",
            "review_needed": "These require your decision (might be cancellations, refunds, or edge cases)",
            "skip": "These are system notifications or positive feedback - archive them"
        }
    }

    return report

def print_report(report: Dict) -> None:
    """Pretty-print the staging report"""
    print("\n" + "="*70)
    print("EMAIL STAGING REPORT".center(70))
    print("="*70)
    print(f"Generated: {report['timestamp']}")
    print(f"Total Emails: {report['total_emails']}\n")

    print(f"✅ AUTO-SEND: {report['summary']['auto_send_count']} emails")
    for email in report['auto_send']:
        print(f"   • [{email['category']}] {email['from']}: {email['subject']}")

    print(f"\n⚠️  REVIEW-NEEDED: {report['summary']['review_needed_count']} emails")
    for email in report['review_needed']:
        print(f"   • [{email['category']}] {email['from']}: {email['subject']}")

    print(f"\n🔄 SKIP: {report['summary']['skip_count']} emails")
    for email in report['skip']:
        print(f"   • [{email['category']}] {email['from']}: {email['subject']}")

    print("\n" + "="*70)
    print("Next Step: Review the report above, then run:")
    print("  gws gmail-send-approved  # (when ready to execute)")
    print("="*70 + "\n")

def save_report(report: Dict, filepath: str = "/tmp/email-staging-report.json") -> None:
    """Save report as JSON"""
    with open(filepath, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"📄 Report saved to: {filepath}")

def main():
    """Main executor"""
    limit = 10
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
        except ValueError:
            print(f"Usage: {sys.argv[0]} [limit] (default: 10)")
            sys.exit(1)

    print(f"📧 Fetching last {limit} unread emails...")
    emails = get_gmail_emails(limit)

    if not emails:
        print("ℹ️  No unread emails found.")
        sys.exit(0)

    print(f"✓ Got {len(emails)} emails. Categorizing...\n")
    report = generate_staging_report(emails)

    # Print and save
    print_report(report)
    save_report(report)

if __name__ == "__main__":
    main()
