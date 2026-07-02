---
name: evennia-evmenu
description: >
  Work with Evennia's EvMenu system — branching multi-choice menus for character creation, NPC
  conversations, and interactive prompts. Use when Codex needs to: create menu nodes, define
  options (goto callbacks), use template language, handle user input (yield/get_input), customize
  menu formatting, or build interactive game menus. Triggers on "menu system", "EvMenu", "branching
  menu", "multi-choice", "character creation menu", "NPC conversation", or when building interactive
  prompt systems.
---

# Evennia EvMenu

EvMenu creates **branching multi-choice menus**. Each node returns `(text, options)`.

## Basic Usage
```python
from evennia.utils import evmenu

def node_question(caller, raw_string, **kwargs):
    text = "Is your answer yes or no?"
    options = (
        {"key": ("[Y]es!", "yes"), "desc": "Answer yes.", "goto": "node_yes"},
        {"key": ("[N]o!", "no"), "desc": "Answer no.", "goto": "node_no"},
    )
    return text, options

def node_yes(caller, raw_string, **kwargs):
    return "You chose yes!", None  # None options = exit node

evmenu.EvMenu(caller, {"start": node_question, "end": node_yes}, startnode="start")
```

## Node Signature
```python
def nodename(caller, raw_string, **kwargs):
    return text, options
```
- `caller` — user of menu
- `raw_string` — input from previous node
- `kwargs` — passed from goto-callable

## Options Format
```python
{"key": ("Display", "alias1"), "desc": "Description", "goto": "next_node"}
```
- `key` tuple: first = display, rest = aliases
- `goto` = `"nodename"` | `callable` | `(callable, kwargs)`
- `goto` callable returns `("nodename", kwargs)` or `None` (re-run current node)
- `_default` key catches any free input

## Template Language
```
## node start
Your text here.
## options
key: desc -> next_node
1: description -> handler(func=arg)
```
Use `evmenu.template2menu(caller, template, {"handler": callable})`

## User Input
```python
# yield (Commands only)
result = yield("Enter your name:")

# get_input
from evennia.utils.evmenu import get_input
get_input(caller, "Write: ", callback)
```

## Options
- `startnode` — starting node
- `cmdset_mergetype` — `"Replace"` (exclusive) or `"Union"` (coexist)
- `auto_quit/look/help` — auto-add commands
- `cmd_on_exit` — command after exit
- `persistent` — survive @reload
- `session` — specify session (MULTISESSION_MODE > 2)

## Temporary Storage
`caller.ndb._evmenu` — deleted on menu close
