import json
import math
from datetime import datetime
from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ml2 import average_angle_between_groups

app = FastAPI(title="PD Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Reference spiral ──────────────────────────────────────────────────────────

def _generate_spiral(canvas_size: int = 200, turns: float = 2.5, samples: int = 500) -> list:
    """Generate an Archimedean spiral as a list of [x, y] points."""
    cx = cy = canvas_size / 2
    max_r = canvas_size / 2 - 8
    points = []
    for i in range(samples):
        t = i / (samples - 1)
        angle = t * turns * 2 * math.pi
        r = t * max_r
        x = round(cx + r * math.cos(angle))
        y = round(cy + r * math.sin(angle))
        points.append([x, y])
    return points


def _path_length(points: list) -> float:
    total = 0.0
    for i in range(len(points) - 1):
        dx = points[i + 1][0] - points[i][0]
        dy = points[i + 1][1] - points[i][1]
        total += math.sqrt(dx * dx + dy * dy)
    return total


REFERENCE_POINTS = _generate_spiral(canvas_size=400)
REFERENCE_LENGTH = _path_length(REFERENCE_POINTS)

# ── ML model ──────────────────────────────────────────────────────────────────

MODEL_PATH = Path(__file__).parent / "model" / "pd_model.pkl"
_model = None


@app.on_event("startup")
async def startup():
    global _model
    if MODEL_PATH.exists():
        _model = joblib.load(MODEL_PATH)
    else:
        print(
            "WARNING: model file not found. "
            "Run `python backend/train_model.py` then restart the server."
        )


# ── Request / response schemas ────────────────────────────────────────────────

class PredictRequest(BaseModel):
    line_length: float
    length_pct_diff: float
    match_pct: float
    pen_lifts: int
    avg_angle: float


class SubmitRequest(BaseModel):
    features: PredictRequest
    prediction: str
    save_drawing: bool = False
    drawing_data: list = []


class AngleRequest(BaseModel):
    points: list   # list of [x, y]


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/reference")
def get_reference():
    """Return the reference spiral points and its total pixel length."""
    return {"points": REFERENCE_POINTS, "length": REFERENCE_LENGTH}


@app.post("/predict")
def predict(req: PredictRequest):
    """Run the GaussianNB model and return a prediction with confidence."""
    if _model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Run `python backend/train_model.py` then restart the server.",
        )
    features = [[
        req.line_length,
        req.length_pct_diff,
        req.match_pct,
        req.pen_lifts,
        req.avg_angle,
    ]]
    prediction = _model.predict(features)[0]
    probabilities = _model.predict_proba(features)[0]
    confidence = float(max(probabilities))
    return {"prediction": str(prediction), "confidence": round(confidence, 4)}


@app.post("/angle")
def angle(req: AngleRequest):
    """Calculate the average angle between consecutive groups of 3 points."""
    if len(req.points) < 3:
        return {"avg_angle": 0.0}
    avg = average_angle_between_groups(req.points, group_size=3)
    return {"avg_angle": round(avg, 6)}


@app.post("/submit")
def submit(req: SubmitRequest):
    """Optionally persist a drawing + its features and prediction to a local JSON file."""
    if not req.save_drawing:
        return {"status": "skipped"}

    submissions_path = Path(__file__).parent / "data" / "submissions.json"
    try:
        if submissions_path.exists():
            with open(submissions_path) as f:
                submissions = json.load(f)
        else:
            submissions = []

        submissions.append({
            "timestamp": datetime.utcnow().isoformat(),
            "features": req.features.dict(),
            "prediction": req.prediction,
            "drawing_data": req.drawing_data,
        })

        with open(submissions_path, "w") as f:
            json.dump(submissions, f, indent=2)

        return {"status": "saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
