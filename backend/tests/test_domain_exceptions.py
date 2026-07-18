from app.domain.exceptions.domain_exceptions import (
    AnalysisNotFoundError,
    DomainError,
    DuplicateAnalysisError,
    IncompatibleTracksError,
    InvalidBPMError,
    InvalidCamelotKeyError,
    InvalidConfidenceError,
    InvalidDurationError,
    InvalidEnergyError,
    TrackNotAnalyzedError,
    UnsupportedAudioFormatError,
)


class TestDomainExceptions:
    def test_invalid_bpm_error(self) -> None:
        exc = InvalidBPMError(bpm=400.0)
        assert isinstance(exc, DomainError)
        assert "400" in str(exc)

    def test_invalid_energy_error(self) -> None:
        exc = InvalidEnergyError(energy=2.0)
        assert isinstance(exc, DomainError)
        assert "2.0" in str(exc)

    def test_invalid_camelot_key_error(self) -> None:
        exc = InvalidCamelotKeyError(key="13A")
        assert isinstance(exc, DomainError)
        assert "13A" in str(exc)

    def test_invalid_confidence_error(self) -> None:
        exc = InvalidConfidenceError(value=200)
        assert isinstance(exc, DomainError)
        assert "200" in str(exc)

    def test_invalid_duration_error(self) -> None:
        exc = InvalidDurationError(duration=-5.0)
        assert isinstance(exc, DomainError)
        assert "-5.0" in str(exc)

    def test_incompatible_tracks_error(self) -> None:
        exc = IncompatibleTracksError()
        assert isinstance(exc, DomainError)

    def test_track_not_analyzed_error(self) -> None:
        exc = TrackNotAnalyzedError(track_id="abc")
        assert "abc" in str(exc)

    def test_track_not_analyzed_error_default(self) -> None:
        exc = TrackNotAnalyzedError()
        assert "not been analyzed" in str(exc)

    def test_analysis_not_found_error(self) -> None:
        exc = AnalysisNotFoundError(analysis_id="xyz")
        assert "xyz" in str(exc)

    def test_duplicate_analysis_error(self) -> None:
        exc = DuplicateAnalysisError(analysis_id="xyz")
        assert "xyz" in str(exc)

    def test_unsupported_audio_format_error(self) -> None:
        exc = UnsupportedAudioFormatError(filename="test.xyz")
        assert "test.xyz" in str(exc)
