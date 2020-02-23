# -*- coding: utf-8 -*-
from odoo.addons.bds.models.bds_tools  import  request_html, g_or_c_ss,  get_or_create_user_cho_tot_batdongsan, g_or_c_chotot_quan
from bs4 import BeautifulSoup
import re
from unidecode import unidecode
import datetime
##Nh fetch_bds

import pytz
##############Cho tot###############

def create_cho_tot_page_link(url_input, page_int):
    repl = 'o=%s'%(20*(page_int-1))
    url_input = re.sub('o=\d+',repl,url_input)
    url = url_input +  '&page=' +str(page_int)
    return url

MAP_CHOTOT_DATE_TYPE_WITH_TIMEDELTA = {u'ngày':'days',u'tuần':'weeks',u'hôm qua':'days',u'giờ':'hours',u'phút':'minutes',u'giây':'seconds',u'năm':'days',u'tháng':'days'}

def convert_chotot_date_to_datetime(string):
    rs = re.search (r'(\d*?)\s?(ngày|tuần|hôm qua|giờ|phút|giây|năm|tháng)',string,re.I)
    rs1 =rs.group(1)
    rs2 =rs.group(2)
    if rs1=='':
        rs1 =1
    rs1 = int (rs1)
    if rs2==u'tháng':
        rs1 = rs1*365/12
    elif rs2==u'năm':
        rs1 = rs1*365
    rs2 = MAP_CHOTOT_DATE_TYPE_WITH_TIMEDELTA[rs2]
    dt = datetime.datetime.now() - datetime.timedelta(**{rs2:rs1})
    return dt



def gmt_7_a_native_time(datetime_input):
    local = pytz.timezone("Etc/GMT-7")
    local_dt = local.localize(datetime_input, is_dst=None)
    return local_dt



def convert_chotot_price(html):
    try:
        price = float(html['price'])/1000000000
        price_trieu = float(html['price'])/1000000
    except KeyError:
        price = 0
        price_trieu = 0
    return price, price_trieu
    
def get_topic_chotot(self,update_dict, topic_html, siteleech_id, only_return_price = False):
    #mục đích thêm các thông số vào update_dict
    def create_or_get_one_in_m2m_value(val):
            val = val.strip()
            if val:
                return g_or_c_ss(self,'bds.images',{'url':val})
            
    html = topic_html['ad']
    self.test_html = html
    
    
    date = html['date']
#     native_dt = convert_chotot_date_to_datetime(date)
#     update_dict['public_datetime'] = native_dt
    
    self.test_url = date



    price, price_trieu = convert_chotot_price(html)
    update_dict['date_text'] = date
    update_dict['siteleech_id'] = siteleech_id.id
    
    if only_return_price:
        return price
    images = html.get('images',[])
    if images:
        update_dict['present_image_link'] = images[0]  
        object_m2m_list = list(map(create_or_get_one_in_m2m_value, images))
        m2m_ids = list(map(lambda x:x.id, object_m2m_list))
        ###print '**m2m_ids**',m2m_ids
        if m2m_ids:
            val = [(6, False, m2m_ids)]
            update_dict['images_ids'] = val
    try:
        address = html['address']
        update_dict['address'] = address
    except KeyError:
        pass
    
    try:
        quan = topic_html['ad_params']['area']['value']
        rs = g_or_c_chotot_quan(self,quan)
        update_dict['quan_id'] = rs
    except KeyError:
        pass
    update_dict['gia'] = price
    update_dict['gia_trieu'] = price_trieu
    mobile,name = get_mobile_name_cho_tot(html)
    user = get_or_create_user_cho_tot_batdongsan(self,mobile,name ,siteleech_id.name)
    update_dict['user_name_poster']=name
    update_dict['phone_poster']=mobile
    update_dict['poster_id'] = user.id
    try:
        update_dict['html'] = html['body']
    except KeyError:
        pass
    
    update_dict['area']=html.get('size',0)
    update_dict['title']=html['subject']
    
    
def local_a_native_time(datetime_input):
    local = pytz.timezone("Etc/GMT-7")
    local_dt = local.localize(datetime_input, is_dst=None)
    utc_dt = local_dt.astimezone (pytz.utc)
    return utc_dt#utc_dt

def get_mobile_name_cho_tot(html):
    mobile = html['phone']
    name = html['account_name']
    return mobile,name


# def get_date_cho_tot_old(string):  
#     try:
#         ###print 'ngay dang from cho tot',string
#         if u'hôm nay' in string:
#             new = string.replace(u'hôm nay',datetime.date.today().strftime('%d/%m/%Y'))
#         elif u'hôm qua' in string:
#             hom_qua_date = datetime.date.today() -  datetime.timedelta(days=1)
#             new = string.replace(u'hôm qua',hom_qua_date.strftime('%d/%m/%Y'))
#         else:
#             new=string.replace(u'ngày ','').replace(u' tháng ','/').replace(' ','/2017 ')
#         new_date =  datetime.datetime.strptime(new,'%d/%m/%Y %H:%M')     
#         return local_a_native_time(new_date)
#     except:
#         return False
# 
# 
# 
# def get_date_cho_tot(string):  
#     dt = convert_chotot_date_to_datetime(string)
#     return local_a_native_time(dt)





################# cho tot  ##################

