---
name: evennia-signals
description: >
  Work with Evennia's Signal system — event-driven hooks using Django Signals. Use when Codex needs
  to: attach handlers to game events (account login, object puppet, exit traverse), implement
  cross-cutting functionality without overriding typeclasses, or listen to system events. Triggers
  on "signal system", "SIGNAL_ACCOUNT", "SIGNAL_OBJECT", "event handler", "Django signals", or
  when building reactive game systems.
---

# Evennia Signals

Event-driven system using Django Signals — attach handlers without overriding typeclasses.

## Basic Usage
```python
from evennia import signals

def myhandler(sender, **kwargs):
    # action

signals.SIGNAL_OBJECT_POST_CREATE.connect(myhandler)
```

## Key Signals

### Account
- `SIGNAL_ACCOUNT_POST_CREATE` — account created (`ip` kwarg)
- `SIGNAL_ACCOUNT_POST_LOGIN` — logged in (`session`)
- `SIGNAL_ACCOUNT_POST_FIRST_LOGIN` — first time (`session`)
- `SIGNAL_ACCOUNT_POST_LOGIN_FAIL` — login failed (`session`)
- `SIGNAL_ACCOUNT_POST_LOGOUT` — logged out (`session`)
- `SIGNAL_ACCOUNT_POST_LAST_LOGOUT` — last session out (`session`)
- `SIGNAL_ACCOUNT_POST_RENAME` — renamed (`old_name`, `new_name`)

### Object
- `SIGNAL_OBJECT_POST_PUPPET` — puppeted (`session`, `account`)
- `SIGNAL_OBJECT_POST_UNPUPPET` — unpuppeted
- `SIGNAL_TYPED_OBJECT_POST_RENAME` — renamed (`old_key`, `new_key`)

### Other
- `SIGNAL_SCRIPT_POST_CREATE`, `SIGNAL_CHANNEL_POST_CREATE`, `SIGNAL_HELPENTRY_POST_CREATE`
- `SIGNAL_EXIT_TRAVERSED` — exit traversed (`sender`=exit, `traverser`=keyword)

### Django Defaults
- `pre_save`/`post_save`, `pre_delete`/`post_delete`
- `pre_init`/`post_init`

## Limit to Specific Entity
```python
account = search_account("foo")[0]
signals.SIGNAL_ACCOUNT_POST_CONNECT.connect(handler, account)
```
