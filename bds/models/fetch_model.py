# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons.bds.models.fetch import fetch, fetch_all_url
import psycopg2
from odoo.addons.bds.models.laza import  fetch_lazada
import threading
import re
from odoo.exceptions import UserError
import datetime


class Fetch(models.Model):
    _name = 'bds.fetch'
    ghi_chu = fields.Char()
    name = fields.Char()
    url_id = fields.Many2one('bds.url')
    url_ids = fields.Many2many('bds.url')
    last_fetched_url_id = fields.Many2one('bds.url')#>0
    web_last_page_number = fields.Integer()
    set_leech_max_page = fields.Integer()
    is_for_first = fields.Selection([('1','1'),('2','2')])
    set_number_of_page_once_fetch = fields.Integer(default=5)
    link_number = fields.Integer()
    update_link_number = fields.Integer()
    create_link_number = fields.Integer()
    existing_link_number = fields.Integer()
    
    
    note = fields.Char()
    update_field_of_existing_recorder = fields.Selection([(u'giá',u'giá'),(u'all',u'all')],default = u'all')
    lazada_url = fields.Char()
    test_url = fields.Char()
    test_html = fields.Text()
    test_1 = fields.Char()
    invisible_or_show_html_lazada =  fields.Boolean(store=False)
    test_lazada = fields.Text()
    html_lazada = fields.Text()
    html_lazada_thread = fields.Text()
    html_lazada_thread_gia = fields.Text()
    topic_id = fields.Many2one('bds.bds')
    
    @api.multi
    def fetch(self):
        fetch(self)
    @api.multi
    def fetch_all_url(self):
        fetch_all_url(self)
        
    @api.multi
    def trigger(self):
        self.env['bds.bds'].search([]).write({'trigger':False})
    
    @api.multi
    def trigger2(self):
        self.env['bds.bds'].search([]).write({'trigger2':False})
    @api.multi
    def trigger3(self):
        self.env['bds.bds'].search([]).write({'trigger3':False})  
        
    @api.multi
    def poster_trigger(self):
        self.env['bds.poster'].search([]).write({'trigger4':False})
    
    @api.multi
    def quan_trigger(self):
        self.env['bds.quan'].search([]).write({'trigger':False})
        
        
    @api.multi
    def test_quan(self):
#         sql_cmd = "select AVG(don_gia),count(id) from bds_bds where  quan_id = %s and  don_gia >= 20 and don_gia <300"%r.id
        quan_10_id = self.env['bds.quan'].search([('name','ilike','quận 10')]).id
        alist = []
        for w in ['and ti_le_don_gia > 0.5 and ti_le_don_gia <5','']:
            sql_cmd = "select AVG(don_gia), count(id) from bds_bds where  quan_id = %s %s "%(quan_10_id,w)
            self.env.cr.execute(sql_cmd)
            rsul = self.env.cr.fetchall()
            alist.append(rsul)
        raise UserError('%s'%alist)
        
        
        
    @api.multi
    def set_0(self):
        self.url_ids.write({'current_page':0})
        
    @api.multi
    def set_0_2(self):
        self.url_ids.write({'current_page_for_first':0})
        
    @api.multi
    def xac_dinh_mg_hay_cc(self):
        pass
        
    @api.multi
    def test_something(self):
        url_id = self.env['bds.url'].search([('name','ilike','https://muaban.net/nha-mat-tien-quan-tan-phu-l5923-c3201')])
#         bds = self.env['bds.bds'].search([('url_id','=',url_id.id)])
        bds = self.env['bds.bds'].search([],limit=500)
        for r in  bds:
            
            rhtml = r.html
#             rs = re.search('(?<!(, |\. ))(?<!(\w|,|\.))[1-9]\d{0,3}[a-h]{0,1} (?!(tầng|lửng|lầu|trệt|x\d|x \d))[\w\s/]{,30}', rhtml,re.I)
            rs = re.search('(?<!(cách ))(bán nhà |số |mặt tiền |mt |địa chỉ |đc |dc )([1-9]\d{0,3}[a-h]{0,1} (?!mặt|tầng|lầu|tỷ|căn|xẹt|m)[\w\s/]{3,30})',rhtml,re.I)
#             rs = re.search('(bán nhà|số|mặt tiền|mt|địa chỉ|đc|dc)( |: |:| : )((([1-9]\d{0,3}[a-h]{0,1})|(\d+\w{0,2}(/\d+\w{0,1})+)) (?!mặt tiền|tầng)[\w\s/]{,30})',rhtml,re.I)
            
            
            if rs:
                dcmt = rs.group(0)
            else:
                dcmt = False
                
            rs = re.search('.{5,10}(\d+\w{0,2}(/\d+\w{0,1})+)[\w\s/]{,30}',rhtml,re.I)
            if rs:
                dia_chi_2 = rs.group(0)
            else:
                dia_chi_2 = False
            r.dia_chi_2 =dia_chi_2 
            r.dia_chi_mat_tien = dcmt
            
            
            
            print (r)
#         print ('******************%s'%datetime.datetime.now())
#         bdss = self.env['bds.bds'].search([('public_datetime','>',datetime.datetime.now() + datetime.timedelta(months=-1))])
# #         count = 0
#         for bds in bdss:
#             public_datetime = bds.public_datetime
#             public_date  = fields.Date.from_string(public_datetime)
#             bds.public_date = public_date
#             html = bds.html
#             rs = re.search('\d+/\d+.*?[() ]',html)
#             is_trich_dia_chi = None
#             if rs:
#                 count +=1
#                 trich_dia_chi = rs.group(0)
#                 trich_dia_chi = trich_dia_chi.replace('.','').replace(',','').replace(')','')
#                 trich_dia_chi = trich_dia_chi.strip()
#                 if trich_dia_chi not in ['24/24','3/2','30/4','19/5','24/7','3/2.','3/2,']:
#                     is_day = re.search('\d\d/\d\d\d\d', trich_dia_chi)
#                     if not is_day:
#                         if ')' not in trich_dia_chi:
#                             bds.trich_dia_chi = trich_dia_chi
#                             is_trich_dia_chi  = True
#             if not is_trich_dia_chi:
#                 bds.trich_dia_chi = False
#                 
#         bds.ghi_chu = count
                
                
    @api.depends('set_number_of_page_once_fetch')
    def name_(self):
        for r in self:
            r.name = 'Fetch, id:%s-url_ids:%s-set_number_of_page_once_fetch: %s'%(r.id,u','.join(r.url_ids.mapped('description')),r.set_number_of_page_once_fetch)
#     @api.multi
#     def test_something(self):
#         try:
#             connect_str = "dbname='d4hjs9k7gebcdj' user='efvchsjfsrkbak' host='ec2-54-225-72-238.compute-1.amazonaws.com' " + \
#                           "password='c7fc4dced7e7c6ee9f7d9eff7846fcbb18a8976a425e905a6e8673a125b6b205'"
#             # use our connection values to establish a connection
#             conn = psycopg2.connect(connect_str)
#             # create a psycopg2 cursor that can execute queries
#             cursor = conn.cursor()
# #             cursor.execute("""CREATE TABLE tutorials (name char(40));""")
# #             cursor.execute("""ALTER TABLE tutorials ADD Email varchar(255);""")
# #             cursor.execute("""INSERT INTO tutorials (Email)
# # VALUES ('Cardinal');""")
#             cursor.execute("""SELECT * from tutorials""")
#             conn.commit() # <--- makes sure the change is shown in the database
#             
# #             conn.close()
# #             cursor.close()
#             rows = cursor.fetchall()
#             print(rows)
#         except Exception as e:
#             print("Uh oh, can't connect. Invalid dbname, user or password?")
#             print(e)
            
            
    @api.multi
    def fetch_lazada(self):
        fetch_lazada(self)
    @api.multi
    def fetch_laza_cron(self,id_fetch):
        fetch_id2 = self.browse(id_fetch)
        fetch_lazada(fetch_id2)
    
    @api.multi
    def test_mail(self):
        pass
#         fromaddr = 'nguyenductu@gmail.com'
#         toaddrs  = 'nguyenductu@gmail.com'
# #         msg = 'Why,Oh why fffffffffffform !'
#         
#         msg = MIMEMultipart()
#         msg['From'] = fromaddr
#         msg['To'] = toaddrs
#         msg['Subject'] = "SUBJECT OF THE MAIL"
#          
#         body = "YOUR MESSAGE HERE"
#         msg.attach(MIMEText(body, 'plain'))
#         text = msg.as_string()
# 
#         username = 'tunguyen19771@gmail.com'
#         password = 'Tu87cucgach'
#         server = smtplib.SMTP('smtp.gmail.com:587')
#         server.starttls()
#         server.login(username,password)
#         server.sendmail(fromaddr, toaddrs, text)
#         server.quit()
        #print 'dont'
        
        
        
  

    @api.multi
    def group_quan(self):
        pass
#         product_category_query = '''select count(bds_bds.quan_id),bds_bds.phuong_id from odoo.addons.bds.models.fetch_bds_relate inner join bds_bds on fetch_bds_relate.bds_id = bds_bds.id where fetch_id = %s group by bds_bds.phuong_id'''%self.id
#         self.env.cr.execute(product_category_query)
#         product_category = self.env.cr.fetchall()
#         phuong_list = reduce(lambda y,x:([x[1]]+y) if x[1]!=None else y,product_category,[] )
        #self.phuong_ids = phuong_list
#         phuong_list = get_quan_list_in_big_page(self)
#         quan_list = get_quan_list_in_big_page(self,column_name='bds_bds.quan_id')
#         self.write({'phuong_ids':[(6,0,phuong_list)],'quan_ids':[(6,0,quan_list)]})#'quan_ids':[(6,0,quan_list)]
#         update_phuong_or_quan_for_url_id(self)
    
    

    def thread(self):
        thread_number = 5
        url_imput = self.url_id.url
        fetch_object = self
        for i in range(1,6):
            url_id = self.url_id.id
            w2 = threading.Thread(target=self.env['ir.cron'].worker,kwargs={'thread_index':i,'url_id':url_id,
                                                                            "thread_number" : thread_number,
                                                                            'url_imput':url_imput,
                                                                            "fetch_object":fetch_object
                                                                            })
            w2.start()


