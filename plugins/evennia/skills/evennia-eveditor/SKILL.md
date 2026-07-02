---
name: evennia-eveditor
description: >
  Work with Evennia's EvEditor — VI/Vim-style in-game line editor. Use when Codex needs to: create
  in-game editors for Attributes or code, handle editor callbacks (load/save/quit), work with Vim
  commands in-game, or enable persistent editing. Triggers on "editor system", "EvEditor", "in-game
  editor", "VI editor", "code editing", or when building text editing interfaces.
---

# Evennia EvEditor

VI/Vim-style line editor for in-game text editing.

## Launch
```python
from evennia.utils.eveditor import EvEditor

EvEditor(caller, loadfunc=None, savefunc=None, quitfunc=None, key="", persistent=False)
```

## Vim Commands
```
 <text>   - append to buffer
 :l       - view buffer or line
 :w       - save (don't quit)
 :wq      - save and quit
 :q       - quit (ask to save)
 :q!      - force quit
 :u/:uu   - undo/redo
 :DD      - clear buffer
 :s <w> <txt> - search/replace
```

## Code Mode (@py/edit)
- `:<` — decrease indent
- `:+` — increase indent
- `:=` — toggle auto-indent
- `:w` — execute code
- `:!` — execute and keep open

## Example
```python
from evennia import Command
from evennia.utils import eveditor

class CmdSetAttr(Command):
    key = "setattr"
    def func(self):
        def load(caller):
            return caller.attributes.get("test")
        def save(caller, buffer):
            caller.attributes.add("test", buffer)
        eveditor.EvEditor(self.caller, loadfunc=load, savefunc=save, key="test")
```
