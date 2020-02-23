 # -*- coding: utf-8 -*-
from odoo.addons.importexcel.models.model_dict_folder.tool_tao_instance import get_key
from odoo.osv import expression
import datetime
from odoo import  fields
from odoo.exceptions import UserError
from odoo.addons.downloadwizard.models.dl_models.dl_model  import wrap_center_vert_border_style
from odoo.tools.float_utils import float_compare, float_round
from odoo.addons.importexcel.models.model_dict_folder.tool_tao_instance import BreakRowException

CREATE_IN_M2X = False
def get_create_write_x2m (self,
                                search_dict,
                                write_dict ={},
                                MD = {},
                                exist_val=False,
                                setting= {},
                                check_file = False,
                                is_search = True,
                                is_write = True,
#                                 main_call = False,
                                x2m_fields = False,
                                needdata = None,
                                f_name_call = None
                                 ):
#     x2m_fields = MD.get('x2m_fields')
    if x2m_fields:
        x2m_field = x2m_fields[0]
        x2m_values = search_dict[x2m_field]
        len_x2m_vals = len(x2m_values)
#         try:
#             len_x2m_vals = len(x2m_values)
#         except TypeError:
#             len_x2m_vals = 1
    else:
        len_x2m_vals = 1
    instance_build_noti_dict = {}  
    for count_i, i in enumerate(range(0, len_x2m_vals)):
        if x2m_fields:
            x2m_obj = []
            x2m_searched_obj = []
            search_dict[x2m_field] = x2m_values[i] #
        obj, searched_obj, new_noti_dict = get_create_write(self, 
                                search_dict,
                                write_dict =write_dict,
                                MD = MD,
                                exist_val=exist_val,
                                setting = setting,
                                check_file = check_file,
                                is_search = is_search,
                                is_write = is_write,
                                needdata = needdata,
                                f_name_call = f_name_call,
                                is_x2m_fields =  bool(x2m_fields)
                                )
       
        for k,v in new_noti_dict.items():
            instance_build_noti_dict[k] = instance_build_noti_dict.get(k,0) + v
        if x2m_fields:
            x2m_obj.append(obj)
            x2m_searched_obj.append(searched_obj)
    if x2m_fields:
        obj = x2m_obj
        searched_obj = x2m_searched_obj
       
    if not check_file and not obj:
        raise UserError('not check_file and not obj')
        
    return obj, searched_obj, instance_build_noti_dict


def get_create_write(
                                self,
                                search_dict,
                                write_dict ={},
                                MD = {},
                                exist_val= None,
                                setting = {},
                                check_file=False,
                                is_search = True,
                                is_write = True,
#                                 main_call = False,
                                needdata = None, 
                                f_name_call = None,
                                is_x2m_fields = False
                                ):
    new_noti_dict = {} 
    model_name = MD.get('model')
    empty_object  = self.env[model_name]
    
# is_search_default_when_not_check_file = False    
#             is_search= check_file or (exist_val ==None or  func_check_if_excel_is_same_existence)
#             is_write = not check_file and (exist_val ==None or  st_is_allow_write_existence  )
    
    if is_search:
        searched_obj = search_handle(self, MD, search_dict, model_name, setting, needdata)
        new_noti_dict['search']=1
    else:
        searched_obj = empty_object
    
    return_obj =  exist_val if  exist_val != None else searched_obj
    if return_obj and len(return_obj) > 1:
        if MD.get('get_first_one',False):
            return_obj = return_obj[0]
        else:
            try:
                mapped_name = return_obj.mapped('name')
            except:
                mapped_name = return_obj
            raise UserError (u'len_return_obj > 1, mapped_name: %s,model_name: %s,search_dict:%s  '%(str(mapped_name),model_name, search_dict))
    
    if (exist_val ==None and return_obj  == empty_object ) and not check_file:
        create_obj = create_handle(self, search_dict, write_dict, MD, model_name, f_name_call, is_x2m_fields)
        return_obj = create_obj
        new_noti_dict['create'] =1
    elif return_obj and is_write  :
        write_handle(self, return_obj, MD, write_dict, new_noti_dict, f_name_call = f_name_call )
    return return_obj, searched_obj, new_noti_dict

def search_handle(self, model_dict, search_dict, model_name, setting, needdata):
    search_func = model_dict.get('search_func')
    if search_func:
        searched_obj = search_func(self, model_dict, setting, needdata)
    else:
        if search_dict :
            pass
        else:
            raise UserError(u'Không có search dict, model_name: %s-MD: %s'%(model_name, model_dict))
        if model_dict.get('inactive_include_search'):
            domain_not_active = ['|',('active','=',True),('active','=',False)]
        else:
            domain_not_active = []
        domain = []
        has_none_val_search_field = False
        for f_name in search_dict:
            field_attr = model_dict['fields'][f_name]
            val =  search_dict[f_name]
            f_name = get_key(field_attr, 'transfer_name') or f_name
            operator_search = field_attr.get('operator_search','=')
            tuple_in = (f_name, operator_search, val)
            domain.append(tuple_in)
        if not has_none_val_search_field:
            domain = expression.AND([domain_not_active, domain])
            searched_obj  = self.env[model_name].search(domain)
    return searched_obj
                
def create_handle(self, search_dict, write_dict, MD, model_name, f_name_call,is_x2m_fields):
    search_dict_new ={}
    context = MD.get('context',{})
    allow_create = MD.get('allow_create', True)
    if not allow_create:
        if getattr(self, 'BreakRowException_if_raise_allow_create'):
            raise BreakRowException(u'Model %s này với giá trị f_name_call:%s, name: "%s" chỉ được get chứ không được tạo'%(model_name, f_name_call,  MD['fields']['name']['val']))
        else:
            raise UserError(u'Model %s này với giá trị f_name_call:%s,  name: "%s" chỉ được get chứ không được tạo, hãy tạo tay hoặc chọn thuộc tính BreakRowException_if_raise_allow_create để bỏ qua thông báo này'%(model_name, f_name_call,  MD['fields']['name']['val']))
#     search_dict.update(write_dict)
    write_dict.update(search_dict)
    for f_name,val in write_dict.items():
        field_attr = MD['fields'][f_name]
        f_name = get_key(field_attr, 'transfer_name') or f_name
        delete_when_return_x2m_create_if_false = field_attr.get('delete_when_return_x2m_create_if_false',False)
        if not delete_when_return_x2m_create_if_false:
            
            search_dict_new[f_name]=val
    if is_x2m_fields and not CREATE_IN_M2X:
#         for i in search_dict:
#             delete_when_return_x2m_create_if_false = MD.get('delete_when_return_x2m_create_if_false',False)
#             if delete_when_return_x2m_create_if_false:
                
        return search_dict_new
        
    
    created_object = self.env[model_name].sudo().with_context(**context).create(search_dict_new)
    return_obj = created_object
    return return_obj

        
def write_handle(self, return_obj, MD, write_dict, new_noti_dict, f_name_call=False ):
    write_dict_new = {}
    writed_object = return_obj
    for key_f_name, val in write_dict.items():
        field_MD=  MD['fields'][key_f_name]
        if field_MD.get('val_goc') != False or field_MD.get('write_false', False):
            f_name = get_key(field_MD, 'transfer_name') or key_f_name
            is_write_this_field = field_MD['write_field']
            if  is_write_this_field :
                orm_field_val = getattr(writed_object, f_name)
                func_in_write_handle = field_MD.get('func_in_write_handle')
                if func_in_write_handle:
                    val = func_in_write_handle(orm_field_val,val)
                is_x2m = field_MD.get('x2m_fields', False)
                diff = check_diff_write_val_with_exist_obj(orm_field_val, val, field_MD, is_x2m)
                if diff:
                    if is_write_this_field:
                        write_dict_new[f_name] = val
    if write_dict_new:
        writed_object.write(write_dict_new)
        new_noti_dict['update'] = 1
        if f_name_call =='main_call' or MD.get('print_wite',False):
            print ('**write_dict_new:%s for obj:%s'%(write_dict_new, writed_object))
    else:#'not update'
        new_noti_dict['skipupdate'] = 1
            
  
     

  
  
def check_diff_write_val_with_exist_obj(orm_field_val, field_dict_val, field_MD, is_x2m):
    field_type = field_MD.get('field_type')
    is_write = False
    if is_x2m:
        pass
#     elif isinstance(orm_field_val, datetime.date):
#         converted_orm_val_to_dict_val = fields.Date.from_string(orm_field_val)
#     elif isinstance(orm_field_val, datetime.datetime):
#         converted_orm_val_to_dict_val = fields.Datetime.from_string(orm_field_val)
    else:
        try:
            converted_orm_val_to_dict_val = getattr(orm_field_val, 'id', orm_field_val)
            if converted_orm_val_to_dict_val == None: #recorderset.id ==None when recorder set = ()
                converted_orm_val_to_dict_val = False
        except:
            converted_orm_val_to_dict_val = orm_field_val
    
    if '2many' in field_type:
        is_write = True
#         is_write = False
#         if not all(field_MD['obj']):
#             is_write = True
#         else:
#             for field_dict_val_item in field_MD['obj']:
#                 is_write_item = field_dict_val_item not in orm_field_val
#                 is_write = is_write or is_write_item
    elif field_type=='float':
        is_write = float_compare(orm_field_val, field_dict_val, precision_rounding=0.01)# 1 la khac, 0 la giong
    else:
        is_write =  converted_orm_val_to_dict_val != field_dict_val
    return is_write
    
                
                

