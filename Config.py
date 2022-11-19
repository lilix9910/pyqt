#! /usr/bin/env python3
import os
from configparser import ConfigParser

cfg = ConfigParser()
cfg.read(filenames="./config.ini", encoding="utf-8")
USERNAME = cfg.get("account", "username")
PASSWORD = cfg.get("account", "password")
ALLOWS = cfg.get("busi_type", "allows")
ALLOWS_LIST = ALLOWS.split(",")
ALL_ALLOWS = cfg.get("busi_type", "all_allows")
ALL_ALLOWS_LIST = ALL_ALLOWS.split(",")
DING_CAPTCHA_MODE = cfg.getint("captcha", "ding_mode")
CBSS_CAPTCHA_MODE = cfg.getint("captcha", "cbss_mode")
BAIDU_ADDR = cfg.get("baidu", "addr")
BAIDU_TOKEN = cfg.get("baidu", "token")
SLEEP_TIME = cfg.getint("time", "sleep")
DELAY_TIME = cfg.getint("time", "delay")
WAIT_TIME = cfg.getint("time", "wait")
AUTO_SWITCH = cfg.getboolean("switch", "auto")
SWITCH_MAX = cfg.getint("switch", "max")
SWITCH_MIN = cfg.getint("switch", "min")
DING_BROWSER = cfg.get("browser", "ding")
CBSS_BROWSER = cfg.get("browser", "cbss")
NO_RES_FILE = cfg.get("files", "no_res_file")
ERROR_FILE = cfg.get("files", "error_file")
CHARGE_FEE_FILE = cfg.get("files", "charge_fee_file")
GROUP_NUMBER_FILE = cfg.get("files", "group_number_file")
LOG_DIR = cfg.get("files", "log_dir")
ERR_DIR = cfg.get("files", "err_dir")


if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

if not os.path.exists(ERR_DIR):
    os.makedirs(ERR_DIR)

if __name__ == "__main__":
    pass
