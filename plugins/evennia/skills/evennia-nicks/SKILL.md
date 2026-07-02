---
name: evennia-nicks
description: >
  Work with Evennia's Nick system — custom replacement names for game entities. Use when Codex
  needs to: add/remove/view nicks, understand nick types (inputline/object/account), implement
  nick aliases, or work with the nick handler. Triggers on "nick system", "nickname", "nick
  command", "nick handler", or when building command aliases and name replacements.
---

# Evennia Nicks

Nicks are **private aliases** — only the owning object sees the substitution.

## Nick vs Alias
- **Alias** — entity's own attribute, everyone can use it
- **Nick** — personal to the owning object, only they see it

## Three Types
- `inputline` — replace command line input (default)
- `object` — replace when referring to objects
- `account` — replace when referring to accounts

## Usage
```
nick ls = look                      # inputline default
nick/object mycar2 = The red sports car
nick/accounts tom = Thomas Johnsson
nick build $1 $2 = @create/drop $1;$2  # template variables
```

## Code API
```python
obj.nicks.add("greetjack", "tell Jack = Hello pal!")
obj.nicks.add("rose", "The red flower", nick_type="object")
obj.nicks.add("tom", "Tommy Hill", nick_type="account")
obj.nicks.get("rose", nick_type="object")
obj.nicks.remove("rose", nick_type="object")
```

## Internal Storage
Stored as Attribute with `db_attrype="nick"`. Value is tuple: `(regex_nick, template_string, raw_nick, raw_template)`.

Channel aliases use `nick_type="channel"`.
