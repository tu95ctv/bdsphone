# -*- coding: utf-8 -*-
from odoo.addons.bds.models.bds_tools  import  request_html,g_or_c_ss, get_or_create_user_cho_tot_batdongsan,g_or_c_chotot_quan
from bs4 import BeautifulSoup
import re
import datetime
############mua ban ############
def get_mobile_name_for_muaban(soup):
    try:
        mobile_and_name_soup = soup.select('div.ct-contact ')[0]
        mobile_soup = mobile_and_name_soup.select('div.price-name + div > b')[0]
        mobile = mobile_soup.get_text()
        name = mobile
    except IndexError:
        mobile =  None
        name= None
    return mobile,name
def get_muaban_vals_one_topic(self,update_dict,html,siteleech_id,only_return_price=False):
    def create_or_get_one_in_m2m_value(val):
            val = val.strip()
            if val:
                return g_or_c_ss(self,'bds.images',{'url':val})
    
    update_dict['data'] = html
    soup = BeautifulSoup(html, 'html.parser')
#     date = soup.select('span.detail-clock')[0].get_text()
#     date = date.strip()
#     print (date)
#     public_datetime = datetime.datetime.strptime(date,"%d/%m/%Y")
#     update_dict['public_datetime'] = public_datetime
    test = ''
    image_soup = soup.select('div.ct-image img')
    content_soup = soup.select('div.ct-body')
    update_dict['html']  = content_soup[0].get_text()
#     #print ('**image_soup',image_soup)
    images = []
    for i in image_soup:
        data_src = i.get('data-src',False)
        if data_src:
            images.append(data_src)
        
    if images:
        update_dict['present_image_link'] = images[0]  
        object_m2m_list = list(map(create_or_get_one_in_m2m_value, images))
        m2m_ids = list(map(lambda x:x.id, object_m2m_list))
        if m2m_ids:
            val = [(6, False, m2m_ids)]
            update_dict['images_ids'] = val
    self.test_1 = test
    gia_soup = soup.select('div.price-value span')
    
    
    try:
        gia =  gia_soup[0].get_text()
        gia = re.sub(u'\.|đ|\s', '',gia)
        gia = float(gia)
        gia = gia/1000000000.0
    except IndexError:
        gia = 0
        
        
        
    if only_return_price:
        return gia
    update_dict['gia'] = gia
    title = soup.select('div.cl-title > h1')[0].get_text()
    title = title.strip()
    update_dict['title']=title
    update_dict['siteleech_id'] = siteleech_id.id
   
    quan_soup = soup.select('span.detail-location')
    quan_txt =  quan_soup[0].get_text()
    quan_name =  quan_txt.split('-')[0].strip()
#     quan_name.replace(u'Quận ','')
    quan_id = g_or_c_chotot_quan(self,quan_name)
    update_dict['quan_id'] = quan_id
    mobile,name = get_mobile_name_for_muaban(soup)
    if mobile != None:
        user = get_or_create_user_cho_tot_batdongsan(self,mobile,name,siteleech_id.name)
        update_dict['user_name_poster']=name
        update_dict['phone_poster']=mobile
        update_dict['poster_id'] = user.id
############## end mua ban  ###########