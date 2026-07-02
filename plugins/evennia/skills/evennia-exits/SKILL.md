---
name: evennia-exits
description: >
  Work with Evennia's Exit system — one-way connections between rooms. Use when Codex needs to:
  create exits, customize exit behavior, handle traversal (move_between rooms), work with
  DefaultExit, override exit commands, or manage exit locks. Triggers on "exit system", "exit
  typeclass", "traverse lock", "move between rooms", "BASE_EXIT_TYPECLASS", or when building
  connections between game locations.
---

# Evennia Exits

Exits are [Objects](./evennia-objects) that **connect rooms** (or other objects) one-way.

## Inheritance
```
DefaultObject → DefaultExit → Exit (in mygame/typeclasses/exits.py)
```

## Key Properties
- `.destination` — points to the target location (required)
- Define a **Transit Command** (named after the exit) — entering the exit name moves you

> Exits are **one-way**! Bidirectional requires two Exits.

## Traversal Flow
1. Command matches Exit's command name
2. Exit checks `traverse` lock
3. Calls `at_traverse(obj, destination)`
4. `move_to(destination)` triggers hooks:
   - `obj.at_pre_move(destination)` → abort if False
   - `origin.at_pre_leave(obj, destination)`
   - `obj.announce_move_from(destination)`
   - Move executed (changes location)
   - `obj.announce_move_to(source)`
   - `destination.at_object_receive(obj, source)`
   - `obj.at_post_move(source)`
5. `at_post_traverse(obj, source)` on Exit

## Error Handling
- Check Attribute `err_traverse` for error message
- Otherwise call `at_failed_traverse(obj)`

## Customizing
```python
BASE_EXIT_TYPECLASS = "typeclasses.exits.Exit"
```
