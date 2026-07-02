---
name: evennia-typeclasses
description: Create and work with Evennia typeclasses - the core building blocks of an Evennia MUD game. Use when Codex needs to define new game entities (Objects, Characters, Rooms, Exits, Accounts, Scripts, Channels), understand the typeclass inheritance hierarchy, override hook methods (at_object_creation, at_init, etc.), query the database, or work with typeclass properties like key, dbref, locks, tags, and attributes. Triggers on requests like "create a typeclass", "make a new object type", "define a character", "set up a room", or when working with Evennia game entities and inheritance.
---

# Evennia Typeclasses

Typeclasses are the core data storage mechanism in Evennia. Every game entity (Accounts, Objects, Scripts, Channels) is a Python class inheriting from `evennia.typeclasses.models.TypedObject`.

## Inheritance Hierarchy

```
TypedObject (base DB model)
├── AccountDB → DefaultAccount → Account (your game dir)
├── ScriptDB → DefaultScript → Script (your game dir)
├── ChannelDB → DefaultChannel → Channel (your game dir)
└── ObjectDB → DefaultObject
    ├── Character → DefaultCharacter → Character
    ├── Room → DefaultRoom → Room
    └── Exit → DefaultExit → Exit
```

Level 1 = Django DB models. Level 2 = Evennia defaults with hooks. Level 3 = Your game dir classes.

## Creating a Typeclass

```python
from evennia import DefaultObject

class Furniture(DefaultObject):
    pass
```

Create instances with `create_*` functions (recommended) or manually:

```python
# Recommended
chair = create_object(Furniture, key="Chair")
# or by path string
chair = create_object("furniture.Furniture", key="Chair")

# Manual
chair = Furniture(db_key="Chair")
chair.save()
```

## Key Properties

All typeclasses share these fields (use wrapper names without `db_` prefix):

| Property | Type | Description |
|----------|------|-------------|
| `key` | str | Main identifier (alias: `name`) |
| `date_created` | datetime | Creation timestamp |
| `typeclass_path` | str | Python path to the class |
| `id` / `dbid` / `pk` | int | Database primary key |
| `dbref` | str | String form "#id" |

## Typeclass Handlers

Every typeclass entity has these built-in handlers:

```python
obj.tags          # TagHandler - tags.add(), tags.get(), etc.
obj.locks         # LockHandler - locks.add(), locks.get(), etc.
obj.attributes    # AttributeHandler - attributes.add(), etc.
obj.db            # Shortcut to AttributeHandler (no category)
obj.nattributes   # Non-persistent AttributeHandler
obj.ndb           # Shortcut for non-persistent attributes
```

## Hook Methods

Override hooks to customize behavior. Never overload `__init__` — use hooks instead:

```python
class MyObject(DefaultObject):
    def at_object_creation(self):
        """Called ONCE when object is first saved to DB."""
        self.db.health = 100

    def at_init(self):
        """Called EVERY TIME object is loaded into memory."""
        pass

    def at_search_result(self, search_results, display_string):
        """Called when this object is found via search."""
        pass

    def at_become(self, session):
        """Called when Account puppets this Object (Character)."""
        pass

    def at_forget(self, session, from_session):
        """Called when Account un-puppets from this Object."""
        pass
```

Common hooks by type:
- **Objects**: `at_object_creation`, `at_init`, `at_search_result`, `at_move`, `at_desc`, `at_receive`
- **Characters**: `at_become`, `at_forget`, `at_login`, `at_logout`, `at_traverse`
- **Rooms**: `at_object_receive`, `at_object_leave`, `at_look`, `at_turn`
- **Exits**: `at_traverse`
- **Accounts**: `at_login`, `at_logout`, `at_access`, `at_post_new_account`

## Querying Objects

```python
# Via command caller
matches = caller.search("sword")

# Via Evennia search functions (returns list)
sword = evennia.search_object(key="sword")

# Via Django ORM (full DB query)
matches = Furniture.objects.get(db_key="Chair")

# Find across subclasses
furniture_family = Furniture.objects.get_family(db_key="Chair")
```

## Database Fields

Database fields use `db_*` prefix. Use the wrapper name (without `db_`) for convenience — it auto-saves:

```python
# Full form
chair.db_key = "Table"
chair.save()

# Wrapper form (preferred)
chair.key = "Table"  # auto-saves
```

## Tips

- Typeclass names must be globally unique across the server
- Import new typeclass modules so Evennia can discover them
- Use `typeclass/list` in-game to see all registered typeclasses
- For migration of existing objects after code changes, search and update manually:
  ```python
  for obj in evennia.search_object(typeclass="mygame.typeclasses.furniture.Furniture"):
      obj.db.new_attr = "value"
  ```
