import datetime
import pendulum 

from server.sources import corp

get_data = corp.get_data
execute = corp.execute


#TODO: Change to pendulum.parse if it possible
def cast_date(date):    
    if isinstance(date, (datetime.datetime, )):
        return date
    elif isinstance(date, (str)):
        try:
            dt = datetime.datetime.strptime(date, '%d.%m.%Y')
            result = dt.strftime("%Y-%m-%d")
        except:
            dt = pendulum.parse(date)
            result = dt.to_date_string()

        return result


def get_ui_data(idx):
    
    q = "select * from v_signal_info where id = %(id)s"
    sgn = get_data(q, {"id": idx})

    if len(sgn) == 1:
        row = sgn[0]
        signal_type = row.get('signal_type')

        additional_data = row

        qq = "select query_type, title, query, columns, content_type, visible from tbl_conf_sig_query where signal_key = %(signal_type)s"
        sgnq = get_data(qq, {"signal_type": signal_type})

        ui_data = []
        for qd in sgnq:
            qr = qd.get('query')
            columns = qd.get('columns', "")
            part = qd.get('query_type')
            title = qd.get('title', part)
            content_type = qd.get('content_type', 'dict')
            visible = qd.get('visible')

            par = {}
            par['id'] = idx

            res = get_data(qr, par)

            if len(res) > 0 and content_type == 'list':
                sp_cols = dict(zip(res[0].keys(), [x.strip() for x in columns.split(',')]))
            else:
                sp_cols = {}
            

            ui_data.append({"part": part, "title": title, "data": res, "columns": columns, "sp_cols": sp_cols, "content_type": content_type, "visible": visible})
        
        return ui_data, additional_data
        
    return []


def get_signal_list_limit(data):
    
    start_date = data.get('date_from', '1900-01-01')
    end_date = data.get('date_to', '5999-12-31')
    limit = int(data.get('limit', 1000))
    offset = int(data.get('offset', 0))
    lst = data.get('lst', "all")
    order = data.get('order', "n") 
    
    order_by = "signal_date desc, signal_type" if order == 'n' else order.replace(':', ' ')

    q = f"""
    WITH RECURSIVE
    T as ( SELECT %(type_list)s AS items),
    N as ( SELECT 1 AS n 
           UNION 
           SELECT n + 1 
             FROM N, T
            WHERE n <= LENGTH(items) - LENGTH(REPLACE(items, ',', ''))
         ),
    list as (
        SELECT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(items, ',', n), ',', -1)) signal_type 
          FROM N, T
    )  
    SELECT id, signal_id, signal_type, signal_date, ins_date, inn, name, signal_sum, comment, close_date, elapsed_time, 
           confirmation, group_id, os_user, signal_sub_type, 
           moneyflow_uid, 
           case_id, case_caption, case_report, case_hazard_level, case_risk_amount, case_risk_date, case_status_id
      FROM v_signal_info
     WHERE signal_date >= %(start_date)s AND signal_date <= %(end_date)s
       AND (signal_type IN (SELECT signal_type FROM list) OR %(type_list)s = 'all')
       AND (signal_sub_type = %(signal_sub_type)s or %(signal_sub_type)s = '')
       AND (inn rlike %(inn)s or %(inn)s = '')
       AND (ifnull(confirmation, 'null') rlike %(confirmation)s or %(confirmation)s = '')
       AND (group_id = %(group_id)s or %(group_id)s = '')
       AND (upper(name) rlike upper(%(name)s) or %(name)s = '')
       AND (upper(os_user) rlike upper(%(os_user)s) or %(os_user)s = '')
       AND (upper(close_date) rlike %(close_date)s or %(close_date)s = '')
    ORDER BY {order_by}
    LIMIT %(limit)s OFFSET %(offset)s
    """

    qcnt = """
    WITH RECURSIVE
    T as ( SELECT %(type_list)s AS items),
    N as ( SELECT 1 AS n 
           UNION 
           SELECT n + 1 
             FROM N, T
            WHERE n <= LENGTH(items) - LENGTH(REPLACE(items, ',', ''))
         ),
    list as (
        SELECT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(items, ',', n), ',', -1)) signal_type 
          FROM N, T
    )  
    SELECT COUNT(*) cnt
      FROM v_signal_info
     WHERE signal_date >= %(start_date)s AND signal_date <= %(end_date)s
       AND (signal_type IN (SELECT signal_type FROM list) OR %(type_list)s = 'all')
       AND (signal_sub_type = %(signal_sub_type)s or %(signal_sub_type)s = '')
       AND (inn rlike %(inn)s or %(inn)s = '')
       AND (ifnull(confirmation, 'null') rlike %(confirmation)s or %(confirmation)s = '')
       AND (group_id = %(group_id)s or %(group_id)s = '')
       AND (upper(name) rlike upper(%(name)s) or %(name)s = '')
       AND (upper(os_user) rlike upper(%(os_user)s) or %(os_user)s = '')
       AND (upper(close_date) rlike %(close_date)s or %(close_date)s = '')
    """

    qdisttype = """
        select distinct signal_type signal_type
        from v_signal_info
        order by signal_type
    """

    # parameters for query
    params = {}
    params['limit'] = limit
    params['offset'] = offset
    params['type_list'] = lst

    # fields will set to empty strinf if they not exists in kwargs    
    nn = ['signal_sub_type', 'inn', 'confirmation', 'group_id', 'name', 'os_user', 'close_date']

    params.update({x:'' for x in nn})

    # pass all entered kwargs into query params!!!
    # for avoid changes for each new field filter
    # params.update(kwargs)

    params['start_date'] = cast_date(start_date)
    params['end_date'] = cast_date(end_date)

    return get_data([q, qcnt, qdisttype], params)
