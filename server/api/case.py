# from aiohttp import web
import json

from server.model import case as main 

from fastapi import APIRouter
from fastapi.responses import JSONResponse

restapi = APIRouter()

BASE_URL = '/api/v1'

def serializer( obj ):
    return json.dumps(obj, default=str)


@restapi.get(f'{BASE_URL}/cases/list')
async def get_case_list(request):
    """Возвращает список кейсов
    """
    res = main.get_case_list()

    return web.json_response( res, dumps=serializer)     


@restapi.get(f'{BASE_URL}/cases/{{case_id}}')
async def get_case(request):
    """Получение содержимого кейса
    """
    case_id = request.match_info.get('case_id', None)
    if case_id:
        res = main.get_case( int(case_id) )
        return web.json_response( res, dumps=serializer)      
    
    raise web.HTTPBadRequest(text='Got empty case identifier')  


@restapi.get(f'{BASE_URL}/cases/{{case_id}}/graph')
async def get_case_graph(request):
    """Возвращает список __Графов__ сохраненных для **Кейса**
    """
    case_id = request.match_info.get('case_id', None)
    res = main.get_case_graph(case_id)

    return web.json_response( res, dumps=serializer)


@restapi.post(f'{BASE_URL}/cases/new')
async def create_case(request):
    """Создание нового кейса
    """
    data = await request.post()

    res = main.create_case(data)

    return web.json_response( res, dumps=serializer)  


@restapi.post(f'{BASE_URL}/cases/{{case_id}}/edit')
async def edit_case(request):    
    """Редактирование данных **Кейса**
    """
    data = await request.post()
    
    res = main.edit_case(data)

    return web.json_response( res, dumps=serializer)   


@restapi.post(f'{BASE_URL}/cases/{{case_id}}/del')
async def delete_case(request):
    """Удаление **Кейса**

    Производится мягкое удаление. С возможностью восстановить с помощью __Администратора__ системы через базу данных.
    """
    data = await request.post()
    idx  = data.get('id')

    res = main.delete_case(idx) 

    return web.json_response( res, dumps=serializer)


@restapi.get(f'{BASE_URL}/cases/ui/signals')
async def get_case_ui_signals(request):
    """Список сигналов для формы выбора сигналов для кейса.
       Только сигналы в статусе confirmation in (0,1)
    """
    res = main.get_signal_list()

    return web.json_response( res, dumps=serializer)


@restapi.get(f'{BASE_URL}/cases/ui/users')
async def get_users_data(request):
    """Список пользователей системы для формы редактирования и отображения **Кейсов**
    """
    res = main.get_user_list()

    return web.json_response( res, dumps=serializer)


