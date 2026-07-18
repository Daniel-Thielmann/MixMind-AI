import pytest

from app.domain.exceptions.domain_exceptions import (
    InvalidBPMError,
    InvalidCamelotKeyError,
    InvalidConfidenceError,
    InvalidDurationError,
    InvalidEnergyError,
)
from app.domain.value_objects.bpm import BPM
from app.domain.value_objects.camelot_key import CamelotKey
from app.domain.value_objects.compatibility_score import CompatibilityScore
from app.domain.value_objects.confidence_score import ConfidenceScore
from app.domain.value_objects.duration import Duration
from app.domain.value_objects.energy import Energy
from app.domain.value_objects.mix_difficulty import MixDifficulty


class TestBPM:
    def test_creates_valid_bpm(self) -> None:
        bpm = BPM(value=128.0)
        assert bpm.value == 128.0

    def test_raises_on_below_20(self) -> None:
        with pytest.raises(InvalidBPMError):
            BPM(value=10.0)

    def test_raises_on_above_300(self) -> None:
        with pytest.raises(InvalidBPMError):
            BPM(value=400.0)

    def test_difference_to(self) -> None:
        a = BPM(value=128.0)
        b = BPM(value=130.0)
        assert a.difference_to(b) == 2.0

    def test_is_compatible(self) -> None:
        a = BPM(value=128.0)
        b = BPM(value=130.0)
        assert a.is_compatible(b, threshold=5.0) is True
        assert a.is_compatible(b, threshold=1.0) is False


class TestEnergy:
    def test_creates_valid_energy(self) -> None:
        energy = Energy(value=0.5)
        assert energy.value == 0.5

    def test_raises_on_negative(self) -> None:
        with pytest.raises(InvalidEnergyError):
            Energy(value=-0.1)

    def test_raises_on_above_one(self) -> None:
        with pytest.raises(InvalidEnergyError):
            Energy(value=1.5)

    def test_difference_to(self) -> None:
        a = Energy(value=0.5)
        b = Energy(value=0.7)
        assert a.difference_to(b) == 0.2

    def test_is_compatible(self) -> None:
        a = Energy(value=0.5)
        b = Energy(value=0.52)
        assert a.is_compatible(b, threshold=0.05) is True
        assert a.is_compatible(b, threshold=0.01) is False


class TestCamelotKey:
    def test_creates_inner_wheel(self) -> None:
        key = CamelotKey(value="1A")
        assert key.number == 1
        assert key.letter.value == "A"

    def test_creates_outer_wheel(self) -> None:
        key = CamelotKey(value="12B")
        assert key.number == 12

    def test_raises_on_invalid(self) -> None:
        with pytest.raises(InvalidCamelotKeyError):
            CamelotKey(value="13A")

    def test_raises_on_unknown(self) -> None:
        with pytest.raises(InvalidCamelotKeyError):
            CamelotKey(value="Unknown")

    def test_perfect_match(self) -> None:
        a = CamelotKey(value="1A")
        b = CamelotKey(value="1A")
        assert a.is_perfect_match(b) is True
        assert a.harmonic_similarity(b) == 1.0

    def test_relative_match(self) -> None:
        a = CamelotKey(value="1A")
        b = CamelotKey(value="1B")
        assert a.is_relative_match(b) is True
        assert a.harmonic_similarity(b) == 0.8

    def test_adjacent_match(self) -> None:
        a = CamelotKey(value="1A")
        b = CamelotKey(value="2A")
        assert a.is_adjacent_match(b) is True
        assert a.harmonic_similarity(b) == 0.8

    def test_adjacent_wrap_match(self) -> None:
        a = CamelotKey(value="1A")
        b = CamelotKey(value="12A")
        assert a.is_adjacent_match(b) is True

    def test_energy_boost(self) -> None:
        a = CamelotKey(value="1A")
        b = CamelotKey(value="3A")
        assert a.is_energy_boost(b) is True
        assert a.harmonic_similarity(b) == 0.6

    def test_clash(self) -> None:
        a = CamelotKey(value="1A")
        b = CamelotKey(value="5A")
        assert a.harmonic_similarity(b) == 0.0
        assert a.similarity_label(b) == "Clash"

    def test_to_musical_key(self) -> None:
        assert CamelotKey(value="1A").to_musical_key() == "C Minor"
        assert CamelotKey(value="1B").to_musical_key() == "C Major"


class TestDuration:
    def test_creates_valid_duration(self) -> None:
        d = Duration(value=180.0)
        assert d.value == 180.0

    def test_raises_on_zero(self) -> None:
        with pytest.raises(InvalidDurationError):
            Duration(value=0.0)

    def test_raises_on_negative(self) -> None:
        with pytest.raises(InvalidDurationError):
            Duration(value=-10.0)

    def test_minutes_seconds(self) -> None:
        d = Duration(value=185.0)
        assert d.minutes_seconds == (3, 5)

    def test_str(self) -> None:
        d = Duration(value=185.0)
        assert str(d) == "3:05"


class TestConfidenceScore:
    def test_creates_valid(self) -> None:
        cs = ConfidenceScore(value=85)
        assert cs.value == 85

    def test_raises_on_below_zero(self) -> None:
        with pytest.raises(InvalidConfidenceError):
            ConfidenceScore(value=-1)

    def test_raises_on_above_100(self) -> None:
        with pytest.raises(InvalidConfidenceError):
            ConfidenceScore(value=101)

    def test_level_very_high(self) -> None:
        assert ConfidenceScore(value=95).level == "Very High"

    def test_level_high(self) -> None:
        assert ConfidenceScore(value=80).level == "High"

    def test_level_medium(self) -> None:
        assert ConfidenceScore(value=60).level == "Medium"

    def test_level_low(self) -> None:
        assert ConfidenceScore(value=30).level == "Low"

    def test_level_very_low(self) -> None:
        assert ConfidenceScore(value=10).level == "Very Low"


class TestCompatibilityScore:
    def test_creates_valid(self) -> None:
        cs = CompatibilityScore(value=85.5)
        assert cs.value == 85.5

    def test_raises_on_below_zero(self) -> None:
        with pytest.raises(ValueError):
            CompatibilityScore(value=-1.0)

    def test_raises_on_above_100(self) -> None:
        with pytest.raises(ValueError):
            CompatibilityScore(value=101.0)

    def test_rating_excellent(self) -> None:
        assert CompatibilityScore(value=95.0).rating == "Excellent"

    def test_rating_very_good(self) -> None:
        assert CompatibilityScore(value=80.0).rating == "Very Good"

    def test_rating_good(self) -> None:
        assert CompatibilityScore(value=65.0).rating == "Good"

    def test_rating_fair(self) -> None:
        assert CompatibilityScore(value=45.0).rating == "Fair"

    def test_rating_poor(self) -> None:
        assert CompatibilityScore(value=20.0).rating == "Poor"

    def test_as_int(self) -> None:
        assert CompatibilityScore(value=85.5).as_int == 86


class TestMixDifficulty:
    def test_transition_bars(self) -> None:
        assert MixDifficulty.VERY_EASY.suggested_transition_bars == 64
        assert MixDifficulty.EASY.suggested_transition_bars == 32
        assert MixDifficulty.MEDIUM.suggested_transition_bars == 32
        assert MixDifficulty.HARD.suggested_transition_bars == 16
        assert MixDifficulty.EXPERT.suggested_transition_bars == 8
