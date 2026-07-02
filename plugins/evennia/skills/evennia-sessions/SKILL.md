---
name: evennia-sessions
description: >
  Work with Evennia's Session system — individual client connections to the server. Use when Codex
  needs to: manage sessions, send messages to specific sessions, customize session behavior,
  understand MULTISESSION_MODE effects, or work with Portal/Server session synchronization.
  Triggers on "session system", "ServerSession", "PortalSession", "multi session", "send message
  to session", "session handler", or when dealing with multi-client setups.
---

# Evennia Sessions

A Session represents **one client connection** to the server.

## Key Properties
- `sessid` — unique integer ID
- `address` — client address
- `logged_in` — authenticated?
- `account` — associated Account
- `puppet` — current puppeted object
- `ndb` — non-persistent attributes (Session dies on disconnect)
- `db` = `ndb` alias

## Sending Messages
```python
account.msg("hello")                               # all sessions
account.msg("hello", session=mysession)             # specific session
character.msg("hello")                              # auto to controlling session
command.msg("hello")                                # safest — triggers session
```

## Customizing
```python
CMDSET_SESSION = "mygame.typeclasses.session.SessionCmdSet"
SERVER_SESSION_CLASS = "typeclasses.session.Session"
```

## MULTISESSION_MODE > 1
- Session-level cmdset affects only that session
- Account-level cmdset affects all sessions

## Portal ↔ Server Sync
- PortalSession ↔ ServerSession (one-to-one mapping)
- Synced on: disconnect, quit, server reboot
