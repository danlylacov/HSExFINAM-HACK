from fastapi import FastAPI
from backend_api.services.model_service import load_models
from backend_api.routers import predict, train, health

app = FastAPI(title="Price Prediction API", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    if not load_models():
        print("Warning: Models not loaded. Train models first.")

app.include_router(health.router)
app.include_router(predict.router)
app.include_router(train.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009)
