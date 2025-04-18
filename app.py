import os
import tempfile
from fastapi import FastAPI, File, UploadFile
from transformers import pipeline
import torch
from pydub import AudioSegment
import warnings
import json
warnings.filterwarnings('ignore')
app = FastAPI()

with open('./config.json', 'r') as f:
    config = json.load(f)
TEMP_DIR = config['tempDir']
MODEL_NAME = config['modelName']
os.makedirs(TEMP_DIR, exist_ok=True)

# Load model
device = 0 if torch.cuda.is_available() else "cpu"

pipe = pipeline(
    task="automatic-speech-recognition",
    model=MODEL_NAME,
    chunk_length_s=30,
    device=device,
)

def convert_audio(input_path: str, output_path: str):
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format="wav")

def transcribe(audio_path: str):
    text = pipe(audio_path)["text"]
    return text

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    file_ext = file.filename.split(".")[-1].lower()
    # Save file in temp directory
    with tempfile.NamedTemporaryFile(delete=True, suffix=".wav", dir=TEMP_DIR) as temp_audio:
        temp_audio_path = temp_audio.name
        file_bytes = await file.read()
        with open(temp_audio_path, "wb") as f:
            f.write(file_bytes)
        # Convert if MP3
        if file_ext == "mp3":
            wav_path = os.path.join(TEMP_DIR, "converted_" + os.path.basename(temp_audio_path))
            convert_audio(temp_audio_path, wav_path)
            temp_audio_path = wav_path 
        # Transcribe
        transcription = transcribe(temp_audio_path)
    # delete converted file 
    if file_ext == 'mp3':
        if os.path.isfile(temp_audio_path):
            os.remove(temp_audio_path)

    return {"transcription": transcription}
