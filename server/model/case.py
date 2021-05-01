from server.sources import corp

get_data = corp.get_data
execute = corp.execute


def get_case_list():
    q = """SELECT c.id, 
                  c.caption, 
                  c.owner_id, 
                  c.report, 
                  c.status_id, 
                  c.user_id,
                  ou.displayName owner,
                  ou.mail        owner_mail,
                  uu.displayName executor,
                  uu.mail        executor_mail,
                  c.signalization,
                  c.hazard_level,
                  c.main_signal,
                  c.risk_amount,
                  c.risk_date,
                  c.upd_date last_update
        FROM corp.tbl_cs_cases c
        JOIN auth.tbl_users ou on ou.id = c.owner_id
        JOIN auth.tbl_users uu on uu.id = c.user_id
       WHERE c.isd = 0 
        """

    return get_data(q)


def get_case(case_id):

    q = """SELECT c.id, 
                  c.caption, 
                  c.risk_amount,
                  c.risk_date,
                  c.hazard_level,
                  c.owner_id, 
                  c.report, 
                  c.status_id, 
                  c.user_id,
                  c.conf_pages,
                  c.signalization,
                  c.main_signal,
                  ou.displayName owner,
                  ou.mail        owner_mail,
                  uu.displayName executor,
                  uu.mail        executor_mail
             FROM corp.tbl_cs_cases c
             JOIN auth.tbl_users ou on ou.id = c.owner_id
             JOIN auth.tbl_users uu on uu.id = c.user_id
            WHERE c.id = %(case_id)s"""

    q2 = """SELECT * 
              FROM tbl_cs_case_to_signal cts
              JOIN v_signal_info si on si.id = cts.signal_id
            WHERE cts.case_id = %(case_id)s
    """
    
    q3 = """
        SELECT *
          FROM tbl_cs_case_actions ca
          WHERE ca.case_id = %(case_id)s
    """
    
    q4 = """
        SELECT id,
               filename,
               value content,
               comment
          FROM tbl_cs_case_attachments cat
         WHERE cat.case_id = %(case_id)s
    """

    q5 = """
        SELECT cca.*,
               c.ztaxidnum inn,
               d.zdept_name,
               p.zdept_name parent_zdept_name,
               r.calday rests_date,
               r.restor 
          FROM tbl_cs_case_accounts cca
          JOIN tbl_ciw_accounts a on a.KSSS_ID = cca.ksss_id
          JOIN tbl_ciw_clients c on c.ksss_id = a.ZCLIENT_ID
          LEFT JOIN tbl_ciw_dept d on d.system_key = a.DEPT_SRC and d.system_id = a.SYSTEM_ID and d.status_src = 'V'
          LEFT JOIN tbl_ciw_dept p on p.system_key = d.zdept_parent and p.system_id = d.SYSTEM_ID and p.status_src = 'V'
          LEFT JOIN tbl_ciw_current_rests r on r.zpersaccn = a.ZPERSACCN and r.zpersacc = lpad(a.KSSS_ID, 20, '0')
         WHERE cca.case_id = %(case_id)s 
    """
    params = {"case_id": case_id}

    # r1 = get_data(q, params)
    # r2 = get_data(q2, params)
    # r3 = get_data(q3, params)
    # r4 = get_data(q4, params)
    # r5 = get_data(q5, params)

    return get_data([q, q2, q3, q4, q5], params)


def get_case_graph(case_id):

    return []


def create_case(data):
    caption   = data.get('caption', "")
    risk_amount = data.get('risk_amount', 0)
    risk_date   = data.get('risk_date', "")
    hazard_level = data.get('hazard_level', 0)
    report    = data.get('report', "")
    status_id = data.get('status_id', 0)
    user_id = data.get('user_id')
    signals = data.get('signals', {})
    attachments = data.get('attachments', {})
    actions = data.get('actions', {})
    accounts = data.get('accounts', {})

    #TODO: ADD SESSION USER
    # owner_id = current_user.corp_id
    user_id = user_id if user_id != None else owner_id

    q = """
    INSERT INTO tbl_cs_cases (caption, risk_amount, risk_date, hazard_level, owner_id, report, status_id, user_id)
    VALUES (%(caption)s, %(risk_amount)s, %(risk_date)s, %(hazard_level)s, %(owner_id)s, %(report)s, %(status_id)s, %(user_id)s)
    """

    commit = "COMMIT;"

    q2 = "SELECT LAST_INSERT_ID() case_id"

    execute([q, commit], {"caption": caption, "risk_amount": risk_amount, "risk_date": risk_date, "hazard_level": hazard_level, "owner_id": owner_id, "report": report, "status_id": status_id, "user_id": user_id}, make_dict=True)
    data = get_data(q2)


    # zero dataset, zero row
    case_id = data[0][0]['case_id']

    q3 = """
        INSERT INTO tbl_cs_case_to_signal (case_id, signal_id, user_id) 
        VALUES (%(case_id)s, %(signal_id)s, %(user_id)s)
    """

    for s in signals:
        res = execute([q3, commit], {"case_id": case_id, "signal_id": s['id'], "user_id": owner_id})

    q4 = """
        INSERT INTO tbl_cs_case_actions(case_id, owner_id, user_id, comment, results, beg_date, end_date, duration, status_id)
        VALUES(%(case_id)s, %(owner_id)s, %(user_id)s, %(comment)s, %(results)s, %(beg_date)s, %(end_date)s, %(duration)s, %(status_id)s)
    """

    for a in actions:
        params = {
            "case_id": case_id,
            "owner_id": owner_id,
            "user_id": a['user']['id'] if a.get('user') else owner_id,
            "comment": a.get('comment'),
            "results": a.get('results'),
            "beg_date": datetime.datetime.strptime(a.get('beg_date'), '%d.%m.%Y'),
            "end_date": datetime.datetime.strptime(a.get('end_date'), '%d.%m.%Y'),
            "duration": a.get('duration'),
            "status_id": a['status']['id'] if a.get('status_id') else 0,
            }
        execute([q4, commit], params)

    q5 = """
        INSERT INTO tbl_cs_case_attachments(case_id, filename, value, user_id)
        VALUES(%(case_id)s, %(filename)s, %(value)s, %(user_id)s)        
    """

    for a in attachments:
        execute([q5, commit], {"case_id": case_id, "filename": a['filename'], "value": a['content'], "user_id": owner_id})

    q6 = """
        INSERT INTO tbl_cs_case_accounts(case_id, zpersaccn, acc_limit, acc_debet, agreement, agr_open_date, agr_close_date, loan_security, closest_repayment, user_id)
        VALUES(%(case_id)s, %(zpersaccn)s, %(acc_limit)s, %(acc_debet)s, %(agreement)s, %(agr_open_date)s, %(agr_close_date)s, %(loan_security)s, %(closest_repayment)s, %(user_id)s)
    """
    for a in accounts:
        params = {
            "case_id": a["case_id"],
            "zpersaccn": a["zpersaccn"],
            "acc_limit": a["acc_limit"],
            "acc_debet": a["acc_debet"],
            "agreement": a["agreement"],
            "agr_open_date": a["agr_open_date"],
            "agr_close_date": a["agr_close_date"],
            "loan_security": a["loan_security"],
            "closest_repayment": a["closest_repayment"],
            "user_id": owner_id
        }
        execute([q6, commit], params)

    return case_id    


def edit_case(data):  
    idx       = data.get('id')
    caption   = data.get('caption')
    risk_amount  = data.get('risk_amount', 0)
    risk_date    = data.get('risk_date', "")
    hazard_level = data.get('hazard_level', 0)
    report       = data.get('report')
    status_id    = data.get('status_id')
    user_id      = data.get('user_id')
    signals_new  = data.get('signals_new')
    actions_new  = data.get('actions_new')
    attachments_new = data.get('attachments_new') 
    attachments_del = data.get('attachments_del')
    accounts_new    = data.get('accounts_new')
    signalization   = data.get('signalization')
    
    # Executor info
    owner_id = current_user.corp_id
    user_id = user_id if user_id != None else owner_id

    q = """
        UPDATE tbl_cs_cases
           SET caption = %(caption)s, 
               risk_amount = %(risk_amount)s,
               risk_date = %(risk_date)s,
               hazard_level = %(hazard_level)s,
               report = %(report)s, 
               status_id = %(status_id)s, 
               user_id = %(user_id)s
         WHERE id = %(case_id)s        
    """

    commit = "COMMIT;"

    execute(q, {"case_id": case_id, "caption": caption, "risk_amount": risk_amount, "risk_date": risk_date, "hazard_level": hazard_level, "report": report, "status_id": status_id, "user_id": user_id}, make_dict=True)
    execute(commit)

    # signals_new
    q2 = """
        INSERT INTO tbl_cs_case_to_signal (case_id, signal_id, user_id) 
        VALUES (%(case_id)s, %(signal_id)s, %(user_id)s)
    """

    for s in signals_new:
        execute(q2, {"case_id": case_id, "signal_id": s['id'], "user_id": owner_id})    
        execute(comit)

    # actions_new
    q3 = """
        INSERT INTO tbl_cs_case_actions(case_id, owner_id, user_id, comment, results, beg_date, end_date, duration, status_id)
        VALUES(%(case_id)s, %(owner_id)s, %(user_id)s, %(comment)s, %(results)s, %(beg_date)s, %(end_date)s, %(duration)s, %(status_id)s)
    """
    arc = 0
    for a in actions_new:
        params = {
            "case_id": case_id,
            "owner_id": owner_id,
            "user_id": a['user']['id'] if a.get('user') else owner_id,
            "comment": a.get('comment'),
            "results": a.get('results'),
            "beg_date": datetime.datetime.strptime(a.get('beg_date'), '%d.%m.%Y') if a.get('beg_date') else None,
            "end_date": datetime.datetime.strptime(a.get('end_date'), '%d.%m.%Y') if a.get('end_date') else None,
            "duration": a.get('duration'),
            "status_id": a['status']['id'] if a.get('status_id') else 0,
            }
        execute(q3, params)
        
    # attachments_new
    q4 = """
        INSERT INTO tbl_cs_case_attachments(case_id, filename, value, user_id)
        VALUES(%(case_id)s, %(filename)s, %(value)s, %(user_id)s)        
    """

    for a in attachments_new:
        execute(q4, {"case_id": case_id, "filename": a['filename'], "value": a['content'], "user_id": owner_id})
        execute(commit)
    
    # attachments_del
    q5 = """ DELETE FROM tbl_cs_case_attachments where id = %(id)s"""

    for a in attachments_del:
        execute(q5, {"id": a['id']})
        
    # accounts new
    q6 = """
        INSERT INTO tbl_cs_case_accounts(case_id, zpersaccn, ksss_id, acc_limit, acc_debet, agreement, agr_open_date, agr_close_date, loan_security, closest_repayment, user_id)
        VALUES(%(case_id)s, %(zpersaccn)s, %(ksss_id)s, %(acc_limit)s, %(acc_debet)s, %(agreement)s, %(agr_open_date)s, %(agr_close_date)s, %(loan_security)s, %(closest_repayment)s, %(user_id)s)
    """
    for a in accounts_new:
        params = {
            "case_id": case_id,
            "zpersaccn": a.get("zpersaccn"),
            "ksss_id": a.get("ksss_id"),
            "acc_limit": a.get("acc_limit"),
            "acc_debet": a.get("acc_debet"),
            "agreement": a.get("agreement"),
            "agr_open_date": datetime.datetime.strptime(a.get("agr_open_date"), '%d.%m.%Y') if a.get("agr_open_date") else None,
            "agr_close_date": datetime.datetime.strptime(a.get("agr_close_date"), '%d.%m.%Y') if a.get("agr_close_date") else None,
            "loan_security": a.get("loan_security"),
            "closest_repayment": datetime.datetime.strptime(a.get("closest_repayment"), '%d.%m.%Y') if a.get("closest_repayment") else None,
            "user_id": owner_id
        }
        execute(q6, params)
        execute(commit)

    q10 = """
        UPDATE tbl_cs_cases
           SET signalization = %(signalization)s
         WHERE id = %(case_id)s
    """

    execute(q10, {"case_id": case_id, "signalization": signalization})
    execute(execute)

    return True


def check_case(data):

    idx, signals_removed, actions_removed, actions_edited, accounts_edited, accounts_removed, conf_pages = data.values()


    q = """ 
        UPDATE tbl_cs_case_actions
           SET comment = %(comment)s,
               results = %(results)s,
               user_id = %(user_id)s,
               beg_date = %(beg_date)s,
               end_date = %(end_date)s,
               duration = %(duration)s,
               status_id = %(status_id)s
         WHErE id = %(action_id)s
    """

    commit = "COMMIT;"

    qrc = "SELECT row_count() rc"

    ae = 0
    for a in actions_edited:
        params = {
            "action_id": a.get('id'),
            "comment": a.get('comment'),
            "results": a.get('results'),
            "user_id": a.get('user', []).get('id'),
            "beg_date": datetime.datetime.strptime(a.get("beg_date"), '%d.%m.%Y') if a.get("beg_date") else None,
            "end_date": datetime.datetime.strptime(a.get("end_date"), '%d.%m.%Y') if a.get("end_date") else None,
            "duration": a.get('duration'),
            "status_id": a.get('status', []).get('id')
        }
        execute(q, params)
        execute(commit)
    
    q2 = """
      DELETE FROM tbl_cs_case_actions
       WHERE id = %(action_id)s
    """

    for a in actions_removed:
        execute(q2, {"action_id": a['id']})
        execute(commit)

    # signals_removed
    q3 = """
        DELETE FROM tbl_cs_case_to_signal 
         WHERE signal_id = %(signal_id)s 
           AND case_id = %(case_id)s
    """

    for s in signals_removed:
        execute([q3, commit], {"signal_id": s['id'], "case_id": s['case_id']})
    

    # accounts removed
    q7 = """
        DELETE FROM tbl_cs_case_accounts
        WHERE id = %(id)s
    """
    for a in accounts_removed:
        execute([q7, commit], {"id": a["id"]})
    
    # accounts updated
    q8 = """
        UPDATE tbl_cs_case_accounts
           SET acc_limit = %(acc_limit)s, 
               acc_debet = %(acc_debet)s, 
               agreement = %(agreement)s, 
               agr_open_date = %(agr_open_date)s, 
               agr_close_date = %(agr_close_date)s, 
               loan_security = %(loan_security)s, 
               closest_repayment = %(closest_repayment)s,
               comment = %(comment)s
            WHERE id = %(id)s
    """

    for a in accounts_edited:
        params = {
            "acc_limit": a.get('acc_limit'),
            "acc_debet": a.get('acc_debet'),
            "agreement": a.get('agreement'),
            "agr_open_date": datetime.datetime.strptime(a.get("agr_open_date"), '%d.%m.%Y') if a.get("agr_open_date") else None,
            "agr_close_date": datetime.datetime.strptime(a.get("agr_close_date"), '%d.%m.%Y') if a.get("agr_close_date") else None,
            "loan_security": a.get('loan_security'),
            "closest_repayment": datetime.datetime.strptime(a.get("closest_repayment"), '%d.%m.%Y') if a.get("closest_repayment") else None,
            "comment": a.get('comment'),
            "id": a.get("id")
        }
           
        execute(q8, params)
    
    q9 = """
        UPDATE tbl_cs_cases
           SET conf_pages = %(conf_pages)s
         WHERE id = %(case_id)s
    """

    execute(q9, {"case_id": case_id, "conf_pages": conf_pages})
    execute(commit)
    
    return True


def delete_case(idx):

    q = """UPDATE tbl_cs_cases 
              SET isd = 1
            WHERE id = %(case_id)s"""
    
    commit = "COMMIT;"

    execute([q, commit], {"case_id": case_id})

    return True


def get_signal_list():

    q = """SELECT * 
             FROM v_signal_info si
            WHERE confirmation in (0,1)
        """

    return execute(q)


def get_user_list():

    q = """
        SELECT id,
               cn,
               title
          FROM auth.tbl_users
         WHERE isd = 0;
    """

    return execute(q)    