---
name: evennia-web-admin
description: >
  Work with Evennia's Web Admin — Django admin interface for managing the game database. Use when
  Codex needs to: manage game database via web UI, link accounts to characters, build rooms in
  admin, customize admin appearance, or understand admin permissions. Triggers on "web admin",
  "admin panel", "Django admin", "admin link", "staff status", or when managing game data through
  the web interface.
---

# Evennia Web Admin

Django admin-based web interface at `http://localhost:4001/admin`.

## Access
- Requires `Staff status` flag on Account
- Only Superusers can grant it
- `User Permissions` only affect admin, **not** in-game Permissions

## Link Account ↔ Character
1. Create Account
2. Create Character object with `DefaultCmdSet`
3. Set `Puppeting Account` field
4. Click `Link to Account` button

## Build Rooms in Admin
1. Create Room-type Object
2. Add `desc` Attribute
3. Add `alias` Tag

## Build Exits
1. Create Exit-type Object
2. Set `Location` and `Destination`
3. Add `desc` Attribute and `alias` Tag

## Customize
- Templates: `evennia/web/templates/admin/`
- Backend: `evennia/web/admin/`
- Change title:
```python
from django.conf.admin import site
site.site_header = "My Game Admin"
```
