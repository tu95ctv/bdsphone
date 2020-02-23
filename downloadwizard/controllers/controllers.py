# -*- coding: utf-8 -*-
from odoo import http
# from odoo.addons.downloadwizard.download_tool import  download_all_model_by_url

import json
from openerp.http import request
from odoo import fields
from datetime import datetime, timedelta
from odoo.exceptions import UserError
from unidecode  import unidecode

def download_all_model_by_url(download_model=None,download_model_id = None, active_domain=None, download_key= None,**karg):
    if active_domain:
        active_domain = active_domain.replace("'",'"')
        active_domain = json.loads(active_domain)
    dj_obj = request.env[download_model].browse(int(download_model_id))
    download_key = download_key or dj_obj.function_key
    pick_func = request.env['downloadwizard.download'].gen_pick_func()
    try:
        call_func = pick_func[download_key]
    except KeyError:
        raise UserError(u'download_key khong co:%s'%download_key)
    active_domain = [active_domain] if active_domain !=None else []
    workbook,name = call_func(dj_obj,*active_domain,**karg)
    name = unidecode(name).replace(' ','_')
    
    response = request.make_response(None,
        headers=[('Content-Type', 'application/vnd.ms-excel'),
                ('Content-Disposition', 'attachment; filename=%s;target=blank' %name)],
        )
    workbook.save(response.stream)
    return response



class DownloadAllModel(http.Controller):
    @http.route('/web/binary/download_model',type='http', auth="public")
    def download_all_model_controller(self,download_model=None,download_model_id = None, active_domain=None, download_key= None,debug=False, **kw):
#         try:
#             response = download_all_model_by_url(download_model=download_model,download_model_id = download_model_id, active_domain=active_domain, download_key= download_key, **kw)
#         except TypeError:
        response = download_all_model_by_url(download_model=download_model,download_model_id = download_model_id, active_domain=active_domain, download_key= download_key,**kw)
        return response

