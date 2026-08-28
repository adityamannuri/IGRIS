import sys
from pathlib import Path

import soundfile as sf
import torch

from speechbrain.inference.speaker import SpeakerRecognition
from speechbrain.utils.fetching import LocalStrategy


PROJECT_DIR = Path(__file__).resolve().parent

BOSS_VOICE = PROJECT_DIR / "boss_voice.wav"
MODEL_DIR = PROJECT_DIR / "pretrained_models" / "spkrec-ecapa-voxceleb"

THRESHOLD = 0.22


verification = SpeakerRecognition.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir=str(MODEL_DIR),
    local_strategy=LocalStrategy.COPY_SKIP_CACHE,
)


def load_voice(path: Path) -> torch.Tensor:
    audio, sample_rate = sf.read(str(path), dtype="float32")

    if sample_rate != 16000:
        raise ValueError(
            f"{path.name} is {sample_rate} Hz. Expected 16000 Hz."
        )

    audio_tensor = torch.from_numpy(audio)

    if audio_tensor.ndim > 1:
        audio_tensor = audio_tensor.mean(dim=1)

    return audio_tensor


def is_boss(audio_file: Path) -> bool:
    boss_audio = load_voice(BOSS_VOICE).unsqueeze(0)
    test_audio = load_voice(audio_file).unsqueeze(0)

    score, prediction = verification.verify_batch(
        boss_audio,
        test_audio,
        threshold=THRESHOLD,
    )

    print(f"Score: {score.item()}")
    return bool(prediction.item())


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python voice_checker.py <audio_file>")
        sys.exit(2)

    audio_file = Path(sys.argv[1])

    if not audio_file.exists():
        print(f"Audio file not found: {audio_file}")
        sys.exit(2)

    try:
        if is_boss(audio_file):
            print("BOSS")
            sys.exit(0)
        else:
            print("OTHER")
            sys.exit(1)

    except Exception as error:
        print(f"Voice check error: {error}")
        sys.exit(2)