import edge_tts
from fastapi import FastAPI, Response
import io

app = FastAPI()

@app.get("/tts")
async def text_to_speech(text: str, voice: str = "bn-BD-BashkarNeural"):
    try:
        # Create speech from text
        # Using a direct communicate and saving to buffer
        communicate = edge_tts.Communicate(text, voice)
        
        audio_data = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data.write(chunk["data"])
        
        audio_content = audio_data.getvalue()
        
        if len(audio_content) == 0:
            return Response(content="No audio generated", status_code=500)
            
        return Response(content=audio_content, media_type="audio/mpeg")
    except Exception as e:
        print(f"Error: {str(e)}")
        return Response(content=f"Internal Error: {str(e)}", status_code=500)

@app.get("/")
async def root():
    return {"status": "Tura POS Edge-TTS Server is Live!"}
