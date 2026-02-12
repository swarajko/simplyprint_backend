from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.printers import router as printers_router

app = FastAPI(
    title="PrintFarm Onground Backend",
    description="Intranet service for 3D printer orchestration and monitoring",
    version="1.0.0"
)

# Add CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "PrintFarm Onground Backend Service", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "onground-backend"}

app.include_router(printers_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4000)
