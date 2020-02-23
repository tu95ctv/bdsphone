import json
from openerp.http import request
from odoo import fields
from datetime import datetime, timedelta
from odoo.exceptions import UserError
def do_if_function_key_wrapper(function_key):
    def do_if_function_key(func):
        def f_wrapper(self):
            if self.function_key ==function_key:
                func(self)
            else:
                pass
        return f_wrapper
    return do_if_function_key


