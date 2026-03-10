# Circle Admin API V2 Reference

Base URL: `https://app.circle.so/api/admin/v2`
Auth: `Authorization: Token $CIRCLE_ADMIN_API_KEY`
Community ID: 346419
Rate Limit: 60 req/min (sleep 1.1s between calls)
API Docs: `~/Desktop/Area/Community/logic/circle-api-v2.md`

## .env Loading (CRITICAL)

`source ~/Desktop/.env` does NOT reliably load CIRCLE_ADMIN_API_KEY.
Always use: `CIRCLE_KEY=$(grep '^CIRCLE_ADMIN_API_KEY=' ~/Desktop/.env | cut -d= -f2)`

## Members

### List all (paginated)
```bash
GET /community_members?community_id=346419&per_page=100&page=1
# Response: {"page":1,"per_page":100,"has_next_page":true,"count":1305,"records":[...]}
```

### Get single member
```bash
GET /community_members/{id}?community_id=346419
# Response includes: member_tags[], profile_fields[], flattened_profile_fields{}
```

### Search by email
```bash
GET /community_members?community_id=346419&search=email@example.com&per_page=1
```

## Tag Assignment (THE CORRECT WAY)

This is the most error-prone part. Only `member_tag_ids` works.

### Step 1: GET existing tags
```bash
GET /community_members/{id}?community_id=346419
# Extract: member_tags[].id -> [200831, 215031]
```

### Step 2: MERGE and PUT
```bash
PUT /community_members/{id}
{"community_id": 346419, "member_tag_ids": [200831, 215031, 230678]}
#                                           ^existing^        ^new^
```

DOES NOT WORK (silently ignored):
- `tag_ids: [...]`
- `add_tag_ids: [...]`
- `POST /member_tag_members`
- `PATCH /community_members/{id}` with tag_ids

## Tag Management

### List all tags
```bash
GET /member_tags?community_id=346419&per_page=100
# Response: {"records":[{"id":230678,"name":"connect-monthly","tagged_members_count":10},...]}
```

### Create tag (display_format REQUIRED!)
```bash
POST /member_tags
{"community_id": 346419, "name": "tag-name", "display_format": "label"}
# Without display_format -> 422 error
```

### Delete tag
```bash
DELETE /member_tags/{id}?community_id=346419
```

## Profile Fields

### Set custom profile fields
```bash
PUT /community_members/{id}
{
  "community_id": 346419,
  "custom_profile_field_values": {
    "stripe_customer_id": "cus_xxx",
    "stripe_subscription_id": "sub_xxx",
    "stripe_email": "email@example.com",
    "subscription_price": "69.00 EUR",
    "subscription_interval": "monthly"
  }
}
```

Keys (not IDs!) are used for profile fields. Available keys:
stripe_customer_id, stripe_subscription_id, stripe_email, subscription_price, subscription_interval

## Access Groups

| ID | Product |
|----|---------|
| 88537 | X.0 Coaching |
| 78507 | Connect |
| 72778 | C9 |
| 71906 | Happy Body Training |
