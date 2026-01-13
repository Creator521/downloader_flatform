from fastapi import FastAPI

app = FastAPI(title="Downloader Platform")

@app.get("/health")
def health():
    return {"status": "ok"}
