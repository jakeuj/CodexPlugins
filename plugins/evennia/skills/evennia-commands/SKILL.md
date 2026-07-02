---
name: evennia-commands
description: Create and configure Evennia commands. Use when Codex needs to define new commands, override default commands, implement command parsing, handle command switches and arguments, work with command instances, or create dynamic commands. Triggers on requests like "create a command", "add a look command", "make a custom command", "implement a command", "write a command class", or when working with Evennia command systems.
---

# Evennia Commands

Commands are Python classes that handle all user input to the game. Each command is a class inheriting from `evennia.Command` (or `evennia.commands.default.muxcommand.MuxCommand` for MUX-style syntax).

## Basic Command Structure

```python
from evennia import Command

class CmdEcho(Command):
    """
    Echo your input back to you.
    Usage:
      echo <text>
    Echoes the text back to you.
    """
    key = "echo"
    aliases = ["repeat"]
    locks = "cmd:all()"
    help_category = "General"

    def parse(self):
        """Parse command arguments (optional)."""
        pass

    def func(self):
        """Execute the command."""
        self.caller.msg(f"Echo: {self.args}")
```

## Key Properties

| Property | Type | Description |
|----------|------|-------------|
| `key` | str | Command identifier (must be unique within a cmdset) |
| `aliases` | list | Alternative names for the command |
| `locks` | str | Lock string, e.g., `"cmd:all()"` or `"cmd:perm(admin)"` |
| `help_category` | str | Category for auto-help (default: "General") |
| `arg_regex` | str | Regex to define where args start (e.g., `r" "` for space) |
| `auto_help` | bool | Enable/disable auto-help generation (default: True) |
| `save_for_next` | bool | Save command state for next command (default: False) |
| `is_exit` | bool | Mark as exit command (default: set by Exit objects) |
| `is_channel` | bool | Mark as channel command (default: set by Channel objects) |

## Command Execution Flow

1. `at_pre_cmd()` — Called first. Return True to abort.
2. `parse()` — Parse `self.args`. Store results on `self`.
3. `func()` — Main command logic. Return a Deferred.
4. `at_post_cmd()` — Cleanup after func().

## Runtime Properties

When a command executes, Evennia assigns these automatically:

| Property | Description |
|----------|-------------|
| `self.caller` | Object executing the command (Character, Account, or Session) |
| `self.session` | Session object (None if called from Account/Object directly) |
| `self.sessid` | Session ID integer |
| `self.account` | Account object |
| `self.cmdstring` | Matched command key |
| `self.args` | Rest of input after command name |
| `self.obj` | Object the command is defined on |
| `self.cmdset` | Reference to the merged CmdSet |
| `self.raw_string` | Raw user input |

## MuxCommand (MUX-style Syntax)

For default MUX-like commands, inherit from `MuxCommand`:

```python
from evennia.commands.default.muxcommand import MuxCommand

class CmdLook(MuxCommand):
    key = "look"
    aliases = ["l"]
    locks = "cmd:all()"

    def func(self):
        # MuxCommand provides self.switches (list of /switches)
        if "short" in self.switches:
            self.caller.msg("Short look")
        else:
            self.caller.msg(f"You see: {self.obj.db.desc}")
```

MuxCommand auto-handles:
- `/switches` → `self.switches`
- `=` splitting → `self.lhs` and `self.rhs`
- Space-separated args → `self.args`

## Creating Commands Programmatically

```python
from evennia import create_command

# Create a command instance
cmd = create_command(CmdLook, key="look2")

# Or create on-the-fly
cmd = CmdLook()
cmd.key = "look2"
cmd.dbref = None  # not saved yet
```

## Adding Commands to CmdSets

Commands must be added to a Command Set to be available:

```python
from evennia import DefaultCmdSet

class MyCmdSet(DefaultCmdSet):
    def at_cmdset_creation(self):
        self.add(CmdLook())
        self.add(CmdEcho())
```

Attach to an object:
```python
obj.cmdset.add(MyCmdSet)
obj.cmdset.delete()  # remove
```

## Useful Utilities

```python
# Get client screen width
self.client_width()

# Create styled table
table = self.styled_table(header1, header2, ...)

# Get help entry
self.get_help(caller, cmdset)
```

## Tips

- The docstring (`__doc__`) is auto-used for the help system
- `self.caller.msg()` sends to the command caller
- For NPC commands, use `object.execute_cmd("cmd args")`
- Command instances are reused — don't store persistent state on them
- Use `save_for_next=True` if you need to pass state between consecutive commands
