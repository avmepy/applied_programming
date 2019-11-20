#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov

from time import sleep
from urllib.request import urlopen
from urllib.parse import urlencode, quote
import html.parser
import datetime
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


P_DATE_LIGA = r'\d{2}\.\d{2}\.\d{2}'
P_DATE_PRAVDA = r'\d{2}\.\d{2}\.\d{4}'
P_ENC = r'\bcharset=(?P<ENC>.+)\b'


def getencoding(http_file):
    """Отримати кодування файлу http_file з Інтернет."""
    headers = http_file.getheaders()    # отримати заголовки файлу
#    print(headers)
    dct = dict(headers)                 # перетворити у словник
    content = dct.get('Content-Type', '')  # знайти 'Content-Type'
    mt = re.search(P_ENC, content)      # знайти кодування (після 'charset=' )
    if mt:
        enc = mt.group('ENC').lower().strip()  # виділити кодування
    elif 'html' in content:
        enc = 'utf-8'
    else:
        enc = None
    return enc


class LigaNetParser(html.parser.HTMLParser):
    """
    https://www.liga.net/
    """
    def __init__(self, *args, **kwargs):
        html.parser.HTMLParser.__init__(self, *args, **kwargs)
        self._mentions = list()
        self._in_article = None

    def handle_starttag(self, tag, attrs):
        # print("STARTTAG", tag, "ATTRS", attrs)
        if tag == 'div' and ('class', 'news-nth-time') in attrs:
            self._in_article = True

    def handle_endtag(self, tag):
        # print("ENDTAG", tag)
        if tag == 'div' and self._in_article:
            self._in_article = False

    def handle_data(self, data):
        # print('DATA', data)
        if self._in_article:
            if re.match(P_DATE_LIGA, data):
                self._mentions.append(data[:8])

    def error(self, message):
        print(message)
        pass

    @property
    def get_mentions(self):
        return self._mentions


class LigaNet:
    FIND_URL = "https://www.liga.net/search/result/page/{page}/q/{query}"
    ENC = 'utf-8'

    def __init__(self, from_date: datetime.datetime, to_date: datetime.datetime, politics: list):
        self._from_date = from_date
        self._to_date = to_date
        self._politics = dict().fromkeys(politics, 0)

        for politician in politics:
            self._politics[politician] = self._find_mentions(politician)

    def _find_mentions(self, name):
        params = {'search': name}
        query = quote(name, encoding=LigaNet.ENC)
        page_num = 1
        mention_number = 0

        flag = True
        while flag:
            while True:
                try:
                    # print("Trying to open..")
                    html_page = urlopen(self.FIND_URL.format(page=page_num, query=query), context=ctx)
                    if html_page.getcode() == 200:
                        break
                    if html_page.getcode() == 404:
                        flag = False
                        break
                except Exception as inst:
                    print(inst)
                    sleep(1)

            if not flag:
                break

            # print('Opened!')
            lnp = LigaNetParser()
            lnp.feed(str(html_page.read(), encoding=self.ENC))
            mentions = lnp.get_mentions
            for mention in mentions:
                mention_date = datetime.datetime.strptime(mention, '%d.%m.%y')
                if self._from_date <= mention_date <= self._to_date:
                    mention_number += 1
                elif mention_date < self._from_date:
                    flag = False
            page_num += 1

            # print(name, mention_number)

        return mention_number

    @property
    def mentions(self):
        """
        :return: dict {POLITIC_NAME: NUMBER_OF_MENTIONS}
        """
        return self._politics


class PravdaNewsParser(html.parser.HTMLParser):
    """
    https://www.pravda.com.ua/rus/archives/date_05022014/
    """
    def __init__(self, *args, **kwargs):
        html.parser.HTMLParser.__init__(self, *args, **kwargs)
        self._mentions = list()
        self._in_article = None

    def handle_starttag(self, tag, attrs):
        # print("STARTTAG", tag, "ATTRS", attrs)
        if tag == 'div' and attrs == [('class', 'article__date')]:
            self._in_article = True

    def handle_endtag(self, tag):
        # print("ENDTAG", tag)
        if tag == 'div' and self._in_article:
            self._in_article = False

    def handle_data(self, data):
        # print('DATA', data)
        if self._in_article:
            if re.match(P_DATE_PRAVDA, data):
                self._mentions.append(data[:10])

    def error(self, message):
        print(message)
        pass

    @property
    def get_mentions(self):
        return self._mentions


class PravdaNews:
    FIND_URL = "https://www.pravda.com.ua/search/page_{page}/?{query}"
    ENC = 'windows-1251'

    def __init__(self, from_date: datetime.datetime, to_date: datetime.datetime, politics: list):
        self._from_date = from_date
        self._to_date = to_date
        self._politics = dict().fromkeys(politics, 0)

        for politician in politics:
            self._politics[politician] = self._find_mentions(politician)

    def _find_mentions(self, name):
        params = {'search': name}
        query = urlencode(params, encoding=PravdaNews.ENC)
        page_num = 1
        mention_number = 0

        flag = True
        while flag:
            while True:
                try:
                    # print("Trying to open..")
                    html_page = urlopen(self.FIND_URL.format(page=page_num, query=query), context=ctx)
                    if html_page.getcode() == 200:
                        break
                    if html_page.getcode() == 404:
                        flag = False
                        break
                except Exception as inst:
                    print(inst)
                    sleep(1)

            if not flag:
                break

            # print('Opened!')
            pnp = PravdaNewsParser()
            pnp.feed(str(html_page.read(), encoding=self.ENC))
            mentions = pnp.get_mentions
            for mention in mentions:
                mention_date = datetime.datetime.strptime(mention, '%d.%m.%Y')
                if self._from_date <= mention_date <= self._to_date:
                    mention_number += 1
                elif mention_date < self._from_date:
                    flag = False
            page_num += 1

            # print(name, mention_number)

        return mention_number

    @property
    def mentions(self):
        """
        :return: dict {POLITIC_NAME: NUMBER_OF_MENTIONS}
        """
        return self._politics



if __name__ == '__main__':
    s1, s2 = "01.11.2019", "20.11.2019"
    politicians = ["Зеленский", "Порошенко"]
    start_date = datetime.datetime.strptime(s1, '%d.%m.%Y')
    end_date = datetime.datetime.strptime(s2, '%d.%m.%Y')

    # start_date = datetime.datetime.strptime(input("News from [dd.mm.yyyy]: "), '%d.%m.%Y')
    # end_date = datetime.datetime.strptime(input("to [dd.mm.yyyy]: "), '%d.%m.%Y')


    print("testing.....")
    print(f'date from: {s1}   date to: {s2}')
    print(f'politicians: {" ".join(politicians)}')

    print('=========# https://www.liga.net/ #=========')
    news = LigaNet(start_date, end_date, politicians)
    print(news.mentions)

    print('=========# https://www.pravda.com.ua// #=========')
    news = PravdaNews(start_date, end_date, politicians)
    print(news.mentions)
