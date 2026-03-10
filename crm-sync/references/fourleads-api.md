# 4leads REST API Reference

Base URL: `https://api.4leads.net/v1`
Auth: `Authorization: Bearer $FOURLEADS_API_KEY`
Rate Limit: 1 call / 1.5s. On 429: sleep(3) then retry.
Key format: `4l.xxx.xxx`

## .env Loading

```bash
FOURLEADS_KEY=$(grep '^FOURLEADS_API_KEY=' ~/Desktop/.env | cut -d= -f2)
```

## Contact Operations

### Search by email (returns HTTP 201!)
```bash
POST /contacts/search
{"email": "user@example.com"}
# Response (HTTP 201): {"data": {"id": 3169886, "email": "...", "fname": "...", ...}}
```

HTTP 201 is NORMAL for this endpoint. It is not an error.

### Create/upsert contact
```bash
POST /contacts
{"email": "user@example.com", "fname": "Vorname", "lname": "Nachname"}
```

## Tag Operations

### Assign tag to contact (ONLY PUT!)
```bash
PUT /contacts/{contact_id}/tags/{tag_id}
# Response: 200 with full contact data
```

POST and PATCH do NOT work for tag assignment. Only PUT.

### Remove tag from contact
```bash
DELETE /contacts/{contact_id}/tags/{tag_id}
```

### Create tag
```bash
POST /tags
{"name": "tag-name"}
# Response: {"data": {"id": 43540, "name": "tag-name"}}
```

### Delete tag
```bash
DELETE /tags/{tag_id}
# Fails if tag is referenced in Make.com blueprints
```

## Custom Field Operations

### Set custom field value (ONLY PUT!)
```bash
PUT /contacts/{contact_id}/global-field-values/{field_id}
{"value": "cus_xxx"}
# Response: 200 with full contact data
```

The endpoint is NOT `/fields` or `/custom-fields`. It is `/global-field-values/{field_id}`.

### No list endpoint for fields
There is no GET endpoint to list available custom fields. Field IDs must be known in advance.
See `references/field-ids.json` for known IDs.

## n8n Integration (fleads Node)

Credential ID: `PzZd7uq7Kum2G6zQ` ("4leads")

```js
// Contact upsert
{ resource: "contact", contactEmail, contactFirstname, contactLastname }

// Tag assignment
{ resource: "contact", operation: "addATag",
  contactId: {__rl: true, value: "={{id}}", mode: "id"},
  bListOfTags: true, contactTagIdList: "={{ [TAG_ID] }}" }

// Custom field
{ resource: "contact", operation: "setValue",
  globalFieldContactId: {__rl: true, value: "={{id}}", mode: "id"},
  bSetMultiFields: true,
  fieldsToSet: {field: [{globalFieldId: {__rl: true, value: FIELD_ID, mode: "id"}, value: "..."}]} }
```
