# coding=utf-8
import os
import random
import shutil

from myApp.manager.products_manager import productManager
from myApp.translate import translator


class AdminEditManager(object):
    def __init__(self):
        self.img_base_path = 'img/products_list/'

    @staticmethod
    def edit_home_text(request, part):
        p1 = request.POST['p1']
        p2 = request.POST['p2']
        p3 = request.POST['p3']
        productManager.edit_home_data('update', part, 'p1', p1)
        productManager.edit_home_data('update', part, 'p2', p2)
        productManager.edit_home_data('update', part, 'p3', p3)

    def edit_products(self, request, operate, type_, kind, id_, old_img):
        data = []
        if operate == 'update':
            for i in range(0, 5):
                data.append(request.POST['p' + str(i + 1)])
            images = self.uploaded_files(type_, kind, id_, request.FILES, 'update', old_img)
            productManager.update_products_data(type_, kind, id_, data)
            productManager.change_images('update', type_, kind, images, id_)
        elif operate == 'add':
            for i in range(0, 5):
                data.append(request.POST['p' + str(i + 1)])
            id_ = self.create_id()
            productManager.add_products_data(type_, kind, data, id_)
            images = self.uploaded_files(type_, kind, id_, request.FILES, 'add', '')
            productManager.change_images('add', type_, kind, images, '')
        else:
            delete_path = 'static/' + self.img_base_path + type_ + '/' + \
                       kind + '/' + kind + '_' + id_
            shutil.rmtree(delete_path)
            productManager.delete_products_data(type_, kind, id_)

    def add_products_kind(self, type_, kind_zh):
        kind_en = translator.translate(kind_zh, 'zh', 'en')
        kind_es = translator.translate(kind_zh, 'zh', 'es')
        kind_key = kind_en.replace(' ', '_')
        new_path = 'static/' + self.img_base_path + type_ + \
                   '/' + kind_key
        os.mkdir(new_path)
        productManager.add_kind(type_, kind_zh, kind_en, kind_es, kind_key)

    def delete_products_kind(self, type_, kind):
        old_path = 'static/' + self.img_base_path + type_ + '/' + kind
        shutil.rmtree(old_path)
        productManager.delete_kind(type_, kind)

    def add_products_type(self, type_):
        type_en = translator.translate(type_, 'zh', 'en')
        type_es = translator.translate(type_, 'zh', 'es')
        key = type_en.replace(' ', '_')
        new_path = 'static/' + self.img_base_path + key
        os.mkdir(new_path)
        productManager.add_type(type_, type_en, type_es, key)

    def delete_products_type(self, type_):
        old_path = 'static/' + self.img_base_path + type_
        shutil.rmtree(old_path)
        productManager.delete_type(type_)

    @staticmethod
    def list_top(type_, kind, index):
        productManager.list_top(type_, kind, index)

    def uploaded_files(self, type_, kind, id_, files, operate, old_img):
        images = {}
        path = kind + '_' + id_
        new_path = 'static/' + self.img_base_path + type_ + \
                   '/' + kind + '/' + path
        show_img = files.getlist('show_img')
        detail_imgs = files.getlist('detail_imgs')
        if operate == 'add':
            self.write_img(new_path, files, 'show_img', images, '')
            self.write_imgs(new_path, detail_imgs, 'detail_imgs', images)
        else:
            if len(show_img) != 0:
                if len(detail_imgs) != 0:
                    shutil.rmtree(new_path)
                    self.write_img(new_path, files, 'show_img', images, '')
                    self.write_imgs(new_path, detail_imgs, 'detail_imgs', images)
                else:
                    self.write_img(new_path, files, 'show_img', images, old_img)
            else:
                if len(detail_imgs) != 0:
                    old_path = new_path + '/' + old_img
                    f = open(old_path, 'r')
                    content = f.read()
                    shutil.rmtree(new_path)
                    os.mkdir(new_path)
                    self.write_imgs(new_path, detail_imgs, 'detail_imgs', images)
                    f = open(old_path, 'w')
                    f.write(content)
                    f.close()
                else:
                    pass
        return images

    @staticmethod
    def create_id():
        id_ = ''
        for i in range(0, 10):
            ran = chr(random.randint(97, 122))
            id_ += ran
        return id_

    @staticmethod
    def write_img(new_path, files, name, images, old_img):
        if not old_img:
            os.mkdir(new_path)
        else:
            os.remove(new_path + '/' + old_img)
        f = files[name]
        new_file = new_path + '/' + str(f)
        images[name] = new_file
        destination = open(new_file, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()

    @staticmethod
    def write_imgs(new_path, detail_imgs, name, images):
        other_images = []
        for count, x in enumerate(detail_imgs):
            new_file = new_path + '/' + str(x)
            other_images.append(new_file)
            destination = open(new_file, 'wb+')
            for chunk in x.chunks():
                destination.write(chunk)
            destination.close()
        images[name] = other_images


adminEditManager = AdminEditManager()
