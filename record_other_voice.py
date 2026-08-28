import sounddevice as sd
import soundfile as sf

SAMPLE_RATE = 16000
DURATION = 5
OUTPUT_FILE = "test_voice.wav"

print("Speak naturally for 5 seconds...")

recording = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="float32"
)

sd.wait()

sf.write(OUTPUT_FILE, recording, SAMPLE_RATE)

print("Other voice saved as test_voice.wav")