# -*- coding:utf-8 -*-
from appannieenum import AppannieCountry


class SimpleCountryLevelAccountProxy:
    def __init__(self, country):
        self._original_country = country

    def get_country(self):
        if self._original_country in [
            AppannieCountry.UNITED_STATE,
            AppannieCountry.JAPAN,
            AppannieCountry.INDONESIA,
            AppannieCountry.SINGAPORE,
            AppannieCountry.MALAYSIA
        ]:
            return self._original_country
        elif self._original_country == AppannieCountry.THAILAND:
            return AppannieCountry.UNITED_STATE
        elif self._original_country == AppannieCountry.HONG_KONG:
            return AppannieCountry.JAPAN
        elif self._original_country == AppannieCountry.TAIWAN:
            return AppannieCountry.INDONESIA
        elif self._original_country == AppannieCountry.REPUBLIC_OF_KOREA:
            return AppannieCountry.SINGAPORE
        elif self._original_country == AppannieCountry.FRANCE:
            return AppannieCountry.MALAYSIA
        else:
            return self._original_country


if __name__ == '__main__':
    assert SimpleCountryLevelAccountProxy(AppannieCountry.UNITED_STATE).get_country() == 'US'
    assert SimpleCountryLevelAccountProxy(AppannieCountry.JAPAN).get_country() == 'JP'
    assert SimpleCountryLevelAccountProxy(AppannieCountry.INDONESIA).get_country() == 'ID'
    assert SimpleCountryLevelAccountProxy(AppannieCountry.SINGAPORE).get_country() == 'SG'
    assert SimpleCountryLevelAccountProxy(AppannieCountry.MALAYSIA).get_country() == 'MY'

    assert SimpleCountryLevelAccountProxy(AppannieCountry.THAILAND).get_country() == 'US'
    assert SimpleCountryLevelAccountProxy(AppannieCountry.HONG_KONG).get_country() == 'JP'
    assert SimpleCountryLevelAccountProxy(AppannieCountry.TAIWAN).get_country() == 'ID'
    assert SimpleCountryLevelAccountProxy(AppannieCountry.REPUBLIC_OF_KOREA).get_country() == 'SG'
    assert SimpleCountryLevelAccountProxy(AppannieCountry.FRANCE).get_country() == 'MY'
