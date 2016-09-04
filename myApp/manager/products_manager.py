# coding=utf-8
import json
import os
from myApp.translate import translator


class ProductsManager(object):
    def __init__(self):
        self.home_data_path = 'static/data/home.json'
        self.home_img_path = 'img/home/'
        self.products_data_path = 'static/data/'
        self.products_img_path = 'img/products_list/'

    # part指首页的第几部分
    def edit_home_data(self, kind, part, key, value):
        data = self.read_json(self.home_data_path)
        if kind == 'update' or kind == 'insert':  # 跟新或插入(key, value)
            data[part][key] = value
        else:  # 删除(key, value)
            del data[part][key]
        self.write_json(self.home_data_path, data)

    # 增删首页第一部分的轮播图片
    def edit_home_first_images(self, kind, index, value):
        data = self.read_json(self.home_data_path)
        img_path = self.home_img_path + 'turns/' + value
        if kind == 'insert':
            data['first']['images'].append(img_path)
        else:
            del data['first']['images'][index]
        self.write_json(self.home_data_path, data)

    # 修改首页第二三部分的展示图片
    def change_home_data(self, part, value):
        data = self.read_json(self.home_data_path)
        img_path = self.home_img_path + part + '/' + value
        data[part]['image'] = img_path
        self.write_json(self.home_data_path, data)

    # 修改产品数据
    def update_products_data(self, type_, kind, id_, data):
        products_data_path = self.products_data_path + type_ + '.json'
        data_ = self.read_json(products_data_path)
        index = self.find_detail_by_id(id_, data_['details'][kind])
        translator.change_data(data_['details'][kind][int(index)], data)
        self.write_json(products_data_path, data_)

    # 添加产品数据
    def add_products_data(self, type_, kind, data, id_):
        products_data_path = self.products_data_path + type_ + '.json'
        data_ = self.read_json(products_data_path)
        new_data = {}
        translator.change_data(new_data, data)
        new_data['id'] = id_
        data_['details'][kind].insert(0, new_data)
        self.write_json(products_data_path, data_)

    # 添加细节图片
    def change_images(self, operate, type_, kind, images, id_):
        products_data_path = self.products_data_path + type_ + '.json'
        data_ = self.read_json(products_data_path)
        if operate == 'add':
            data_['details'][kind][0]['image'] = images['show_img']
            data_['details'][kind][0]['otherImages'] = images['detail_imgs']
        else:
            origin_index = self.find_detail_by_id(id_, data_['details'][kind])
            if images.has_key('show_img'):
                data_['details'][kind][origin_index]['image'] = images['show_img']
            if images.has_key('detail_imgs'):
                data_['details'][kind][origin_index]['otherImages'] = images['detail_imgs']
        self.write_json(products_data_path, data_)

    # 删除产品数据
    def delete_products_data(self, type_, kind, id_):
        products_data_path = self.products_data_path + type_ + '.json'
        data = self.read_json(products_data_path)
        delete_index = self.find_detail_by_id(id_, data['details'][kind])
        del data['details'][kind][int(delete_index)]
        self.write_json(products_data_path, data)

    # 删除产品款式
    def delete_kind(self, type_, kind):
        products_data_path = self.products_data_path + type_ + '.json'
        data = self.read_json(products_data_path)
        del data['details'][kind]
        for item in data['kinds']:
            if item['key'] == kind:
                data['kinds'].remove(item)
        self.write_json(products_data_path, data)

    # 添加产品款式
    def add_kind(self, type_, kind_zh, kind_en, kind_es, kind_key):
        products_data_path = self.products_data_path + type_ + '.json'
        data = self.read_json(products_data_path)
        newkind = {}
        newkind['es'] = kind_es
        newkind['zh'] = kind_zh
        newkind['key'] = kind_key
        newkind['en'] = kind_en
        data['kinds'].append(newkind)
        data['details'][kind_key] = []
        self.write_json(products_data_path, data)

    # 添加产品类型
    def add_type(self, type_zh, type_en, type_es, key):
        type_path = self.products_data_path + 'type.json'
        data = self.read_json(type_path)
        data['types'].append(key)
        self.write_json(type_path, data)

        f = open(self.products_data_path + key + '.json', 'w')
        f.write('{}')
        f.close()
        products_data_path = self.products_data_path + key + '.json'
        data = self.read_json(products_data_path)
        data['kinds'] = []
        name = {
            "zh": type_zh,
            "en": type_en,
            "es": type_es,
            "key": key
        }
        data['name'] = name
        data['details'] = {}
        self.write_json(products_data_path, data)

    # 删除产品类型
    def delete_type(self, type_):
        type_path = self.products_data_path + 'type.json'
        data = self.read_json(type_path)
        data['types'].remove(type_)
        self.write_json(type_path, data)
        os.remove(self.products_data_path + type_ + '.json')

    # 将某个产品置顶
    def list_top(self, type_, kind, index):
        products_data_path = self.products_data_path + type_ + '.json'
        data = self.read_json(products_data_path)
        flag = data['details'][kind][int(index)]
        del data['details'][kind][int(index)]
        data['details'][kind].insert(0, flag)
        self.write_json(products_data_path, data)

    @staticmethod
    def read_json(path):
        json_file = open(path, "r")
        data = json.load(json_file)
        json_file.close()
        return data

    @staticmethod
    def write_json(path, data):
        json_file = open(path, "w")
        json_file.write(json.dumps(data))
        json_file.close()

    @staticmethod
    def get_data():
        data = {}
        json_file = open('static/data/home.json', "r")
        home_data = json.load(json_file)
        data['home_data'] = home_data
        json_file.close()
        return data

    @staticmethod
    def find_detail_by_id(id_, details):
        index = 0
        for detail in details:
            if detail['id'] == id_:
                return index
            else:
                index += 1

productManager = ProductsManager()
