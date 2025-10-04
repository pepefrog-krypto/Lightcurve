print("loading libraries...")
import torch
import torch.nn as nn
import pandas as pd
import joblib

model = nn.Sequential(
    nn.Linear(34, 64),   # input → hidden
    nn.ReLU(),
    nn.Linear(64, 64),   # hidden → hidden
    nn.ReLU(),
    nn.Linear(64, 64),   # hidden → hidden
    nn.ReLU(),
    nn.Linear(64, 32),   # hidden → hidden
    nn.ReLU(),
    nn.Linear(32, 1)     # hidden → output (no Sigmoid here!)
)

print("loading model...")
model.load_state_dict(torch.load("model.pth"))
model.eval()

scaler = joblib.load("scaler.pkl")
model.eval()

df_new = pd.read_csv("dummy.csv")
df_new = df_new.dropna()
df_new = df_new.apply(pd.to_numeric, errors="coerce").astype("float64")

df_new_scaled = pd.DataFrame(scaler.transform(df_new), columns=df_new.columns)
X_new = df_new_scaled.drop(['koi_score', 'koi_fpflag_nt', 'koi_fpflag_ss', 'koi_fpflag_co', 'koi_fpflag_ec'], axis=1).values
X_new = torch.tensor(X_new, dtype=torch.float32)

#dummy = torch.randn(1, 3, 224, 224)  # ajusta al input real

torch.onnx.export(
    model, X_new, "model.onnx",
    input_names=["input"], output_names=["output"],
    opset_version=17,
    dynamic_axes={"input": {0: "batch"}, "output": {0: "batch"}}
)
