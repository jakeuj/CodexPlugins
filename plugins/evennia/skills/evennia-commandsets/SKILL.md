---
name: evennia-commandsets
description: Organize Evennia commands into Command Sets (CmdSets) for modular command management. Use when Codex needs to group commands, merge command sets, create context-sensitive commands (e.g., commands available only when looking at an object), manage command availability, or override default commands. Triggers on requests like "create a command set", "group commands", "merge cmdsets", "context commands", "override default commands", or when organizing Evennia command systems.
---

# Evennia Command Sets

Command Sets (CmdSets) are containers that hold commands. Commands must be added to a CmdSet to be available — the CmdSet is then attached to a typeclass (Character, Account, Object).

## Defining a Command Set

```python
from evennia import DefaultCmdSet

class MyCmdSet(DefaultCmdSet):
    def at_cmdset_creation(self):
        """Called once when the CmdSet is created."""
        self.add(CmdLook())
        self.add(CmdEcho())
        self.add(CmdInventory())
```

## Attaching CmdSets

```python
# Attach to a character
character.cmdset.add(MyCmdSet)

# Attach to an object (commands available when interacting with object)
chair.cmdset.add(ClimbCmdSet)

# Remove
character.cmdset.delete()
```

## Command Set Merging

When multiple CmdSets are attached, they merge into one effective set:

```python
# Character has: DefaultCmdSet + MyCmdSet
# When player types "look", Evennia searches the merged set
# If two commands have the same key, the FIRST one wins
```

Merge order (last added takes precedence for same-key commands):
1. DefaultCmdSet (always present on Characters)
2. Account cmdset
3. Object cmdsets (in room order)

## Adding/Merging CmdSets Programmatically

```python
# Add entire cmdset
character.cmdset.add(MyCmdSet)

# Merge specific commands from another cmdset
other_cmds = MyCmdSet()
character.cmdset.add(other_cmds)

# Replace a specific command
character.cmdset.replace(CmdLook, NewCmdLook)

# Delete specific commands
character.cmdset.delete(CmdLook)
```

## CmdSet Properties

```python
# Command set attributes
cmdset.key           # Identifier
cmdset.desc          # Description
cmdset locks          # Access restrictions for the cmdset
cmdset no_cmds       # If True, no commands available
cmdset no_exits      # If True, exit commands disabled
cmdset no_channels   # If True, channel commands disabled
```

## Context-Sensitive Commands

Attach CmdSets to objects for context-specific commands:

```python
# Tree with climb/chop commands
tree = create_object("mygame.typeclasses.objects.Tree", key="Oak Tree")
tree.cmdset.add(ClimbTreeCmdSet())
tree.cmdset.add(ChopTreeCmdSet())

# Player can only climb/chop when looking at the tree
# The cmdset is merged into the player's available commands
# when they have the tree in their line of sight
```

## Overriding Default Commands

```python
# Replace a default command
from evennia.commands.default.cmdsetcharacter import DefaultCharacterCmdSet

class MyCharacterCmdSet(DefaultCharacterCmdSet):
    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        # Replace 'look' with custom version
        self.replace(CustomLook())
        # Add new commands
        self.add(CustomCommand())
```

## In-Game Commands

```
> cmdset                         # Show current cmdsets
> cmdset/add mygame.cmdsets.MyCmdSet
> cmdset/delete MyCmdSet
> cmdset/replace CmdLook NewCmdLook
> cmdset/clear                   # Remove all non-default cmdsets
```

## Tips

- Always call `super().at_cmdset_creation()` when overriding
- CmdSets are created once and reused — don't store mutable state on them
- Use `self.add()` (not `self.append()`) to add commands
- Commands with duplicate keys: first registered wins
- Use `cmdset.replace()` to swap commands without removing
- Empty CmdSets (`no_cmds=True`) are useful for disabling all commands temporarily
- CmdSets on objects are merged into the caller's cmdset when the object is in scope
