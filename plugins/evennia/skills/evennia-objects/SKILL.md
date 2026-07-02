---
name: evennia-objects
description: >
  Work with Evennia's Object system — the core building blocks for all in-game entities. Use when
  Codex needs to: create or modify objects (weapons, items, houses), customize object appearance
  (look command), manage object properties (location, home, destination, aliases, contents, exits),
  handle object movement (move_to), object searching (search), or work with DefaultObject subclasses
  (Object, Characters, Rooms, Exits). Triggers on "create object", "object system", "look command
  appearance", "object properties", "ObjectParent mixin", "return_appearance", or when building
  game items and entities in Evennia.
---

# Evennia Objects

All in-game objects (characters, chairs, monsters, rooms, hand grenades) are Evennia **Objects**.
Object is the core of Evennia — probably the most-used typeclass.

## Inheritance Tree
```
DefaultObject
  └─ ObjectParent (empty mixin for shared functionality)
       └─ Object (base in-game entity)
       └─ DefaultCharacter → Character
       └─ DefaultRoom → Room
       └─ DefaultExit → Exit
```

## Creating Custom Objects
```python
from typeclasses.objects import Object

class Rose(Object):
    def at_object_creation(self):
        self.db.desc = "A pretty rose with thorns."
```
Create in-game: `create/drop MyRose:flowers.Rose`
Create in code: `from evennia import create_object; create_object("typeclasses.flowers.Rose", key="MyRose")`

## Object Properties
- `aliases` — handler for aliases (aliases.add/remove)
- `location` — current containing object
- `home` — backup location (when location is destroyed)
- `destination` — linked target (mainly for Exits)
- `nicks` — nickname handler
- `account` — controlling Account
- `sessions` — connected Session list
- `has_account` — check if online account
- `contents` — list of contained objects
- `exits` — list of Exit objects inside

## Object Methods
- `msg()` — send message to user
- `search(objname, global_search=True)` — search for objects
- `execute_cmd()` — run command string
- `move_to(new_location)` — move object with all hooks
- `clear_exits()` — delete all exits
- `clear_contents()` — move all contents to home
- `delete()` — delete object
- `return_appearance(looker)` — customize look output

## Customizing Look Appearance
Override the `appearance_template` and its helper hooks:
```python
appearance_template = """
{header}
|c{name}|n
{desc}
{exits}{characters}{things}
{footer}
"""
```
Override: `get_display_name()`, `get_display_desc()`, `get_display_header()`, `get_display_footer()`, `format_appearance()`
