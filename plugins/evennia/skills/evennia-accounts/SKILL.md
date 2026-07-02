---
name: evennia-accounts
description: >
  Work with Evennia's Account system — unique game accounts (one per player). Use when Codex needs
  to: handle account creation/login, manage puppet/unpuppet, work with AccountCmdSet, customize
  account commands (ooc/ic/exit), set account permissions, or manage multi-session mode. Triggers
  on "account system", "DefaultAccount", "account creation", "ooc ic", "account cmdset",
  "MULTISESSION_MODE", or when building account-related game logic.
---

# Evennia Accounts

Account represents a **unique game account** — one player.

## Key Concepts
- One player → one Account (but multiple Sessions possible)
- Account has **no in-game representation** — must puppet an Object (normally Character)
- Default Account lives in `mygame/typeclasses/accounts.py`

## Account CmdSet (AccountCmdSet)
Commands available regardless of which character is puppeted:
- `exit` — log out
- `who` — list players
- `ooc` — leave puppet, OOC mode (no location, only Account cmdset)
- `ic` — re-puppet latest character
- Chat-channel commands

## Properties
- `user` — Django User link
- `obj` / `name` — aliases for character/username
- `sessions` — ObjectSessionHandler managing all sessions
- `is_superuser` — superuser flag

## Methods
- `puppet_object(session, obj)` — connect session to object
- `unpuppet_object(session, obj)` — disconnect
- `get_puppet(sessionid)` — get puppeted object
- `msg()` — send message
- `search()` — search accounts

## Permissions
- Account permissions **override** Character permissions
- Use `quell` to temporarily switch permission set
- Normaly put permissions at Account level for consistency

## Customizing
```python
BASE_ACCOUNT_TYPECLASS = "typeclasses.accounts.Account"
```
