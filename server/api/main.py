# from aiohttp import web
import json

from server.model import main 

from fastapi import APIRouter
from fastapi.responses import JSONResponse

restapi = APIRouter()

BASE_URL = '/api/v1'

def serializer( obj ):
    return json.dumps(obj, default=str)


@restapi.get(f'{BASE_URL}/stat/signals_info')
async def api_signals_info(request):
    """Returns signal statistics
    """
    data = main.get_signals_stat()

    return web.json_response( data, dumps=serializer)


@restapi.get(f'{BASE_URL}/company_balance')
async def rests_by_inn(request):
    """Возвращает остатки по счетам принадлежащим указанному ИНН
    """
    
    inn = request.rel_url.query.get('inn', None)
    if inn:
        data = main.get_rests_by_inn(inn)
        return web.json_response( data, dumps=serializer)
    
    raise web.HTTPBadRequest(text='Got empty INN param')


@restapi.get(f'{BASE_URL}/client_x_inn')
async def clients_by_inn(request):
    """Возвращает записи из таблицы клиентов содержащие указанный ИНН
    """
    
    inn = request.rel_url.query.get('inn', None)
    if inn:
        data = main.get_client_by_inn(inn)
        return web.json_response( data, dumps=serializer)

    raise web.HTTPBadRequest(text='Got empty INN param')   


@restapi.get(f'{BASE_URL}/client_x_group')
async def get_groups_data():
    """Возвращает список групп компаний и ИНН входящие в группу        
    """
    res = main.get_inn_groups()

    return web.json_response( data, dumps=serializer)


@restapi.get(f'{BASE_URL}/client_loans')
async def get_loaners_monitor():
    """Возвращает данные по задолженности заемщиков банка.
    """

    res = main.get_loaners_monitor()
    
    return web.json_response( data, dumps=serializer)