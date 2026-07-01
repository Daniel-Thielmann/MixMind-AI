from pathlib import Path

import numpy as np
import soundfile as sf
from app.audio.services import waveform as waveform_module
from app.audio.services.analyzer import AudioAnalyzer
from app.audio.services.waveform import WaveformGenerator


def test_waveform_generator_creates_png_and_directory(tmp_path, monkeypatch) -> None:
    audio_path = tmp_path / "track.wav"
    sample_rate = 44100
    duration_seconds = 1.0
    time = np.linspace(
        0.0,
        duration_seconds,
        int(sample_rate * duration_seconds),
        endpoint=False,
    )
    waveform = 0.2 * np.sin(2 * np.pi * 128.0 * time)
    stereo = np.column_stack([waveform, waveform])
    sf.write(audio_path, stereo, sample_rate)

    processed_root = tmp_path / "processed"
    monkeypatch.setattr(
        waveform_module,
        "settings",
        type("SettingsStub", (), {"processed_path": processed_root})(),
    )

    generator = WaveformGenerator()
    result = generator.generate(audio_path)

    generated_path = processed_root / "waveforms" / Path(result.image_path).name

    assert processed_root.joinpath("waveforms").exists()
    assert generated_path.exists()
    assert result.image_path.startswith("processed/waveforms/")
    assert result.width == 1200
    assert result.height == 300

    from PIL import Image

    assert Image.open(generated_path).size == (1200, 300)


def test_audio_analyzer_extracts_audio_metrics(tmp_path) -> None:
    audio_path = tmp_path / "track.wav"
    sample_rate = 44100
    duration_seconds = 2.0
    time = np.linspace(
        0.0, duration_seconds, int(sample_rate * duration_seconds), endpoint=False
    )
    waveform = 0.2 * np.sin(2 * np.pi * 128.0 * time)
    stereo = np.column_stack([waveform, waveform])
    sf.write(audio_path, stereo, sample_rate)

    result = AudioAnalyzer().analyze(audio_path)

    assert result.filename == "track.wav"
    assert result.sample_rate == sample_rate
    assert result.duration == 2.0
    assert result.energy > 0
