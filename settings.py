# -*- coding:utf-8 -*-
from appannieenum import *

# crawler mode
default_crawl_mode = CrawlerMode.Runtime
need_proxy = False

# proxy
proxy_host = ''
proxy_port = ''

# appannie uri
appannie_host = 'https://www.appannie.com'
ios_top_chart_uri = 'apps/ios/top-chart'
appannie_login_referer_url = 'https://www.appannie.com/account/login/?_ref=header'
appannie_home_url = 'https://www.appannie.com'
appannie_i18n_us_redirect_url = 'https://www.appannie.com/i18n/activate/en/?next='

# regular properties
chrome_driver_path = './chromedriver'
top_charts_page_crawler_time_out = 90  # ?s
store_url_crawl_interval = 5  # ?s
enable_offline_concat_app_store_url = True

# cookie management
cookies_json_file = 'cookies.json'
cookies_json_file_suffix = '.cookies.json'
cookies_durable_days = 7

# appannie page element
appannie_captcha_div_class = 'g-recaptcha'
appannie_captcha_form_id = 'captcha_form'
ios_skip_column_with_class = 'tbl-col-rank-and-changes--number'
appannie_detail_page_store_elem = '//*[@id="sub-container"]/div[2]/div[2]/div[1]/div[2]/div/div[1]/div/app-header/div/div/div[2]/div[2]/div[2]/a'
appannie_detail_page_store_elem_2 = '//*[@id="sub-container"]/div[2]/div[2]/div[1]/div[2]/div/div[1]/div/app-header/div/div/div[2]/div[2]/div[2]/a[2]'
appannie_have_store_url_attr = 'app-confirm'
appannie_block_account_body_class = 'body-page-error'

# db settings
mysql_host = ''
mysql_user = ''
mysql_pwd = ''
mysql_db = 'adsinfo_crawler'
mysql_ios_top_free_table = 'ios_top_game'
mysql_android_top_free_table = 'android_top_game'
mysql_app_icon_table = 'appannie_app_icon'
mysql_top_app_table = 'top_app'
mysql_app_ranking_table = 'appannie_app_ranking'

# mail settings
mail_user = 'a@b.com'
mail_pwd = 'pwd'
mail_port = 25
mail_service = 'c@d.com'
mail_receives = 'e@f.com'


def get_real_path():
    # arg_0 = sys.argv[0]
    # arg_0 = os.path.abspath(arg_0)
    arg_0 = __file__
    sap = '/'
    if arg_0.find(sap) == -1:
        sap = '\\'
    index = arg_0.rfind(sap)
    path = arg_0[:index] + sap
    return path


# data directories
current_dir = get_real_path()
runtime_data_dir = current_dir
default_data_store_dir = runtime_data_dir + 'data/'
default_screenshot_dir = runtime_data_dir + 'screenshot/'
default_log_dir = runtime_data_dir + 'logs/'
default_cookies_dir = runtime_data_dir + 'managercookies/mycookies/'


ios_category_to_crawl = [IOSGameCategory.CATEGORY_ACTION, IOSGameCategory.CATEGORY_ADVENTURE,
                         IOSGameCategory.CATEGORY_ARCADE, IOSGameCategory.CATEGORY_BOARD,
                         IOSGameCategory.CATEGORY_CARD, IOSGameCategory.CATEGORY_CASINO,
                         IOSGameCategory.CATEGORY_DICE, IOSGameCategory.CATEGORY_EDUCATION,
                         IOSGameCategory.CATEGORY_FAMILY, IOSGameCategory.CATEGORY_KIDS,
                         IOSGameCategory.CATEGORY_MUSIC, IOSGameCategory.CATEGORY_PUZZLE,
                         IOSGameCategory.CATEGORY_RACING, IOSGameCategory.CATEGORY_ROLE_PLAYING,
                         IOSGameCategory.CATEGORY_SIMULATION, IOSGameCategory.CATEGORY_SPORTS,
                         IOSGameCategory.CATEGORY_STRATEGY, IOSGameCategory.CATEGORY_TRIVIA,
                         IOSGameCategory.CATEGORY_WORD, IOSGameCategory.CATEGORY_ALL]

ios_feed_to_crawl = [IOSFeedType.FEED_FREE, IOSFeedType.FEED_GROSSING]

android_category_to_crawl = [AndroidGameCategory.CATEGORY_ACTION,
                             AndroidGameCategory.CATEGORY_ADVENTURE, AndroidGameCategory.CATEGORY_ARCADE,
                             AndroidGameCategory.CATEGORY_BOARD, AndroidGameCategory.CATEGORY_CARD,
                             AndroidGameCategory.CATEGORY_CASINO, AndroidGameCategory.CATEGORY_CASUAL,
                             AndroidGameCategory.CATEGORY_EDUCATIONAL, AndroidGameCategory.CATEGORY_FAMILY,
                             AndroidGameCategory.CATEGORY_LIVE_WALLPAPER, AndroidGameCategory.CATEGORY_MUSIC,
                             AndroidGameCategory.CATEGORY_PUZZLE, AndroidGameCategory.CATEGORY_RACING,
                             AndroidGameCategory.CATEGORY_ROLE_PLAYING, AndroidGameCategory.CATEGORY_SIMULATION,
                             AndroidGameCategory.CATEGORY_SPORTS, AndroidGameCategory.CATEGORY_STRATEGY,
                             AndroidGameCategory.CATEGORY_TRIVIA, AndroidGameCategory.CATEGORY_WIDGETS,
                             AndroidGameCategory.CATEGORY_WORD, AndroidGameCategory.CATEGORY_ALL
                             # AndroidGameCategory.CATEGORY_ARCADE_AND_ACTION,
                             # AndroidGameCategory.CATEGORY_BRAIN_AND_PUZZLE,
                             # AndroidGameCategory.CATEGORY_CARDS_AND_CASINO,
                             ]

android_feed_to_crawl = [AndroidFeedType.FEED_FREE, AndroidFeedType.FEED_GROSSING]


if __name__ == '__main__':
    print(get_real_path(__file__))
