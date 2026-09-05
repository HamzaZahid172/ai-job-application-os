from pathlib import Path
import shutil

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.config import settings
from backend.models import (
    JobAnalysisRequest,
    JobAnalysisResponse,
    CoverLetterRequest,
    CoverLetterResponse,
    ApplicationCreate,
    ApplicationOut,
    CandidateProfile,
)
from backend.services.llm_client import parse_job, generate_cover_letter
from backend.services.matcher import analyze_match
from backend.database import init_db, create_application, list_applications
from backend.services.cv_parser import load_candidate_from_cv

app = FastAPI(
    title=settings.app_name,
    version="1.1.0",
    description="AI-assisted job analysis, CV matching, cover-letter generation, and application tracking.",
)

STATIC_DIR = Path("frontend")
CV_DIR = Path("data/cv")
DEFAULT_CV = CV_DIR / "DEFAULT_CV.pdf"
ACTIVE_CV = CV_DIR / "active_cv.pdf"

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.on_event("startup")
def startup() -> None:
    init_db()
    CV_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/")
def home():
    index = STATIC_DIR / "index.html"
    if index.exists():
        return FileResponse(index)
    return {"message": settings.app_name, "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok", "llm_enabled": settings.use_llm, "llm_model": settings.ollama_model}


def get_current_candidate() -> CandidateProfile:
    if ACTIVE_CV.exists():
        return load_candidate_from_cv(str(ACTIVE_CV))
    if DEFAULT_CV.exists():
        return load_candidate_from_cv(str(DEFAULT_CV))
    return CandidateProfile()


@app.get("/candidate", response_model=CandidateProfile)
def current_candidate():
    return get_current_candidate()


@app.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...)):
    filename = file.filename or "candidate.pdf"
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF CV files are supported.")

    CV_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with ACTIVE_CV.open("wb") as destination:
            shutil.copyfileobj(file.file, destination)
        candidate = load_candidate_from_cv(str(ACTIVE_CV))
    except Exception as exc:
        ACTIVE_CV.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail=f"Could not read CV: {exc}")
    finally:
        await file.close()

    return {
        "message": "CV uploaded and parsed successfully.",
        "filename": filename,
        "candidate": candidate.model_dump(),
    }


@app.delete("/upload-cv")
def clear_uploaded_cv():
    ACTIVE_CV.unlink(missing_ok=True)
    return {"message": "Uploaded CV cleared. Default CV/profile will be used."}


@app.post("/analyze-job", response_model=JobAnalysisResponse)
async def analyze_job(payload: JobAnalysisRequest):
    candidate = payload.candidate or get_current_candidate()
    parsed = await parse_job(payload.job_description)
    return analyze_match(parsed, candidate)


@app.post("/generate-cover-letter", response_model=CoverLetterResponse)
async def cover_letter(payload: CoverLetterRequest):
    candidate = payload.candidate or get_current_candidate()
    letter = await generate_cover_letter(
        payload.job_description,
        candidate,
        payload.tone,
    )
    return CoverLetterResponse(cover_letter=letter)


@app.post("/applications", response_model=ApplicationOut)
def save_application(payload: ApplicationCreate):
    try:
        return create_application(payload)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))


@app.get("/applications", response_model=list[ApplicationOut])
def get_applications():
    return list_applications()
