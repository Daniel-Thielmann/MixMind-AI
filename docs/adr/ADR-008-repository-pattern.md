# ADR-008: Repository Pattern for Aggregate Persistence

## Status

Accepted

## Context

The original codebase had a single `TrackRepository` interface defined in `domain/repositories/track_repository.py`. As the domain model grew to include aggregates (Analysis, Mix), each aggregate needed its own persistence strategy with clear interfaces in the domain layer.

## Decision

Adopt the Repository pattern with interfaces in the domain layer:

- **`TrackRepository`** (existing) — `save_analysis()`, `get_analysis()`, `get_audio_path()`
- Future repositories to be added as needed:
  - `AnalysisRepository` — Save/load `Analysis` aggregates
  - `MixRepository` — Save/load `Mix` aggregates
  - `RecommendationRepository` — Save/load `Recommendation` entities

Repository rules:
- Interfaces live in `domain/repositories/`
- Implementations live in `infrastructure/database/`
- Repositories operate on aggregates (not individual entities)
- Methods use domain types (not ORM models) in their signatures
- Abstractions use the `ABC` pattern from `abc` module

## Consequences

- Domain layer remains free of infrastructure concerns
- Repositories can be swapped (in-memory, filesystem, PostgreSQL) without domain changes
- Tests can use in-memory implementations
- Future ORM transition (ADR-003 addressed later) is isolated to infrastructure
