# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from lxml import etree
from urllib.parse import quote
import base64
import contextlib
import io


    
    
class DownloadWizard(models.TransientModel):
    _name = "downloadwizard.download"
    file_name = fields.Char(string=u'File name')
    data = fields.Binary('File', readonly=True)
    is_moi_sheet_moi_loai = fields.Boolean(string=u' Chia nhóm',default=True)
    is_not_skip_field_stt = fields.Boolean(string=u'Không xuất trường STT')
#     is_cho_phep_dl_right_now = fields.Boolean(default=True,string=u'Cho phép download ngay')
    font_height = fields.Integer(default=12)
    def model_(self):
        model = self._context.get('active_model')
        return model
    model = fields.Char(default= model_)
    def function_key_(self):
        function_key =  self._context.get('function_key') or self._context.get('active_model')
        return function_key
    function_key = fields.Char(default=function_key_)
    verbal_function_key = fields.Char(compute='verbal_function_key_',store=True,string=u'Tên Hàm')
    
    @api.depends('function_key')
    def verbal_function_key_(self):
        for r in self:
            r.verbal_function_key = self.gen_model_verbal_dict().get(r.function_key,r.function_key)

    
    @api.multi
    def gen_model_verbal_dict(self): 
        return {}
    
    @api.multi
    def gen_pick_func(self): 
        return {}
    
    
    @api.multi
    def download_all_model(self):
        active_domain = self._context.get('active_domain',[])
        self.domain_text = self._context
        if self._context.get('download_right_now') :#self.is_dl_right_now:
            url = '/web/binary/download_model?download_model=downloadwizard.download&download_model_id=%s&active_domain=%s'%( self.id,quote(u'%s'%active_domain))
            return {
                 'type' : 'ir.actions.act_url',
                 'url': url,
                 'target': 'current',
            }
        else:
            pick_func = self.gen_pick_func()
            dl_obj = self
            call_func = pick_func[self.function_key]
            workbook,name = call_func(dl_obj,active_domain)
            with contextlib.closing(io.BytesIO()) as buf:
                workbook.save(buf)
                out = base64.encodestring(buf.getvalue())
            dl_obj.write({ 'data': out, 'file_name': name})
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'downloadwizard.download',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': dl_obj.id,
                'context':{'active_model':self.model, 'function_key': self.function_key},
                'views': [(False, 'form')],
                'target': 'new',
            }


