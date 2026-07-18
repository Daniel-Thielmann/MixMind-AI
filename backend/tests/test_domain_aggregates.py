import pytest

from app.domain.aggregates.analysis import Analysis, AnalysisCollection
from app.domain.aggregates.mix import Mix
from app.domain.entities.track import AudioAnalysis
from app.domain.exceptions.domain_exceptions import (
    AnalysisNotFoundError,
    DuplicateAnalysisError,
)
from app.domain.value_objects.compatibility_score import CompatibilityScore
from app.domain.value_objects.visualization import (
    SpectrogramResult,
    Spectrograms,
    WaveformResult,
    Waveforms,
)


class TestAnalysis:
    def test_add_tracks(self) -> None:
        analysis = Analysis()
        analysis_a = AudioAnalysis(
            filename="a.mp3", duration=10.0, sample_rate=44100, bpm=128.0, energy=0.5
        )
        analysis_b = AudioAnalysis(
            filename="b.mp3", duration=10.0, sample_rate=44100, bpm=130.0, energy=0.6
        )
        analysis.add_track_a(analysis_a)
        analysis.add_track_b(analysis_b)
        assert analysis.track_a is not None
        assert analysis.track_b is not None

    def test_complete_emits_event(self) -> None:
        analysis = Analysis()
        analysis.add_track_a(
            AudioAnalysis(
                filename="a.mp3",
                duration=10.0,
                sample_rate=44100,
                bpm=128.0,
                energy=0.5,
            )
        )
        analysis.add_track_b(
            AudioAnalysis(
                filename="b.mp3",
                duration=10.0,
                sample_rate=44100,
                bpm=128.0,
                energy=0.5,
            )
        )
        event = analysis.complete()
        assert event.analysis_id == str(analysis.analysis_id)

    def test_is_not_complete_initially(self) -> None:
        analysis = Analysis()
        assert analysis.is_complete is False

    def test_is_complete_after_adding_all(self) -> None:
        analysis = Analysis()
        analysis.add_track_a(
            AudioAnalysis(
                filename="a.mp3",
                duration=10.0,
                sample_rate=44100,
                bpm=128.0,
                energy=0.5,
            )
        )
        analysis.add_track_b(
            AudioAnalysis(
                filename="b.mp3",
                duration=10.0,
                sample_rate=44100,
                bpm=128.0,
                energy=0.5,
            )
        )
        analysis.add_visualizations(
            Waveforms(
                track_a=WaveformResult(image_path="a.png", width=100, height=100),
                track_b=WaveformResult(image_path="b.png", width=100, height=100),
            ),
            Spectrograms(
                track_a=SpectrogramResult(image_path="a.png", width=100, height=100),
                track_b=SpectrogramResult(image_path="b.png", width=100, height=100),
            ),
        )
        analysis.complete()
        assert analysis.is_complete is True


class TestAnalysisCollection:
    def test_add_and_get(self) -> None:
        collection = AnalysisCollection()
        analysis = Analysis()
        collection.add(analysis)
        assert collection.get(str(analysis.analysis_id)) is analysis

    def test_get_raises_on_missing(self) -> None:
        collection = AnalysisCollection()
        with pytest.raises(AnalysisNotFoundError):
            collection.get("nonexistent")

    def test_add_raises_on_duplicate(self) -> None:
        collection = AnalysisCollection()
        analysis = Analysis()
        collection.add(analysis)
        with pytest.raises(DuplicateAnalysisError):
            collection.add(analysis)


class TestMix:
    def test_score_emits_event(self) -> None:
        analysis = Analysis()
        mix = Mix(analysis=analysis)
        score = CompatibilityScore(value=85.0)
        event = mix.score(score)
        assert event.compatibility_score == 85.0
        assert mix.is_scored is True

    def test_not_scored_initially(self) -> None:
        mix = Mix()
        assert mix.is_scored is False
