---
name: evennia-locks
description: Control access to Evennia typeclasses using Locks. Use when Codex needs to restrict who can use commands, enter rooms, pick up objects, edit exits, or perform any action on game entities. Covers lock string syntax, lock functions (access, view, delete, edit, poundcode), lock handlers, and permission checks. Triggers on requests like "add a lock", "restrict access", "permission check", "lock system", "who can do this", or when implementing Evennia security and access control.
---

# Evennia Locks

Locks control access to typeclasses. Every typeclass has a `locks` handler for managing access restrictions.

## Lock String Format

```
locktype:lockfunction(arguments)
```

Common lock types:
- `cmd:` — Controls command execution (e.g., `cmd:all()`)
- `edit:` — Controls editing the object
- `delete:` — Controls deleting the object
- `puppet:` — Controls puppeting (for Accounts)
- `view:` — Controls viewing the object
- `call:` — Controls calling the object
- `broadcast:` — Controls broadcasting

## Built-in Lock Functions

```python
# Permission-based
all()           # Everyone
none()          # Nobody
perm(perm_name) # Specific permission
id(1234)        # Specific dbref
nick(nick_name) # Specific nick

# Combination
and(perm(admin), perm(builder))  # Both required
or(perm(admin), id(1234))        # Either
not(perm(banned))                # Negation

# Poundcode (expression evaluation)
poundcode:#1234.db.admin  # Check attribute on another object
```

## Common Lock Examples

```python
# Command locks
locks = "cmd:all()"              # Anyone can use
locks = "cmd:perm(admin)"        # Only admins
locks = "cmd:id(1234)"           # Only specific player
locks = "cmd:not(banned())"      # Not banned

# Object locks
locks = "edit:perm(builder)"     # Only builders can edit
locks = "delete:perm(god)"       # Only gods can delete
locks = "puppet:id(1234)"        # Only specific account can puppet

# Combined
locks = "cmd:all();edit:perm(builder);delete:perm(god)"
```

## Lock Handler Methods

```python
# Add a lock
obj.locks.add("cmd:all()")
obj.locks.add("edit:perm(builder)")

# Get lock string
lock_string = obj.locks.get("cmd")

# Check access
obj.locks.check(caller, access_type="cmd", no_entry_msg="You can't!")

# Remove lock
obj.locks.remove("cmd")

# Clear all locks
obj.locks.clear()
```

## Custom Lock Functions

Define in `mygame/server/conf/lockfuncs.py`:

```python
from evennia.locks.lockfuncs import lockfuncs

@lockfuncs.register
def my_custom_func(accessing_obj, accessed_obj, *args, **kwargs):
    """Custom lock function."""
    # Return True if access allowed, False otherwise
    return accessed_obj.db.custom_flag

# Use in lock string
locks = "cmd:my_custom_func()"
```

## Locks on Commands

Commands have a `locks` property set at class level:

```python
class CmdAdmin(Command):
    key = "admin"
    locks = "cmd:perm(admin)"  # Only admins
```

## Permissions

Permissions are higher-level access levels:

```
admin     — Full administrative access
builder   — Can build/edit objects
player    — Regular player access
guest     — Guest access
newuser   — New user (limited)
```

Set permissions:
```python
account.permissions.add("builder")
account.permissions.remove("admin")
account.permissions.has("admin")  # Check
```

## In-Game Commands

```
> lock obj = cmd:all()
> lock obj/edit = perm(builder)
> lock obj/delete = perm(god)
> perms account = +admin
> perms account = -builder
```

## Tips

- Default lock for new objects is `"cmd:all()"`
- Lock strings are separated by `;` for multiple lock types
- Use `locks.check()` for explicit permission checking in code
- Permissions are additive — `+perm` adds, `-perm` removes
- The `id()` lock function checks database references
- Locks are evaluated at runtime — changes take effect immediately
