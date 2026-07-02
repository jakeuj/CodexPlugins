---
name: evennia-on-demand-handler
description: >
  Work with Evennia's OnDemandHandler — lazy state computation that only fires when actually
  queried. Use when Codex needs to: implement on-demand state changes (plant growth, trap states),
  avoid unnecessary computation, create state machines that only update when checked, or build
  looping/bouncing stage systems. Triggers on "on demand handler", "lazy state", "on demand
  state", "ON_DEMAND_HANDLER", or when building efficient game state systems.
---

# Evennia OnDemandHandler

Compute state **only when queried** — zero cost until someone looks.

## Usage
```python
from evennia import ON_DEMAND_HANDLER

ON_DEMAND_HANDLER.add(
    self,
    category="plantgrowth",
    stages={
        0: "seedling",
        600: "sprout",          # 10 min
        18000: "flowering",     # 5 hours
        36000: "wilting",       # 10 hours
        43200: "dead"           # 12 hours
    }
)

# Query
stage = ON_DEMAND_HANDLER.get_state(self, category="plantgrowth")
```

## CRUD
```python
ON_DEMAND_HANDLER.add(key, category, stages)
ON_DEMAND_HANDLER.get(key, category)
ON_DEMAND_HANDLER.get_state(key, category)
ON_DEMAND_HANDLER.get_dt(key, category)
ON_DEMAND_HANDLER.remove(key, category)
ON_DEMAND_HANDLER.batch_add(task1, task2)
ON_DEMAND_HANDLER.batch_remove(task1, task2)
```

## Stage Callables
```python
stages={0: "new", 10: ("old", mycallable)}
# callable(task, **kwargs) — must be pickleable
```

## Loop & Bounce
```python
from evennia import OnDemandTask

# Loop: harmless → solvable → primed → deadly → (reset)
stages={0: "harmless", 50: "solvable", 100: "primed",
        200: "deadly", 250: ("_reset", OnDemandTask.stagefunc_loop)}

# Bounce: cold → warm → hot → warm → cold → ...
stages={0: ("cold", OnDemandTask.stagefunc_bounce),
        300: "warm", 600: ("HOT!", OnDemandTask.stagefunc_bounce)}
```

## Not Suitable For
- Needing to **notify** players without input (use ticker/script instead)
- States that assume previous stages made changes (stages can be skipped)
