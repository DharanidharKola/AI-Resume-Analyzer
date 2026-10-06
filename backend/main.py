from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import uvicorn
from backend.utils import extract_text_from_pdf, analyze_resume

app = FastAPI()

class JDModel(BaseModel):
    job_description: str
    resume_text: str

@app.post("/analyze")
def analyze(data: JDModel):
    result = analyze_resume(data.resume_text, data.job_description)
    return result

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    text = extract_text_from_pdf(await file.read())
    return {"resume_text": text}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)