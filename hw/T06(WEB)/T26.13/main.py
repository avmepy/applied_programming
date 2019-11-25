#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov

from time import sleep
from urllib.request import urlopen
from urllib.parse import urlencode, quote
import html.parser
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE




def getencoding(http_file):
    """Отримати кодування файлу http_file з Інтернет."""
    headers = http_file.getheaders()    # отримати заголовки файлу
#    print(headers)
    dct = dict(headers)                 # перетворити у словник
    content = dct.get('Content-Type', '')  # знайти 'Content-Type'
    mt = re.search(r'\bcharset=(?P<ENC>.+)\b', content)      # знайти кодування (після 'charset=' )
    if mt:
        enc = mt.group('ENC').lower().strip()  # виділити кодування
    elif 'html' in content:
        enc = 'utf-8'
    else:
        enc = None
    return enc


class ElleParser(html.parser.HTMLParser):
    """
    https://www.elle.ua/
    """
    def __init__(self, *args, **kwargs):
        html.parser.HTMLParser.__init__(self, *args, **kwargs)
        self._mentions = list()
        self._in_article = None

    def handle_starttag(self, tag, attrs):
        # print("STARTTAG", tag, "ATTRS", attrs)
        if tag == 'div' and ('class', 'zodiac-desc') in attrs:
            self._in_article = True

    def handle_endtag(self, tag):
        # print("ENDTAG", tag)
        if tag == 'div' and self._in_article:
            self._in_article = False

    def handle_data(self, data):
        # print('DATA', data)
        if self._in_article:

            self._mentions.append(data)

    def error(self, message):
        print(message)
        pass

    @property
    def get_mentions(self):
        return self._mentions


class Elle:
    FIND_URL = 'https://elle.ua/astro/{query}/'
    ENC = 'utf-8'

    def __init__(self, signs: list):
        self._signs = dict().fromkeys(signs, 0)

        for politician in signs:
            self._signs[politician] = self._find_mentions(politician)

    def _find_mentions(self, name):
        query = quote(name, encoding=Elle.ENC)
        mentions = None


        while True:
            try:
                html_page = urlopen(self.FIND_URL.format(query=query), context=ctx)
                if html_page.getcode() == 200:
                    break
                if html_page.getcode() == 404:
                    break
            except Exception as inst:
                print(inst)
                sleep(1)


        lnp = ElleParser()
        lnp.feed(str(html_page.read(), encoding=self.ENC))
        mentions = lnp.get_mentions
        res = ' '.join(mentions).replace('\n', '').strip()

        return res

    @property
    def mentions(self):
        return self._signs





if __name__ == '__main__':
    zodiack_sings = ["aquarius", "aries", "cancer", "virgo"]




    news = Elle(zodiack_sings)
    for k, v in news.mentions.items():
        print(f'==={k}===\n{v}\n\n')

