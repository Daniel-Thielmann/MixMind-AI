# ADR-007: Aggregate Design

## Status

Accepted

## Context

The existing codebase had no aggregates — entities were used in isolation. Operations like "analyse two tracks and produce a mix score" spanned multiple entities without a transactional boundary, making it unclear what should be persisted as a unit.

## Decision

Define two aggregates with clear transactional boundaries:

1. **Analysis** (`domain/aggregates/analysis.py`)
   - Root: `Analysis` (identified by `AnalysisId`)
   - Contains: `track_a` (`AudioAnalysis`), `track_b` (`AudioAnalysis`), `waveforms`, `spectrograms`
   - Invariants: Both tracks must be present before `complete()` is called
   - Emits: `TrackAnalyzed` event on completion
   - Collection: `AnalysisCollection` with `add()`/`get()` semantics and duplicate detection

2. **Mix** (`domain/aggregates/mix.py`)
   - Root: `Mix` (identified by `MixId`)
   - Contains: reference to `Analysis`, `CompatibilityScore`
   - Invariants: Score must be set before `is_scored` returns true
   - Emits: `MixComputed` event on scoring

## Consequences

- Clear transactional boundaries for persistence
- Invariants enforced at the aggregate level
- Events provide an audit trail
- Repositories (ADR-008) map one-to-one with aggregates
- No cross-aggregate references — only `AnalysisId` references from `Mix`
