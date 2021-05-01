import io
import zipfile

from server.sources import corp


get_data = corp.get_data
execute = corp.execute

def save_graph(uid, data):
    q = """
    insert into tbl_graph_moneyflow (uid, zdata, user_id)
                             values (%(uid)s, %(zdata)s, %(user_id)s)
    ON DUPLICATE KEY UPDATE 
        zdata = %(zdata)s,
        user_id = %(user_id)s     
    """
    zdata = io.BytesIO()
    zfile = zipfile.ZipFile(zdata, 'w', zipfile.ZIP_DEFLATED, False)
    zfile.writestr('content.json', data)
    zfile.close()
    zdata.seek(0)

    execute([q, 'COMMIT;'], {"uid":uid, "zdata": zdata.getvalue(), "user_id": current_user.corp_id})

    return True


def get_graph_list():
    q = """
    select uid,
           inn,
           data_date,
           summ,
           creator,
           user_id
           -- graph_data
       from v_graph_moneyflow  
    """

    res = get_data(q)

    return res

def get_graph(uid):
    q = """
    select uid,
           inn,
           data_date,
           summ,
           creator,
           user_id,
           graph_data
      from v_graph_moneyflow
     where uid = %(uid)s
    """

    res = get_data(q, {"uid": uid})
    if len(res)> 0:
        zfile = zipfile.ZipFile(io.BytesIO(res[0]['graph_data']), 'r', zipfile.ZIP_DEFLATED, False)
        uzdata = zfile.read('content.json')
        res[0]['graph_data'] = uzdata.decode('utf-8')


    return res


def delete_graph(uid):
    q = """
    update tbl_graph_moneyflow
       set isd = 1
     where uid = %(uid)s
    """

    execute([q, 'COMMIT;'], {"uid": uid})

    return True 
