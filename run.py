import uvicorn

if __name__ == "__main__":
    print("http://localhost:8000")
    print("=" * 50)

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
