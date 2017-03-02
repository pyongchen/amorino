# coding=utf-8
import json
import os

from member_manager import memberManager
from myApp.manager.products_manager import productManager
from login_manager import loginManager


class ResponseDataManager(object):
    def __init__(self):
        self.frame_path = 'static/data/frame.json'
        self.home_path = 'static/data/home.json'
        self.base_info_path = 'static/data/base.json'
        self.types_info_path = 'static/data/type.json'
        self.admin_collect_path = 'static/data/collects.json'
        self.user_collect_path = 'static/data/collects/'
        self.data = {
            "products": {},
            "collects": {},
            "users": {}
        }
        self.type_name = []
        self.types_num = 0
        self.data_list = {
            'admin_username': '',
            'users': '',
            'data': '',
            'info': '',
            'documents': '',
            'collect': ''
        }

    def frame_data(self):
        js = open(self.frame_path, 'r')
        data = json.load(js)
        return json.dumps(data)

    def base_info(self):
        js = open(self.base_info_path, 'r')
        data = json.load(js)
        return json.dumps(data)

    def home_data(self):
        js = open(self.home_path, 'r')
        data = json.load(js)
        return json.dumps(data)

    def get_type_path(self):
        js = open(self.types_info_path, 'r')
        data = json.load(js)
        self.types_num = len(data['types'])
        for i in range(0, self.types_num):
            self.type_name.append(data['types'][i])

    def products_data(self):
        self.type_name = []
        self.get_type_path()
        self.data['products'] = {}
        for name in self.type_name:
            path = 'static/data/' + name + '.json'
            print path
            js = open(path, "r")
            data_ = json.load(js)
            js.close()
            self.data['products'][name] = data_

    def user_data(self):
        self.products_data()
        return json.dumps(self.data)

    def admin_data(self):
        self.users()
        self.products_data()
        self.get_admin_collect_data()
        return json.dumps(self.data)

    def user_collect_data(self, request):
        username = request.session['username']
        data_path = self.user_collect_path + username + '.json'
        if not os.path.exists(data_path):
            f = open(data_path, 'w')
            f.write('{"user":[]}')
            f.close()
        js = open(data_path, "r")
        data_ = json.load(js)
        js.close()
        return json.dumps(data_)

    def get_admin_collect_data(self):
        js = open(self.admin_collect_path, "r")
        data_ = json.load(js)
        js.close()
        self.data['collects'] = data_

    def users(self):
        self.data['users'] = memberManager.get_members()

responseDataManager = ResponseDataManager()
