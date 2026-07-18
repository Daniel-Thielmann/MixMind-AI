from __future__ import annotations


class DomainError(Exception):
    pass


class InvalidBPMError(DomainError):
    def __init__(self, bpm: float) -> None:
        super().__init__(f"BPM must be between 20 and 300, got {bpm}")


class InvalidEnergyError(DomainError):
    def __init__(self, energy: float) -> None:
        super().__init__(f"Energy must be between 0.0 and 1.0, got {energy}")


class InvalidCamelotKeyError(DomainError):
    def __init__(self, key: str) -> None:
        super().__init__(f"Invalid Camelot key format: {key!r}")


class InvalidKeyError(DomainError):
    def __init__(self, key: str) -> None:
        super().__init__(f"Invalid musical key: {key!r}")


class InvalidConfidenceError(DomainError):
    def __init__(self, value: int) -> None:
        super().__init__(f"Confidence must be between 0 and 100, got {value}")


class InvalidDurationError(DomainError):
    def __init__(self, duration: float) -> None:
        super().__init__(f"Duration must be positive, got {duration}")


class IncompatibleTracksError(DomainError):
    def __init__(self, detail: str = "Tracks are not compatible for mixing") -> None:
        super().__init__(detail)


class TrackNotAnalyzedError(DomainError):
    def __init__(self, track_id: str = "") -> None:
        msg = (
            f"Track {track_id} has not been analyzed yet"
            if track_id
            else "Track has not been analyzed yet"
        )
        super().__init__(msg)


class AnalysisNotFoundError(DomainError):
    def __init__(self, analysis_id: str) -> None:
        super().__init__(f"Analysis not found: {analysis_id}")


class DuplicateAnalysisError(DomainError):
    def __init__(self, analysis_id: str) -> None:
        super().__init__(f"Analysis already exists: {analysis_id}")


class UnsupportedAudioFormatError(DomainError):
    def __init__(self, filename: str) -> None:
        super().__init__(f"Unsupported audio format: {filename}")
