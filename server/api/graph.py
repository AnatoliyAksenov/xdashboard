# from aiohttp import web
import json
import uuid

from server.model import graph as main 

from fastapi import APIRouter
from fastapi.responses import JSONResponse

restapi = APIRouter()

BASE_URL = '/api/v1'

def serializer( obj ):
    return json.dumps(obj, default=str)


@restapi.post(f'{BASE_URL}/graphs/:uid?')
async def save_graph(request):
    """Сохранение данных по построенному **Графу**
    """
    data = await request.post()
    
    uid = data.get('uid') or uuid.uuid4().hex
    graph = data.get('data', None)

    main.save_graph(uid, graph)

    res = {"uid": uid, "status": "OK"}
    return web.json_response( res, dumps=serializer)  


@restapi.get(f'{BASE_URL}/graphs/list')
async def get_graph_list(request):
    """Возвращает список сохраненных **Графов**
    """
    res = main.get_graph_list()

    return web.json_response( res, dumps=serializer)  


@restapi.get(f'{BASE_URL}/graphs/:uid')
async def get_graph(request):
    """Возвращает данные по сохраненному **Графу**
    """
    uid = request.match_info.get('uid', None)
    res = main.get_graph(uid)

    return web.json_response( res, dumps=serializer)  


@restapi.get(f'{BASE_URL}/graphs/:uid/del')
async def delete_moneyflow_graph_data(request):
    """Удаление построенного графа.

    Выполняется мягкое удаление.
    """
    res = main.delete_graph(uid)

    return web.json_response( res, dumps=serializer) 