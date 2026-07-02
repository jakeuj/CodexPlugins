---
name: evennia-web-api
description: >
  Work with Evennia's REST API — Django Rest Framework-based web API for external access to the
  game database. Use when Codex needs to: create external clients or editors, make API requests
  (GET/POST/PUT/PATCH), customize API endpoints, or work with Django Rest Framework in Evennia.
  Triggers on "REST API", "web API", "API endpoint", "Django REST framework", "external client",
  or when building web clients or external tools for Evennia.
---

# Evennia REST API

Django Rest Framework API at `http://localhost:4001/api`.

## Enable
```python
REST_API_ENABLED = True
```

## Endpoints
`/api/accounts/`, `/api/objects/`, `/api/characters/`, `/api/exits/`, `/api/rooms/`, `/api/scripts/`, `/api/helpentries/`

## Usage (Python)
```python
import requests

# List
response = requests.get("https://game.com/api/objects", auth=("user", "pass"))
data = response.json()  # {count, next, previous, results: [...]}

# Create
requests.post("https://game.com/api/objects", data={"db_key": "Sword"}, auth=("user", "pass"))

# Update (PUT = full, PATCH = partial)
requests.put("https://game.com/api/objects/214", data={"db_key": "SHINIER"}, auth=("user", "pass"))

# Filter
requests.get("https://game.com/api/accounts/?permission=developer", auth=("user", "pass"))
```

## Frontend
Use Axios or Fetch API from JavaScript.

## Customizing
- API code: `evennia/web/api/`
- Copy `evennia/web/api/urls.py` to `mygame/web/api/urls.py` to customize
