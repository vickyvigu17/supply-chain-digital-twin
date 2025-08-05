from fastapi import FastAPI

app = FastAPI()

@app.get("/api/")
def root():
    return {"message": "Supply Chain Digital Twin API", "version": "1.0.0"}
