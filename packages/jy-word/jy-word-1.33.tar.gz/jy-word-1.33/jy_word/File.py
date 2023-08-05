# -*- coding: utf-8 -*-
# !/usr/bin/python
# Create Date 2017/9/29 0029
import os
import json
import xlrd
import chardet
from demo_xml import demo_xml
try:
    import csv
except:
    pass
__author__ = 'huohuo'
if __name__ == "__main__":
    pass


class File:

    def __init__(self, base_dir=''):
        self.__description__ = '文件相关， 包括读文件，写文件， 下载文件'
        self.base_dir = base_dir

    def read(self, file_name, sheet_name='', read_type='r', dict_name='', to_json=True, **kwargs):
        file_type = file_name.split('.')[-1]
        url = os.path.join(self.base_dir, dict_name, file_name)
        if os.path.exists(url) is False:
            print 'File not exists, %s. Please check.' % url
            return None
        if file_type in ['xlsx', 'xls']:
            data = xlrd.open_workbook(url)
            return data.sheet_by_name(sheet_name)

        f = open(url, read_type)
        text = f.read()
        f.close()
        if file_type in ['csv', 'tsv'] or 'sep' in kwargs:
            encoding = chardet.detect(text)['encoding']
            sep = ',' if file_type == 'csv' else '\t'
            if 'sep' in kwargs:
                sep = kwargs['sep']
            delimiter = {'delimiter': sep}
            f = open(url, read_type)
            csv.register_dialect('my_dialect', **delimiter)
            cons = csv.reader(f, 'my_dialect')
            items = []
            keys = next(cons)
            for c in cons:
                if to_json:
                    item = {}
                    for i in range(len(keys)):
                        item[keys[i]] = c[i].decode(encoding).encode('utf-8')
                    items.append(item)
                else:
                    items.append([x.decode(encoding).encode('utf-8') for x in c])
            csv.unregister_dialect('my_dialect')
            return items
        if file_type == 'json':
            return json.loads(text)
        return text

    def read_message(self, file_name, file_type='json', sheet_name='', read_type='r', developer='huohuo', message='success'):
        error_message = u'【开发者】：%s\n' % developer
        error_message += u'【文件类型】：%s\n' % file_type
        if file_type in ['xlsx', 'xls']:
            error_message += u'【sheet_name】：%s\n' % sheet_name
        error_message += u'【消息】：%s\n' % message
        error_message += u'【文件名】：\n%s\n' % file_name

    def write(self, file_name, data):
        file_type = file_name.split('.')[-1]
        url = os.path.join(self.base_dir, file_name)
        f = open(url, "w")
        if file_type == 'json':
            f.write(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False))
        else:
            f.write(data)
        f.close()

    def download(self, pkg_parts, file_name):
        temp_data = demo_xml.replace('<pkg:part id="pkg_parts"></pkg:part>', pkg_parts)
        self.write(file_name, temp_data)
