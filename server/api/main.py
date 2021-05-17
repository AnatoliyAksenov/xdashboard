from server.model import main 

from server.model.auth import User, check_user_permissions, get_current_active_user

from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse

BASE_URL = '/api/v1'

restapi = APIRouter(
    prefix=f"{BASE_URL}/main",
    tags=["main"],
    responses={404: {"description": "Not found"}},
)


@restapi.get('/dict/{key}/{format}')
async def get_dictionary(request: Request, current_user: User = Depends(get_current_active_user)):
    """Returns dictionary by key in required format
    """
    key = request.path_params.get('key', None)
    fmt = request.path_params.get('format', 'dict')

    key = key.upper()
    fmt = fmt.lower()

    res = main.get_dictionary(key)
    if res:
        if fmt == 'dict':
            return {x.get('dict_key'):x.get('dict_val') for x in res}
        if fmt == 'list':
            return res

    return None

@restapi.get('/signals_stat')
async def api_signals_info(request: Request, current_user: User = Depends(get_current_active_user)):
    """Returns signal statistics
    """
    res = main.get_signals_stat()

    return res


@restapi.get('/company_balance')
async def rests_by_inn(request: Request, current_user: User = Depends(get_current_active_user)):
    """Возвращает остатки по счетам принадлежащим указанному ИНН
    """
    
    inn = request.query_params.get('inn', None)
    if inn:
        res = main.get_rests_by_inn(inn)
        return res
    
    raise []


@restapi.get('/client_x_inn')
async def clients_by_inn(request: Request, current_user: User = Depends(get_current_active_user)):
    """Возвращает записи из таблицы клиентов содержащие указанный ИНН
    """
    
    inn = request.query_params.get('inn', None)
    if inn:
        res = main.get_client_by_inn(inn)
        return res

    raise []


@restapi.get('/client_x_group')
async def get_groups_data(request: Request, current_user: User = Depends(get_current_active_user)):
    """Возвращает список групп компаний и ИНН входящие в группу        
    """
    res = main.get_inn_groups()

    return res


@restapi.get('/client_loans')
async def get_loaners_monitor(request: Request, current_user: User = Depends(get_current_active_user)):
    """Возвращает данные по задолженности заемщиков банка.
    """

    res = main.get_loaners_monitor()
    
    return request
   