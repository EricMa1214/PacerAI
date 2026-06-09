from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
from app.database import supabase

load_dotenv()

app = FastAPI()


# --- Define the shape of an incoming run ---
class RunCreate(BaseModel):
    run_date: str          # e.g. "2026-06-09"
    distance: float        # in kilometers, e.g. 5.0
    duration_seconds: int  # total run time in seconds, e.g. 1680
    avg_heart_rate: Optional[int] = None  # optional
    notes: Optional[str] = None           # optional


# --- Existing endpoints ---
@app.get("/")
def root():
    return {"message": "Welcome to PacerAI 🏃"}


@app.get("/health")
def health():
    return {"status": "ok"}


# --- Log a new run ---
@app.post("/runs")
def create_run(run: RunCreate):
    response = supabase.table("runs").insert(run.model_dump()).execute()
    return {"message": "Run logged!", "data": response.data}


# --- Get runs ---
@app.get("/runs")
def get_runs():
    response = supabase.table("runs").select("*").order("run_date", desc=True).execute()
    return {"count": len(response.data), "data": response.data}