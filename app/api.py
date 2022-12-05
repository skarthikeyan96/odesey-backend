from fastapi import FastAPI

app = FastAPI()

@app.get("/", tags=["Home"])
def get_root() -> dict:
    return {
        "message": "Welcome to the okteto's app."
    }