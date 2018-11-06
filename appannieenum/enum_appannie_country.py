# -*- coding:utf-8 -*-


class AppannieCountry:
    UNITED_STATE = 'US'
    JAPAN = 'JP'
    INDONESIA = 'ID'
    SINGAPORE = 'SG'
    MALAYSIA = 'MY'

    THAILAND = 'TH'
    HONG_KONG = 'HK'
    TAIWAN = 'TW'
    REPUBLIC_OF_KOREA = 'KR'
    FRANCE = 'FR'

    UNITED_KINGDOM = 'GB'
    GERMANY = 'DE'
    SAUDI_ARABIA = 'SA'
    INDIA = 'IN'
    MACAU = 'MO'

    @staticmethod
    def get_all_countries():
        ret = []
        obj_me = AppannieCountry()
        for _x in AppannieCountry.__dict__:
            if not _x.startswith('_') and _x != 'get_all_countries':
                ret.append(AppannieCountry.__getattribute__(obj_me, _x))
        return ret


if __name__ == '__main__':
    cs = AppannieCountry().get_all_countries()
    cs = [str.lower(c) for c in cs]
    print(cs)
