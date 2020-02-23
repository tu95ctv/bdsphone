# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class Statistics(models.Model):
    _name='setaction.statistics'
    def model_(self):
        active_model =   self._context.get('active_model')
        return active_model
    model = fields.Char(default=model_, readonly=True, store=True)
    
    def function_key_(self):
        active_model =  self._context.get('function_key') or self._context.get('active_model')
        return active_model
    function_key = fields.Char(default= function_key_, readonly=True,store=True)
    date_time = fields.Datetime(default=fields.Datetime.now)
    statistics_ids = fields.One2many('setaction.statisticslinestrans','statistics_id',compute='statistics_ids_',store=True)
    
    
    def statistics_ids_collect(self):
        return {}
    
    
    @api.depends('function_key')
    def statistics_ids_(self):
        picked_function = self.statistics_ids_collect()[self.function_key]
        statistics_ids = picked_function()
        self.statistics_ids = statistics_ids
        
        
        
class Statisticslines(models.TransientModel):
    _name = 'setaction.statisticslinestrans'
    
    statistics_id = fields.Many2one('downloadwizard.statistics')
    
    
    
    
    




    
    

        


