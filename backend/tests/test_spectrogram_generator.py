from pathlib import Path

import numpy as np
import soundfile as sf
from app.infrastructure.audio.spectrogram import SpectrogramGenerator


def test_spectrogram_generator_creates_png_and_directory(tmp_path) -> None:
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

    generator = SpectrogramGenerator(output_dir=tmp_path / "spectrograms")
    result = generator.generate(audio_path)

    from PIL import Image

    generated_path = tmp_path / "spectrograms" / Path(result.image_path).name
    assert generated_path.exists()
    assert result.width == 1200
    assert result.height == 500

    assert Image.open(generated_path).size == (1200, 500)
