# -*- coding: utf-8 -*-
import re
# rhtml = '23a/23a '

rhtml= 'bán nhà 11 phan van tri'
rs = re.search('(bán nhà |số |mặt tiền |mt |địa chỉ |đc |dc )([1-9]\d{0,3}[a-h]{0,1} (?!mặt|tầng|lầu|tỷ)[\w\s/]{,30})',rhtml,re.I)
# rs = re.search('(?<!\d)[1-9]\d{0,3}[\D]{5,}[\W\S]', rhtml)
# rs = re.search('(?<!\d)[1-9]\d{0,3} [\w\s/]{,30}', rhtml) 
# rs = re.search('(?<!(giá |nhà |các ))(?<!(, |\. ))(?<!(\w|,|\.))[1-9]\d{0,3}[a-h]{0,1} (?!(tầng|lửng|lầu|trệt|x\d|x \d))[\w\s/]{,30}', rhtml,re.I)
print (rs.group(0))