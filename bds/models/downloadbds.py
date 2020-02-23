# -*- coding: utf-8 -*-
from odoo import models, fields, api


from odoo.addons.downloadwizard.models.dl_models.dl_model import  download_model
FIELDNAME_FIELDATTR_quants = [
       ('name',{}),
       ('du_doan_cc_or_mg',{}),
       ('quan_chuyen_1_id',{}),
       ('username',{}),
       ('count_post_all_site',{}),
       ('address_topic_number',{}),
       ('ten_zalo',{}),
                 ]
Export_Para_quants = {
     'exported_model':'bds.poster',
     'FIELDNAME_FIELDATTR':FIELDNAME_FIELDATTR_quants,
 #     'gen_domain':gen_domain_stock_quant,
     'search_para':{'order': 'name asc'},#desc
     }
def download_poster(dl_obj,append_domain = []):
    filename = 'users'
    name = "%s%s" % (filename, '.xls')
    workbook =  download_model(dl_obj,
                         Export_Para=Export_Para_quants,
                         append_domain=append_domain
                        )
    return workbook,name
        
    
    
class DownloadCVI(models.TransientModel):
    _inherit = "downloadwizard.download"
    
    @api.multi
    def gen_pick_func(self): 
        rs = super(DownloadCVI, self).gen_pick_func()
        pick_func = {'bds.poster':download_poster}
        rs.update(pick_func)
        return rs
    
    
    