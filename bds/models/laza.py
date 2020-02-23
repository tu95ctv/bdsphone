# -*- coding: utf-8 -*-
from odoo.addons.bds.models.bds_tools  import  request_html,g_or_c_ss
from bs4 import BeautifulSoup
import re
from unidecode import unidecode
import datetime

def get_link_on_one_page_laz(self,page_url):
    html = request_html(page_url)
    ##print 'html a page',html
    self.html_lazada = html
    soup = BeautifulSoup(html, 'html.parser')
    links_per_page = []
    title_soups = soup.select("div.c-product-card__description  a")
    ##print 'title_soups',title_soups
    for a in title_soups:
        ###print 'link hehe',a
        l =a['href']
        title = a.get_text().strip()
        ###print 'title',title
        links_per_page.append((l,title))
    
    return links_per_page
def send_mail(Subject,body):
    pass
#     body = unidecode(body)
#     Subject = unidecode(Subject)
#     fromaddr = 'nguyenductu@gmail.com'
#     toaddrs  = 'nguyenductu@gmail.com'
# #         msg = 'Why,Oh why fffffffffffform !'
#     
#     msg = MIMEMultipart()
#     msg['From'] = fromaddr
#     msg['To'] = toaddrs
#     msg['Subject'] =Subject# "SUBJECT OF THE MAIL"
#      
#     body = body#"YOUR MESSAGE HERE"
#     msg.attach(MIMEText(body, 'plain'))
#     text = msg.as_string()
# 
#     username = 'tunguyen19771@gmail.com'
#     password = 'Tu87cucgach'
#     server = smtplib.SMTP('smtp.gmail.com:587')
#     server.starttls()
#     server.login(username,password)
#     server.sendmail(fromaddr, toaddrs, text)
#     server.quit()
    ###print 'dont'

def detect_iphone_type(self,string):
    try:
        rs = re.search(r'iphone 8 plus|iphone 8|iphone X',string,re.I)
        name_cate =  rs.group(0)
        name_cate = name_cate.lower()
    except:
        name_cate = False
    try:
        rs = re.search(r'256|64',string,re.I)
        dung_luong =  rs.group(0)
    except:
        dung_luong = False
    
    try:
        rs = re.search(r'Chính Thức|Nhập Khẩu',string,re.I)
        nhap_khau_hay_chinh_thuc =  rs.group(0).lower()
    except:
        nhap_khau_hay_chinh_thuc = False
        
    ip_type = g_or_c_ss(self,'iphonetype', {'name_cate':name_cate,'dung_luong':dung_luong,'nhap_khau_hay_chinh_thuc':nhap_khau_hay_chinh_thuc})
    return ip_type

def check_bien_dong(find_last_item,compare_dict):
                list_bien_dong = []
                noi_dung_bien_dong_dict = {}
                for k,v in compare_dict.iteritems():
                    val_of_last_item = getattr(find_last_item, k)
                    if val_of_last_item != v:
                        list_bien_dong.append(k)
                        if k == 'gia':
                            delta = v - val_of_last_item
                            if delta > 0 :
                                tang_hay_giam_str = u'Tăng'
                            else:
                                tang_hay_giam_str = u'Giảm'
                            noi_dung_bien_dong_dict[k]= u'giá cũ:%s,giá mới%s,%s:%s'%(val_of_last_item,v,tang_hay_giam_str,abs(delta))
                        else:
                            noi_dung_bien_dong_dict[k]= u'%s--->%s'%(val_of_last_item,v)
                    else:
                        pass
                        ###print '**= nhau',k,val_of_last_item,val_of_last_item
                if list_bien_dong:
                    return (True,list_bien_dong,noi_dung_bien_dong_dict)
                else:
                    return (False,list_bien_dong,noi_dung_bien_dong_dict)
def trich_xuat_so_luong(so_luong):
    if u'hết' in so_luong:
        easy_so_luong = 0
    elif so_luong:
        rs =  re.search('\d+',so_luong)
        if rs:
            easy_so_luong = int(rs.group(0))
    else:
        easy_so_luong = -1
    return easy_so_luong
    
def fetch_lazada(self):
    ##print 'lazada'
    page_url = self.lazada_url
#     html = request_html(page_url)
#     soup = BeautifulSoup(html, 'html.parser')
#     links_per_page = []
#     title_soups = soup.select("div.c-product-card__description  a")
#     for a in title_soups:
#         ###print 'link hehe',a
#         l =a['href']
#         links_per_page.append(l)

    links_per_page = get_link_on_one_page_laz(self,page_url)
    ###print 'links_per_page',links_per_page
    test_page = []
    noti_dict = {}
    count = 0 
    len_links_per_page = len(links_per_page)
    for thread_link,title in links_per_page:
#     for thread_link in links_per_page:
        count +=1
        ##print 'fetch %s/%s'%(count,len_links_per_page)
        test_ones = []
        compare_dict = {}
        write_dict = {}
        link = 'https://www.lazada.vn' +  thread_link
        ###print '***thread_link**',link
        write_dict['title'] = title
        write_dict['link'] = link
        ###print '**tt**',title
        
        html = request_html(link)
        soup = BeautifulSoup(html, 'html.parser')
        gia = soup.select("span#special_price_box")[0].get_text()
        gia = gia.replace('.','')
        gia = float(gia)
        ###print 'gia',gia
        compare_dict['gia'] = gia
        write_dict['gia'] = gia
        test_ones.append(unicode(gia))
        so_luong = soup.select("span#product-option-stock-number")[0].get_text().strip()
        so_luong = trich_xuat_so_luong(so_luong)
        compare_dict['so_luong'] = so_luong
        write_dict['so_luong'] = so_luong
        duoc_ban_boi = soup.select(".basic-info__name")[0].get_text().strip()
        write_dict['duoc_ban_boi'] = duoc_ban_boi
        rs = re.search('(\d+)\.html',link)
        topic_id = rs.group(1)
        write_dict['topic_id'] = topic_id
        ipt_id = detect_iphone_type(self,title)
        original_item = self.env['dienthoai'].search([('topic_id','ilike',topic_id)],order = "create_date asc",limit=1)
        is_bien_dong = False
        if original_item:
            original_item = original_item[0]
            find_last_item = self.env['dienthoai'].search([('topic_id','ilike',topic_id)],order = "create_date desc",limit=1)[0]
            is_bien_dong,list_bien_dong,noi_dung_bien_dong_dict = check_bien_dong(find_last_item,compare_dict)
        if not original_item or  (original_item and  is_bien_dong) :
            object = self.env['dienthoai'].create(write_dict)
#             mail_body = u'link: %s \n gia: %s so luong: %s'%(link,gia,unidecode(so_luong))
#             send_mail(mail_body,mail_body)
            object.iphonetype_id = ipt_id
            if not original_item:
                mail_body = u'Create sp:%s, gia %s, so luong: %s, link: %s \n: '% (object.iphonetype_id.name,gia,so_luong,link)
                send_mail(mail_body,mail_body)
            if  original_item and  is_bien_dong:
#                     if 'gia' in list_bien_dong:
#                         mail_body = u' so luong: %s link: %s \n gia %s: '%(gia,unidecode(so_luong),link)
#                         send_mail(mail_body,mail_body)
                    object.write({'original_itself_id':original_item.id,'is_bien_dong_item':True,'noi_dung_bien_dong':noi_dung_bien_dong_dict})
                    original_item.gia_hien_thoi = gia
                    original_item.noi_dung_bien_dong = noi_dung_bien_dong_dict
                    if 'so_luong' in list_bien_dong:
                        original_item.so_luong_hien_thoi = so_luong
                    mail_body = u'%s,link%s'%(noi_dung_bien_dong_dict,link)
                    send_mail(mail_body,mail_body)

                        
        test_one =  u'|'.join(test_ones)
        test_page.append(test_one)
    self.html_lazada_thread_gia = u'\n'.join(test_page)
    self.test_lazada = noti_dict
