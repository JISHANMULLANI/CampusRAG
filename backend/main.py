from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from api.health import router as health_router
from api.documents import router as documents_router
from api.chat import router as chat_router


app = FastAPI(
    title="Hybrid RAG College Knowledge Assistant"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# API ROUTES
# ==========================================

app.include_router(health_router)
app.include_router(documents_router)
app.include_router(chat_router)


# ==========================================
# FRONTEND
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

FRONTEND_DIR = BASE_DIR / "frontend"


@app.get("/")
def serve_frontend():

    return FileResponse(
        FRONTEND_DIR / "index.html"
    )


@app.get("/style.css")
def serve_css():

    return FileResponse(
        FRONTEND_DIR / "style.css",
        media_type="text/css"
    )


@app.get("/script.js")
def serve_javascript():

    return FileResponse(
        FRONTEND_DIR / "script.js",
        media_type="application/javascript"
    )