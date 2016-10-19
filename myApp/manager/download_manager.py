import zipstream
import os
import shutil
from django.http import StreamingHttpResponse


class DownloadManager(object):
    def __init__(self):
        self.source_path = ''
        self.new_path = ''

    def put_images_in_other_dic(self, new_path, source_path):
        self.new_path = new_path
        if not os.path.exists(new_path):
            os.mkdir(new_path)
        else:
            shutil.rmtree(new_path)
            os.mkdir(new_path)
        for root, dirs, files in os.walk(source_path):
            files_list = files
            for file_ in files_list:
                f = open(root + '/' + file_)
                data = f.read()
                new_file = open(new_path + '/' + file_, 'w')
                new_file.write(data)
                new_file.close()

    def create_zipfile(self):
        z = zipstream.ZipFile(mode='w')
        for root, dirs, files in os.walk(self.new_path):
            files_list = files
            for file_ in files_list:
                data = open(root + '/' + file_)
                z.write(data.name)
        response = StreamingHttpResponse(z)
        response['Content-Disposition'] = 'attachment;' \
                                          'filename = {}'.format(self.new_path + '.zip')
        return response

    def download(self, source_path):
        new_path = 'images'
        self.put_images_in_other_dic(new_path, source_path)
        response = self.create_zipfile()
        return response

downloadManager = DownloadManager()
