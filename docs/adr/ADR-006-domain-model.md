# ADR-006: Rich Domain Model with Value Objects

## Status

Accepted

## Context

The original domain model used Pydantic `BaseModel` classes as anemic data containers (e.g., `AudioAnalysis`, `CompatibilityResult`) with no business behavior. Business logic lived in the application layer (`CompatibilityService`, `MixScoringService`), violating the Domain-Driven Design principle that domain logic belongs in the domain layer.

## Decision

Adopt a rich domain model with three categories:

1. **Value Objects** (`domain/value_objects/`) — Immutable, frozen dataclasses with self-contained validation and behavior:
   - `BPM` — Validates range 20–300, provides `difference_to()`, `is_compatible()`
   - `CamelotKey` — Validates Camelot wheel format (1A–12B), provides harmonic matching (`perfect`, `relative`, `adjacent`, `energy_boost`, `clash`)
   - `Energy` — Validates 0.0–1.0 range, provides `difference_to()`
   - `Duration` — Validates positive, provides `minutes_seconds`, string formatting
   - `ConfidenceScore` — Validates 0–100, provides `level` classification
   - `CompatibilityScore` — Validates 0.0–100.0, provides `rating` classification
   - Identifiers (`TrackId`, `AnalysisId`, `MixId`, `PlaylistId`, `RecommendationId`)
   - `MixDifficulty` enum with `suggested_transition_bars`
   - `Genre` — Normalises names with title case
   - Legacy Pydantic models (`CompatibilityResult`, `WaveformResult`, etc.) kept for API serialisation

2. **Entities** (`domain/entities/`) — Objects with identity and lifecycle:
   - `Track` — Rich entity with `analyze()` method (populates from `AudioAnalysis`)
   - `Recommendation` — Rich entity with `to_generated_event()`
   - Legacy `AudioAnalysis`, `AIRecommendationResponse` kept as Pydantic for backwards compatibility

3. **Domain Events** (`domain/events/`) — Immutable event records:
   - `DomainEvent` base with `event_id` and `occurred_at`
   - `TrackUploaded`, `TrackAnalyzed`
   - `MixComputed`, `RecommendationGenerated`

## Consequences

- Business logic is now co-located with the data it operates on
- Validation is guaranteed at construction time via `__post_init__`
- Pydantic models remain for API/serialisation boundaries
- All existing tests pass without modification
- New domain tests cover VO validation, entity behaviour, and event emission
- Ubiquitous Language ("Camelot Key", "Mix Difficulty", "Compatibility Score") is now reflected in the code
