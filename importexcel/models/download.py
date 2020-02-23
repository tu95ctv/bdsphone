# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons.importexcel.models.model_dict_folder.tao_instance_new import importexcel_func



def importexcel_checkfile(dl_obj):
    workbook = importexcel_func(dl_obj, check_file=True)
    filename = 'check_file_of_%s-%s'%(dl_obj.filename,dl_obj.id)
    name = "%s%s" % (filename, '.xls')
    return workbook,name
class CheckFileDownloadwizard(models.TransientModel):
    _inherit = "downloadwizard.download"
    @api.multi
    def gen_pick_func(self): 
        rs = super(CheckFileDownloadwizard, self).gen_pick_func()
        pick_func = {'importexcel.checkfile':importexcel_checkfile}
        rs.update(pick_func)
        return rs
    
    