import edge_tts
from fastapi import FastAPI, Response
import io

app = FastAPI()

@app.get("/tts")
async def text_to_speech(text: str, voice: str = "bn-BD-BashkarNeural"):
    """
    Takes text and a voice name, generates speech using Edge-TTS, 
    and returns an MP3 audio file.
    """
    try:
        # Create speech from text
        # Specifically using bn-BD-BashkarNeural for high-quality Bengali voice
        communicate = edge_tts.Communicate(text, voice)
        audio_data = io.BytesIO()
        
        # Stream the audio to buffer
        async for chunk in communicate.stream():
            if chunk["data"]:
                audio_data.write(chunk["data"])
        
        audio_data.seek(0)
        return Response(content=audio_data.read(), media_type="audio/mpeg")
    except Exception as e:
        return Response(content=f"Error generating speech: {str(e)}", status_code=500)

@app.get("/")
async def root():
    return {"status": "Tura POS Edge-TTS Server is Live!"}

if __name__ == "__main__":
    import uvicorn
    # Local testing: uvicorn main:app --reload
    uvicorn.run(app, host="0.0.0.0", port=8000)
