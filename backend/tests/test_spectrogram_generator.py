from pathlib import Path

import numpy as np
import soundfile as sf
from app.audio.services import spectrogram as spectrogram_module
from app.audio.services.spectrogram import SpectrogramGenerator


def test_spectrogram_generator_creates_png_and_directory(tmp_path, monkeypatch) -> None:
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
        spectrogram_module,
        "settings",
        type("SettingsStub", (), {"processed_path": processed_root})(),
    )

    generator = SpectrogramGenerator()
    result = generator.generate(audio_path)

    generated_path = processed_root / "spectrograms" / Path(result.image_path).name

    assert processed_root.joinpath("spectrograms").exists()
    assert generated_path.exists()
    assert result.image_path.startswith("processed/spectrograms/")
    assert result.width == 1200
    assert result.height == 500

    from PIL import Image

    assert Image.open(generated_path).size == (1200, 500)
