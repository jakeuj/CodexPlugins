---
name: evennia-channels
description: Create and manage Evennia channels for in-game messaging and communication. Use when Codex needs to set up chat channels, custom message types, channel commands, or integrate external services (Discord, IRC, etc.) with Evennia. Covers channel creation, messaging, subscriptions, channel commands, and external integrations. Triggers on requests like "create a channel", "chat system", "message system", "channel commands", "Discord integration", or when implementing Evennia communication systems.
---

# Evennia Channels

Channels are Evennia's messaging system. They allow persistent, topic-based communication between players, NPCs, and external services.

## Default Channels

Evennia ships with these default channels:
- `announce` — Server announcements
- `lobby` — General chat room
- `help` — Help requests
- `offtopic` — Off-topic chat
- `pages` — Player-to-player paging

## Creating Channels

```python
from evennia import create_channel

# Create a new channel
channel = create_channel("mychannel", persistent=True)

# With initial connections
channel = create_channel("trade", persistent=True,
                         connection_func=my_connection_func)
```

## Sending Messages

```python
# Send to channel
channel.msg("Hello everyone!")

# Send with caller (shows sender name)
channel.msg(caller=character, message="Hello everyone!")

# Send to specific typeclass
channel.msg(msg="Hello!", receivers=[character1, character2])

# Using Evennia's channel helper
evenniaCHANNEL.msg("message")
```

## Channel Properties

```python
channel.key          # Channel name
channel.dbdesc       # Channel description
channel.db_perm_public  # Who can see the channel list
channel.db_perm_conn    # Who can connect
channel.db_perm_disconn # Who can disconnect
channel.db_perm_read    # Who can read
channel.db_perm_write   # Who can write
channel.db_perm_listen  # Who can listen
channel.db_perm_off     # Who can go offline
```

## Channel Commands

Channels come with built-in commands:
- `channels` — List available channels
- `go <channel>` — Connect to a channel
- `quit <channel>` — Disconnect from a channel
- `<channel>: message` — Send message (when connected)

## Custom Channel Commands

Define in your game directory:

```python
from evennia import DefaultChannel

class MyChannel(DefaultChannel):
    def at_channel_create(self):
        """Called when channel is first created."""
        self.db.desc = "My custom channel"

    def msg(self, msg_obj, **kwargs):
        """Override message sending."""
        # Custom formatting
        formatted = f"[{self.key}] {msg_obj}"
        super().msg(formatted, **kwargs)
```

## External Integrations

Connect channels to external services:

```python
# Discord integration
evennia.conf.settings.CHANNEL_COMM_LINKS["discord"] = {
    "desc": "Discord integration",
    "conntype": "evennia.contrib.full_systems.discord_integration.DiscordConnector",
}

# IRC integration
evennia.conf.settings.CHANNEL_COMM_LINKS["irc"] = {
    "desc": "IRC integration",
    "conntype": "evennia.contrib.full_systems.irc_integration.IRCConnector",
}
```

## Channel Messages (Msg)

Msg objects are the low-level message format:

```python
from evennia import Msg

msg = Msg(
    channels=["lobby"],
    message="Hello!",
    sender=account,
    receiver=character,
    type="chat"
)
msg.send()
```

## Tips

- Channels persist across server reboots (saved in database)
- Use `persistent=True` for channels that should survive restarts
- Channel connections are per-session — players can be on multiple channels
- For real-time messaging, consider using Evennia's WebSocket webclient
- Custom channel types can override `msg()` for formatting
- Use `evennia.search_channel()` to find channels by name
