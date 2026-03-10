#!/usr/bin/env python3
"""
Launch Context Fetcher - Holt aktive Promotions und Preise aus Stripe.
Kombiniert mit ref-current-launch.md für vollständigen Launch-Kontext.

Gibt JSON aus mit:
- Aktive Coupons und Promo-Codes (mit Ablaufdaten)
- Connect-Preise (aktuelle und reguläre)
- BodyGuide-Coupon Status

Usage: python3 ~/.claude/skills/circle-community/scripts/fetch_launch_context.py
"""

import json
import subprocess
import os
from datetime import datetime

ENV_FILE = os.path.expanduser("~/Desktop/.env")

def load_env(key):
    with open(ENV_FILE) as f:
        for line in f:
            if line.startswith(f"{key}="):
                return line.strip().split("=", 1)[1]
    return None

def stripe_api(endpoint, stripe_key):
    result = subprocess.run(
        ["curl", "-s", f"https://api.stripe.com/v1{endpoint}",
         "-u", f"{stripe_key}:"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

def main():
    stripe_key = load_env("STRIPE_API_KEY")
    if not stripe_key:
        print(json.dumps({"error": "STRIPE_API_KEY not found in .env"}))
        return

    # Aktive Promo-Codes holen
    promos = stripe_api("/promotion_codes?active=true&limit=100", stripe_key)
    active_promos = []
    for p in promos.get("data", []):
        coupon = p.get("coupon", {})
        promo = {
            "code": p.get("code", ""),
            "coupon_name": coupon.get("name", ""),
            "percent_off": coupon.get("percent_off"),
            "amount_off": coupon.get("amount_off"),
            "max_redemptions": p.get("max_redemptions"),
            "times_redeemed": p.get("times_redeemed", 0),
            "expires_at": p.get("expires_at"),
            "metadata": p.get("metadata", {}),
            "active": p.get("active", False),
        }
        if promo["expires_at"]:
            promo["expires_at_human"] = datetime.fromtimestamp(promo["expires_at"]).strftime("%d.%m.%Y %H:%M")
        active_promos.append(promo)

    # Aktive Coupons holen (für BodyGuide-Bonus etc.)
    coupons = stripe_api("/coupons?limit=20", stripe_key)
    active_coupons = []
    for c in coupons.get("data", []):
        if c.get("valid"):
            coupon = {
                "id": c.get("id"),
                "name": c.get("name", ""),
                "percent_off": c.get("percent_off"),
                "amount_off": c.get("amount_off"),
                "duration": c.get("duration"),
                "redeem_by": c.get("redeem_by"),
                "times_redeemed": c.get("times_redeemed", 0),
                "max_redemptions": c.get("max_redemptions"),
            }
            if coupon["redeem_by"]:
                coupon["redeem_by_human"] = datetime.fromtimestamp(coupon["redeem_by"]).strftime("%d.%m.%Y %H:%M")
            active_coupons.append(coupon)

    # Connect-Produkte und Preise holen
    # Suche nach aktiven Preisen die "Connect" im Produkt-Namen haben
    prices = stripe_api("/prices?active=true&limit=100&expand[]=data.product", stripe_key)
    connect_prices = []
    for p in prices.get("data", []):
        product = p.get("product", {})
        if isinstance(product, dict):
            product_name = product.get("name", "")
        else:
            product_name = ""

        if "connect" in product_name.lower() or "strongeryou" in product_name.lower():
            price_info = {
                "price_id": p.get("id"),
                "product_name": product_name,
                "unit_amount": p.get("unit_amount"),
                "currency": p.get("currency", "eur"),
                "recurring_interval": p.get("recurring", {}).get("interval") if p.get("recurring") else None,
                "active": p.get("active"),
            }
            if price_info["unit_amount"]:
                price_info["amount_eur"] = price_info["unit_amount"] / 100
            connect_prices.append(price_info)

    output = {
        "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "active_promo_codes": active_promos,
        "active_coupons": active_coupons,
        "connect_prices": connect_prices,
        "summary": {
            "total_active_promos": len(active_promos),
            "total_active_coupons": len(active_coupons),
            "total_connect_prices": len(connect_prices),
        }
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
