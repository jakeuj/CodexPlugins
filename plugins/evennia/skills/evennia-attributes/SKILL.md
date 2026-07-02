---
name: evennia-attributes
description: Store and manage arbitrary data on Evennia typeclasses using Attributes. Use when Codex needs to save custom data on Objects, Characters, Rooms, Exits, Accounts, or Scripts that persists across server reboots. Covers .db shortcut, .attributes handler with categories, AttributeProperty at class level, querying by attribute, and in-memory NAttributes. Triggers on requests like "store data on object", "save custom field", "attribute system", "persistent data", "db property", or when implementing game data storage in Evennia.
---

# Evennia Attributes

Attributes store arbitrary Python data on typeclasses, persisting across server reboots. They can hold numbers, strings, lists, dicts, and database object references.

## Three Ways to Use Attributes

### 1. `.db` Shortcut (Simplest)

For attributes without a category:

```python
import evennia
obj = evennia.create_object(key="Foo")

# Set
obj.db.health = 100
obj.db.inventory = ["sword", "shield"]
obj.db.weapon = "sword"
obj.db.self_ref = obj  # store reference to another object
rose = evennia.search_object(key="rose")[0]
rose.db.has_thorns = True

# Get (returns None if not found, never raises AttributeError)
health = obj.db.health
items = obj.db.inventory
has_thorns = rose.db.has_thorns

# Get all attributes
all_attrs = obj.db.all

# Delete
del obj.db.health
```

### 2. `.attributes` Handler (With Categories)

For grouping attributes by category or dynamic access:

```python
# Add with category
obj.attributes.add("neck", gold_necklace, category="clothing")
obj.attributes.add("neck", ringmail_armor, category="armor")

# Get with category
neck_clothing = obj.attributes.get("neck", category="clothing")
neck_armor = obj.attributes.get("neck", category="armor")

# Without category (same as .db)
obj.attributes.add("helmet", "Knight's helmet")
helmet = obj.attributes.get("helmet")
```

Handler methods:
```python
obj.attributes.has("attr_name")              # Check existence
obj.attributes.get("attr_name", default=None)  # Get with default
obj.attributes.get("attr_name", raise_exception=True)  # Raise if missing
obj.attributes.add("name", value, category="cat")  # Add
obj.attributes.remove("name")                 # Remove
obj.attributes.clear()                        # Remove all
obj.attributes.all(category="cat")            # List all in category
```

### 3. `AttributeProperty` (Class-Level)

Define attributes at the typeclass level, like Django model fields:

```python
from evennia import DefaultObject, AttributeProperty

class MyObject(DefaultObject):
    health = AttributeProperty(default=100)
    inventory = AttributeProperty(default=[], setter="private")
    custom_data = AttributeProperty(100, category="bar")
```

## Non-Persistent Attributes (NAttributes)

For data that should NOT survive reboot:

```python
# Using .ndb shortcut
obj.ndb.temporary = "data"
obj.ndb.counter = 0

# Using nattributes handler
obj.nattributes.add("temp", "value")
obj.nattributes.get("temp")
```

## In-Game Commands

```
> set obj/myattr = "test"        # Create attribute
> set obj/myattr                 # View attribute
> set obj/myattr =               # Delete attribute
> set obj/all                      # List all attributes
```

## Tips

- `.db` never raises AttributeError — returns None for missing attributes
- Categories let you have same-named attributes on the same object
- Database object references stored in attributes are automatically resolved
- `AttributeProperty` provides type hints and default values at the class level
- For large text data, consider using `strattr=True` with `.attributes.add()` for serialization optimization
