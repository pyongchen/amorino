import json
import os
import datetime
import random


class CollectManager(object):
    def __init__(self):
        self.admin_path = 'static/data/collects.json'
        self.user_path = 'static/data/collects/'

    def operation(self, data, operate, username):
        if operate == 'add':
            self.add_data(data, username)
        elif operate == 'delete':
            self.delete_data(data, username)
        else:
            self.update_data(data, username)

    def add_data(self, data, username):
        info = dict()
        info['status'] = 'edit'
        info['member'] = username
        info['product'] = data['detail']
        info['number'] = data['number']
        info['message'] = data['message']
        info['id'] = random.randint(1, 99999999)
        info['date'] = str(datetime.datetime.now())[:16]
        self.add_user_data(username, info)
        self.add_admin_data(info)

    def delete_data(self, data, username):
        user_path = self.user_path + username + '.json'
        data_ = self.read_json(user_path)
        id_ = int(data['id'])
        for each in data_['user']:
            if each['id'] == id_:
                data_['user'].remove(each)
                pass
        self.write_json(user_path, data_)
        data_ = self.read_json(self.admin_path)
        for each in data_['admin']:
            if each['member'] == username and each['id'] == id_:
                data_['admin'].remove(each)
                pass
        self.write_json(self.admin_path, data_)

    def add_user(self, username):
        user_path = self.user_path + username + '.json'
        f = open(user_path, 'w')
        f.write('{"user":[]}')
        f.close()

    def delete_user(self, username):
        user_path = self.user_path + username + '.json'
        os.remove(user_path)
        data_ = self.read_json(self.admin_path)
        deletes = []
        for each in data_['admin']:
            if each['member'] == username:
                deletes.append(each)
        for delete in deletes:
            data_['admin'].remove(delete)
        self.write_json(self.admin_path, data_)

    def update_data(self, data, username):
        user_path = self.user_path + username + '.json'
        data_ = self.read_json(user_path)
        id_ = int(data['id'])
        update_index = 0
        for each in data_['user']:
            if each['id'] == id_:
                data_['user'][update_index]['message'] = data['message']
                data_['user'][update_index]['number'] = data['number']
                data_['user'][update_index]['date'] = str(datetime.datetime.now())[:16]
                pass
            else:
                update_index += 1
        self.write_json(user_path, data_)
        data_ = self.read_json(self.admin_path)
        admin_index = 0
        for each in data_['admin']:
            if each['member'] == username and each['id'] == id_:
                data_['admin'][admin_index]['message'] = data['message']
                data_['admin'][admin_index]['number'] = data['number']
                data_['admin'][admin_index]['date'] = str(datetime.datetime.now())[:16]
                pass
            else:
                admin_index += 1
        self.write_json(self.admin_path, data_)

    def add_user_data(self, username, data):
        user_path = self.user_path + username + '.json'
        data_ = self.read_json(user_path)
        data_['user'].insert(0, data)
        self.write_json(user_path, data_)

    def add_admin_data(self, data):
        data_ = self.read_json(self.admin_path)
        data_['admin'].insert(0, data)
        self.write_json(self.admin_path, data_)

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


collectManager = CollectManager()
