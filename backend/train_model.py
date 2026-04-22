import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

DATA_PATH = Path(__file__).parent / "data" / "predictiontable.xlsx"
MODEL_DIR  = Path(__file__).parent / "model"
MODEL_PATH = MODEL_DIR / "pd_model.pkl"

FEATURE_COLS = [
    "Length of line drawing",
    "Percentage Difference from Reference Length",
    "Percentage Similarity to Reference Drawing",
    "Number of Times Pen was Lifted",
    "Average angle between consecutive groups of 3 points",
]
TARGET_COL = "Prediction of Parkinson's Disease"


def train():
    if not DATA_PATH.exists():
        print(f"ERROR: training data not found at {DATA_PATH}", file=sys.stderr)
        sys.exit(1)

    df = pd.read_excel(DATA_PATH)

    X = df[FEATURE_COLS]
    y = df[TARGET_COL]

    # stratify=y ensures both classes are proportionally represented in train
    # and test — critical with small datasets to avoid a biased split.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = GaussianNB()
    clf.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, clf.predict(X_test))
    print(f"Test accuracy: {accuracy:.4f}")

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(clf, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    train()
