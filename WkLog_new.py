# -*- coding: utf-8 -*-
# @Date     : 2023-10-12 17:20:00
# @Author   : WangKang
# @Blog     : kang17.xyz
# @Email    : 1686617586@qq.com
# @Filepath : WkLog.py
# @Brief    : 日志类 参考了springboot和logging模块的设计方法
# Copyright 2023 WANGKANG, All Rights Reserved.

""" 
默认配置:
    0. 时间格式: %Y-%m-%d %H:%M:%S.%f
    1. 文件输出关闭
    2. 单文件最大尺寸: 10MB
    3. 默认输出路径: ./log
"""

# 使用colorama重写
import os
import inspect
from colorama import Fore, init
from datetime import datetime

""" 
重构方案：
1. 使用config记录配置
2. 级别优化为5个 与logging模块保持一致
3. 输出模式设置 文件、控制台、文件+控制台
4. 程序结构优化
5. 配置的获取与初始化
"""

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


# 配置类
# 奶奶的，突然发现pytyon也已经提供了可以读取config的配置类，不过我还是决定自己写好吧
class Config:
    ROLLING_CUTTING_START_INDEX = 1  # 滚动切割起始序号 # 这里其实是有问题的，因为每次日期改变，都应该使index从0开始
    PRE_FILE_ARCHIVE_NAME = None  # 用来更新index

    def __init__(self, config_path=None) -> None:
        self.level = DEBUG  # 模式
        self.time_format = "%Y-%m-%d %H:%M:%S.%f"  # 日期格式
        self.output_location = 0  # 控制输出位置0/1/2
        self.dir_path = "./log"  # 默认输出文件路径
        self.log_file_name = "log.txt"  # 默认日志文件名称
        self.file_archive = False  # 日志归档
        self.file_archive_format = "%Y-%m-%d"  # 日志归档格式 默认按照天数归档  使用 - 符号进行分割
        self.rolling_cutting = False  # 滚动切割
        self.file_max_size = 10 * 1024  # 单位kb
        self.rolling_cutting_index = 0  # 用来记录当前归档序号（一般从1开始计数） 如果为0则由程序自动搜索并设置序号
        self.clear_pre_output = False  # 是否清空之前的日志输出
        self.color = True  # 是否彩色输出 默认彩色输出
        self.slient = False  # 是否输出类名和函数名 默认输出

        if config_path:
            self.readConfig(config_path)

        self.init_settings()

    # config_path: 配置文件路径
    def readConfig(self, config_path):
        if not os.path.exists(config_path):
            return

        config = self.getConfig()
        with open(config_path, "r", encoding="utf-8") as f:
            text = f.read()
            lines = text.split("\n")
            for line in lines:
                if line.strip().startswith("#"):
                    continue
                key_value = self._get_key_value(line)
                if key_value:
                    if key_value[0] in config.keys():
                        # 整数字符串转数字
                        if key_value[1].isdigit():
                            key_value[1] = int(key_value[1])
                        # true or false 转为bool类型
                        elif (
                            key_value[1].lower() == "true"
                            or key_value[1].lower() == "false"
                        ):
                            key_value[1] = (
                                True if key_value[1].lower() == "true" else False
                            )
                        # nameToLevel
                        if key_value[0] == "level":
                            key_value[1] = _NAME_TO_LEVEL[key_value[1].upper()]

                        config[key_value[0]] = key_value[1]
                    # else:
                    #     print(f"{key_value[0]} not in config")

    def saveConfig(self, config_path="./log.properties"):
        with open(config_path, "w", encoding="utf-8") as f:
            f.write("# log config by WANGKANG\n")
            config = self.getConfig()
            for key, data in config.items():
                if key == "level":
                    f.write(f"{key} = {_LEVEL_TO_NAME[data]}\n")
                else:
                    f.write(f"{key} = {data}\n")

    # 获取配置信息
    def getConfig(self):
        return vars(self)

    def _get_key_value(self, line):
        if not line or not line.strip():
            return None
        key_value = [data.strip() for data in line.split("=", 1)]
        return key_value

    def init_settings(self):
        if not (self.output_location >= _FILE):
            return

        if self.clear_pre_output and os.path.exists(self.dir_path):
            # 清除之前的日志内容
            for file_name in os.listdir(self.dir_path):
                print(file_name)
                os.remove(f"{self.dir_path}/{file_name}")

        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)

        if (
            self.file_archive
            and self.rolling_cutting
            and self.rolling_cutting_index == 0
        ):
            self.rolling_cutting_index = self._get_rolling_cutting_start_index()

    def _get_rolling_cutting_start_index(self):
        file_archive_name = datetime.now().strftime(self.file_archive_format)
        index = self.ROLLING_CUTTING_START_INDEX
        if os.listdir(self.dir_path):
            for file_name in os.listdir(self.dir_path):
                if (
                    file_name.find(file_archive_name) != -1
                    and file_name.find("_") != -1
                ):
                    i = int(file_name[:-4].rsplit("_", 1)[1])
                    index = max(index, i)
            # os.path.getsize 单位为B
            if os.path.exists(f"{self.dir_path}/{file_archive_name}_{index}.txt"):
                size = os.path.getsize(
                    f"{self.dir_path}/{file_archive_name}_{index}.txt"
                )
                if size >= self.file_max_size * 1024:
                    index += 1
        return index

    def get_rolling_cutting_index(self, file_archive_name):
        if self.PRE_FILE_ARCHIVE_NAME != file_archive_name:
            self.PRE_FILE_ARCHIVE_NAME = file_archive_name
            self.rolling_cutting_index = self.ROLLING_CUTTING_START_INDEX
            return self.rolling_cutting_index
        size = os.path.getsize(
            f"{self.dir_path}/{file_archive_name}_{self.rolling_cutting_index}.txt",
        )
        if size >= self.file_max_size * 1024:
            self.rolling_cutting_index += 1
        return self.rolling_cutting_index

    def get_file_archive_name(self):
        return datetime.now().strftime(self.file_archive_format)


class MyLog:
    def __init__(self, config_path="./log.properties"):
        self.config = Config(config_path)
        init(autoreset=True)

    def debug(self, msg):
        if DEBUG < self.config.level:
            return
        self._print_msg(DEBUG, msg)

    def info(self, msg):
        if INFO < self.config.level:
            return
        self._print_msg(INFO, msg)

    def warn(self, msg):
        if WARN < self.config.level:
            return
        self._print_msg(WARN, msg)

    def warning(self, msg):
        if WARNING < self.config.level:
            return
        self._print_msg(WARNING, msg)

    def error(self, msg):
        if ERROR < self.config.level:
            return
        self._print_msg(ERROR, msg)

    def critical(self, msg):
        if CRITICAL < self.config.level:
            return
        self._print_msg(CRITICAL, msg)

    def fatal(self, msg):
        if FATAL < self.config.level:
            return
        self._print_msg(FATAL, msg)

    def _print_msg(self, level, msg):
        class_name = self._get_calling_class_name()
        method_name = self._get_calling_method_name()
        msg_time = datetime.now().strftime(self.config.time_format)

        if self.config.output_location == _CONSOLE:
            self._print_msg_to_console(level, msg, msg_time, class_name, method_name)
        elif self.config.output_location == _FILE:
            self._print_msg_to_file(level, msg, msg_time, class_name, method_name)
        elif self.config.output_location == _FILE_CONSOLE:
            self._print_msg_to_console(level, msg, msg_time, class_name, method_name)
            self._print_msg_to_file(level, msg, msg_time, class_name, method_name)

    def _print_msg_to_console(self, level, msg, msg_time, class_name, method_name):
        if not self.config.slient:
            if self.config.color:
                res_to_console = f"{_TIME_COLOR + msg_time} {(_LEVEL_TO_COLOR[level] + _LEVEL_TO_NAME[level]):13s} {_RESET_COLOR}--- {f'class={class_name}, ' if class_name else ''}{f'method={method_name}' if method_name else ''}: {_LEVEL_TO_COLOR[level] + msg}"
            else:
                res_to_console = f"{msg_time} {_LEVEL_TO_NAME[level]:8s} --- {f'class={class_name}, ' if class_name else ''}{f'method={method_name}' if method_name else ''}: {msg}"
        else:
            if self.config.color:
                res_to_console = f"{_TIME_COLOR + msg_time} {(_LEVEL_TO_COLOR[level] + _LEVEL_TO_NAME[level]):13s} {_RESET_COLOR}--- {_LEVEL_TO_COLOR[level] + msg}"
            else:
                res_to_console = f"{msg_time} {_LEVEL_TO_NAME[level]:8s} --- {msg}"

        print(res_to_console)

    def _print_msg_to_file(self, level, msg, msg_time, class_name, method_name):
        # 没有开启静默模式
        if not self.config.slient:
            res_to_file = f"{msg_time} {_LEVEL_TO_NAME[level]:8s} --- {f'class={class_name}, ' if class_name else ''}{f'method={method_name}' if method_name else ''}: {msg}\n"
        else:
            # 开启静默模式
            res_to_file = f"{msg_time} {_LEVEL_TO_NAME[level]:8s} --- {msg}\n"
        if not self.config.file_archive:
            with open(
                f"{self.config.dir_path}/{self.config.log_file_name}",
                "a",
                encoding="utf-8",
            ) as f:
                f.write(res_to_file)
        elif self.config.file_archive and not self.config.rolling_cutting:
            file_archive_name = self.config.get_file_archive_name()
            with open(
                f"{self.config.dir_path}/{file_archive_name}.txt",
                "a",
                encoding="utf-8",
            ) as f:
                f.write(res_to_file)
        elif self.config.file_archive and self.config.rolling_cutting:
            file_archive_name = self.config.get_file_archive_name()
            rolling_cutting_index = self.config.get_rolling_cutting_index(
                file_archive_name
            )
            with open(
                f"{self.config.dir_path}/{file_archive_name}_{rolling_cutting_index}.txt",
                "a",
                encoding="utf-8",
            ) as f:
                f.write(res_to_file)

    def _get_calling_method_name(self):
        try:
            return inspect.getframeinfo(inspect.currentframe().f_back.f_back.f_back)[2]
        except:
            return None

    def _get_calling_class_name(self):
        try:
            return type(
                inspect.currentframe().f_back.f_back.f_back.f_locals["self"]
            ).__name__
        except:
            return None


log = MyLog()
