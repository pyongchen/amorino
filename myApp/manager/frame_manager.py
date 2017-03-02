# coding=utf-8

import os
import shutil

from myApp.manager.json_manager import jsonManager
from myApp.translate import translator


class FrameManager(object):
    def __init__(self):
        self.data_path = 'static/data/frame.json'
        self.img_path = 'static/img/frame/'

    def update(self, request):
        self.update_data(request)
        self.update_img(request)

    def update_data(self, request):
        nav = request.POST['nav']
        address_zh = request.POST['address']
        phone = request.POST['phone']
        weChat = request.POST['weChat']
        other = request.POST['other']
        data = jsonManager.read_json(self.data_path)
        data['nav'] = nav
        data['address_zh'] = address_zh
        en = translator.translate(address_zh, 'zh', 'en')
        es = translator.translate(address_zh, 'zh', 'spa')
        files = request.FILES
        img = files.getlist('bottom_img')
        if len(img) != 0:
            f = files['bottom_img']
            data['image'] = self.img_path + str(f)
        data['address_en'] = en
        data['address_es'] = es
        data['phone'] = phone
        data['weChat'] = weChat
        data['other'] = other
        jsonManager.write_json(self.data_path, data)

    def update_img(self, request):
        files = request.FILES
        img = files.getlist('bottom_img')
        if len(img) != 0:
            f = files['bottom_img']
            new_file = self.img_path + str(f)
            shutil.rmtree(self.img_path)
            os.mkdir(self.img_path)
            destination = open(new_file, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()

frameManager = FrameManager()
