# coding=utf-8

import json

# import sqlite3

from collect_manager import collectManager
from json_manager import jsonManager


# 会员管理
class MemberManager(object):
    def __init__(self):
        self.users_path = 'static/data/users.json'
        self.users = []
        self.get_user()
        self.infos = {
            "err": "用户名或密码不能为空",
            'exist': "注册用户名已存在",
            'noExist': "删除的用户名不存在",
            'addSuccess': "注册成功",
            'deleteSuccess': "删除成功"
        }
        self.result = {
            "info": "",
            "users": ""
        }

    def get_user(self):
        data = jsonManager.read_json(self.users_path)
        for user in data['users']:
            self.users.append(user)

    def operate(self, request, operation):
        if operation == 'add':
            self.result['info'] = self.add_user(request)
        else:
            self.result['info'] = self.delete_user(request)
        self.result['users'] = self.users
        return json.dumps(self.result)

    def add_user(self, request):
        username = request['username']
        password = request['password']
        if username == '' or password == '':
            return self.infos['err']
        if self.exist(username):
            return self.infos['exist']
        user = {
            'username': username,
            'password': password
        }
        data = jsonManager.read_json(self.users_path)
        data['users'].append(user)
        jsonManager.write_json(self.users_path, data)
        self.users = data['users']
        collectManager.add_user(username)
        return self.infos['addSuccess']

    def delete_user(self, request):
        username = request['username']
        if self.exist(username) == 0:
            return self.infos['noExist']
        data = jsonManager.read_json(self.users_path)
        for user in data['users']:
            if user['username'] == username:
                data['users'].remove(user)
                pass
        jsonManager.write_json(self.users_path, data)
        self.users = data['users']
        collectManager.delete_user(username)
        return self.infos['deleteSuccess']

    def exist(self, username):
        for user in self.users:
            if user['username'] == username:
                return 1
        return 0

    def valid(self, username, password):
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                return 1
        return 0

    def get_members(self):
        return self.users

memberManager = MemberManager()
