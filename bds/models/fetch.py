# -*- coding: utf-8 -*-
# import urllib2
# import sys

from odoo.exceptions import UserError
from odoo import models,fields
# VERSION_INFO   = sys.version_info[0]
# try:
#     import urllib.request as url_lib
# except:
#     import urllib2 as url_lib
from odoo.addons.bds.models.bds_tools  import  request_html,g_or_c_ss, get_or_create_user_cho_tot_batdongsan, MyError
from odoo.addons.bds.models.fetch_bds_com_vn  import get_bds_dict_in_topic, get_last_page_from_bdsvn_website, convert_gia_from_string_to_float
from odoo.addons.bds.models.fetch_chotot  import  get_topic_chotot, create_cho_tot_page_link, local_a_native_time, convert_chotot_price, convert_chotot_date_to_datetime, gmt_7_a_native_time
from odoo.addons.bds.models.fetch_muaban  import  get_muaban_vals_one_topic
from bs4 import BeautifulSoup
import datetime
import re
from unidecode import unidecode
import json
import math
from copy import deepcopy

import pytz
def convert_native_utc_datetime_to_gmt_7(utc_datetime_inputs):
    local = pytz.timezone('Etc/GMT-7')
    utc_tz =pytz.utc
    gio_bat_dau_utc_native = utc_datetime_inputs#fields.Datetime.from_string(self.gio_bat_dau)
    gio_bat_dau_utc = utc_tz.localize(gio_bat_dau_utc_native, is_dst=None)
    gio_bat_dau_vn = gio_bat_dau_utc.astimezone (local)
    return gio_bat_dau_vn


def gen_page_number_list(self, url_id, set_number_of_page_once_fetch, set_current_page= None):
    set_leech_max_page = self.set_leech_max_page
    url_id_site_leech_name  = url_id.siteleech_id.name
    
    if set_current_page == None:
        if self.is_for_first=='2':
            current_page_or_current_page_for_first = 'current_page_for_first'
        else:
            current_page_or_current_page_for_first = 'current_page'
        current_page = getattr(url_id, current_page_or_current_page_for_first)
    else:
        current_page = set_current_page
    
    if url_id_site_leech_name ==  'batdongsan':
        last_page_from_website =  get_last_page_from_bdsvn_website(url_id.url)
        self.web_last_page_number = last_page_from_website
    elif url_id_site_leech_name=='chotot':
        page_1_url = create_cho_tot_page_link(url_id.url, 1)
        html = request_html(page_1_url)
        html = json.loads(html)
        total = int(html["total"])
        last_page_from_website = int(math.ceil(total/20.0))
        self.web_last_page_number = last_page_from_website
    elif url_id_site_leech_name=='muaban':
        last_page_from_website = 100
        self.web_last_page_number = last_page_from_website   
    
    
   
    
    if  set_leech_max_page and set_leech_max_page < last_page_from_website:
        max_page = set_leech_max_page
    else:
        max_page = last_page_from_website
        
        
    begin = current_page + 1
    if begin > max_page:
        begin  = 1
    end = begin   + set_number_of_page_once_fetch - 1
    if end > max_page:
        end = max_page
    end_page_number_in_once_fetch = end
    page_lists = range(begin, end+1)
    so_page = end - begin + 1
    return end_page_number_in_once_fetch, page_lists, begin, so_page

def fetch_a_url_id (self, url_id, set_number_of_page_once_fetch, set_current_page = None):
    end_page_number_in_once_fetch, page_lists, begin, so_page =  gen_page_number_list(self, url_id, set_number_of_page_once_fetch, set_current_page = set_current_page) 
    begin_time = datetime.datetime.now()
    number_notice_dict = {
                                        'page_int':0,
                                        'curent_link':u'0/0',
                                        'link_number' : 0,
                                        'update_link_number' : 0,
                                        'create_link_number' : 0,
                                        'existing_link_number' : 0,
                                        'begin_page':begin,
                                        'so_page':so_page,
                                        'page_lists':page_lists,
                                        'length_link_per_curent_page':0,
                                        'topic_index':0,
    }
    
    
    page_index = 0
    for page_int in page_lists:
        page_index +=1
        number_notice_dict['page_int'] = page_int
        number_notice_dict['page_index'] = page_index
        page_handle(self, page_int, url_id, number_notice_dict)
   
    self.last_fetched_url_id = url_id.id
#     self.create_link_number=number_notice_dict['create_link_number']
#     self.update_link_number =number_notice_dict["update_link_number"]
#     self.link_number = number_notice_dict["link_number"]
#     self.existing_link_number = number_notice_dict["existing_link_number"]
    
    if self.is_for_first=='2':
        current_page_or_current_page_for_first = 'current_page_for_first'
    else:
        current_page_or_current_page_for_first = 'current_page'
    interval = (datetime.datetime.now() - begin_time).total_seconds()
    url_id.interval = interval
    url_id.write({current_page_or_current_page_for_first: end_page_number_in_once_fetch,
                   'web_last_page_number':self.web_last_page_number,
                   'create_link_number': number_notice_dict['create_link_number'],
                   'update_link_number': number_notice_dict["update_link_number"],
                   'link_number': number_notice_dict["link_number"],
                   'existing_link_number': number_notice_dict["existing_link_number"],
                   })
    return None


def fetch (self, note=False):
    url_ids = self.url_ids.ids
    if not self.last_fetched_url_id.id:
        new_index = 0
    else:
        try:
            index_of_last_fetched_url_id = url_ids.index(self.last_fetched_url_id.id)
            new_index =  index_of_last_fetched_url_id+1
        except ValueError:
            new_index = 0
        if new_index > len(url_ids)-1:
            new_index = 0
    url_id = self.url_ids[new_index]
    set_number_of_page_once_fetch = self.set_number_of_page_once_fetch
    try:
        fetch_a_url_id (self, url_id, set_number_of_page_once_fetch)
    except MyError as e:
        self.env['bds.error'].create({'name':str(e),'des':e.url})


def fetch_all_url(self):
    url_ids = self.url_ids
    set_number_of_page_once_fetch = self.set_number_of_page_once_fetch
    for url_id in url_ids:
        fetch_a_url_id (self, url_id, set_number_of_page_once_fetch, set_current_page = url_id.current_page)
    
    




def convert_muaban_string_gia_to_float(str):
    rs = re.search('(\d+) tỷ',str,re.I)
    if rs:
        ty = float(rs.group(1))*1000000000
    else:
        ty = 0
    rs = re.search('(\d+) triệu',str,re.I)
    if rs:
        trieu = float(rs.group(1))*1000000
    else:
        trieu = 0
    
    kq = (ty + trieu)/1000000000.0
    if not kq:
        gia = re.sub(u'\.|đ|\s', '',str)
        gia = float(gia)
        kq = gia/1000000000.0
    return kq


            
            
def page_handle(self, page_int, url_id, number_notice_dict):
    number_notice_dict['page_int'] = page_int
    links_of_one_page = []
    url_input = url_id.url
    siteleech_id = url_id.siteleech_id
    allow_write_public_datetime = True
    if siteleech_id.name=='batdongsan':
        url = url_input + '/' + 'p' +str(page_int)
        html = request_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        title_and_icons = soup.select('div.search-productItem')
        for title_and_icon in title_and_icons:
            topic_dict = {}
            title_soups = title_and_icon.select("div.p-title  a")
            topic_dict['list_id'] = title_soups[0]['href']
            icon_soup = title_and_icon.select('img.product-avatar-img')
            topic_dict['thumb'] = icon_soup[0]['src']
            
            gia_soup = title_and_icon.select('strong.product-price')
            gia = gia_soup[0].get_text()
            print ('gia%s'%gia)
            int_gia = convert_gia_from_string_to_float(gia)
            topic_dict['gia'] = int_gia
            
            date_dang = title_and_icon.select('div.p-main div.p-bottom-crop div.floatright')
            date_dang = date_dang[0].get_text().replace('\n','')
            print ('date_dang%s'%date_dang)
            date_dang = date_dang[-10:]
            public_datetime = datetime.datetime.strptime(date_dang,"%d/%m/%Y")
            topic_dict['public_datetime'] = public_datetime
#            
            topic_dict['thumb'] = icon_soup[0]['src']
            links_of_one_page.append(topic_dict)
    elif siteleech_id.name =='chotot':
        url = create_cho_tot_page_link(url_input,page_int)
        json_a_page = request_html(url)
        json_a_page = json.loads(json_a_page)
        links_of_one_page_origin = json_a_page['ads']
        for topic_dict_cho_tot in links_of_one_page_origin:
            topic_dict = deepcopy (topic_dict_cho_tot)
            gia,trieu_gia = convert_chotot_price(topic_dict)#topic_dict['price']
            topic_dict ['gia'] = gia
#             print (gia)
#             raise UserError('gia%s abd'%gia)
            date = topic_dict['date']
            naitive_dt = convert_chotot_date_to_datetime(date)
            
#             public_datetime_dt = convert_chotot_date_to_datetime(naitive_dt)
            topic_dict ['public_datetime'] = naitive_dt
            links_of_one_page.append(topic_dict)
#             print (date_obj)
#             raise UserError('date_obj%s abd'%date_obj)
            
    
    elif siteleech_id.name =='muaban':
        if page_int > 2:
            allow_write_public_datetime = False
        page_url =  re.sub('\?cp=(\d*)', '?cp=%s'%page_int, url_input)
        a_page_html = request_html(page_url)
        a_page_html_soup = BeautifulSoup(a_page_html, 'html.parser')
        title_and_icons = a_page_html_soup.select('div.mbn-box-list-content')
        for title_and_icon in title_and_icons:
            topic_dict = {}
            title_soups = title_and_icon.select("a.mbn-image")
            title_soup = title_soups[0]
            href = title_soup['href']
            img = title_soup.select('img')[0]
            src_img = img.get('data-original',False)
            topic_dict['list_id'] = href
            topic_dict['thumb'] = src_img
            area = 0
            try:
                area = title_and_icon.select('span.mbn-item-area b')[0].get_text()
                area = area.split(' ')[0].strip().replace(',','.')
                area = float(area)
            except IndexError:
                pass
            topic_dict['area']=area
            
            gia_soup = title_and_icon.select('span.mbn-price')
            if gia_soup:
                gia = gia_soup[0].get_text()
                gia = convert_muaban_string_gia_to_float(gia)
            else:
                gia = 0
            topic_dict['gia'] = gia  
            ngay_soup = title_and_icon.select('span.mbn-date')
            ngay = ngay_soup[0].get_text().strip().replace('\n','')
            public_datetime = datetime.datetime.strptime(ngay,"%d/%m/%Y")
            topic_dict['public_datetime'] = public_datetime  
#             raise UserError(public_datetime)
            links_of_one_page.append(topic_dict)
    elif siteleech_id.name =='lazada':
        url = url_input +'?page=' +int(page_int)
    number_notice_dict['curent_page'] = page_int 
    number_notice_dict['length_link_per_previous_page']  = number_notice_dict.get('length_link_per_curent_page',0)
    number_notice_dict['length_link_per_curent_page'] = len(links_of_one_page)
    topic_index = 0
    page_info = {'allow_write_public_datetime':allow_write_public_datetime, 'url_id':url_id.id}
    for topic_dict in links_of_one_page:
        topic_index +=1
        number_notice_dict['topic_index'] = topic_index
        if  siteleech_id.name =='chotot':
            link  = 'https://gateway.chotot.com/v1/public/ad-listing/' + str(topic_dict['list_id'])
        elif 'batdongsan' in siteleech_id.name:
            link  = 'https://batdongsan.com.vn' +  topic_dict['list_id']
        else:
            link = topic_dict['list_id']
        deal_a_topic(self,link, number_notice_dict, url_id, topic_dict=topic_dict, page_info= page_info)


# def deal_a_topic_old(self,link, number_notice_dict, url_id, topic_dict={}):
#     print (link)
#     print (u'topic_index %s/%s- page_int %s - page_index %s/so_page %s'%(number_notice_dict['topic_index'],number_notice_dict['length_link_per_curent_page'],
#                                                                         number_notice_dict['page_int'], number_notice_dict['page_index'],number_notice_dict['so_page']))
#     search_dict = {}
#     update_dict = {'again_update_date':datetime.datetime.now()}
#     search_dict['link'] = link
#     
#     
#     
#     html = request_html(link)
#     self.test_html = html
#     self.test_url = link
#     siteleech_id = url_id.siteleech_id
#     if siteleech_id.name =='chotot':
#         html = json.loads(html)
#     if siteleech_id.name =='batdongsan':    
#         get_bds_dict_in_topic(self,update_dict, html, siteleech_id)
#         update_dict['thumb'] = topic_dict.get('thumb',False)
#     elif siteleech_id.name =='chotot':
#         get_topic_chotot(self, update_dict, html, siteleech_id)
#         update_dict['thumb'] = topic_dict.get('image',False)
#         moi_gioi_hay_chinh_chu = topic_dict.get('company_ad',False)
#         if moi_gioi_hay_chinh_chu:
#             moi_gioi_hay_chinh_chu = 'moi_gioi'
#         else:
#             moi_gioi_hay_chinh_chu = 'chinh_chu'
#         update_dict['moi_gioi_hay_chinh_chu'] = moi_gioi_hay_chinh_chu
#     elif siteleech_id.name =='muaban':
#         get_muaban_vals_one_topic(self,update_dict,html,siteleech_id)
#         update_dict['area'] = topic_dict.get('area',False)
#         update_dict['thumb'] = topic_dict.get('thumb','ahahah')
#     search_link_obj= self.env['bds.bds'].search([('link','=',link)])
#     
#     
#     if search_link_obj:
#         number_notice_dict["existing_link_number"] = number_notice_dict["existing_link_number"] + 1
#         update_gia = update_dict['gia']
#         gia_cu = search_link_obj.gia
#         if gia_cu != update_gia:
#             diff_gia = update_gia-gia_cu
#             update_dict.update({'diff_gia':diff_gia, 'gialines_ids':[(0,False,{'gia':update_gia,'gia_cu':gia_cu,'diff_gia':diff_gia})],'ngay_update_gia':local_a_native_time(datetime.datetime.now())})
#             search_link_obj.write(update_dict)
#             number_notice_dict['update_link_number'] = number_notice_dict['update_link_number'] + 1
#     else:
#         update_dict['link'] = link
#         update_dict.update({'url_ids':[(4,url_id.id)]})
#         self.env['bds.bds'].create(update_dict)
#         number_notice_dict['create_link_number'] = number_notice_dict['create_link_number'] + 1    
#     link_number = number_notice_dict.get("link_number",0) + 1
#     number_notice_dict["link_number"] = link_number


def request_topic (self,link,update_dict, url_id, topic_dict):
    html = request_html(link)
    self.test_html = html
    self.test_url = link
    siteleech_id = url_id.siteleech_id
    if siteleech_id.name =='chotot':
        html = json.loads(html)
    if siteleech_id.name =='batdongsan':    
        get_bds_dict_in_topic(self,update_dict, html, siteleech_id)
        update_dict['thumb'] = topic_dict.get('thumb',False)
    elif siteleech_id.name =='chotot':
        get_topic_chotot(self, update_dict, html, siteleech_id)
        update_dict['thumb'] = topic_dict.get('image',False)
        moi_gioi_hay_chinh_chu = topic_dict.get('company_ad',False)
        if moi_gioi_hay_chinh_chu:
            moi_gioi_hay_chinh_chu = 'moi_gioi'
        else:
            moi_gioi_hay_chinh_chu = 'chinh_chu'
        update_dict['moi_gioi_hay_chinh_chu'] = moi_gioi_hay_chinh_chu
    elif siteleech_id.name =='muaban':
        get_muaban_vals_one_topic(self,update_dict,html,siteleech_id)
        update_dict['area'] = topic_dict.get('area',False)
        update_dict['thumb'] = topic_dict.get('thumb','ahahah')
        
        
def deal_a_topic(self,link, number_notice_dict, url_id, topic_dict={},  page_info= None):
    print (link)
#     print (u'topic_index %s/%s- page_int %s - page_index %s/so_page %s'%(number_notice_dict['topic_index'],number_notice_dict['length_link_per_curent_page'],
#                                                                         number_notice_dict['page_int'], number_notice_dict['page_index'],number_notice_dict['so_page']))
    
    update_dict = {}
    public_datetime = topic_dict['public_datetime']
    gmt7 = convert_native_utc_datetime_to_gmt_7(public_datetime)
    public_date  = gmt7.date()
    
    search_link_obj= self.env['bds.bds'].search([('link','=',link)])
    if search_link_obj:
        number_notice_dict["existing_link_number"] = number_notice_dict["existing_link_number"] + 1
        public_date_cu  = fields.Date.from_string(search_link_obj.public_date)
        if page_info['allow_write_public_datetime'] and  public_date != public_date_cu and public_date_cu and public_date:
            diff_public_date = (public_date - public_date_cu).days
            update_dict.update({'public_date':public_date})
            update_dict.update({'ngay_update_gia':datetime.datetime.now(),'diff_public_date':diff_public_date, 'public_date':public_date, 'publicdate_ids':[(0,False,{'diff_public_date':diff_public_date,'public_date':public_date,'public_date_cu':public_date_cu})]})
     
        
        update_gia = topic_dict['gia']
        gia_cu = search_link_obj.gia
#         if gia_cu != update_gia:
#             diff_gia = update_gia-gia_cu
#             update_dict.update({'gia':update_gia, 'diff_gia':diff_gia, 'gialines_ids':[(0,False,{'gia':update_gia,'gia_cu':gia_cu,'diff_gia':diff_gia})],'ngay_update_gia':local_a_native_time(datetime.datetime.now())})
        if update_dict:
            print (u'___________Update giá topic_index %s/%s- page_int %s - page_index %s/so_page %s'%(number_notice_dict['topic_index'],number_notice_dict['length_link_per_curent_page'],
                                                                        number_notice_dict['page_int'], number_notice_dict['page_index'],number_notice_dict['so_page']))
            search_link_obj.write(update_dict)
            number_notice_dict['update_link_number'] = number_notice_dict['update_link_number'] + 1
    else:
        update_dict.update({'public_date':public_date, 'public_datetime':public_datetime, 'url_id': page_info['url_id']})
        print (u'+++++++++Create topic_index %s/%s- page_int %s - page_index %s/so_page %s'%(number_notice_dict['topic_index'],number_notice_dict['length_link_per_curent_page'],
                                                                        number_notice_dict['page_int'], number_notice_dict['page_index'],number_notice_dict['so_page']))
        request_topic (self,link,update_dict, url_id, topic_dict)
        update_dict['link'] = link
        update_dict.update({'url_ids':[(4,url_id.id)]})
        self.env['bds.bds'].create(update_dict)
        number_notice_dict['create_link_number'] = number_notice_dict['create_link_number'] + 1    
    link_number = number_notice_dict.get("link_number",0) + 1
    number_notice_dict["link_number"] = link_number
    

        
        


                 




    

    

    
    
    
    
    
    
quan_huyen_data = '''<ul class="advance-options" style="min-width: 218px;">
<li vl="0" class="advance-options current" style="min-width: 186px;">--Chọn Quận/Huyện--</li><li vl="72" class="advance-options" style="min-width: 186px;">Bình Chánh</li><li vl="65" class="advance-options" style="min-width: 186px;">Bình Tân</li><li vl="66" class="advance-options" style="min-width: 186px;">Bình Thạnh</li><li vl="73" class="advance-options" style="min-width: 186px;">Cần Giờ</li><li vl="74" class="advance-options" style="min-width: 186px;">Củ Chi</li><li vl="67" class="advance-options" style="min-width: 186px;">Gò Vấp</li><li vl="75" class="advance-options" style="min-width: 186px;">Hóc Môn</li><li vl="76" class="advance-options" style="min-width: 186px;">Nhà Bè</li><li vl="68" class="advance-options" style="min-width: 186px;">Phú Nhuận</li><li vl="53" class="advance-options" style="min-width: 186px;">Quận 1</li><li vl="62" class="advance-options" style="min-width: 186px;">Quận 10</li><li vl="63" class="advance-options" style="min-width: 186px;">Quận 11</li><li vl="64" class="advance-options" style="min-width: 186px;">Quận 12</li><li vl="54" class="advance-options" style="min-width: 186px;">Quận 2</li><li vl="55" class="advance-options" style="min-width: 186px;">Quận 3</li><li vl="56" class="advance-options" style="min-width: 186px;">Quận 4</li><li vl="57" class="advance-options" style="min-width: 186px;">Quận 5</li><li vl="58" class="advance-options" style="min-width: 186px;">Quận 6</li><li vl="59" class="advance-options" style="min-width: 186px;">Quận 7</li><li vl="60" class="advance-options" style="min-width: 186px;">Quận 8</li><li vl="61" class="advance-options" style="min-width: 186px;">Quận 9</li><li vl="69" class="advance-options" style="min-width: 186px;">Tân Bình</li><li vl="70" class="advance-options" style="min-width: 186px;">Tân Phú</li><li vl="71" class="advance-options" style="min-width: 186px;">Thủ Đức</li>
</ul>'''
def import_quan_data(self):
    soup = BeautifulSoup(quan_huyen_data, 'html.parser')
    lis =  soup.select('li')
    for li in lis:
        quan =  li.get_text()
        name_without_quan = quan.replace(u'Quận ','')
        quan_unidecode = unidecode(quan).lower().replace(' ','-')
        g_or_c_ss(self,'bds.quan', {'name':quan}, {'name_unidecode':quan_unidecode,'name_without_quan':name_without_quan}, True)
    return len(lis)
def request_and_write_to_disk(url):
    url = 'https://muaban.net/nha-hem-ngo-ho-chi-minh-l59-c3202'
    my_html = request_html(url)
    file = open('E:\mydata\python_data\my_html.html','w')
    file.write(my_html)
    file.close()
def get_soup_from_file():
    file = open('E:\mydata\python_data\my_html.html','r')
    my_html = file.read()
    soup = BeautifulSoup(my_html, 'html.parser')
    return soup

    


        
if __name__== '__main__':
    request_and_write_to_disk()

    
