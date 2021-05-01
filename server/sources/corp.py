import os
import pymysql

from contextlib import closing

server = os.environ.get("MYSQL_SERVER")
user = os.environ.get("MYSQL_USER")
pwd = os.environ.get("MYSQL_PWD")

host, *port = server.split(":")
port = int(port[0]) if port else 3306

conn = pymysql.connect(host=host, port=port, user=user, password=pwd, database="corp")
conn.autocommit = True

def make_result(data, cols):
    return [ {cols[i]: x for i,x in enumerate(row)} for row in data]

def get_data(q, p=None):
    """Query data with `q` statement with `p` parameters.
    """

    with closing( conn.cursor() ) as cur:
        if isinstance(q, list):
            result = []
            for qq in q:
                cur.execute(qq, p)
                data = cur.fetchall()
                cols = [x[0] for x in cur.description or []]            

                result.append( make_result(data, cols) )

            return result
        else:
            cur.execute(q, p)
            data = cur.fetchall()
            cols = [x[0] for x in cur.description or []]

            return make_result(data, cols)

def execute(q, p=None):
    """Execute query `q` statement with `p` parameters without returns data.
    """

    with closing( conn.cursor() ) as cur:
        if isinstance(q, list):
            
            for qq in q:
                cur.execute(qq, p)
            
            return True
        else:
            cur.execute(q, p)

            return True          


