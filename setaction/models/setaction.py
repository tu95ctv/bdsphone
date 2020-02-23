# -*- coding: utf-8 -*-
from odoo import models, fields, api,exceptions,tools,_



class SetactionSingle(models.TransientModel):
    _name = "setaction.setactionsingle"
    name = fields.Char()
    context_val = fields.Char(compute='context_val_')
    notice = fields.Text()
    active_model = fields.Char(compute='active_model_')
    @api.depends('name')
    def active_model_(self):
        self.active_model = self._context.get('active_model')
    @api.depends('name')
    def context_val_(self):
        self.context_val = self._context.get('context_val')
    new_name = fields.Char()
        
        
class Setaction(models.TransientModel):
    _name = "setaction.setaction"
    _inherit = "setaction.setactionsingle"
#     name = fields.Char()
#     context_val = fields.Char(compute='context_val_')
#     @api.depends('choosed_object_qty')
#     def context_val_(self):
#         self.context_val = self._context.get('context_val')
    choosed_object_qty = fields.Integer()
    affected_object_qty = fields.Integer()
    
    
    
    
    
    
#     @api.multi
#     def multi_approved(self):
#         active_ids = self._context.get('active_ids')
#         if active_ids:
#             cac_linh_ids = self.env.user.cac_linh_ids
#             for r in self.env['cvi'].browse(active_ids):
#                 if r.is_sep:#or r.is_admin or (cac_linh_ids and (r.create_uid == r.env.user or r.user_id == r.env.user)):
#                     r.state = 'approved'
#                 else:
#                     raise UserError (u'Bạn không phải là lãnh đạo của nhân viên tạo record này')
#         else:
#             raise UserError (u'Bạn chưa chọn dòng nào')