---
name: evennia-prototypes
description: >
  Work with Evennia's Prototype and Spawner system — define and create objects from templates.
  Use when Codex needs to: create prototype dictionaries, use the spawner to create objects, define
  protfuncs, manage prototype inheritance, or use the OLC (object layout console) to create/save
  prototypes. Triggers on "prototype system", "spawner", "create object from template", "protfunc",
  "OLC", "spawn command", or when building object creation systems.
---

# Evennia Prototypes & Spawner

Prototypes define **object templates** — Python dicts describing per-instance changes.

## Prototype Dict Format
```python
{
    "prototype_key": "house",
    "key": "Large house",
    "typeclass": "typeclasses.rooms.house.House"
}
```

## Prototype Keys
- `prototype_key` — name for referencing and inheritance
- `prototype_parent` — parent prototype(s) for inheritance `(A, B)`
- `prototype_desc` — display description
- `prototype_tags` / `prototype_locks` — tags and locks

## Object Properties in Prototype
- `key`, `typeclass`, `location`, `home`, `destination`
- `permissions`, `locks` (lock string)
- `aliases`, `tags`, `attrs`
- Any other keyword → non-category Attribute

## Inheritance Rules
- `prototype_*` keys are **never inherited**
- `attrs` and `tags`: **complementary** (only replace colliding key+category)
- Other keys: **full replacement** (child value replaces parent)

## Value Types
1. Hard-coded: `{"key": "My object"}`
2. Callable: `{"key": _get_random_name}`
3. Lambda: `{"key": lambda: random.choice(["A","B"])} `
4. **Protfuncs** — `$funcname(args)` embedded in strings

## Protfuncs
Built-in: `$random()`, `$randint()`, `$left/right/center_justify()`, `$obj()`, `$eval()`, `$add/sub/mult/div()`, `$toint()`, `$protkey()`

Define custom:
```python
def red(*args, **kwargs):
    return f"|r{args[0]}|n"
```
Register in settings: `PROT_FUNC_MODULES += ["world.myprotfuncs"]`

## Storage
- **Database**: Stored as Scripts, modifiable in-game via OLC
- **Module**: In `settings.PROTOTYPE_MODULES` modules, all global dicts are prototypes

## Spawning
In-game: `spawn goblin` or `spawn {"prototype_key": "shaman", "key": "Orc shaman"}`
Code: `from evennia import spawn; spawn({"key": "Obj1"}, {"key": "Obj2"})`
