from server.sources import corp

get_data = corp.get_data

q_id = "select last_insert_rowid() as id"

def get_dictionary(key):
    q = """select dict_key, dict_val from corp1.tbl_dictionary where dict_type = %(type)s
    """
    p = {"type": key}
    res = get_data(q, p)

    return res


def get_signals_stat():
    q = """
    select * from v_signal_stat order by 1,2,3
    """

    res = get_data(q)

    return res


def get_rests_by_inn(inn):
    q = """
        SELECT r.*,
               ROW_NUMBER() OVER(partition by acc_type_id order by restor desc) rn,
               COUNT(acc_type_id) OVER(partition by acc_type_id order by restor desc ROWS between UNBOUNDED PRECEDING and UNBOUNDED FOLLOWING) cn,
               (select ZCLOSEDAT from tbl_ciw_accounts where ksss_id = cast(r.zpersacc as INTEGER) and system_id = ZSRCSYST) zclosedat
          FROM (SELECT t.*, 
                       DATEDIFF(calday, prev_calday) dd,
                       CASE 
                           WHEN is_checking_acc(zpersaccn)        THEN 0
                           WHEN is_loan_acc(zpersaccn)            THEN 1
                           WHEN is_overdraft_acc(zpersaccn)       THEN 2
                           WHEN is_overdue_loan_acc(zpersaccn)    THEN 3
                           WHEN is_overdue_persent_acc(zpersaccn) THEN 4
                           WHEN is_pledge_acc(zpersaccn)          THEN 5
                           WHEN is_guarantees_acc(zpersaccn)      THEN 6
                           WHEN is_surety_acc(zpersaccn)          THEN 7                           
                           ELSE 8
                       END acc_type_id
                  FROM tbl_ciw_current_rests t
                 WHERE (zpersaccn, zsrcsys) in (SELECT zpersaccn, system_id 
                                                  FROM tbl_ciw_accounts a
                                                 WHERE a.ZCLIENT_ID IN (SELECT ksss_id 
                                                                          FROM tbl_ciw_clients
                                                                         WHERE ztaxidnum = %(inn)s
                                                                        )
                                                ) 
               ) r 
        """

    res = get_data(q, {"inn": inn})

    return res


def get_client_by_inn(inn):
    q = """SELECT * 
             FROM tbl_ciw_clients 
            WHERE ztaxidnum = %(inn)s"""

    res = get_data(q, {"inn": inn})

    return res    


def get_inn_groups():

    q = """ SELECT g.inn, 
                   (select zclient_sh_name from tbl_ciw_clients c where c.ztaxidnum = g.inn and zsrcsyst = 'U' order by ins_date desc limit 1) zclient_sh_name,
                   gn.group_name,
                   gn.group_comment,
                   u.sAMAccountName user_name
              FROM tbl_sig_inn_group g
              JOIN tbl_sig_groups gn on gn.group_id = g.group_id
              JOIN auth.tbl_users u on u.id = g.user_id
             ORDER BY group_name
    """

    res = get_data(q)

    return res


def get_loaners_monitor():

    q = """
    select * from tbl_ui_loan_rests
    """
    res = get_data(q)

    return res