# -*- coding: utf-8 -*-
import re
import base64
from odoo import models, fields, api,sql_db, tools
try:
    import urllib.request as urllib2_or_urllib_request
except:
    import urllib2 as urllib2_or_urllib_request
from odoo.exceptions import UserError
from unidecode import unidecode
import datetime

class Setread(models.TransientModel):
    _name = "bds.setread"
    
    @api.multi
    def set_bdsread(self):
        print ('self._context',self._context,'self._context.get("active_ids")',self._context.get("active_ids"))
        self.env['bds.bds'].browse(self._context.get("active_ids")).write({'is_read':True})
        return {
                'type': 'ir.actions.act_window',
                'res_model': 'bds.setread',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': self.id,
                'views': [(False, 'form')],
                'target': 'new',
            }
         
class QuanTamBDSUser(models.Model):
    _name = 'bds.quantam'
    bds_id = fields.Many2one('bds.bds')
    user_id = fields.Many2one('res.users',default=lambda self: self.env.user.id)
    dt = fields.Datetime(default = lambda self: datetime.datetime.now())
    
class KhachXemBDS(models.Model):
    _name = 'bds.khachxembds'
    bds_id = fields.Many2one('bds.bds')
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user.id)
    poster_id = fields.Many2one('bds.poster')     

    
class Images(models.Model):
    _name='bds.myimage'
    image = fields.Binary(attachment=True)
    name = fields.Char()
    bds_id = fields.Many2one('bds.bds')
    
class Gialines(models.Model):
    _name='bds.gialines'
    gia = fields.Float()
    bds_id = fields.Many2one('bds.bds')
    gia_cu = fields.Float()
    diff_gia = fields.Float()
    
class Publicdate(models.Model):
    _name='bds.publicdate'
    public_date_cu = fields.Date()
    bds_id = fields.Many2one('bds.bds')
    public_date = fields.Date()
    diff_public_date = fields.Integer()


        
        
        

class bds(models.Model):
    _name = 'bds.bds'
    _order = "id desc"
   
    url_id = fields.Many2one('bds.url')
    khachxembds_ids = fields.One2many('bds.khachxembds','bds_id')
    quantam_ids = fields.One2many('bds.quantam','bds_id')
    publicdate_ids =fields.One2many('bds.publicdate','bds_id')
    len_publicdate_ids = fields.Integer(compute='len_publicdate_ids_', store=True)
    
    public_date = fields.Date()
    diff_public_date = fields.Integer()
    gialines_ids = fields.One2many('bds.gialines','bds_id')
    my_images_ids = fields.One2many('bds.myimage','bds_id')
    is_co_image = fields.Boolean(compute='is_co_image_', store=True)
    html_replace = fields.Html(compute='html_replace_')
    
    chieu_ngang = fields.Float()
    chieu_dai =  fields.Float()
    my_dien_tich = fields.Float()
 
    is_read = fields.Boolean()
    name = fields.Char(compute = 'name_',store = True)
    title = fields.Char()
    images_ids = fields.One2many('bds.images','bds_id')
    siteleech_id = fields.Many2one('bds.siteleech')
    thumb = fields.Char()
    thumb_view = fields.Binary(compute='thumb_view_')  
    image = fields.Binary(compute='thumb_view_')   
    present_image_link = fields.Char()
    present_image_link_show = fields.Binary(compute='present_image_link_show_')
    muc_gia = fields.Selection([('<1','<1'),('1-2','1-2'),('2-3','2-3'),('3-4','3-4'),('4-5','4-5'),('5-6','5-6'),('6-7','6-7'),('7-8','7-8'),('8-9','8-9'),('9-10','9-10'),('10-11','10-11'),('11-12','11-12'),('>12','>12')],
                               compute='muc_gia_',store = True,string=u'Mức Giá')
    muc_dt = fields.Selection(
        [('<10','<10'),('10-20','10-20'),('20-30','20-30'),('30-40','30-40'),('40-50','40-50'),('50-60','50-60'),('60-70','60-70'),('>70','>70')],
        compute='muc_dt_',store = True,string=u'Mức diện tích')
    don_gia = fields.Float(digit=(6,0),compute='don_gia_',store=True,string=u'Đơn giá')
    muc_don_gia = fields.Selection([('0-30','0-30'),('30-60','30-60'),('60-90','60-90'),
                                    ('90-120','90-120'),('120-150','120-150'),('150-180','150-180'),('180-210','180-210'),('>210','>210')],compute='muc_don_gia_',store=True)
    ti_le_don_gia = fields.Float(digits=(6,2),compute='ti_le_don_gia_',store=True)
    muc_ti_le_don_gia = fields.Selection([('0-0.4','0-0.4'),('0.4-0.8','0.4-0.8'),('0.8-1.2','0.8-1.2'),
                                    ('1.2-1.6','1.2-1.6'),('1.6-2.0','1.6-2.0'),('2.0-2.4','2.0-2.4'),('2.4-2.8','2.4-2.8'),('>2.8','>2.8')],compute='muc_ti_le_don_gia_',store=True)
    
    poster_id = fields.Many2one('bds.poster')
    
    
    
    # related
    
    post_ids_of_user  = fields.One2many('bds.bds','poster_id',related='poster_id.post_ids')
    username = fields.Char(related='poster_id.username')
    detail_du_doan_cc_or_mg = fields.Selection(related='poster_id.detail_du_doan_cc_or_mg', store = True)
    du_doan_cc_or_mg = fields.Selection(related='poster_id.du_doan_cc_or_mg', store = True)
    ket_luan_cc_or_mg = fields.Selection(related='poster_id.ket_luan_cc_or_mg', store = True)
    max_trang_thai_lien_lac = fields.Selection(related='poster_id.max_trang_thai_lien_lac',store=True)
    count_chotot_post_of_poster = fields.Integer(related= 'poster_id.count_chotot_post_of_poster',store=True,string=u'chotot post quantity')
    count_bds_post_of_poster = fields.Integer(related= 'poster_id.count_bds_post_of_poster',store=True,string=u'bds post quantity')
    count_post_all_site = fields.Integer(related= 'poster_id.count_post_all_site',store=True)
    post_ids_of_user  = fields.One2many('bds.bds','poster_id',related='poster_id.post_ids')
    
    
    # related
    
#     username = fields.Char()
#     
#     
# 
#     post_ids_of_user = fields.Many2many('bds.bds','bds_bds_rel','bds_id','bds_id_here')
#     du_doan_cc_or_mg = fields.Selection([('dd_mg','dd_mg'),('dd_dt','dd_dt'), ('dd_cc','dd_cc'), ('dd_kb', 'dd_kb')])
#     detail_du_doan_cc_or_mg = fields.Selection(
#                                                   [('dd_cc_b_moi_gioi_n_address_rate_gt_0_5','dd_cc_b_moi_gioi_n_address_rate_gt_0_5'),
#                                                    ('dd_mg_b_moi_gioi_n_address_rate_lte_0_5','dd_mg_b_moi_gioi_n_address_rate_lte_0_5'), 
#                                                    ('dd_cc_b_kw_co_n_address_rate_gt_0_5', 'dd_cc_b_kw_co_n_address_rate_gt_0_5'),
#                                                    ('dd_mg_b_kw_co_n_address_rate_lte_1','dd_mg_b_kw_co_n_address_rate_lte_1'),
#                                                    ('dd_cc_b_chinh_chu_n_cpas_lte_3','dd_cc_b_chinh_chu_n_cpas_lte_3'),
#                                                   
#                                                    
#                                                    ('dd_cc_b_chinh_chu_n_cpas_gt_3_n_address_rate_gt_0', 'dd_cc_b_chinh_chu_n_cpas_gt_3_n_address_rate_gt_0'),
#                                                    ('dd_mg_b_chinh_chu_n_cpas_gt_3_n_address_rate_eq_0', 'dd_mg_b_chinh_chu_n_cpas_gt_3_n_address_rate_eq_0'),
#                                                    ('dd_cc_b_chinh_chu_n_cpas_lte_3_n_address_rate_gt_0', 'dd_cc_b_chinh_chu_n_cpas_lte_3_n_address_rate_gt_0'),
#                                                    ('dd_mg_b_chinh_chu_n_cpas_lte_3_n_address_rate_eq_0', 'dd_mg_b_chinh_chu_n_cpas_lte_3_n_address_rate_eq_0'),
# 
#                                                    
#                                                    ('dd_cc_b_khong_biet_n_cpas_gt_3_n_address_rate_gte_0_3','dd_cc_b_khong_biet_n_cpas_gt_3_n_address_rate_gte_0_3'),
#                                                    ('dd_cc_b_khong_biet_n_cpas_lte_3_n_address_rate_gt_0','dd_cc_b_khong_biet_n_cpas_lte_3_n_address_rate_gt_0'),
#                                                    ('dd_mg_b_khong_biet_n_cpas_gt_3_n_address_rate_lt_0_3','dd_mg_b_khong_biet_n_cpas_gt_3_n_address_rate_lt_0_3'),
#                                                    ('dd_kb','dd_kb')
#                                                    ])
#     
#     
#     ket_luan_cc_or_mg = fields.Selection([('dd_mg','dd_mg'),('dd_dt','dd_dt'), ('dd_cc','dd_cc'), ('dd_kb', 'dd_kb')])
#     max_trang_thai_lien_lac = fields.Selection([(u'1',u'request zalo'),(u'2',u'added zalo'),
#                                             (u'3',u'Đã gửi sổ'),(u'4',u'Đã xem nhà'),(u'5',u'Đã Dẫn khách'),
#                                             (u'6',u'Không có zalo')])    
#     
#     count_chotot_post_of_poster = fields.Integer()
#     count_bds_post_of_poster = fields.Integer()
#     count_post_all_site = fields.Integer()
    
    
    
    html = fields.Html()
    html_khong_dau = fields.Html(compute='html_khong_dau_',store=True)
    link_show =  fields.Char(compute='link_show_')
    moi_gioi_hay_chinh_chu = fields.Selection([('moi_gioi', 'moi_gioi'), ('chinh_chu', 'chinh_chu'), ('khong_biet', 'khong_biet')], default='khong_biet')
    mtg = fields.Boolean(compute = 'mien_tiep_mg_', store = True)
    mqc = fields.Boolean(compute = 'mqc_', store = True)
  
    trich_dia_chi = fields.Char(compute='trich_dia_chi_', store = True)
    dd_tin_cua_co = fields.Boolean(compute='trich_dia_chi_', store = True, string='kw môi giới')
    dd_tin_cua_dau_tu = fields.Boolean(compute='dd_tin_cua_dau_tu_', store = True,string='kw đầu tư')
    
    html_show = fields.Text(compute='html_show_',string = u'Nội dung')
    gia = fields.Float()
    gia_show = fields.Char(compute = 'gia_show_')
  
    gia_trieu = fields.Float()
    area = fields.Float(digits=(32,1))
    address=fields.Char()
    quan_id = fields.Many2one('bds.quan',ondelete='restrict')
    quan_tam = fields.Datetime(string=u'Quan Tâm')
    lam_co = fields.Datetime(string=u'làm có')
    ko_quan_tam = fields.Datetime(string=u'Không Quan Tâm')

    hem_truoc_nha = fields.Float(digit=(6,2))
    comment = fields.Char()
    ket_cau = fields.Selection([(u'Đất Trống',u'Đất Trống'),(u'Cấp 4',u'Cấp 4'),(u'1 Tầng',u'1 Tầng'),(u'2 Tầng',u'2 Tầng'),(u'3 Tầng',u'3 Tầng'),(u'4 Tầng',u'4 Tầng'),(u'5 Tầng',u'5 Tầng'),(u'lon hon 5 ',u'lon hon 5')])
#     quan_id_selection = fields.Selection([])
    date_text = fields.Char()
    quan_id_selection = fields.Selection('get_quan_')
    trigger2 = fields.Boolean()
    trigger3 = fields.Boolean()
    sub_html = fields.Html(compute='sub_html_',store=True)
    auto_ngang = fields.Float(compute = 'auto_ngang_doc_',store=True)
    auto_doc = fields.Float(compute = 'auto_ngang_doc_',store=True)
    auto_dien_tich = fields.Float(compute = 'auto_ngang_doc_',store=True)
    ti_le_dien_tich_web_vs_auto_dien_tich = fields.Float(compute = 'auto_ngang_doc_',store=True)
    choosed_area = fields.Float(compute = 'auto_ngang_doc_',store=True)
    same_address_bds_ids = fields.Many2many('bds.bds','same_bds_and_bds_rel','same_bds_id','bds_id',compute='same_address_bds_ids_',store=True)
    len_same_address_bds_ids = fields.Integer(compute='same_address_bds_ids_',store=True)
    
    
    phuong_quan = fields.Char(compute='phuong_quan_', store=True)
    phuong = fields.Char(compute='phuong_quan_', store=True)
    quan = fields.Char(compute='phuong_quan_', store=True)
    after_trich_dia_chi = fields.Char(compute='trich_dia_chi_',store = True)
    mien_tiep_mg = fields.Char(compute='mien_tiep_mg_', store=True)
    diff_gia = fields.Float()
    
    
    phuong_id = fields.Many2one('bds.phuong')
    link = fields.Char()
    cho_tot_link_fake = fields.Char(compute='cho_tot_link_fake_')
    public_datetime = fields.Datetime()
    first_public_datetime = fields.Datetime()
   
#     count_chotot_post_of_poster = fields.Integer()
#     count_bds_post_of_poster = fields.Integer()
#     count_post_all_site = fields.Integer()
#     max_trang_thai_lien_lac = fields.Char()
#     du_doan_cc_or_mg = fields.Selection([('dd_mg','dd_mg'),('dd_dt','dd_dt'), ('dd_cc','dd_cc'), ('dd_kb', 'dd_kb')])
#     ket_luan_cc_or_mg = fields.Selection([('dd_mg','dd_mg'),('dd_dt','dd_dt'), ('dd_cc','dd_cc'), ('dd_kb', 'dd_kb')])
  
    
    
    
    data = fields.Text()
    url_ids = fields.Many2many('bds.url','url_post_relate','post_id','url_id')
    is_triger = fields.Boolean()
    again_update_date = fields.Datetime()
    phuong_15 = fields.Boolean()
    greater_day = fields.Integer()
    trang_thai_lien_lac = fields.Selection([(u'1',u'request zalo'),(u'2',u'added zalo'),
                                            (u'3',u'Đã gửi sổ'),(u'4',u'Đã xem nhà'),(u'5',u'Đã Dẫn khách'), (u'6',u'Không có zalo')])
    
    ngay_update_gia = fields.Datetime()
    begin_gia = fields.Float()
    dia_chi_mat_tien = fields.Char()
    dia_chi_2 = fields.Char()
    def test(self):
        for r in self:
            same_address_bds_ids  = self.env['bds.bds'].search([('trich_dia_chi','=ilike',r.trich_dia_chi), ('id','!=',r.id)])
            raise UserError(same_address_bds_ids)
    
    
    @api.depends('publicdate_ids')
    def len_publicdate_ids_(self):
        for r in self:
            r.len_publicdate_ids = len(r.publicdate_ids)
    @api.depends('html')
    def html_replace_(self):
        for r in self:
            html =  r.html
            html_replace = re.sub('[\d. ]{10,11}','',html)
            if r.trich_dia_chi:
                html_replace = html_replace.replace(r.trich_dia_chi,'')
            r.html_replace = html_replace
    @api.depends('gia')
    def gia_show_(self):
        for r in self:
            r.gia_show = '%s tỷ'%r.gia
            
            
    @api.depends('my_images_ids')
    def is_co_image_(self):
        for r in self:
            r.is_co_image = bool(r.my_images_ids)
    @api.depends('html','trigger3')
    def mien_tiep_mg_(self):
        for r in self:
            rs = re.search('(miễn|không)[\w ]{0,15}(môi giới|mg|trung gian|tg|cò)|mtg|mmg',r.html,re.I)
            if rs:
                r.mien_tiep_mg = rs.group(0)
                r.mtg = True
    @api.depends('html', 'trigger2')
    def phuong_quan_(self):
        for r in self:
            str= r.html
            rs = re.search(r'(?:\bphường|p)[ .]{0,2}((?:\w+ {0,1}){1,4})[ ,]{1,3}(?:quận|q)[ .]{0,2}((?:\w+ {0,1}){1,4})\b',str,re.I)
            if rs:
                r.phuong_quan = rs.group(0)
                r.phuong = rs.group(1)
                r.quan = rs.group(2)
    
    @api.depends('html','trigger')
    def trich_dia_chi_(self):
        for r in self:
            black_list = ['11/21 Nguyễn Hữu Tiến']
            title = r.title
            html =  r.html
            address = r.address
            trich_dia_chi = False
            if address:
                rs = re.search('^(\d+\w{0,2}(/\d+\w{0,2})+)[^\w/]',address)
                if rs:
                    trich_dia_chi = rs.group(1)
            adict = {'title':title, 'html':html}
            if address:
                adict.update({'address':address})
            if html:
                dd_tin_cua_co = False
                for key,rhtml in adict.items():
                    if key =='html':
                        for bl in black_list:
                            black_list_re = re.search(bl,rhtml,re.I)
                            if black_list_re:
                                r.dd_tin_cua_co = True
                                return True
                    
                    if not trich_dia_chi:
                        rs = re.search('(?<!hẻm) (\d+\w{0,2}(/\d+\w{0,1})+)[^\w/]',rhtml)
                        
                        if rs:
                            trich_dia_chi = rs.group(1)
                            trich_dia_chi = trich_dia_chi.replace('.','').replace(',','').replace('(','').replace(')','')
                            trich_dia_chi = trich_dia_chi.strip()
                            if trich_dia_chi in ['24/24','24/7','24/24h', '24/24H','24/24/7']:
                                dd_tin_cua_co = True
                            elif trich_dia_chi not in ['3/2','30/4','19/5','3/2.','3/2,','23/9']:
                                is_day = re.search('\d+/\d\d\d\d', trich_dia_chi)
                                if not is_day:
                                    if 'm2' not in trich_dia_chi:
                                        r.trich_dia_chi = trich_dia_chi
                                        r.after_trich_dia_chi= rhtml[rs.span()[1]:rs.span()[1]+30]
                                        break
                if dd_tin_cua_co == False:       
                    kss= ['mmg','mqc','mtg', 'bds', 'cần tuyển','tuyển sale', 'tuyển dụng', 'bất động sản','bđs','ký gửi','land','tư vấn','thông tin chính xác']
                    is_match = False
                    for ks in kss:
                        rs = re.search(ks,html, re.I)
                        if rs:
                            is_match = True
                            break
                    if is_match:
                        dd_tin_cua_co = True
                r.dd_tin_cua_co = dd_tin_cua_co
                
                
    
    
    
    @api.depends('trich_dia_chi')
    def same_address_bds_ids_(self):
        for r in self:
            if r.trich_dia_chi:
                same_address_bds_ids  = self.env['bds.bds'].search([('trich_dia_chi','=ilike',r.trich_dia_chi),('id','!=',r.id)])
                r.len_same_address_bds_ids = len(same_address_bds_ids)
                r.same_address_bds_ids = [(6,0,same_address_bds_ids.mapped('id'))]
                
                
    @api.depends('html','trigger2')
    def auto_ngang_doc_(self):
        for r in self:
#             pt= '(\d{1,3}[m\.,]{0,1}\d{0,2}) {0,1}m{0,1} {0,1}x {0,1}(\d{1,3}[m\.,]{0,1}\d{0,2})'
#             pt= '(\d{1,3}[\.,m]{0,1}\d{0,2}) {0,1}m{0,1}(( {0,1}x {0,1})|([, ]{1,3}(dài|rộng|chiều dài|chiều rộng) ))(\d{1,3}[\.,m]{0,1}\d{0,2})'
            pt= '(\d{1,3}[\.,m]{0,1}\d{0,2}) {0,1}m{0,1}(( {0,1}x {0,1}))(\d{1,3}[\.,m]{0,1}\d{0,2})'
            rs = re.search(pt, r.html,flags = re.I)
            if rs:
                auto_ngang,auto_doc = float(rs.group(1).replace(',','.').replace('m','.').replace('M','.')),float(rs.group(4).replace(',','.').replace('m','.').replace('M','.'))
            elif not rs:
                pt= '(dài|rộng|chiều dài|chiều rộng)[: ]{1,2}(\d{1,3}[\.,m]{0,1}\d{0,2}) {0,1}m{0,1}(([, ]{1,3}(dài|rộng|chiều dài|chiều rộng)[: ]{1,2}))(\d{1,3}[\.,m]{0,1}\d{0,2})'
                rs = re.search(pt, r.html,flags = re.I)
                if rs:
                    auto_ngang, auto_doc = float(rs.group(2).replace(',','.').replace('m','.').replace('M','.')),float(rs.group(6).replace(',','.').replace('m','.').replace('M','.'))
            if rs and  auto_ngang and auto_doc:
                auto_dien_tich = auto_ngang*auto_doc
                rarea = r.area
                ti_le_dien_tich_web_vs_auto_dien_tich = rarea/auto_dien_tich
                r.auto_ngang,r.auto_doc, r.auto_dien_tich, r.ti_le_dien_tich_web_vs_auto_dien_tich = auto_ngang, auto_doc, auto_dien_tich, ti_le_dien_tich_web_vs_auto_dien_tich
                
                if ti_le_dien_tich_web_vs_auto_dien_tich < 1.3 and ti_le_dien_tich_web_vs_auto_dien_tich > 0.7:
                    choosed_area =  rarea
                else:
                    choosed_area = auto_dien_tich
            else:
                choosed_area = r.area
            r.choosed_area = choosed_area
                
                
        
    @api.depends('html','trigger')
    def sub_html_(self):
        for r in self:
            pt ='(liên hệ|lh|dt)([: ]{0,3})(.{1,20}[\d. -]{8,14})+'
            rs = re.sub(pt, '', r.html, flags = re.I)
            pt= '(hoa hồng|huê hồng|hh).*?(1%|\d{2,3}\s{0,1}(triệu|tr))'
            rs = re.sub(pt, '',rs, flags = re.I)
            r.sub_html = rs
    
    
    hoahongsearch = fields.Char(compute ='hoahongsearch_',store=True)
    @api.depends('sub_html','trigger')
    def hoahongsearch_(self):
        for r in self:
            pt= '(hoa hồng|huê hồng|hh).+?(\d[\.\d]{0,2}%|\d{2,3}\s{0,1}(triệu|tr))'
            rs = re.search(pt, r.sub_html,flags = re.I)
            if rs:
                r.hoahongsearch = rs.group(0)
                
    
    search_remain_phone = fields.Char(compute ='search_remain_phone_',store=True)
    @api.depends('sub_html','trigger')
    def search_remain_phone_(self):
        for r in self:
            pt ='[\d. -]{8,14}'
            rs = re.search(pt, r.sub_html,flags = re.I)
            if rs:
                r.search_remain_phone = rs.group(0)
                       
            
            
    search_lien_he = fields.Char(compute ='search_lien_he_',store=True)
    @api.depends('html','trigger')
    def search_lien_he_(self):
        for r in self:
            pt ='(liên hệ|lh|dt)([: ]{0,3})(.{1,20}[\d. -]{8,14})+'
            rs = re.search(pt, r.html,flags = re.I)
            if rs:
                r.search_lien_he = rs.group(0)
    
    
    
    
    @api.depends('html','trigger')
    def mqc_(self):
        kss= ['quảng cáo','mqc','miễn qc','miễn tiếp báo']
        for r in self:
            is_match = False
            for ks in kss:
                rs = re.search(ks,r.html, re.I)
                if rs:
                    is_match = True
                    break
            if is_match:
                r.mqc = True
                    
#     @api.depends('html','trigger')
#     def mtg_(self):
#         kss= ['mtg','mmg','miễn trung gian','miễn mô giới']
#         for r in self:
#             is_match = False
#             for ks in kss:
#                 rs = re.search(ks,r.html, re.I)
#                 if rs:
#                     is_match = True
#                     break
#             if is_match:
#                 r.mtg = True
#                 
                
                
    
                    
                    
    @api.depends('html','trigger')
    def dd_tin_cua_dau_tu_(self):
#         pt= '(hoa hồng|huê hồng|hh|phí (môi giới|mg)).+?(\d[\.\d]{0,2}%|\d{2,3}\s{0,1}(triệu|tr))'
#         for r in self:
#             rs = re.search(pt, r.html,flags = re.I)
#             if rs:
#                 r.dd_tin_cua_dau_tu = True
        kss= ['hoa hồng','hh 1%', 'hh 0.5%','hh .{1,3}tr','1%','1 %','huê hồng','phí môi giới',]
        for r in self:
            is_match = False
            for ks in kss:
                rs = re.search(ks,r.html, re.I)
                if rs:
                    is_match = True
                    break
            if is_match:
                r.dd_tin_cua_dau_tu = True
                    
                    
                    
                    
                    
                    
    
    
    


                
                        
                    
                    
    
#     @api.depends('html','trigger')
#     def trich_dia_chi_(self):
#         for r in self:
#             title = r.title
#             html =  r.html
#             if html:
#                 dd_tin_cua_co = False
#                 for rhtml in [title, html]:
# #                     rs = re.search('(\d+\w{0,2}/(\d+\w{0,1}/*)+?)[\.() ]',rhtml)
#                     rs = re.search('(\d+\w{0,2}(/\d+\w{0,1})+?)[\.() ]',rhtml)
#                     if rs:
#                         trich_dia_chi = rs.group(0)
#                         trich_dia_chi = trich_dia_chi.replace('.','').replace(',','').replace('(','').replace(')','')
#                         trich_dia_chi = trich_dia_chi.strip()
#                         if trich_dia_chi in ['24/24','24/7','24/24h','24/24H']:
#                             dd_tin_cua_co = True
#                         elif trich_dia_chi not in ['3/2','30/4','19/5','3/2.','3/2,','23/9']:
#                             is_day = re.search('\d+/\d\d\d\d', trich_dia_chi)
#                             if not is_day:
#                                 if 'm2' not in trich_dia_chi:
#                                     
#                                     r.trich_dia_chi = trich_dia_chi
#                                     break
#                 if dd_tin_cua_co == False:       
#                     kss= ['mmg','mqc','mtg', 'bds', 'cần tuyển','tuyển sale', 'tuyển dụng', 'bất động sản','bđs','ký gửi']
#                     is_match = False
#                     for ks in kss:
#                         rs = re.search(ks,html, re.I)
#                         if rs:
#                             is_match = True
#                             break
#                     if is_match:
#                         dd_tin_cua_co = True
#                 r.dd_tin_cua_co = dd_tin_cua_co
    
    def link_show_(self):
        for r in self:
            if r.siteleech_id.name == 'chotot':
                r.link_show = r.cho_tot_link_fake
            else:
                r.link_show = r.link
    recent_create =  fields.Boolean(compute='recent_create_')
    
    def recent_create_(self):
        for r in self:
            create_date =  fields.Datetime.from_string(r.create_date)
            rs = datetime.datetime.now() - create_date
            rs = rs.seconds
            if rs < 3000:
                r.recent_create = True
#             r.test = rs
#     test = fields.Char(compute='recent_create_')
    
    def get_quan_(self):
        quans = self.env['bds.quan'].search([])
        rs = list(map(lambda i:(i.name,i.name),quans))
        return rs
    
#     spam = fields.Boolean(related='poster_id.spam')
    spam = fields.Boolean()
    siteleech_id_selection = fields.Selection('siteleech_id_selection_')
    def siteleech_id_selection_(self):
        oQuans = self.env['bds.siteleech'].search([])
        rs = list(map(lambda i:(i.name,i.name),oQuans))
        return rs
    trigger = fields.Boolean()
    @api.depends('html','trigger')
    def html_khong_dau_(self):
        for r in self:
            r.html_khong_dau = unidecode(r.html) if r.html else r.html
    
    
    @api.multi
    def open_something(self):
        return {
                'name': 'abc',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'bds.bds',
                'view_id': self.env.ref('bds.bds_form').id,
                'type': 'ir.actions.act_window',
                'res_id': self.id,
                'target': 'new'
            }
        
        
        
        
        
    @api.depends('ti_le_don_gia','is_triger')
    def muc_ti_le_don_gia_(self):
        muc_dt_list =[('0-0.4','0-0.4'),('0.4-0.8','0.4-0.8'),('0.8-1.2','0.8-1.2'),
                                    ('1.2-1.6','1.2-1.6'),('1.6-2.0','1.6-2.0'),('2.0-2.4','2.0-2.4'),('2.4-2.8','2.4-2.8'),('>2.8','>2.8')]
        for r in self:
            selection = None
            for muc_gia_can_tren in range(1,8):
                if r.ti_le_don_gia < muc_gia_can_tren*0.4:
                    selection = muc_dt_list[muc_gia_can_tren-1][0]
                    r.muc_ti_le_don_gia = selection
                    break
            if not selection:
                r.muc_ti_le_don_gia = '>2.8'
    @api.depends('don_gia','quan_id')
    def ti_le_don_gia_(self):
        for r in self:
            try:
                if r.don_gia and r.quan_id.muc_gia_quan:
                    r.ti_le_don_gia = r.don_gia/r.quan_id.muc_gia_quan
            except:
                pass
                
    @api.depends('gia','choosed_area','trigger2')
    def don_gia_(self):
        for r in self:
            if r.gia:
                if r.choosed_area:
                    r.don_gia = r.gia*1000/r.choosed_area
            else:
                r.don_gia = False
    @api.depends('don_gia')
    def muc_don_gia_(self):
        muc_dt_list =[('0-30','0-30'),('30-60','30-60'),('60-90','60-90'),
                                    ('90-120','90-120'),('120-150','120-150'),('150-180','150-180'),('180-210','180-210'),('>210','>210')]
        for r in self:
            selection = None
            for muc_gia_can_tren in range(1,8):
                if r.don_gia < muc_gia_can_tren*30:
                    selection = muc_dt_list[muc_gia_can_tren-1][0]
                    r.muc_don_gia = selection
                    break
            if not selection:
                r.muc_don_gia = '>210'
    @api.depends('choosed_area')
    def muc_dt_(self):
        muc_dt_list = [('<10','<10'),('10-20','10-20'),('20-30','20-30'),('30-40','30-40'),('40-50','40-50'),('50-60','50-60'),('60-70','60-70'),('>70','>70')]
        for r in self:
            selection = None
            for muc_gia_can_tren in range(1,8):
                if r.area < muc_gia_can_tren*10:
                    selection = muc_dt_list[muc_gia_can_tren-1][0]
                    r.muc_dt = selection
                    break
            if not selection:
                r.muc_dt = '>70'
    @api.depends('gia')
    def muc_gia_(self):
        muc_gia_list = [('<1','<1'),('1-2','1-2'),('2-3','2-3'),('3-4','3-4'),('4-5','4-5'),('5-6','5-6'),('6-7','6-7'),('7-8','7-8'),('8-9','8-9'),('9-10','9-10'),('10-11','10-11'),('11-12','11-12'),('>12','>12')]
        for r in self:
            selection = None
            for muc_gia_can_tren in range(1,len(muc_gia_list)):
                if r.gia < muc_gia_can_tren:
                    selection = muc_gia_list[muc_gia_can_tren-1][0]
                    r.muc_gia = selection
                    break
            if not selection:
                r.muc_gia = muc_gia_list[-1][0]
#     @api.depends('html')
#     def html_show_(self):
#         for r in self:
#             
#             if  r.html and len(r.html) > 201:
#                 r.html_show = r.html[:200] + '...'
#             else:
#                 r.html_show = r.html
    rq_zalo_hello = fields.Char(compute='rq_zalo_hello_', store = True)    
    @api.depends('title')
    def rq_zalo_hello_(self):
        for r in self:
            r.rq_zalo_hello = (u'Chào anh/chị %s, em bên cty môi giới, anh chị có thể  kết bạn zalo và gửi sổ căn nhà "%s" không ạ, phí cty là 1 %%'%(r.username if r.username else '', r.title) if r.title else '')
    
    @api.depends('html')
    def html_show_(self):
        for r in self:
            html = ((r.title) if r.title else '') + \
            ('\n' +r.quan_id.name if r.quan_id.name  else '') +\
            ('\n' + r.html if r.html else '') + ('\n' +r.poster_id.name if r.poster_id.name  else '') +\
            ('\n' +r.link_show if  r.link_show else '') + (u'\n Giá: %s tỷ'%r.gia if r.gia else '') + (u'\n Area: %s m2'%r.area if r.area else '')+\
            ('\n siteleech_id:%s'%r.siteleech_id.name) +\
            ('\n choosed_area:%s'%r.choosed_area) + (u', auto_ngang: %s'%r.auto_ngang) + (u', auto_doc: %s'%r.auto_doc) + (u', auto_dien_tich:%s'%r.auto_dien_tich) +  \
            ('\ndon_gia:%.2f'%r.don_gia) + (u' ti_le_don_gia: %.2f'%r.ti_le_don_gia)  + \
            ('\ncount_post_all_site:%s'%r.count_post_all_site) +\
            (u', len_same_address_bds_ids: %s'%r.len_same_address_bds_ids) +\
            (u', moi_gioi_hay_chinh_chu: %s'%r.moi_gioi_hay_chinh_chu) + \
            (u', ket_luan_cc_or_mg: %s'%r.ket_luan_cc_or_mg) +  \
            (u', detail_du_doan_cc_or_mg: %s'%r.detail_du_doan_cc_or_mg)
        #   ('\n' + u'Chào anh/chị %s, em bên cty môi giới, anh chị có thể  kết bạn zalo và gửi sổ căn nhà "%s" không ạ, phí cty là 1 %%'%(r.username if r.username else '', r.title) if r.title else '')

            r.html_show = html
            
    @api.model
    def create(self, vals):
        if 'gia' in vals:
            vals['begin_gia'] = vals['gia']
        if 'public_datetime' in vals:
            vals['first_public_datetime'] = vals['public_datetime']
        cv = super(bds, self).create(vals)
        return cv
        
    @api.multi
    def cho_tot_link_fake_(self):
        for r in self:
            if 'chotot' in r.link:
                rs = re.search('/(\d*)$',r.link)
                id_link = rs.group(1)
                r.cho_tot_link_fake = 'https://nha.chotot.com/quan-10/mua-ban-nha-dat/' + 'xxx-' + id_link+ '.htm'
    @api.depends('thumb')
    def thumb_view_(self):
        for r in self:
            if r.thumb:
                if 'nophoto' not in r.thumb:
                    photo = base64.encodestring(urllib2_or_urllib_request.urlopen(r.thumb).read())
                    r.thumb_view = photo 
                    r.image = photo
    @api.depends('present_image_link')
    def present_image_link_show_(self):
        for r in self:
            if r.present_image_link:
                photo = base64.encodestring(urllib2_or_urllib_request.urlopen(r.present_image_link).read())
                r.present_image_link_show = photo 

    @api.depends('title')
    def name_(self):
        self.name = self.title
        

               

