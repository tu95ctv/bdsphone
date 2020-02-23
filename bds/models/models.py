# -*- coding: utf-8 -*-
from odoo import models, fields, api,sql_db
from . import fetch 
from odoo.addons.bds.models.fetch import fetch
from odoo.addons.bds.models.import_contact import import_contact
import logging
from odoo.addons.bds.models.fetch import request_html
_logger = logging.getLogger(__name__)
# from threading import current_thread
from odoo.addons.bds.models.fetch import g_or_c_ss
import re
import datetime
from odoo.osv import expression

# from email.MIMEMultipart import MIMEMultipart
# from email.MIMEText import MIMEText
# from odoo.addons.bds.models.fetch import page_handle_for_thread

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )



    
class SiteDuocLeech(models.Model):
    _name = 'bds.siteleech'
    name = fields.Char() 
    name_viet_tat = fields.Char()  
    

class Images(models.Model):
    _name = 'bds.images'
    url = fields.Char()
    bds_id = fields.Many2one('bds.bds')
    


  

class PosterNameLines(models.Model):
    _name = 'bds.posternamelines'
    username_in_site = fields.Char()
    site_id = fields.Many2one('bds.siteleech')
    poster_id = fields.Many2one('bds.poster')


    
class QuanOfPoster(models.Model):
    _name = 'bds.quanofposter'
    name = fields.Char(compute='name_',store=True)
    
    quan_id = fields.Many2one('bds.quan')
    siteleech_id = fields.Many2one('bds.siteleech')
    quantity = fields.Integer()
    min_price = fields.Float(digits=(32,1))
    avg_price = fields.Float(digits=(32,1))
    max_price = fields.Float(digits=(32,1))
    poster_id = fields.Many2one('bds.poster')
    @api.depends('quan_id','quantity') 
    def name_(self):
        for r in self:
            if r.siteleech_id or  r.quan_id:
                r.name = (( r.siteleech_id.name + ' ' ) if r.siteleech_id.name else '') +  r.quan_id.name + ':' + str(r.quantity)
            else:
                r.name ='all'
            

    
class SMS(models.Model):
    _name= 'bds.sms'
    name=  fields.Char()
    noi_dung = fields.Text()
    getphoneposter_ids = fields.One2many('bds.getphoneposter','sms_id')
    poster_ids = fields.Many2many('bds.poster','sms_poster_relate','sms_id','poster_id',compute='poster_ids_',store=True)
    len_poster_ids  =fields.Integer(compute='poster_ids_',store=True)
    @api.depends('getphoneposter_ids','name','noi_dung')
    def poster_ids_(self):
        for r in self:
            poster_ids = self.env['bds.poster'].search([('getphoneposter_ids','in',r.getphoneposter_ids.ids)])
            r.poster_ids = poster_ids
            r.len_poster_ids = len(poster_ids)
    @api.depends('getphoneposter_ids','getphoneposter_ids.poster_ids')
    def last_name_of_that_model_(self):
        for r in self:
            pass
   
class GetPhonePoster(models.Model):
    _name = 'bds.getphoneposter'
    name = fields.Char(compute='name_',store=True)
    description = fields.Text()
    is_repost_for_poster = fields.Boolean()
    filter_sms_or_filter_sql = fields.Selection([('sms_ids','sms_ids'),('by_sql','by_sql')],default='sms_ids')
#     name = fields.Char()
    sms_id = fields.Many2one('bds.sms',required=True)
    nha_mang = fields.Selection([('vina','vina'),('mobi','mobi'),('viettel','viettel'),('khac','khac')],default='vina')
    post_count_min = fields.Integer(default=10)
    len_poster = fields.Integer()
    exclude_poster_ids = fields.Many2many('bds.poster')#,inverse="exclude_poster_inverse_")
#     len_posters_of_sms = fields.Integer()
    phuong_loc_ids = fields.Many2many('bds.phuong')
    quan_ids = fields.Many2many('bds.quan')#,default = lambda self:self.default_quan())
    phone_list = fields.Text(compute='phone_list_',store=True)
    poster_ids = fields.Many2many('bds.poster','getphone_poster_relate','getphone_id','poster_id')#,compute='poster_ids_',store=True)
    loc_gian_tiep_quan_bds_topic = fields.Selection([
                                                    (u'Qua Thống Kê Quận Object 1',u'Qua Thống Kê Quận Object 1'),
                                                    (u'Qua Thống Kê Quận Object',u'Qua Thống Kê Quận Object (không xài nữa)'),
                                                     (u'Qua BDS Object',u'Qua BDS Object'),
                                                     (u'Qua BDS SQL',u'Qua BDS SQL'),
                                                     (u'Qua BDS SQL 1',u'Qua BDS SQL 1'),
                                                     ],default = u'Qua BDS SQL')
    gia_be_hon = fields.Float(digits=(6,2))
    gia_lon_hon = fields.Float(digits=(6,2))
    bds_ids = fields.Many2many('bds.bds',compute='poster_ids_',store=True)
    poster_da_gui_cua_sms_nay_ids = fields.Many2many('bds.poster',compute='poster_ids_',store=True)
#     @api.onchange('poster_ids')
#     def danh_sach_doi_tac_(self):
#         for r in self:
#             r.danh_sach_doi_tac = '\r\n'.join(r.poster_ids.mapped('name'))
            
    @api.depends('sms_id','nha_mang')
    def name_(self):
        for r in self:
                r.name = u'get phone,id %s- nhà mạng %s' %(r.id,r.nha_mang)
#     def default_quan(self):
#         quan_10 = self.env['bds.quan'].search([('name','=',u'Quận 10')])
#         return [quan_10.id]
    
 
    @api.depends('poster_ids')
    def phone_list_(self):
        for r in self:
            phone_lists = filter(lambda l: not isinstance(l,bool),r.poster_ids.mapped('phone'))
            r.phone_list = ','.join(phone_lists)
   
    @api.onchange('gia_be_hon','loc_gian_tiep_quan_bds_topic','quan_ids','post_count_min','nha_mang','sms_id','exclude_poster_ids','poster_ids.exclude_sms_ids','phuong_loc_ids','is_repost_for_poster')
    def poster_ids_(self):
        
        def filter_for_poster(poster):
            if poster.id in r.exclude_poster_ids.ids:
                return False
            if r.sms_id.id in poster.exclude_sms_ids.ids:
                return False
            if r.is_repost_for_poster or r.filter_sms_or_filter_sql =='sms_ids':
                return True
            elif r.filter_sms_or_filter_sql =='by_sql':
                product_category_query =\
                         '''select distinct u.id,c.sms_id from bds_poster as u
            inner join getphone_poster_relate as r
            on u.id  = r.poster_id
            inner join bds_getphoneposter as c
            on  r.getphone_id= c.id
            where  u.id = %(r_id)s
            and c.sms_id =  %(sms_id)s
            '''%{'r_id':poster.id,
                 'sms_id':r.sms_id.id
                 }
                self.env.cr.execute(product_category_query)
                product_category = self.env.cr.fetchall()
                if product_category:
                    return False
                else:
                    return True  
                
        for r in self:
            if r.loc_gian_tiep_quan_bds_topic ==u'Qua Thống Kê Quận Object 1':
                domain_tong = []
                if r.quan_ids :
                    domain_tong = expression.AND([[( 'quan_id','in',r.quan_ids.ids)], domain_tong])
                if r.post_count_min:
                    domain_tong = expression.AND([[('quantity','>=',r.post_count_min)], domain_tong])
                if not r.is_repost_for_poster:
                    domain_tong = expression.AND([[('poster_id','not in',r.sms_id.poster_ids.ids)], domain_tong])
                if r.nha_mang:
                    domain_tong = expression.AND([[('poster_id.nha_mang','=',r.nha_mang)], domain_tong])
#                     post_ids_da_gui_cua_sms_nay_ids = r.sms_id.poster_ids
#                     post_ids = post_ids.filtered(lambda r: r.id not in post_ids_da_gui_cua_sms_nay_ids.ids )
#                     r.poster_da_gui_cua_sms_nay_ids = post_ids_da_gui_cua_sms_nay_ids
                poster_quan10_greater_10 = self.env['bds.quanofposter'].search(domain_tong).mapped('poster_id')
                r.poster_ids =poster_quan10_greater_10
                r.len_poster = len(poster_quan10_greater_10)
                
            elif r.loc_gian_tiep_quan_bds_topic ==u'Qua Thống Kê Quận Object':
                if not r.sms_id:
                    pass
                else:
                    domain_tong = []
                    if r.nha_mang:
                        nha_mang_domain = ('nha_mang','=',r.nha_mang)
                        domain_tong.append(nha_mang_domain)
                    if r.quan_ids and r.post_count_min:
                        domain_tong = expression.AND([[( 'quanofposter_ids.quan_id','in',r.quan_ids.ids),('quanofposter_ids.quantity','>=',r.post_count_min)], domain_tong])
                    if r.phuong_loc_ids:
                        domain_tong = expression.AND([('phuong_id' ,'in',r.phuong_loc_ids.mapped('id')),domain_tong])
                    if r.filter_sms_or_filter_sql =='sms_ids' and not r.is_repost_for_poster:
                        domain_tong.append(('sms_ids','!=',r.sms_id.id))
                    poster_quan10_greater_10 = self.env['bds.poster'].search(domain_tong)
                    poster_quan10_greater_10 = poster_quan10_greater_10.filtered(filter_for_poster )
                    r.poster_ids =poster_quan10_greater_10
                    r.len_poster = len(poster_quan10_greater_10)
            elif r.loc_gian_tiep_quan_bds_topic == u'Qua BDS SQL':
                slq_cmd = '''select distinct p.id from bds_bds as b inner join bds_poster as p on b.poster_id = p.id'''
                where_list = []
                if r.quan_ids:
#                     domain = expression.AND([[( 'quan_id','in',r.quan_ids.ids)],domain])
                    where_list.append(("b.quan_id in %s"%(tuple(r.quan_ids.ids),)).replace(',)',')'))
                if r.post_count_min:
#                     domain = expression.AND([[('count_post_all_site','>=',r.post_count_min)],domain])
                    where_list.append("b.count_post_all_site >= %s"%r.post_count_min)
                if r.gia_be_hon:
                    where_list.append("b.gia <= %s"%r.gia_be_hon)
                if r.gia_lon_hon:
                    where_list.append("b.gia >= %s"%r.gia_lon_hon)
                if r.nha_mang:
                    where_list.append("p.nha_mang ='%s'"%r.nha_mang)
#                     post_ids = post_ids.filtered(lambda i: i.nha_mang == r.nha_mang)
                where_clause = u' and '.join(where_list)
                if where_list:
                    slq_cmd = slq_cmd + ' where ' + where_clause
                self.env.cr.execute(slq_cmd)
                rsul = self.env.cr.fetchall()
                poster_ids = map(lambda i:i[0],rsul)
                r.poster_ids = poster_ids
                r.len_poster = len(poster_ids)
                
            elif r.loc_gian_tiep_quan_bds_topic ==u'Qua Thống Kê Quận Object':
                    if not r.sms_id:
                        pass
                    else:
                        domain_tong = []
                        if r.nha_mang:
                            nha_mang_domain = ('nha_mang','=',r.nha_mang)
                            domain_tong.append(nha_mang_domain)
                        if r.quan_ids and r.post_count_min:
                            domain_tong = expression.AND([[( 'quanofposter_ids.quan_id','in',r.quan_ids.ids),('quanofposter_ids.quantity','>=',r.post_count_min)], domain_tong])
                        if r.phuong_loc_ids:
                            domain_tong = expression.AND([('phuong_id' ,'in',r.phuong_loc_ids.mapped('id')),domain_tong])
                        if r.filter_sms_or_filter_sql =='sms_ids' and not r.is_repost_for_poster:
                            domain_tong.append(('sms_ids','!=',r.sms_id.id))
                        poster_quan10_greater_10 = self.env['bds.poster'].search(domain_tong)
                        poster_quan10_greater_10 = poster_quan10_greater_10.filtered(filter_for_poster )
                        r.poster_ids =poster_quan10_greater_10
                        r.len_poster = len(poster_quan10_greater_10)
            
            
            elif r.loc_gian_tiep_quan_bds_topic == u'Qua BDS SQL 1':
#                 slq_cmd = '''select distinct p.id from bds_bds as b inner join bds_poster as p on b.poster_id = p.id'''
#                 slq_cmd = '''SELECT p.id,
#        COUNT(b.id) AS topic_count
#   FROM bds_bds b
#        INNER JOIN bds_poster p
#                   ON b.poster_id = p.id
#     WHERE p.nha_mang = 'vina'
# GROUP BY 
#        p.id
# HAVING COUNT(b.id) > 10'''
                
                slq_cmd = '''SELECT p.id,
         COUNT(b.id) AS topic_count
        FROM bds_bds b
         INNER JOIN bds_poster p
                    ON b.poster_id = p.id '''
                    
                    
                where_list =[]
                if r.nha_mang:
                    where_list.append("p.nha_mang ='%s'"%r.nha_mang)
                if r.quan_ids:
                    where_list.append(("b.quan_id in %s"%(tuple(r.quan_ids.ids),)).replace(',)',')'))
                if not r.is_repost_for_poster:
                    post_ids_da_gui_cua_sms_nay_ids = r.sms_id.poster_ids
                    where_list.append(("p.id not in %s"%(tuple(post_ids_da_gui_cua_sms_nay_ids.ids),)).replace(',)',')'))
                    
                where_clause = u' and '.join(where_list)
                if where_clause:
                    where_clause = 'WHERE ' + where_clause
                slq_cmd = slq_cmd + where_clause + 'GROUP BY p.id '
                
                having_list =[]
                if r.post_count_min:
                    having_list.append("COUNT(b.id) > %s"%r.post_count_min)
           
                having_clause = u' and '.join(having_list)
                if having_clause:
                    having_clause = 'HAVING ' + having_clause
                slq_cmd += having_clause
                print ('**slq_cmd',slq_cmd)
                
                
             
                self.env.cr.execute(slq_cmd)
                rsul = self.env.cr.fetchall()
                print ('**rsul',rsul)
                self.description = rsul
                poster_ids = map(lambda i:i[0],rsul)
                r.poster_ids = poster_ids
                r.len_poster = len(poster_ids)
                
                 
                
                
                #print '*******rsul*******',rsul
            elif r.loc_gian_tiep_quan_bds_topic ==u'Qua BDS Object':
                domain = []
                if r.quan_ids:
                    domain = expression.AND([[( 'quan_id','in',r.quan_ids.ids)],domain])
                if  r.post_count_min:
                    domain = expression.AND([[('count_post_all_site','>=',r.post_count_min)],domain])
                if r.gia_be_hon:
                    domain = expression.AND([[('gia','<=',r.gia_be_hon)],domain])
                if r.gia_lon_hon:
                    domain = expression.AND([[('gia','>=',r.gia_lon_hon)],domain])
                bds = self.env['bds.bds'].search(domain)
                post_ids = bds.mapped('poster_id')
                if r.nha_mang:
                    post_ids = post_ids.filtered(lambda i: i.nha_mang == r.nha_mang)
                    
                
                if not r.is_repost_for_poster:
                    post_ids_da_gui_cua_sms_nay_ids = r.sms_id.poster_ids
                    post_ids = post_ids.filtered(lambda r: r.id not in post_ids_da_gui_cua_sms_nay_ids.ids )
                    r.poster_da_gui_cua_sms_nay_ids = post_ids_da_gui_cua_sms_nay_ids
                r.poster_ids = post_ids
                r.len_poster = len(post_ids)
                r.bds_ids = bds
                
                                

        
class Importcontact(models.Model):
    _name = 'bds.importcontact'
    file = fields.Binary()
    land_contact_saved_number = fields.Integer()
    trigger_fields = fields.Selection([('bds.bds','bds.bds')])
    
    @api.multi
    def trigger(self):
        #print 'hihihihiihih trigger'
        self.env[self.trigger_fields].search([]).write({'is_triger':True})
    @api.multi
    def import_contact(self):
        import_contact(self)
        
  
    @api.multi
    def count_post_of_poster(self):
        for r in self.env['bds.poster'].search([]):
            post_of_poster_cho_tot = self.env['bds.bds'].search([('poster_id','=',r.id),('link','like','chotot')])
            count_bds_post_of_poster = self.env['bds.bds'].search([('poster_id','=',r.id),('link','like','batdongsan')])
            r.count_chotot_post_of_poster = len(post_of_poster_cho_tot)
            r.count_bds_post_of_poster = len(count_bds_post_of_poster)
            count_bds_post_of_poster = self.env['bds.bds'].search([('poster_id','=',r.id)])
            r.count_post_all_site = len(count_bds_post_of_poster)
            
    @api.multi
    def insert_count_by_sql(self):
        product_category_query = '''UPDATE bds_poster 
SET count_post_all_site = i.count
FROM (
    SELECT count(id),poster_id
    FROM bds_bds group by poster_id)  i
WHERE 
    i.poster_id = bds_poster.ID

'''    
        
        #self.env.cr.execute(product_category_query)
        
        bds_site = self.env['bds.siteleech'].search([('name','like','batdongsan')]).id
        chotot_site = self.env['bds.siteleech'].search([('name','like','chotot')]).id
        for x in [bds_site,chotot_site]:
            if x ==bds_site:
                name = 'bds'
            else:
                name ='chotot'
            product_category_query = '''UPDATE bds_poster 
    SET count_post_of_poster_%s = i.count
    FROM (
        SELECT count(id),poster_id,siteleech_id
        FROM bds_bds group by poster_id,siteleech_id)  i
    WHERE 
        i.poster_id = bds_poster.ID and i.siteleech_id=%s'''%(name,x)
        
            self.env.cr.execute(product_category_query) 
        #product_category = self.env.cr.fetchall()
        ##print product_category
    @api.multi
    def add_nha_mang(self):
        for r in self.env['bds.poster'].search([]):
            #print 'handling...',r.name
            patterns = {'vina':'(^091|^094|^0123|^0124|^0125|^0127|^0129|^088)',
                        'mobi':'(^090|^093|^089|^0120|^0121|^0122|^0126|^0128)',
                       'viettel': '(^098|^097|^096|^0169|^0168|^0167|^0166|^0165|^0164|^0163|^0162|^086)'}
            if r.phone:
                for nha_mang,pattern in patterns.items():
                    rs = re.search(pattern, r.phone)
                    if rs:
                        r.nha_mang = nha_mang
                        break
                if not rs:
                    r.nha_mang = 'khac'
    
    @api.multi
    def add_site_leech_tobds(self):
        chotot_site = self.env['bds.siteleech'].search([('name','ilike','chotot')])
        ctbds = self.env['bds.bds'].search([('link','ilike','chotot')])
        ctbds.write({'siteleech_id':chotot_site.id})
        
        chotot_site = self.env['bds.siteleech'].search([('name','ilike','batdongsan')])
        ctbds = self.env['bds.bds'].search([('link','ilike','batdongsan')])
        ctbds.write({'siteleech_id':chotot_site.id})
        
    
  
    @api.multi
    def add_min_max_avg_for_user(self):
        for c,r in enumerate(self.env['bds.poster'].search([])):
            #print 'hadling...one usee' ,c
            product_category_query = '''select min(gia),avg(gia),max(gia) from bds_bds  where poster_id = %s and gia > 0'''%r.id
            self.env.cr.execute(product_category_query)
            product_category = self.env.cr.fetchall()
            r.min_price = product_category[0][0]
            r.avg_price = product_category[0][1]
            r.max_price = product_category[0][2]
            #print' min,avg,max', product_category
            
    @api.multi
    def add_quan_lines_ids_to_poster(self):
        for c,r in enumerate(self.env['bds.poster'].search([])):
            #print 'hadling...one usee' ,c
            product_category_query =\
             '''select count(quan_id),quan_id,min(gia),avg(gia),max(gia) from bds_bds where poster_id = %s group by quan_id'''%r.id
            self.env.cr.execute(product_category_query)
            product_category = self.env.cr.fetchall()
            #print product_category
            for  tuple_count_quan in product_category:
                quan_id = int(tuple_count_quan[1])
                #quantity = int(tuple_count_quan[0].replace('L',''))
                quan = self.env['bds.quan'].browse(quan_id)
                if quan.name in [u'Quận 1',u'Quận 3',u'Quận 5',u'Quận 10',u'Tân Bình']:
                    for key1 in ['count','avg']:
                        if key1 =='count':
                            value = tuple_count_quan[0]
                        elif key1 =='avg':
                            value = tuple_count_quan[3]
                        name = quan.name_unidecode.replace('-','_')
                        name = key1+'_'+name
                        setattr(r, name, value)
                        #print 'set attr',name,value
                g_or_c_ss(self,'bds.quanofposter', {'quan_id':quan_id,
                                                             'poster_id':r.id}, {'quantity':tuple_count_quan[0],
                                                                                'min_price':tuple_count_quan[2],
                                                                                'avg_price':tuple_count_quan[3],
                                                                                'max_price':tuple_count_quan[4],
                                                                                 }, True)
                
                
    @api.multi
    def add_quan_lines_ids_to_poster_theo_siteleech_id(self):
        for c,r in enumerate(self.env['bds.poster'].search([])):
            
            product_category_query_siteleech =\
             '''select count(quan_id),quan_id,min(gia),avg(gia),max(gia),siteleech_id from bds_bds where poster_id = %s group by quan_id,siteleech_id'''%r.id
            product_category_query_no_siteleech = \
            '''select count(quan_id),quan_id,min(gia),avg(gia),max(gia) from bds_bds where poster_id = %s group by quan_id'''%r.id
            a = {'product_category_query_siteleech':product_category_query_siteleech,
                 'product_category_query_no_siteleech':product_category_query_no_siteleech
                 }
            for k,product_category_query in a.items():
                self.env.cr.execute(product_category_query)
                product_category = self.env.cr.fetchall()
                #print product_category
                for  tuple_count_quan in product_category:
                    quan_id = int(tuple_count_quan[1])
                    if k =='product_category_query_no_siteleech':
                        siteleech_id =False
                    else:
                        siteleech_id = int(tuple_count_quan[5])
                    g_or_c_ss(self,'bds.quanofposter', {'quan_id':quan_id,
                                                                 'poster_id':r.id,'siteleech_id':siteleech_id}, {'quantity':tuple_count_quan[0],
                                                                                    'min_price':tuple_count_quan[2],
                                                                                    'avg_price':tuple_count_quan[3],
                                                                                    'max_price':tuple_count_quan[4],
                                                                                     }, True)
                
            
    @api.multi
    def add_site_leech_to_url(self):
        for r in self.env['bds.url'].search([]):
            r.url = r.url
            
        
                          
# class Errors(models.Model):
#     _name = 'bds.error'
#     url = fields.Char()
#     code = fields.Char()
class Luong(models.Model):
    _name = 'bds.luong'
    threadname = fields.Char()
    url_id = fields.Many2one('bds.url')
    current_page = fields.Integer()

    
class Cron(models.Model):
 
    _inherit = "ir.cron"
    _logger = logging.getLogger(_inherit)
    @api.model
    def worker(self,thread_index,url_id,thread_number):
        new_cr = sql_db.db_connect(self.env.cr.dbname).cursor()
        uid, context = self.env.uid, self.env.context
        with api.Environment.manage():
            self.env = api.Environment(new_cr, uid, context)
            luong = g_or_c_ss(self,'bds.luong', {'threadname':str(1),'url_id':url_id})
            if luong[0].current_page==0:
                current_page = thread_index
            else:
                current_page = luong[0].current_page + thread_number
            luong[0].write({'current_page':current_page})
            new_cr.commit()
            self.env.cr.close()
def name_compute(r,adict=None,join_char = u' - '):
    names = []
    for fname,attr_dict in adict:
        val = getattr(r,fname)
        fnc = attr_dict.get('fnc',None)
        if fnc:
            val = fnc(val)
        if  not val:# Cho có trường hợp New ID
            if attr_dict.get('skip_if_False',True):
                continue
            if  fname=='id' :
                val ='New'
            else:
                val ='_'
        if attr_dict.get('pr',None):
            item =  attr_dict['pr'] + u': ' + unicode(val)
        else:
            item = unicode (val)
        names.append(item)
    if names:
        name = join_char.join(names)
    else:
        name = False
    return name
class IphoneType(models.Model):
    _name = 'iphonetype'
    name = fields.Char(compute='name_',store=True)
    name_cate = fields.Char()
    dung_luong = fields.Integer()
    nhap_khau_hay_chinh_thuc = fields.Selection([(u'nhập khẩu',u'Nhập Khẩu'),(u'chính thức',u'chính Thức')])
    @api.depends('name_cate','dung_luong','nhap_khau_hay_chinh_thuc')
    def name_(self):
        for r in self:
            r.name = \
            name_compute(r,[('name_cate',{}),
                            ('dung_luong',{}),
                            ('nhap_khau_hay_chinh_thuc',{})
                            ]
            )
class DienThoai(models.Model):
    _name = 'dienthoai'
    iphonetype_id = fields.Many2one('iphonetype')
    title = fields.Char()
    link = fields.Char()
    gia = fields.Float(digit=(6,2))
    so_luong = fields.Integer()
    duoc_ban_boi = fields.Char()
    is_bien_dong_item = fields.Boolean()
    original_itself_id = fields.Many2one('dienthoai')
    bien_dong_ids = fields.One2many('dienthoai','original_itself_id')
    topic_id  =  fields.Char()
    gia_hien_thoi = fields.Float(digit=(6,2))
    noi_dung_bien_dong = fields.Char()
    so_luong_hien_thoi = fields.Char()


        
        
class Mycontact(models.Model):
    _name = 'bds.mycontact'
    name = fields.Char()
    phone = fields.Char()