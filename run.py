import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Starting TriMessage Server....")
    print("http://127.0.0.1:8000/")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False
    )
