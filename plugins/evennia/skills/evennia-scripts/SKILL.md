---
name: evennia-scripts
description: Create and manage Evennia Scripts for background processes, timers, and persistent system data. Use when Codex needs to implement timed events, background tasks, persistent storage backends, game loops, or systems that run independently of player commands. Covers script creation, timer control, attaching scripts to objects/accounts, GLOBAL_SCRIPTS, and hook methods. Triggers on requests like "create a script", "background task", "timer", "game loop", "persistent system", "script system", or when implementing Evennia background processes.
---

# Evennia Scripts

Scripts are out-of-character typeclasses for background processing, timers, and persistent storage. They have no in-game location or player connection, making them ideal for system-level tasks.

## When to Use Scripts

- Timed events (daily resets, weather cycles, economy updates)
- Persistent storage backends (game state, economy tracking)
- Background processes (combat rounds, event systems)
- System handlers that don't belong to any player or object

## Creating Scripts

```python
from evennia import DefaultScript

class MyScript(DefaultScript):
    def at_script_creation(self):
        """Called once when script is first created."""
        self.key = "myscript"
        self.db.foo = "bar"
```

Create with `create_script`:

```python
# Simple script
script = evennia.create_script("typeclasses.scripts.MyScript")

# With timer
timed = evennia.create_script(
    "typeclasses.scripts.TimedScript",
    key="Timed script",
    interval=34,           # seconds (<=0 means off)
    start_delay=True,      # wait interval before first call
    autostart=True         # start timer immediately
)
```

## Timer Control

```python
script.start()    # Start the timer
script.stop()     # Stop the timer
script.pause()    # Pause (keeps state)
script.unpause()  # Unpause
script.delete()   # Delete (also stops timer)
```

## Attached vs Global Scripts

**Attached Script** — linked to an object/account:
```python
myobj.scripts.add(new_script)
myobj.scripts.add(evennia.DefaultScript)

# Access parent in script
self.obj     # The attached object
self.account  # If attached to an Account

# Manage
myobj.scripts.all()        # All scripts on obj
myobj.scripts.remove(script)
```

**Global Script** — no parent object:
```python
# Access via GLOBAL_SCRIPTS container
from evennia import GLOBAL_SCRIPTS

myscript = GLOBAL_SCRIPTS.myscript
GLOBAL_SCRIPTS.get("Timed script").db.foo = "bar"
```

## Script Hooks

```python
class MyScript(DefaultScript):
    def at_script_creation(self):
        """Set up the script (called once)."""
        self.key = "myscript"

    def at_repeat(self):
        """Called every interval seconds (timer tick)."""
        # Your periodic logic here
        pass

    def at_start(self):
        """Called when timer starts."""
        pass

    def at_stop(self):
        """Called when timer stops."""
        pass

    def at_delete(self):
        """Called when script is deleted."""
        pass
```

## Searching Scripts

```python
# Search by key
scripts = evennia.search_script("myscript")

# Search by typeclass
scripts = evennia.search_script(typeclass="mygame.typeclasses.scripts.MyScript")

# Search on specific object
scripts = evennia.search_script(target=myobj)
```

## In-Game Commands

```
> addscript obj = typeclasses.scripts.MyScript
> scripts                          # List all scripts
> scripts/stop typeclasses.scripts.MyScript
> scripts/start #244
> scripts/pause #11
> scripts/delete #566
```

## Tips

- Scripts are full typeclasses — they have Attributes, Tags, and Locks
- Use `at_repeat` for periodic logic (the script's timer calls it)
- For one-off delayed actions, consider `evennia.utils.delay()` instead
- For recurring actions, `evennia.utils.repeat()` is lighter than a full Script
- GLOBAL_SCRIPTS provides named access to globally registered scripts
- Scripts persist across server reboots (saved in database)
- Never use a Script just to store data with no location — use a Script instead!
