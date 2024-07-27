# -*- coding: utf-8 -*-
# @Date     : 2023-10-12 17:20:00
# @Author   : WangKang
# @Blog     : https://wangkang1717.github.io/
# @Email    : 1686617586@qq.com
# @Filepath : WkLog.py
# @Brief    : 简洁好用的日志类库
# Copyright 2023 WANGKANG, All Rights Reserved.

""" 
项目地址：https://gitee.com/purify_wang/wk-log
"""

# 使用colorama重写
import os
import shutil
import inspect
from colorama import Fore
from colorama import init as colorama_init
from datetime import datetime
from configparser import ConfigParser

NO_OUTPUT = 100
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10

_LEVEL_TO_NAME = {
    CRITICAL: "CRITICAL",
    ERROR: "ERROR",
    WARNING: "WARNING",
    INFO: "INFO",
    DEBUG: "DEBUG",
}

_NAME_TO_LEVEL = {
    "CRITICAL": CRITICAL,
    "FATAL": FATAL,
    "ERROR": ERROR,
    "WARN": WARNING,
    "WARNING": WARNING,
    "INFO": INFO,
    "DEBUG": DEBUG,
}

_LEVEL_TO_COLOR = {
    CRITICAL: Fore.LIGHTRED_EX,
    FATAL: Fore.LIGHTRED_EX,
    ERROR: Fore.RED,
    WARN: Fore.YELLOW,
    WARNING: Fore.YELLOW,
    INFO: Fore.GREEN,
    DEBUG: Fore.BLUE,
}

_TIME_COLOR = Fore.CYAN
_RESET_COLOR = Fore.RESET

# 控制输出位置
_CONSOLE = 0
_FILE = 1
_FILE_CONSOLE = 2

DEFAULT_CONFIG = {  # 默认配置
    "level": DEBUG,  # 模式
    "time_format": "%Y-%m-%d %H:%M:%S.%f",  # 日期格式
    "output_location": _CONSOLE,  # 控制输出位置0/1/2
    "log_dir": "./log",  # 默认输出文件路径
    "log_file_name": "log.txt",  # 默认日志文件名称
    "file_archive": False,  # 日志归档
    "file_archive_format": "%Y-%m-%d",  # 日志归档格式 默认按照天数归档  使用 - 符号进行分割
    "rolling_cutting": False,  # 滚动切割
    "rolling_cutting_file_max_size": 10 * 1024,  # 单位kb
    "rolling_cutting_start_index": 0,  # 滚动切割起始序号
    "clear_pre_output": False,  # 是否清空之前的日志输出
    "color": True,  # 是否彩色输出 默认彩色输出
    "slient": False,  # 是否输出类名和函数名 默认输出
}


class WkLog:
    SECTION_NAME = "wklog"

    def __init__(self, config_path="./config.ini"):
        colorama_init(autoreset=True)

        self.level = None
        self.time_format = None
        self.output_location = None
        self.log_dir = None
        self.log_file_name = None
        self.file_archive = None
        self.file_archive_format = None
        self.rolling_cutting = None
        self.rolling_cutting_file_max_size = None
        self.rolling_cutting_start_index = None
        self.clear_pre_output = None
        self.color = None
        self.slient = None

        config = DEFAULT_CONFIG.copy()
        if os.path.exists(config_path):
            self.read_config(config_path, config)

        vars_ = vars(self)
        vars_.update(config)

        # print(vars(self))
        self._init_settings()

    def read_config(self, config_path, config):
        configParser = ConfigParser(interpolation=None)
        configParser.read(config_path, encoding="utf-8")
        if configParser.has_section(self.SECTION_NAME):
            for key in config.keys():
                if configParser.has_option(self.SECTION_NAME, key):
                    value = configParser.get(self.SECTION_NAME, key)
                    # print(f"config {key} = {value}")
                    if key == "level":
                        value = _NAME_TO_LEVEL[value.upper()]
                    # 整数字符串转数字
                    elif value.isdigit():
                        value = int(value)
                    # true or false 转为bool类型
                    elif value.lower() == "true" or value.lower() == "false":
                        value = True if value.lower() == "true" else False
                    if type(value) != type(config[key]):
                        raise TypeError(f"config {key} type error")
                    config.update({key: value})

    def debug(self, msg):
        if DEBUG < self.level:
            return
        self._print_msg(DEBUG, msg)

    def info(self, msg):
        if INFO < self.level:
            return
        self._print_msg(INFO, msg)

    def warn(self, msg):
        if WARN < self.level:
            return
        self._print_msg(WARN, msg)

    def warning(self, msg):
        if WARNING < self.level:
            return
        self._print_msg(WARNING, msg)

    def error(self, msg):
        if ERROR < self.level:
            return
        self._print_msg(ERROR, msg)

    def critical(self, msg):
        if CRITICAL < self.level:
            return
        self._print_msg(CRITICAL, msg)

    def fatal(self, msg):
        if FATAL < self.level:
            return
        self._print_msg(FATAL, msg)

    def _print_msg(self, level, msg):
        class_name = self._get_calling_class_name()
        method_name = self._get_calling_method_name()
        msg_time = datetime.now().strftime(self.time_format)

        if self.output_location == _CONSOLE:
            self._print_msg_to_console(level, msg, msg_time, class_name, method_name)
        elif self.output_location == _FILE:
            self._print_msg_to_file(level, msg, msg_time, class_name, method_name)
        elif self.output_location == _FILE_CONSOLE:
            self._print_msg_to_console(level, msg, msg_time, class_name, method_name)
            self._print_msg_to_file(level, msg, msg_time, class_name, method_name)

    def _print_msg_to_console(self, level, msg, msg_time, class_name, method_name):
        if not self.slient:
            if self.color:
                res_to_console = f"{_TIME_COLOR + msg_time} {(_LEVEL_TO_COLOR[level] + _LEVEL_TO_NAME[level]):13s} {_RESET_COLOR}--- {f'class={class_name}, ' if class_name else ''}{f'method={method_name}' if method_name else ''}: {_LEVEL_TO_COLOR[level] + msg}"
            else:
                res_to_console = f"{msg_time} {_LEVEL_TO_NAME[level]:8s} --- {f'class={class_name}, ' if class_name else ''}{f'method={method_name}' if method_name else ''}: {msg}"
        else:
            if self.color:
                res_to_console = f"{_TIME_COLOR + msg_time} {(_LEVEL_TO_COLOR[level] + _LEVEL_TO_NAME[level]):13s} {_RESET_COLOR}--- {_LEVEL_TO_COLOR[level] + msg}"
            else:
                res_to_console = f"{msg_time} {_LEVEL_TO_NAME[level]:8s} --- {msg}"

        print(res_to_console)

    def _print_msg_to_file(self, level, msg, msg_time, class_name, method_name):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        # 没有开启静默模式
        if not self.slient:
            res_to_file = f"{msg_time} {_LEVEL_TO_NAME[level]:8s} --- {f'class={class_name}, ' if class_name else ''}{f'method={method_name}' if method_name else ''}: {msg}\n"
        else:
            # 开启静默模式
            res_to_file = f"{msg_time} {_LEVEL_TO_NAME[level]:8s} --- {msg}\n"

        if not self.file_archive:  # 不开启归档
            with open(f"{self.log_dir}/{self.log_file_name}", "a", encoding="utf-8") as f:
                f.write(res_to_file)
        elif self.file_archive and not self.rolling_cutting:  # 开启归档但不开启滚动切割
            file_archive_name = self._get_file_archive_name()
            with open(f"{self.log_dir}/{file_archive_name}.txt", "a", encoding="utf-8") as f:
                f.write(res_to_file)
        elif self.file_archive and self.rolling_cutting:  # 开启归档和滚动切割
            file_archive_name = self._get_file_archive_name()
            rolling_cutting_index = self._get_rolling_cutting_index(file_archive_name)
            with open(f"{self.log_dir}/{file_archive_name}_{rolling_cutting_index}.txt", "a", encoding="utf-8") as f:
                f.write(res_to_file)

    def _get_calling_method_name(self):
        try:
            return inspect.getframeinfo(inspect.currentframe().f_back.f_back.f_back)[2]
        except:
            return None

    def _get_calling_class_name(self):
        try:
            return type(inspect.currentframe().f_back.f_back.f_back.f_locals["self"]).__name__
        except:
            return None

    def _init_settings(self):
        if not (self.output_location >= _FILE):
            return

        if self.clear_pre_output and os.path.exists(self.log_dir):
            # 清除之前的日志内容
            shutil.rmtree(self.log_dir)

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def _get_rolling_cutting_index(self, file_archive_name):
        index = self.rolling_cutting_start_index

        while True:
            if not os.path.exists(f"{self.log_dir}/{file_archive_name}_{index}.txt"):  # 找不到则跳出循环
                break
            # os.path.getsize 单位为B
            size = os.path.getsize(f"{self.log_dir}/{file_archive_name}_{index}.txt")  # 获取文件大小
            if size < self.rolling_cutting_file_max_size * 1024:  # 当前归档文件没有达到切割大小
                break
            index += 1

        return index

    def _get_file_archive_name(self):
        return datetime.now().strftime(self.file_archive_format)


log = WkLog()
