# from aiohttp import web
import json

from server.model import cases as main 

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

BASE_URL = '/api/v1'

restapi = APIRouter(
    prefix=f"{BASE_URL}/cases",
    tags=["cases"],
    responses={404: {"description": "Not found"}},
)


@restapi.get('/all')
async def get_case_all(request: Request):
    """Возвращает список кейсов
    """
    data = dict(request.query_params)
    res = main.get_case_list()

    return res     


@restapi.get('/{case_id}')
async def get_case(request: Request):
    """Получение содержимого кейса
    """
    case_id = request.path_params.get('case_id', None)
    
    res = main.get_case( int(case_id) )
    return res
    

@restapi.get('/{case_id}/graph')
async def get_case_graph(request: Request):
    """Возвращает список __Графов__ сохраненных для **Кейса**
    """
    case_id = request.path_params.get('case_id', None)
    res = main.get_case_graph(case_id)

    return res


@restapi.post('/new')
async def create_case(request: Request):
    """Создание нового кейса
    """
    data = request.json()

    res = main.create_case(data)

    return res


@restapi.post('{case_id}/edit')
async def edit_case(request):    
    """Редактирование данных **Кейса**
    """
    data = request.json()
    case_id = request.path_params.get('case_id', None)
    data['case_id'] = case_id

    res = main.edit_case(data)

    return res


@restapi.delete('/{case_id}/del')
async def delete_case(request: Request):
    """Удаление **Кейса**
    Производится мягкое удаление. С возможностью восстановить с помощью __Администратора__ системы через базу данных.
    """
    case_id = request.path_params.get('case_id', None)

    res = main.delete_case(case_id) 

    return res


@restapi.get('/ui/signals')
async def get_case_ui_signals(request: Request):
    """Список сигналов для формы выбора сигналов для кейса.
       Только сигналы в статусе confirmation in (0,1)
    """
    res = main.get_signal_list()

    return res


@restapi.get('/ui/users')
async def get_users_data(request: Request):
    """Список пользователей системы для формы редактирования и отображения **Кейсов**
    """
    res = main.get_user_list()

    return res


