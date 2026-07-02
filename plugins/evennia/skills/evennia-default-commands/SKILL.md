---
name: evennia-default-commands
description: >
  Work with Evennia's default command system — the 89 built-in commands. Use when Codex needs to:
  understand default command categories (CharacterCmdSet, AccountCmdSet, UnloggedinCmdSet,
  SessionCmdSet), look up built-in commands (@create, @dig, @spawn, ooc, ic, @py, etc.), override
  or remove default commands, or understand command syntax and help categories. Triggers on "default
  commands", "@create", "@dig", "character cmdset", "account cmdset", "unloggedin cmdset", "command
  system built-in", or when working with Evennia's pre-built commands.
---

# Evennia Default Commands

Evennia ships with **89 default commands** across 4 cmdsets.

## CmdSet Categories

### CharacterCmdSet (most commands)
- **Building**: `@create`, `@dig`, `@tunnel`, `@open`, `@link`, `@unlink`, `@desc`, `@set`, `@typeclass`, `@spawn`, `@alias`, `@copy`, `@destroy`, `@find`, `@lock`, `@objects`, `@scripts`, `@tag`, `@teleport`, `@sethome`, `@wipe`, `@cpattr`, `@mvattr`, `@name`, `@cmdsets`, `batchcode`, `batchcommands`
- **System**: `@about`, `@objects`, `@scripts`, `@tasks`, `@time`, `@tickers`, `@server`, `@service`, `access`
- **General**: `look`, `pose`, `inventory`, `drop`, `get`, `give`, `home`, `say`, `whisper`, `setdesc`, `sethelp`

### AccountCmdSet
- `@channel`, `@py`, `@reload`, `@reset`, `@shutdown`, `help`, `password`, `charcreate`, `chardelete`, `color`, `nick`, `ooc`, `ic`, `option`, `quell`, `style`, `who`, `sessions`, `page`, `discord2chan`, `irc2chan`, `grapevine2chan`, `rss2chan`, `ircstatus`

### UnloggedinCmdSet
- `connect`, `create`, `info`, `look`, `help`, `quit`, `encoding`, `screenreader`

### SessionCmdSet
- `sessions`

## Key Commands
- `@py` — run Python code
- `@reload` — reload game
- `ooc / ic` — switch between OOC and character mode
- `@create <name>:<path>` — create object
- `@dig <dir>;<name>` — dig room + exit
- `@spawn` — create from prototype
- `@py/edit` — open EvEditor for code
- `@lock` — set locks
