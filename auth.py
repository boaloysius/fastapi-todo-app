from fastapi import FastAPI

app = FastAPI()


@app.get("/auth/")
async def getUser():
    return {"user": "authenticated"}
