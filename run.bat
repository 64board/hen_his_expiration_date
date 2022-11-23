@echo off

rem cd "C:\opt\selenium"

py hen_his_scraper.py HEN
py hen_his_scraper.py HIS

py update_expiration_dates.py HEN config_db_main.ini
py update_expiration_dates.py HIS config_db_main.ini

py update_expiration_dates.py HEN config_db_intranetb.ini
py update_expiration_dates.py HIS config_db_intranetb.ini

rem timeout 30