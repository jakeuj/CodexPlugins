---
name: evennia-help-system
description: >
  Work with Evennia's help system — in-game documentation with subtopics and suggestions. Use when
  Codex needs to: create help entries (database/file/command), set up subtopics, configure help
  locks (view/read), customize help display, or work with the Lunr search engine. Triggers on
  "help system", "sethelp", "help entry", "help subtopic", "command docstring help", or when
  building game documentation and help topics.
---

# Evennia Help System

Evennia provides comprehensive help with subtopics and fuzzy search.
Use: `help <topic>` or `help <topic>/<subtopic>`

## Three Help Entry Types

### 1. Database (in-game)
```
sethelp <topic>[;aliases] [,category] [,lockstring] = <text>
```
Code: `from evennia import create_help_entry; create_help_entry("topic", "text", category="Cat")`

### 2. File (Python module)
```python
HELP_ENTRY_DICTS = [{"key": "Topic", "aliases": ["alt"], "category": "Cat", "text": "..."}]
```
Register: `FILE_HELP_ENTRY_MODULES = ["world.myhelp"]`

### 3. Command docstring
```python
class MyCommand(Command):
    """Help text here."""
    key = "mycommand"
    help_category = "General"
    auto_help = True
```

## Subtopics
```
Main text here.

# subtopics

## lore
Subtopic text.

### grand opening
Nested subtopic.
```
Access: `help topic`, `help topic/subtopic`, `help topic/sub/nested` (max 5 levels, fuzzy match)

## Locks
- `cmd` — can use command (failure = hidden from help entirely)
- `view` — visible in help index
- `read` — can read the content

## Priority
Command-auto-help > Db-help > File-help

## Technical
- Uses [Lunr](https://github.com/yeraydiazdiaz/lunr.py) search engine
- Long text auto-paginated (EvMore)
- `\f` for manual page breaks
