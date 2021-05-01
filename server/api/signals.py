# from aiohttp import web
import json

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

BASE_URL = '/api/v1'

restapi = APIRouter(
    prefix=f"{BASE_URL}/signals",
    tags=["signals"],
    responses={404: {"description": "Not found"}},
)

from server.model import signals as main 


@restapi.get('/all')
async def get_signal_list_limit(request: Request):
    """Возвращает данные по всем сигналам с установленными ограничениями для формы списка сигналов.
    """
    data = dict(request.query_params)
    
    res = main.get_signal_list_limit(data)    

    return res


@restapi.get('/{id}')
async def get_ui_data_cs_signals(request: Request):
    """ Возвращает результат выполнения запросов для каждого сигнала. Запросы для сигналов хранятся в таблице __tbl_conf_sig_query__.
    """
    idx = request.path_params.get('id', None)
    res = main.get_ui_data(idx)

    return res