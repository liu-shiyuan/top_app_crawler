# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header
import settings as _s
import traceback
from loggers import get_logger
from appannieenum import AccountStatus
from manageraccounts import load_accounts


def _get_mail_client():
    _mail_client = smtplib.SMTP(host=_s.mail_service, port=_s.mail_port)
    _mail_client.login(user=_s.mail_user, password=_s.mail_pwd)
    return _mail_client


def sent_alert_to_receivers(country, account_info, account_status):
    mail_content = 'Appannie Account:\n(%s, %s: %s) \nis abnormal with status: \n%s\n' \
                   '' % (str.lower(country), account_info['no'], account_info['email'], account_status.name)
    message = MIMEText(mail_content, 'Plain', 'utf-8')
    message['Subject'] = Header('Appannie Crawler Alert', 'utf-8')
    message['From'] = _s.mail_user
    message['To'] = _s.mail_receives
    mail_client = _get_mail_client()
    mail_receives = []
    for e in _s.mail_receives.split(','):
        mail_receives.append(e.strip())
    try:
        mail_client.sendmail(_s.mail_user, mail_receives, message.as_string())
    except:
        get_logger().error('traceback:\n%s' % traceback.format_exc())
    finally:
        mail_client.quit()


def sent_alert_to_receivers_with_screenshot(country, account_info, account_status, screenshot_file):
    msg_root = MIMEMultipart('related')
    msg_root['From'] = _s.mail_user
    msg_root['To'] = _s.mail_receives
    _cid = 'screenshot'
    msg_root['Subject'] = Header('Appannie Crawler Alert', 'utf-8')
    mail_content = 'Appannie Account:<br>(%s, %s: %s) <br>is abnormal with status: ' \
                   '<br>%s<br><br><p><img src="cid:%s"></p><br>' % (
                    str.lower(country), account_info['no'], account_info['email'], account_status.name, _cid)
    msg_alternative = MIMEMultipart('alternative')
    msg_root.attach(msg_alternative)
    msg_alternative.attach(MIMEText(mail_content, 'html', 'utf-8'))
    with open(screenshot_file, 'rb') as fp:
        msg_image = MIMEImage(fp.read())
        msg_image.add_header('Content-ID', '<%s>' % _cid)
        msg_root.attach(msg_image)
    mail_receives = []
    mail_client = _get_mail_client()
    for e in _s.mail_receives.split(','):
        mail_receives.append(e.strip())
    try:
        mail_client.sendmail(_s.mail_user, mail_receives, msg_root.as_string())
    except:
        get_logger().error('traceback:\n%s' % traceback.format_exc())
    finally:
        mail_client.quit()


if __name__ == '__main__':
    # sent_alert_to_receivers(_s.appannie_accounts[0], AccountStatus.BLOCKED)
    with load_accounts('JP') as accounts:
        sent_alert_to_receivers_with_screenshot('JP', accounts[0], AccountStatus.BLOCKED,
                                                '#{screenshot path}')
