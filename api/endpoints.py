from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/ping")
def ping():
    return JSONResponse(content={"status": "ok", "message": "Jueguitos.AI is up and running 🚀"})

@router.post("/process-video")
async def process_video(file: UploadFile = File(...)):
    # TODO: Lógica de detección y tracking
    return JSONResponse(content={"message": "Video recibido correctamente."})
