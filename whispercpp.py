from whisper_cpp_python import Whisper
from whisper_cpp_python.whisper_cpp import whisper_progress_callback

def callback(ctx, state, i, p):
    print(i)

model = Whisper('C:/Users/shymk/Downloads/ggml-small-q5.bin')
model.params.progress_callback = whisper_progress_callback(callback)

print(model.transcribe('C:/Users/shymk/Documents/Unreal Projects/Whisper_Prototype/Saved/BouncedWavFiles'))