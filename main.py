from fastapi import FastAPI, Response
from gtts import gTTS
import io

app = FastAPI()

@app.get("/tts")
async def text_to_speech(text: str, voice: str = "bn"):
    try:
        # Google-TTS generates audio in Bengali
        tts = gTTS(text=text, lang='bn')
        audio_data = io.BytesIO()
        tts.write_to_fp(audio_data)
        
        audio_data.seek(0)
        return Response(content=audio_data.read(), media_type="audio/mpeg")
    except Exception as e:
        return Response(content=str(e), status_code=500)

@app.get("/")
async def root():
    return {"status": "Google-TTS Server is Live!"}
