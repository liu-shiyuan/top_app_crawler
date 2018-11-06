# -*- coding:utf-8 -*-
import settings as _s
from db.db_conn import DBConnectionHandler
import requests
import base64
from loggers import get_logger
import urllib


def __get_img_content__(pic_url):
    if pic_url and not pic_url.startswith('http'):
        if pic_url.startswith('/'):
            pic_url = _s.appannie_home_url + pic_url
        else:
            get_logger().info(pic_url)
            return None
    url_elements = urllib.parse.urlparse(pic_url)
    headers = {'authority': url_elements.netloc,
               'method': 'GET',
               'path': url_elements.path,
               'scheme': 'https',
               'cache-control': 'max-age=0',
               'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
               'dnt': '1',
               'accept-encoding': 'gzip, deflate, br',
               'accept-language': 'en-US,en;q=0.8,ja;q=0.6'
               }
    pic = requests.get(pic_url, headers=headers)
    return pic.content


class IconIdDeterminer(DBConnectionHandler):
    def __init__(self):
        super().__init__()

    def get_icon_id(self, icon_url):
        sql = 'select id from %s where icon_url = "%s"' % (_s.mysql_app_icon_table, icon_url)
        super().get_cursor().execute(sql)
        data = super().get_cursor().fetchone()
        if data is None:
            get_logger().debug('get icon of: %s' % icon_url)
            _r = self.insert_new_icon(icon_url)
            if _r:
                return self.get_icon_id(icon_url)
            else:
                return None
        return data[0]

    def insert_new_icon(self, icon_url):
        _img_c = __get_img_content__(icon_url)
        if _img_c:
            _content_str = str(base64.b64encode(_img_c))[2: -1]
            sql = 'insert into %s (icon_url, content) values ("%s", "%s")' \
                  % (_s.mysql_app_icon_table, icon_url, _content_str)
            super().get_cursor().execute(sql)
            super().get_conn().commit()
            return True
        return False


class BrokenIconReDownloader(DBConnectionHandler):
    def __init__(self):
        super().__init__()

    def redownload(self, db_id, icon_url, pre_base64_str=None):
        _img_c = __get_img_content__(icon_url)
        if _img_c:
            _content_str = str(base64.b64encode(_img_c))[2: -1]
            if pre_base64_str:
                if _content_str == pre_base64_str:
                    get_logger().info('redownload icon [%s] failed.' % db_id)
                    return
            self.update_record(db_id, _content_str)

    def update_record(self, db_id, content):
        sql = 'update %s set content = "%s" where id = %s' % (_s.mysql_app_icon_table, content, str(db_id))
        super().get_cursor().execute(sql)
        super().get_conn().commit()
        get_logger().info('update icon [%s] succeeded.' % db_id)


def test_generate_img_from_base64(str_content):
    content = base64.b64decode(str_content)
    with open('base64.jpg', 'wb') as f:
        f.write(content)
        f.flush()


if __name__ == '__main__':
    # obj = IconIdDeterminer()
    # obj.open_conn()
    # x = obj.get_icon_id('https://static-s.aa-cdn.net/img/ios/1053012308/27875c07821a717f3824c63510a7f398_w80')
    # print(x)
    # obj.close_conn()
    main_icon_url = 'https://static-s.aa-cdn.net/img/ios/1034383306/27862b9d7c51df69e74b306ede795c79_w80'
    _img_c = __get_img_content__(main_icon_url)
    print(_img_c)
    #_content_str = str(base64.b64encode(_img_c))[2: -1]
    #main_content = 'PGh0bWw+DQo8aGVhZD48dGl0bGU+NTAzIFNlcnZpY2UgVGVtcG9yYXJpbHkgVW5hdmFpbGFibGU8L3RpdGxlPjwvaGVhZD4NCjxib2R5IGJnY29sb3I9IndoaXRlIj4NCjxjZW50ZXI+PGgxPjUwMyBTZXJ2aWNlIFRlbXBvcmFyaWx5IFVuYXZhaWxhYmxlPC9oMT48L2NlbnRlcj4NCjxocj48Y2VudGVyPm5naW54PC9jZW50ZXI+DQo8L2JvZHk+DQo8L2h0bWw+DQo='
    #test_generate_img_from_base64(main_content)
    #generate_img_from_base64(_content_str)
