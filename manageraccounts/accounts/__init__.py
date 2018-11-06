from appannieenum.enum_appannie_country import AppannieCountry
import traceback
from loggers import get_logger

all_cs = AppannieCountry.get_all_countries()
all_cs = [str.lower(c) for c in all_cs]

for c in all_cs:
    try:
        exec('from manageraccounts.accounts.%s_appannie_accounts import accounts as %s_accounts' % (c, c))
        _tmp = eval('%s_accounts' % c)
        if _tmp:
            get_logger().info('%s %s accounts loaded.' % (str(len(_tmp)), str.upper(c)))
    except ImportError:
        get_logger().error('Traceback:\n%s' % traceback.format_exc())
