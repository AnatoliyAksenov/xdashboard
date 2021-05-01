import uvicorn
import os
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fastapi.responses import FileResponse

from server.api.main import restapi as main_api
from server.api.case import restapi as case_api
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
# app.add_routes(main_api)
# app.add_routes(case_api)
# app.add_routes(graph_api)
app.include_router(signals_api)



if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")