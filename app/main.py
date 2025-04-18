from fastapi import FastAPI

from app.routers import company

app = FastAPI()

@app.get("/")
async def main():
	return {"message": "Hello World"}

app.include_router(company.router)
