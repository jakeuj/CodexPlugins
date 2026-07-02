---
name: evennia-characters
description: >
  Work with Evennia's Character system — in-game player avatars. Use when Codex needs to: create
  character typeclasses, handle puppeting (puppet/unpuppet), customize character behavior on
  login, work with DefaultCharacter, or modify the first-character creation. Triggers on "character
  system", "DefaultCharacter", "puppet", "character creation", or when building player-controlled
  game characters.
---

# Evennia Characters

Characters are [Objects](./evennia-objects) representing **player-controlled avatars**.

## Inheritance
```
DefaultObject → DefaultCharacter → Character (in mygame/typeclasses/characters.py)
```

## Login Flow
1. New Account logs in → Evennia creates a new Character
2. Account **puppets** (controls) the Character
3. First Character name = Account name by default
4. Character must have a [Default CommandSet](./evennia-commandsets) to issue commands

## Customizing
```python
BASE_CHARACTER_TYPECLASS = "typeclasses.characters.Character"
```
Default points to empty class in `mygame/typeclasses/characters.py`.
