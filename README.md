# environment:
```
1. python3
2. centos7(or above version) or docker image selenium/node-chrome:3.13.0-argon(or above version)
when on centos, google chrome need to be installed:

a. add a file 'google-chrome.repo' to directory '/etc/yum.repos.d' with content:
[google-chrome]
name=google-chrome
baseurl=http://dl.google.com/linux/chrome/rpm/stable/$basearch
enabled=1
gpgcheck=1
gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub

b. run command:
#> yum -y install google-chrome-stable

3. you need to change the file mode bits for 'chromedriver' if on linux system.
#> chmod 777 ./chromedriver
```


# install python dependencies:
```
pip install -r requirements.txt
```

# mysql database create script:
```
./mysql_script/*
```

# properties file:
```
./settings.py
```

# log config file:
```
./logger.conf
```


# properties description:
1. **default_crawl_mode**: 
    Runtime|Debug (in contrast to Debug mode, when on Runtime mode, selenium driver will running on headless way)
2. **chrome_driver_path**: 
    path of chrome driver, you can download this executable driver file on: https://chromedriver.storage.googleapis.com/{version}/chromedriver_linux64.zip
    , or you can just use the 'chromedriver' on project base dir
3. **top_charts_page_crawler_time_out**: 
    time limit(? seconds) to download a single appannie web page source before parsing it's html element with bs4.
4. **cookies_durable_days**: 
    how many days would you like to remain the cookies before clean and renew it.
5. **mysql_***: 
    relevant to mysql usage.
6. **store_url_crawl_interval**:
    interval between crawl [appannie app : store url] mapping relations, in case of appannie account blocked for too rapid visit.


# directory management:
1. **default_data_store_dir**: directory to store web page sources, default value is {project_dir}/data/
2. **default_screenshot_dir**: directory to store sreenshot of chrome driver when error occur, default value is {project_dir}/sceenshot/
3. **default_log_dir**: directory where you put your *.log to, default value is {project_dir}/logs/
4. **default_cookies_dir**: directory saving files which contain browser's cookies, default value is {project_dir}/managercookies/mycookies/
5. **runtime_data_dir**: optional directory where you actually want to store all the logs/cookies/screenshots/.. data to.


# log directory:
```
on file ./logger.conf, you have to configure the [handler_fileHandler] correctly if you want to change the log dir
for example:
args=('/services/appannie_crawler/logs/log.log', 'D')
and make sure that the parent directories are already exist before start running.
```

# appannie account management files:
```
on directory manageraccounts/accounts/ you can find many files name end with '_appannie_accounts.py',
you need to add accounts to each country spcific file.
if you don't have as many as accounts to configure all countries '_appannie_accounts.py' files,
you can write a account proxy to re-allocate the accounts, for example: ./managercookies/account_proxy.py
```
