import edge_tts
from fastapi import FastAPI, Response
import io
import asyncio

app = FastAPI()

@app.get("/tts")
async def text_to_speech(text: str, voice: str = "bn-BD-BashkarNeural"):
    try:
        # Create speech from text
        communicate = edge_tts.Communicate(text, voice)
        audio_data = io.BytesIO()
        
        # Proper async streaming to buffer
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data.write(chunk["data"])
        
        audio_data.seek(0)
        content = audio_data.read()
        
        if not content:
            return Response(content="Audio generation failed", status_code=500)
            
        return Response(content=content, media_type="audio/mpeg")
    except Exception as e:
        print(f"Error: {str(e)}")
        return Response(content=str(e), status_code=500)

@app.get("/")
async def root():
    return {"status": "Tura POS Edge-TTS Server is Live!"}
