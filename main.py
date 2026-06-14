from fastapi import FastAPI, HTTPException, status
import uvicorn
from routers import book_routes, report_routes


app = FastAPI()

app.include_router(book_routes.router)
app.include_router(report_routes.router)




if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)