# API transcribes voice with a custom model by Fast API 

You can customise a model (model that can run in the pipeline from transformers) for transcribes in the config.json file.

## Exemple 
- Run services by uvicorn
```
uvicorn app:app --host 0.0.0.0 --port 8000
```
- Test Run
```
import requests
url = "http://0.0.0.0:8000/transcribe"

audio_file_path = "common_voice_th_23646618.mp3"

with open(audio_file_path, "rb") as audio_file:
    files = {"file": (audio_file_path, audio_file, "audio/wav")}  
    response = requests.post(url, files=files)
print(response.json()) 
```
