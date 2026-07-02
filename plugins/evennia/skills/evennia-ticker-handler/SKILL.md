---
name: evennia-ticker-handler
description: >
  Work with Evennia's TickerHandler — a singleton global scheduler that fires callbacks at
  regular intervals. Use when Codex needs to: implement heartbeat/ticker systems, schedule
  periodic updates for multiple objects (weather, environment), manage tick subscriptions, or
  understand when NOT to use tickers. Triggers on "ticker system", "heartbeat", "periodic update",
  "TICKER_HANDLER", or when building game systems that need regular ticks.
---

# Evennia TickerHandler

Singleton global scheduler — fire callbacks at fixed intervals across multiple subscribers.

```python
from evennia import TICKER_HANDLER as tickerhandler
tickerhandler.add(20, obj.at_tick)  # every 20 seconds
tickerhandler.add(30, myfunc)
tickerhandler.remove(20, obj.at_tick)
```

## Full Signature
```python
tickerhandler.add(interval, callback, idstring="", persistent=True, *args, **kwargs)
```
- `interval` — seconds
- `persistent` — survive shutdown if True
- `idstring` — unique identifier (needed when same callback on same interval)

## Identifying Tickers
Key = `(callback, interval, persistent, idstring)`. Same combo = replace existing.

## Warning: Don't Use for Change Detection
> Never use a ticker to detect **changes** — if 99% of ticks do nothing, use self-reporting
> instead. Tickers are for **simultaneous updates** to multiple objects without external input.

## Tools
- `tickerhandler.all()` — list all subscriptions
- `tickerhandler.clear()` — stop all (testing)
