# PD App V2 — Parkinson's Disease Detection App

A reworked version of the original [PD App (v1)](https://github.com/RadioActiveChilli/PD-App) — a web-based tool where users trace a spiral on a drawing canvas. The drawing is then analysed using five metrics and a trained Naive Bayes classifier to predict the likelihood of Parkinson's Disease.

> **Note:** This is the updated version of the original PD App (created May 2024). The original project can be found at [RadioActiveChilli/PD-App](https://github.com/RadioActiveChilli/PD-App).

> **Disclaimer:** This application is for research and educational purposes only. It is not a clinical diagnostic tool. Please consult a qualified medical professional for any health concerns.

---

## What's new in V2

This is a ground-up rework of the original COMP390 university project. Key changes:

- **FastAPI backend** replacing Firebase — predictions are served from a real ML model via a REST API
- **Five ML features** instead of three hardcoded thresholds (adds average drawing angle and length percentage difference)
- **GaussianNB model** properly trained, saved, and loaded — the original never connected its Python model to the frontend
- **400×400 canvas** — doubled from the original 200×200
- **Touch support** — works on tablets and phones
- **Clean project structure** — `frontend/` and `backend/` separation
- **Five bug fixes** from the original (see below)

### Bug fixes from v1

| # | Bug | Fix |
|---|---|---|
| 1 | Pen lift count used `click` events, missing drag strokes | Switched to `mousedown` counting with `-1` initial value |
| 2 | `clickCount` used in thresholds but `clickCount-1` shown in display | Single `penLifts` variable used everywhere |
| 3 | Length reason string condition (`≤5 OR ≥-5`) was always true | Fixed to `>5 OR <-5` — only fires outside the ±5% band |
| 4 | `calculateMatchPercentage` was O(n²) | Rewritten using a `Set` for O(n) lookup |
| 5 | `totalLength` reset to 0 on every `mousedown` | Removed reset from `startDrawing()` — only resets on Clear |

---

## Project structure

```
PD App V2/
├── frontend/
│   ├── index.html          # Drawing interface and results panel
│   └── assets/
│       └── BGspiral.png    # Background spiral reference image
└── backend/
    ├── main.py             # FastAPI app (GET /reference, POST /predict, POST /angle, POST /submit)
    ├── train_model.py      # Trains GaussianNB and saves model to backend/model/
    ├── ml2.py              # Average drawing angle calculation utility
    ├── requirements.txt    # Python dependencies
    └── data/
        ├── predictiontable.xlsx   # Labelled training dataset
        └── new_drawing_data.xlsx  # Additional collected data
```

---

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/reference` | Returns the reference spiral points and total length |
| `POST` | `/predict` | Accepts 5 features, returns ML prediction and confidence |
| `POST` | `/angle` | Accepts drawing points, returns average angle |
| `POST` | `/submit` | Optionally saves drawing + result to `data/submissions.json` |

---

## The 5 ML features

1. Length of line drawing (pixels)
2. Percentage difference from reference length
3. Percentage similarity to reference drawing
4. Number of times pen was lifted
5. Average angle between consecutive groups of 3 points

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/RadioActiveChilli/PD-App-V2.git
cd PD-App-V2
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r backend/requirements.txt
```

### 3. Train the model

```bash
python backend/train_model.py
```

This reads `backend/data/predictiontable.xlsx`, trains a GaussianNB classifier, and saves the model to `backend/model/pd_model.pkl`.

### 4. Start the backend server

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 5. Open the frontend

Open `frontend/index.html` directly in a browser. The page will call the backend on `localhost:8000`.

---

## Resources

- [NHS — Parkinson's Disease](https://www.nhs.uk/conditions/parkinsons-disease/)
- [International Parkinson and Movement Disorder Society](https://www.movementdisorders.org/)
- [WHO — Parkinson Disease Fact Sheet](https://www.who.int/news-room/fact-sheets/detail/parkinson-disease)
- [Parkinson's Foundation — Global Care Network](https://www.parkinson.org/living-with-parkinsons/finding-care/global-care-network)
