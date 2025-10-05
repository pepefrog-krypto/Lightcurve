# server/app.py
import io
from typing import List, Dict, Any, Optional

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import joblib

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# -------------------------
# Config FastAPI + CORS
# -------------------------
app = FastAPI(title="Lightcurve Model API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # en prod: pon tu dominio(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Modelo exactamente como el tuyo
# -------------------------
INPUT_DIM = 34  # tu capa de entrada
H1 = H2 = H3 = 64
H4 = 32

model = nn.Sequential(
    nn.Linear(INPUT_DIM, H1),
    nn.ReLU(),
    nn.Linear(H1, H2),
    nn.ReLU(),
    nn.Linear(H2, H3),
    nn.ReLU(),
    nn.Linear(H3, H4),
    nn.ReLU(),
    nn.Linear(H4, 1)  # logits (¡sin sigmoid!)
)

# columnas a eliminar (como en tu script original)
DROP_COLS = ['koi_score', 'koi_fpflag_nt', 'koi_fpflag_ss', 'koi_fpflag_co', 'koi_fpflag_ec']

device = "cpu"  # cambia a "cuda" si tienes GPU configurada

# -------------------------
# Carga de artefactos
# -------------------------
try:
    print("loading model...")
    state = torch.load("model.pth", map_location=device)
    model.load_state_dict(state)
    model.eval().to(device)
except Exception as e:
    raise RuntimeError(f"Could not load model.pth: {e}")

try:
    scaler = joblib.load("scaler.pkl")
except Exception as e:
    raise RuntimeError(f"Could not load scaler.pkl: {e}")

# Si el scaler conoce los nombres de columnas usadas en entrenamiento:
TRAIN_COLUMNS: Optional[List[str]] = None
if hasattr(scaler, "feature_names_in_"):
    TRAIN_COLUMNS = list(scaler.feature_names_in_)  # numpy array -> list


# -------------------------
# Utilidades de preprocesado
# -------------------------
def coerce_numeric_df(df: pd.DataFrame) -> pd.DataFrame:
    # Asegura numérico, elimina NaN
    df = df.apply(pd.to_numeric, errors="coerce").dropna()
    return df

def ensure_column_order(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ordena/selecciona columnas para coincidir con el entrenamiento.
    Si TRAIN_COLUMNS existe, reindexa; si no, deja como viene.
    """
    if TRAIN_COLUMNS is not None:
        missing = [c for c in TRAIN_COLUMNS if c not in df.columns]
        if missing:
            raise ValueError(f"Missing columns in input: {missing}")
        df = df.reindex(columns=TRAIN_COLUMNS)
    return df

def transform_and_build_tensor(df: pd.DataFrame) -> torch.Tensor:
    """
    - Alinea columnas a entrenamiento (si tenemos TRAIN_COLUMNS)
    - Aplica scaler
    - Elimina columnas DROP_COLS
    - Verifica la dimensionalidad (INPUT_DIM)
    - Devuelve tensor float32 listo para el modelo
    """
    if df.empty:
        raise ValueError("Input DataFrame is empty after cleaning.")

    # Alinear columnas a entrenamiento
    df = ensure_column_order(df)

    # Escalar
    try:
        df_scaled = pd.DataFrame(
            scaler.transform(df),
            columns=df.columns
        )
    except Exception as e:
        raise ValueError(f"Scaler transform failed: {e}")

    # Eliminar columnas no usadas por el modelo
    for col in DROP_COLS:
        if col in df_scaled.columns:
            df_scaled = df_scaled.drop(columns=[col])

    if df_scaled.shape[1] != INPUT_DIM:
        raise ValueError(
            f"Model expects {INPUT_DIM} features, got {df_scaled.shape[1]} after drop(). "
            f"Columns now: {list(df_scaled.columns)}"
        )

    X = torch.tensor(df_scaled.values, dtype=torch.float32, device=device)
    return X

def infer_tensor(X: torch.Tensor) -> Dict[str, Any]:
    """
    Corre el modelo (sin gradiente), calcula probabilidades sigmoide y umbral 0.5.
    Devuelve listas de probs y labels.
    """
    with torch.no_grad():
        logits = model(X)               # [N, 1]
        probs = torch.sigmoid(logits)   # [N, 1]
        labels = (probs > 0.5).int()    # [N, 1]

    return {
        "probabilities": probs.cpu().numpy().reshape(-1).tolist(),
        "labels": labels.cpu().numpy().reshape(-1).tolist(),
        "count": int(X.shape[0]),
    }


# -------------------------
# Esquemas para JSON
# -------------------------
class Record(BaseModel):
    # diccionario de {nombre_columna: valor}
    __root__: Dict[str, float]

class JsonPayload(BaseModel):
    records: List[Record] = Field(
        ..., description="List of row dicts: [{col: val, ...}, ...]"
    )


# -------------------------
# Endpoints
# -------------------------
@app.get("/health")
def health():
    return {"status": "ok", "model_input_dim": INPUT_DIM, "train_columns": TRAIN_COLUMNS}

@app.post("/predict/csv")
async def predict_csv(file: UploadFile = File(...)):
    """
    Recibe CSV. Limpia -> escala -> drop columnas -> predice.
    Respuesta: probabilities[], labels[], count.
    """
    try:
        raw = await file.read()
        # detecta encoding básico
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("latin-1", errors="ignore")

        # pandas lee desde buffer
        df = pd.read_csv(io.StringIO(text))
        df = coerce_numeric_df(df)

        X = transform_and_build_tensor(df)
        out = infer_tensor(X)
        return {"ok": True, **out}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/predict/json")
def predict_json(payload: JsonPayload):
    """
    Recibe JSON: {"records": [ {col: val, ...}, ... ]}
    """
    try:
        # Convierte lista de dicts a DataFrame
        rows: List[Dict[str, float]] = [r.__root__ for r in payload.records]
        df = pd.DataFrame(rows)
        df = coerce_numeric_df(df)

        X = transform_and_build_tensor(df)
        out = infer_tensor(X)
        return {"ok": True, **out}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

