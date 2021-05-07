import uvicorn
import os
import logging
import secrets

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles

from fastapi import HTTPException, status
from fastapi.responses import FileResponse

from server.api.auth import restapi as auth_api
from server.api.main import restapi as main_api
from server.api.cases import restapi as cases_api
from server.api.graph import restapi as graph_api
from server.api.signals import restapi as signals_api

logging.basicConfig(level=logging.DEBUG, filename="board.log")
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
async def root_index():
    return FileResponse("dist/index.html")

@app.get("/index.html")
async def root_index():
    return FileResponse("dist/index.html")

app.mount("/static", StaticFiles(directory="dist/static"), name="dict")

# HANDLE ROUTES
## restapi routes
app.include_router(auth_api)
app.include_router(main_api)
app.include_router(cases_api)
# app.add_routes(graph_api)
app.include_router(signals_api)



if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")