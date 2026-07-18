from app.domain.entities.recommendation import Recommendation
from app.domain.entities.track import AudioAnalysis, Track
from app.domain.value_objects.bpm import BPM
from app.domain.value_objects.camelot_key import CamelotKey
from app.domain.value_objects.duration import Duration
from app.domain.value_objects.energy import Energy


class TestTrack:
    def test_creates_with_defaults(self) -> None:
        track = Track()
        assert track.filename == ""
        assert track.bpm is None

    def test_analyze_populates_from_audio_analysis(self) -> None:
        track = Track()
        analysis = AudioAnalysis(
            filename="test.mp3",
            duration=180.0,
            sample_rate=44100,
            bpm=128.0,
            energy=0.5,
            key="C Minor",
            camelot="1A",
        )
        track.analyze(analysis)
        assert track.filename == "test.mp3"
        assert track.bpm == BPM(value=128.0)
        assert track.energy == Energy(value=0.5)
        assert track.duration == Duration(value=180.0)
        assert track.camelot == CamelotKey(value="1A")
        assert track.key == "C Minor"

    def test_to_uploaded_event(self) -> None:
        track = Track(filename="test.mp3")
        event = track.to_uploaded_event()
        assert event.filename == "test.mp3"
        assert len(event.event_id) == 32


class TestRecommendation:
    def test_to_generated_event(self) -> None:
        rec = Recommendation(summary="Great mix", dj_score=95)
        event = rec.to_generated_event(analysis_id="abc123")
        assert event.analysis_id == "abc123"
        assert event.confidence == 0  # No confidence set

    def test_creates_with_defaults(self) -> None:
        rec = Recommendation()
        assert rec.summary == ""
        assert rec.dj_score == 0
