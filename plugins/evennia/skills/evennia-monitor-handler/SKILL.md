---
name: evennia-monitor-handler
description: >
  Work with Evennia's MonitorHandler — watch changes to object properties or attributes. Use when
  Codex needs to: monitor attribute changes (health bar updates), set up property watchers,
  implement reactive UI updates, or remove monitors. Triggers on "monitor handler", "property
  monitor", "watch attribute", "MONITOR_HANDLER", or when building systems that react to
  attribute changes.
---

# Evennia MonitorHandler

Watch for changes to object properties or attributes.

```python
from evennia import MONITOR_HANDLER as monitorhandler

def _callback(fieldname="", obj=None, **kwargs):
    if fieldname.startswith("db_"):
        new_val = getattr(obj, fieldname)
    else:
        new_val = obj.attributes.get(fieldname)

monitorhandler.add(obj, "desc", _callback)
monitorhandler.add(obj, "db_key", _callback, idstring="key_monitor")
monitorhandler.remove(obj, "desc")
monitorhandler.remove(obj, "db_key", idstring="key_monitor")
```

## Unique Identity
`obj + fieldname + idstring` uniquely identifies a monitor.

## Signature
```python
monitorhandler.add(obj, fieldname, callback, idstring="", persistent=False, **kwargs)
```
- `obj` — must be typeclassed (not Session)
- `fieldname` — `db_*` for db fields, else Attribute name
