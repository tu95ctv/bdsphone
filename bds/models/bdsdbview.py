# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api,sql_db, tools
class bdsview(models.Model):
    _name = 'bds.bdsview3'
    _auto = False
    tieu_de = fields.Char()
    html = fields.Html()
    unit = fields.Float()
    cpas = fields.Integer()
    quantam_dt = fields.Datetime()
    images_ids = fields.One2many('bds.images','bds_id')
     
    khachxembds_ids = fields.One2many('bds.khachxembds','bds_id')
    poster_id = fields.Many2one('bds.poster')
#     khach_xem_nha_id = fields.Many2one('bds.poster')
    post_ids_of_user  = fields.One2many('bds.bds','poster_id',related='poster_id.post_ids')
    full_count = fields.Integer()
    @api.model_cr
    def init(self):
#         tools.drop_view_if_exists(self._cr, 'bds_bdsview3')
        self._cr.execute("""
            create or replace view bds_bdsview3 as (
                select
                    b.id as id,
                    title as tieu_de,
                    html as html,
                    don_gia as unit,
                    p.count_post_all_site as cpas,
                    q.dt as quantam_dt,
                    b.poster_id as poster_id,
                    cb.full_count as full_count
                from bds_bds b
                    left join bds_poster p on 
                    (b.poster_id=p.id)
                    left join  bds_quantam q on (b.id = q.bds_id )
                    left join
                     (select count(id) as full_count,poster_id from bds_bds group by poster_id) cb on cb.poster_id =b.poster_id
                 
                ) 
                 """)
         
        
        
        
class bdsview4(models.Model):
    _name = 'bds.bdsview4'
    _auto = False
    tieu_de = fields.Char()
    html = fields.Html()
    unit = fields.Float()
    images_ids = fields.One2many('bds.images','bds_id')
    khachxembds_ids = fields.One2many('bds.khachxembds','bds_id')
   
    
    
    cpas = fields.Integer()
#     quantam_dt = fields.Datetime()
    poster_id = fields.Many2one('bds.poster')
#     post_ids_of_user  = fields.One2many('bds.bds','poster_id',related='poster_id.post_ids')
    full_count = fields.Integer()
    khach_count = fields.Integer()
    test_field = fields.Char(compute='test_field_')
    
    def test_field_(self):
        for r in self:
            r.test_field = self.env.user.login
    
    @api.model_cr
    def init(self):
        print ('**********************************self.env.user.id',self.env.user.id,self.env.user.login)
        tools.drop_view_if_exists(self._cr, 'bds_bdsview4')
        rule ="""CREATE RULE visits_upd AS
    ON UPDATE TO bds_bdsview4 DO INSTEAD UPDATE bds_bds SET title = NEW.tieu_de
    , html = NEW.html
    WHERE id = NEW.id"""
         
        self._cr.execute("""
            create or replace view bds_bdsview4 as (
                select
                    b.id as id,
                    b.title as tieu_de,
                    b.html as html,
                    p.count_post_all_site as cpas,
                    cb.full_count as full_count,
                    b.don_gia as unit,
                    khach_count
                from bds_bds b
                  left join bds_poster p on 
                    (b.poster_id=p.id)
                left join
                     (select count(id) as full_count,poster_id from bds_bds group by poster_id) cb on cb.poster_id =b.poster_id
                 left join
                     (select count(id) as khach_count, bds_id from bds_khachxembds where bds_khachxembds.user_id = %s  group by bds_id) khachxemnha on (khachxemnha.bds_id =b.id)
                ) 
                 """%self.env.uid)
        self._cr.execute(rule)