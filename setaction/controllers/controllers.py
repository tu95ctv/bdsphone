# -*- coding: utf-8 -*-
from odoo import http

# class ModuleTestmedia/sfCDrive/d4/duanMi/(http.Controller):
#     @http.route('/module_testmedia/sf__c__drive/d4/duan_mi//module_testmedia/sf__c__drive/d4/duan_mi//', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/module_testmedia/sf__c__drive/d4/duan_mi//module_testmedia/sf__c__drive/d4/duan_mi//objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('module_testmedia/sf__c__drive/d4/duan_mi/.listing', {
#             'root': '/module_testmedia/sf__c__drive/d4/duan_mi//module_testmedia/sf__c__drive/d4/duan_mi/',
#             'objects': http.request.env['module_testmedia/sf__c__drive/d4/duan_mi/.module_testmedia/sf__c__drive/d4/duan_mi/'].search([]),
#         })

#     @http.route('/module_testmedia/sf__c__drive/d4/duan_mi//module_testmedia/sf__c__drive/d4/duan_mi//objects/<model("module_testmedia/sf__c__drive/d4/duan_mi/.module_testmedia/sf__c__drive/d4/duan_mi/"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('module_testmedia/sf__c__drive/d4/duan_mi/.object', {
#             'object': obj
#         })