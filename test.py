# import uvicorn
# from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import PlainTextResponse

# app = FastAPI()


# app.mount("/", StaticFiles(directory="dist"), name="dict")

# @app.get("/test")
# async def read_root():
#     return PlainTextResponse('pong')


# if __name__ == "__main__":

#     uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/test")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")