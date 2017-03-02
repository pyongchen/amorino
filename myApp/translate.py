# coding=utf-8
import random
import httplib
import urllib
import json
import md5

class Translator(object):
    def __init__(self):
        self.appid = '20161019000030439'
        self.secretKey = 'fa6A4Fv26nktaLCwVZR1'
        self.myurl = '/api/trans/vip/translate'
        self.langTable = {
            'zh': 'zh-CN',
            'en': 'en',
            'spa': 'spa'
        }
        self.lang = ['zh', 'en', 'spa']
        self.trans_list = [
            'kind', 'material', 'color', 'size', 'price'
        ]
        self.values = ''

    def set_value(self, text, lang_from, lang_to):
        lang_pair = self.langTable[lang_from] + \
                   "|" + self.langTable[lang_to]
        self.values = {
            'h1': 'zh-CN',
            'ie': 'UTF-8',
            'text': text,
            'langpair': lang_pair
        }

    def translate(self, text, lang_from, lang_to):
        text = str(text)
        self.set_value(text, lang_from, lang_to)
        salt = random.randint(32768, 65536)
        sign = self.appid + text + str(salt) + self.secretKey
        m1 = md5.new()
        m1.update(sign)
        sign = m1.hexdigest()
        self.myurl = self.myurl + '?appid=' + self.appid + '&q=' + urllib.quote(
            text) + '&from=' + str(lang_from) + '&to=' + str(lang_to) + '&salt=' + str(
            salt) + '&sign=' + str(sign)
        try:
            httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', self.myurl)

            # response是HTTPResponse对象
            response = httpClient.getresponse()
            result = response.read()
            print result
            return json.loads(result)['trans_result'][0]['dst']
        except Exception, e:
            return e

    def change_data(self, kind, zh_data):
        i = 0
        for text in zh_data:
            if not text or text == ' ':
                text = '无'
            info = self.trans_list[i]
            if info == 'price':
                kind['price'] = text
            else:
                text_en = self.translate(text, 'zh', 'en')
                text_es = self.translate(text, 'zh', 'spa')
                kind[info + '_' + 'zh'] = text
                kind[info + '_' + 'es'] = text_es
                kind[info + '_' + 'en'] = text_en
            i += 1
        # trans_info = trans_info[0:len(trans_info)-1]
        # ens_trans = self.translate(trans_info, 'zh', 'en')
        # ens = ens_trans.split(' / ')
        # ess_trans = self.translate(trans_info, 'zh', 'spa')
        # ess = ess_trans.split(' / ')
        # print ens
        # langs = {'zh': zh_data, 'spa': ess, 'en': ens}
        # i = 0
        # for info in self.trans_list:
        #     if info == 'price':
        #         kind[info] = zh_data[i]
        #     else:
        #         for lang in self.lang:
        #             if lang == 'spa':
        #                 kind[info + '_' + 'es'] = langs[lang][i]
        #             kind[info + '_' + lang] = langs[lang][i]
        #     i += 1


translator = Translator()
text = "光学眼镜"
r = translator.translate('   ', 'zh', 'en')
print r
# print r.split(' / ')
