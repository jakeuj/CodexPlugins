---
name: evennia-tags
description: Manage tags on Evennia typeclasses for categorization, search, and permissions. Use when Codex needs to tag objects (mark them as 'south', 'locked', 'food', etc.), search by tag, use tags for permissions, or work with tag aliases. Triggers on requests like "tag an object", "mark as locked", "search by tag", "tag system", "object categorization", or when implementing game categorization in Evennia.
---

# Evennia Tags

Tags provide a flexible way to categorize and label typeclasses without modifying the database schema. Every typeclass has a `tags` handler.

## Adding Tags

```python
obj.tags.add("south")                    # Simple tag
obj.tags.add("locked", category="status") # Tag with category
obj.tags.add("food", category="type")    # Another category
obj.tags.add("secret", aliases=["hidden", "private"])  # With aliases
```

## Querying Tags

```python
# Get tags by key
tag = obj.tags.get("south")

# Get by category
status_tags = obj.tags.get(category="status")

# Get all tags
all_tags = obj.tags.all()

# Check existence
has_south = obj.tags.has("south")
has_locked = obj.tags.has("locked", category="status")

# Remove tag
obj.tags.remove("south")

# Clear all tags
obj.tags.clear()

# Clear by category
obj.tags.clear(category="status")
```

## Searching by Tag

```python
# Search for objects with a specific tag
south_rooms = evennia.search_object(tag="south")

# Search with tag + category
locked_objects = evennia.search_object(tag="locked", tag_category="status")

# Multiple tags (AND logic)
locked_food = evennia.search_object(tag="locked", tag_category="status",
                                     tag2="food", tag2_category="type")
```

## Tag Properties

- **Key**: The primary identifier for the tag
- **Category**: Groups related tags (e.g., "status", "type", "faction")
- **Aliases**: Alternative names that also match the tag (stored on the tag object)
- **Permission**: Optional permission check for accessing the tag

## In-Game Commands

```
> tag obj = south
> tag obj = locked,status
> tag obj/all                # View all tags on object
> tag obj/south              # Remove tag
> search south               # Search objects with 'south' tag
> search locked,status       # Search with category
```

## Tags vs Attributes

| Feature | Tags | Attributes |
|---------|------|------------|
| Purpose | Categorization, searching | Data storage |
| Persistence | Saved to DB | Saved to DB |
| Categories | Yes | Yes |
| Aliases | Yes | No |
| Searchable | Yes (via search_object) | No (need custom queries) |
| Multiple per object | Yes | Yes |
| Best for | Labels, flags, categories | Values, data, references |

## Tips

- Use tags for binary flags (locked/unlocked, visited/unvisited)
- Use categories to organize tags (status, type, faction, etc.)
- Tags are lightweight — use them freely for categorization
- For complex data that needs querying, use Attributes instead
- Aliases let you search for the same tag with different names
