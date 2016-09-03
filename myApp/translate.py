# coding=utf-8
import re
import urllib
import urllib2


class Translator(object):
    def __init__(self):
        self.url = 'http://translate.google.cn/'
        self.browser = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)'
        self.langTable = {
            'zh': 'zh-CN',
            'en': 'en',
            'es': 'es'
        }
        self.lang = ['zh', 'en', 'es']
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
        self.set_value(text, lang_from, lang_to)
        data = urllib.urlencode(self.values)
        try:
            req = urllib2.Request(self.url, data)
            req.add_header('User-Agent', self.browser)
            response = urllib2.urlopen(req)
        except urllib2.URLError:
            print '翻译请求出问题,请等待'
        else:
            html = response.read()
            p = re.compile(r"(?<=TRANSLATED_TEXT=).*?;")
            m = p.search(html)
            result = m.group(0).strip(';')
            r = re.search(r"'(.*)'", result)
            return r.group(1)
        return ''

    def change_data(self, kind, zh_data):
        trans_info = ""
        for text in zh_data:
            text_ = '/' + text
            trans_info += text_
        trans_info = trans_info[0:len(trans_info)-1]
        ens_trans = self.translate(trans_info, 'zh', 'en')
        ens = ens_trans.split(' / ')
        ess_trans = self.translate(trans_info, 'zh', 'es')
        ess = ess_trans.split(' / ')
        print ens
        langs = {'zh': zh_data, 'es': ess, 'en': ens}
        i = 0
        for info in self.trans_list:
            if info == 'price':
                kind[info] = zh_data[i]
            else:
                for lang in self.lang:
                    kind[info + '_' + lang] = langs[lang][i]
            i += 1


translator = Translator()
# text = "以科学的精度衡量优雅"
# r = translator.translate(text, 'zh', 'en')
# print r
# print r.split(' / ')
