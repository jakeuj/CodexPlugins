---
name: evennia-rooms
description: >
  Work with Evennia's Room system — in-game location containers. Use when Codex needs to: create
  rooms, modify room behavior, set room descriptions, manage room exits, work with DefaultRoom,
  or handle room-related hooks. Triggers on "room system", "room typeclass", "dig command",
  "BASE_ROOM_TYPECLASS", or when building game locations and spaces.
---

# Evennia Rooms

Rooms are [Objects](./evennia-objects) representing **locations** in the game world.

## Inheritance
```
DefaultObject → DefaultRoom → Room (in mygame/typeclasses/rooms.py)
```

## Key Points
- Room is a special Object — it has **no `location`** of its own
- Default commands like `dig`, `tunnel`, `open` create Room-type objects
- All other objects live inside a Room

## Customizing Default Room
```python
BASE_ROOM_TYPECLASS = "typeclasses.rooms.Room"
```

## Important Notes
- Default Room is simple; many contribs extend room functionality
- Room inherits all Object capabilities (msg, search, move_to, etc.)
- `mygame/typeclasses/rooms.py` is where to add custom Room behavior
