---
name: evennia-coding-utils
description: >
  Work with Evennia's coding utilities — search, create, logging, time, text, and async helpers.
  Use when Codex needs to: search for objects/accounts/scripts, create entities in code, use
  logging, handle game time, format text, delay callbacks, or check type inheritance. Triggers on
  "coding utils", "search_object", "create_object code", "gametime", "logger", "utils.delay",
  "inherits_from", or when doing general Evennia programming.
---

# Evennia Coding Utilities

## Searching
```python
obj = self.caller.search(objname)              # location + contents
obj = self.caller.search(objname, global_search=True)
from evennia import search_object, search_account, search_script
from evennia import search_channel, search_message, search_help
```

## Create
```python
import evennia
evennia.create_account(...)
evennia.create_object("typepath", key="name")
evennia.create_script(...)
evennia.create_channel(...)
evennia.create_help_entry(...)
evennia.create_message(...)
```

## Logging
```python
from evennia import logger
logger.log_err/warn/info/dep()
logger.log_trace("msg")  # inside except block
logger.log_file("msg", filename="game.log")  # async file log
```

## Time
```python
from evennia import gametime
gametime.runtime(), gametime.uptime(), gametime.gametime()
gametime.schedule(func, hour=2)
from evennia.utils import time_format
time_format(seconds, style=0)  # "4d:0m:7s"
```

## Async
```python
from evennia import utils
utils.delay(10, callback, obj, "msg", persistent=False)
```

## Type Checking
```python
from evennia import utils
utils.inherits_from(obj, "typeclasses.objects.animals.Animal")
```

## Text
- `utils.fill(text, width, indent)` — fill/align
- `utils.crop(text, width, suffix)` — crop long lines
- `utils.dedent(text)` — remove leading indentation
- `to_str()` / `to_bytes()` — safe encoding conversion
