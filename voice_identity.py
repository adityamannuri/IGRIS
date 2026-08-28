from pathlib import Path
from speechbrain.inference.speaker import SpeakerRecognition
from speechbrain.utils.fetching import LocalStrategy

BOSS_VOICE = Path("boss_voice.wav")
MODEL_DIR = Path("pretrained_models") / "spkrec-ecapa-voxceleb"

print("Loading I.G.R.I.S. speaker-recognition model...")

verification = SpeakerRecognition.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir=str(MODEL_DIR),
    local_strategy=LocalStrategy.COPY_SKIP_CACHE,
)

print("Model loaded successfully.")
print("Comparing test voice with boss voice...")

score, prediction = verification.verify_batch(
    verification.load_audio(str(BOSS_VOICE)).unsqueeze(0),
    verification.load_audio(str(BOSS_VOICE),).unsqueeze(0),
    threshold=0.5,
)

print("Score:", score.item())
print("Prediction:", prediction.item())