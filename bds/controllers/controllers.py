# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.downloadwizard.controllers.controllers import  download_all_model_by_url


class DownloadCvi(http.Controller):
    @http.route('/web/binary/download_model',type='http', auth="public")
    def download_all_model_controller(self,**kw):
        response = download_all_model_by_url(kw)
        return response
    
    
    