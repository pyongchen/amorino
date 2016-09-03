# coding=utf-8

from member_manager import memberManager
from json_manager import jsonManager
from django.shortcuts import render_to_response
import json


class LoginManager(object):
    def __init__(self):
        self.admin_path = 'static/data/admin.json'
        self.users = []
        self.info = {
            'multiUser': {
                'zh': '此用户已经登录',
                'en': 'The User has login',
                'es': 'Este usuario ha firmado'
            },
            'errPass': {
                'zh': '密码不正确,请重新输入',
                'en': 'Password incorrect, please enter again',
                'es': 'El nombre de usuario o contraseña error'
            },
            "noExist": {
                'zh': '用户名不存在',
                'en': 'Username no exist',
                'es': 'El nombre de usuario no existe'
            }
        }
        self.result = {
            'success': '',
            'fail': ''
        }
        self.admin_name = ''
        self.admin_pass = ''
        self.get_admin_mess()
        self.admin = {
            'username': self.admin_name,
            'password': self.admin_pass,
            'info': '',
            'users': memberManager.get_members()
        }

    def login(self, request, flag):
        if flag == 'mobile':
            data = request.POST
        else:
            data = json.loads(request.body)
        if data.has_key('username'):
            username = data['username']
        else:
            username = ''
        if data.has_key('password'):
            password = data['password']
        else:
            password = ''
        if memberManager.exist(username) != 0:
            if memberManager.valid(username, password) == 1:
                if self.has_login(username) == 0:
                    self.users.append(username)
                    request.session['username'] = username
                    self.result['success'] = username
                    self.result['fail'] = ''
                else:
                    self.result['fail'] = self.info['multiUser']
                    self.result['success'] = ''
            else:
                self.result['fail'] = self.info['errPass']
                self.result['success'] = ''
        else:
            self.result['fail'] = self.info['noExist']
            self.result['success'] = ''
        return json.dumps(json.dumps(self.result))

    def mobile_login(self, request):
        self.login(request, 'mobile')
        print self.result['success']
        if self.result['success'] == '':
            return render_to_response('client/mobile/login.html', {
                'title': '登录',
                'info': self.result['fail']
            })
        else:
            return render_to_response('client/mobile/homepage.html', {
                'title': '登录',
            })

    def admin_login(self, request):
        admin = request.POST
        if admin.has_key('username'):
            username = admin['username']
        else:
            username = ''
        if admin.has_key('password'):
            password = admin['password']
        else:
            password = ''
        if username == self.admin['username'] and\
                password == self.admin['password']:
                    return self.admin
        else:
            return 0

    def admin_change(self, request):
        admin = request.POST
        if admin.has_key('username'):
            username = admin['username']
        else:
            username = ''
        if admin.has_key('password'):
            password = admin['password']
        else:
            password = ''
        self.admin['username'] = username
        self.admin['password'] = password
        admin = jsonManager.read_json(self.admin_path)
        admin['admin']['username'] = username
        admin['admin']['password'] = password
        jsonManager.write_json(self.admin_path, admin)

    def get_admin(self, info):
        self.admin['info'] = info
        return self.admin

    def log_out(self, username):
        if username in self.users:
            self.users.remove(username)

    def get_admin_mess(self):
        admin = jsonManager.read_json(self.admin_path)
        admin_name = admin['admin']['username']
        admin_pass = admin['admin']['password']
        self.admin_name = admin_name
        self.admin_pass = admin_pass

    def has_login(self, username):
        for user in self.users:
            if user == username:
                return 1
        return 0

loginManager = LoginManager()
