# FastAPI Endpoint

from fastapi import FastAPI

app = FastAPI(title = "EAIOS", version = "0.1.0")

@app.get("/health")
def health () -> dict[str, str]:
    "Report that the server is running"
    return {"status": "ok"}