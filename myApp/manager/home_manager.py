import os
import shutil

from myApp.manager.json_manager import jsonManager
from myApp.translate import translator


class HomeManager(object):
    def __init__(self):
        self.home_path = 'static/data/home.json'
        self.img_path = 'static/img/home/'
        self.first_img_path = self.img_path + 'turns'
        self.parts = ['p1', 'p2', 'p3']

    def update(self, request, part):
        files = request.FILES
        if part == 'first':
            self.update_first(files)
        else:
            self.update_part(request, files, part)

    def update_first(self, files):
        data = jsonManager.read_json(self.home_path)
        imgs = files.getlist('firstImages')
        if len(imgs) != 0:
            shutil.rmtree(self.first_img_path)
            os.mkdir(self.first_img_path)
            data['first']['images'] = []
            for count, x in enumerate(imgs):
                new_file = self.first_img_path + '/' + str(x)
                data['first']['images'].append(new_file)
                destination = open(new_file, 'wb+')
                for chunk in x.chunks():
                    destination.write(chunk)
                destination.close()
        jsonManager.write_json(self.home_path, data)

    def update_part(self, request, files, part):
        data = jsonManager.read_json(self.home_path)
        self.translate_parts_data(part, request.POST, data)
        img = files.getlist('img')
        if len(img) != 0:
            img_path = self.img_path + part
            shutil.rmtree(img_path)
            os.mkdir(img_path)
            f = files['img']
            data[part]['image'] = img_path + '/' + str(f)
            new_file = img_path + '/' + str(f)
            destination = open(new_file, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
        jsonManager.write_json(self.home_path, data)

    def translate_parts_data(self, part, post, data):
        for p in self.parts:
            data[part][p + '_zh'] = post[p]
            data[part][p + '_en'] = translator.translate(post[p], 'zh', 'en')
            data[part][p + '_es'] = translator.translate(post[p], 'zh', 'es')

homeManager = HomeManager()
