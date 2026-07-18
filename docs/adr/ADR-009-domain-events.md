# ADR-009: Domain Events

## Status

Accepted

## Context

The original application had no mechanism to notify other parts of the system when domain-significant events occurred. Operations like "track analysed" or "mix scored" were side-effect free, making it difficult to add cross-cutting concerns like logging, auditing, or cache invalidation.

## Decision

Introduce a lightweight Domain Events pattern using frozen dataclasses:

**Base Event** (`domain/events/base.py`):
```python
@dataclass(frozen=True)
class DomainEvent:
    event_id: str = uuid4().hex
    occurred_at: datetime = datetime.now(timezone.utc)
```

**Concrete Events** (`domain/events/`):
- `TrackUploaded` — Emitted when audio files are saved
- `TrackAnalyzed` — Emitted when an `Analysis` aggregate is completed
- `MixComputed` — Emitted when a `Mix` aggregate receives a score
- `RecommendationGenerated` — Emitted when an AI recommendation is produced

Event usage rules:
- Events are created by aggregate methods (e.g., `Analysis.complete()` returns `TrackAnalyzed`)
- Events are immutable (`frozen=True`, `kw_only=True`)
- Events carry only primitive/scalar data (no entity references)
- The application layer is responsible for dispatching events
- No event bus or message broker in this sprint — events are returned from methods and dispatched by the caller

## Consequences

- Decouples domain operations from side effects
- Provides an audit trail for significant state changes
- Simplifies future integration with message brokers (RabbitMQ, Redis Streams)
- Zero runtime overhead — events are only created when explicitly requested
- Simple, testable pattern with no framework dependency
