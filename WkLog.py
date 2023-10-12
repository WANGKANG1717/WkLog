# -*- coding: utf-8 -*-
# @Date     : 2023-09-20 10:50:19
# @Author   : WangKang
# @Blog     : kang17.xyz
# @Email    : 1686617586@qq.com
# @Filepath : WkLog.py
# @Brief    : 日志类，仿照springboot编写的简化版
# Copyright 2023 WANGKANG, All Rights Reserved.

""" 
默认配置:
    0. 时间格式: %Y-%m-%d %H:%M:%S.%f
    1. 文件输出关闭
    2. 单文件最大尺寸: 10MB
    3. 默认输出路径: ./log
"""
import os
import datetime
import inspect


class MyLog:
    LEVEL_COLOR = {
        "Debug": "green",
        "Info": "blue",
        "Warn": "yellow",
        "Error": "red",
    }
    MODE = ["debug", "info", "warning", "error"]

    def __init__(self):
        self.mode = "debug"
        self.time_format = "%Y-%m-%d %H:%M:%S.%f"
        self.output_to_file = False  # 是否输出到文件
        self.dir_path = "./log"  # 默认输出文件路径
        self.file_archive = False  # 文件归档
        self.rolling_cutting = False  # 滚动切割
        self.file_max_size = 10 * 1024  # 单位kb
        self.rolling_cutting_index = 1  # 用来记录当前归档序号
        self.clear_pre_output = False  # 是否清空之前的日志输出
        self.init_settings()
        # print(self.mode)
        # print(self.time_format)
        # print(self.output_to_file)
        # print(self.dir_path)
        # print(self.file_max_size)
        # print(self.file_archive)
        # print(self.rolling_cutting)
        # print(self.clear_pre_output)

    def Debug(self, msg):
        if self.mode.strip() in self.MODE[1:]:
            return
        class_name = self.get_calling_class_name()
        func_name = self.get_calling_func_name()
        level = "Debug"
        self.print_msg(class_name, func_name, level, msg)

    def Info(self, msg):
        if self.mode in self.MODE[2:]:
            return
        class_name = self.get_calling_class_name()
        func_name = self.get_calling_func_name()
        level = "Info"
        self.print_msg(class_name, func_name, level, msg)

    def Warning(self, msg):
        if self.mode in self.MODE[3:]:
            return
        class_name = self.get_calling_class_name()
        func_name = self.get_calling_func_name()
        level = "Warn"
        self.print_msg(class_name, func_name, level, msg)

    def Error(self, msg):
        class_name = self.get_calling_class_name()
        func_name = self.get_calling_func_name()
        level = "Error"
        self.print_msg(class_name, func_name, level, msg)

    def print_msg(self, class_name, func_name, level, msg):
        now = datetime.datetime.now()
        msg_time = now.strftime(self.time_format)
        today = now.strftime("%Y-%m-%d")
        if class_name != None:
            res = f"{self.color(msg_time, 'cyan')} {self.color(level, self.LEVEL_COLOR[level]):14s} --- class={class_name}, func={func_name}: {self.color(msg, self.LEVEL_COLOR[level])}"
        else:
            res = f"{self.color(msg_time, 'cyan')} {self.color(level, self.LEVEL_COLOR[level]):14s} --- func={func_name}: {self.color(msg, self.LEVEL_COLOR[level])}"
        print(res)
        if self.output_to_file:
            if class_name != None:
                res = f"{msg_time} {level:5s} --- class={class_name}, func={func_name}: {msg}\n"
            else:
                res = f"{msg_time} {level:5s} --- func={func_name}: {msg}\n"
            if not self.file_archive:
                with open(f"{self.dir_path}/log.txt", "a") as f:
                    f.write(res)
            elif self.file_archive and not self.rolling_cutting:
                with open(f"{self.dir_path}/{today}.txt", "a") as f:
                    f.write(res)
            elif self.file_archive and self.rolling_cutting:
                with open(f"{self.dir_path}/{today}_{self.rolling_cutting_index}.txt", "a") as f:
                    f.write(res)
                size = os.path.getsize(f"{self.dir_path}/{today}_{self.rolling_cutting_index}.txt")
                if size >= self.file_max_size * 1024:
                    self.rolling_cutting_index += 1

    def get_calling_func_name(self):
        try:
            return inspect.getframeinfo(inspect.currentframe().f_back.f_back)[2]
        except:
            return None

    def get_calling_class_name(self):
        try:
            return type(inspect.currentframe().f_back.f_back.f_locals["self"]).__name__
        except:
            return None

    def color(self, msg, color):
        if color == "red":
            return f"\033[31m{msg}\033[0m"
        elif color == "green":
            return f"\033[32m{msg}\033[0m"
        elif color == "yellow":
            return f"\033[33m{msg}\033[0m"
        elif color == "blue":
            return f"\033[34m{msg}\033[0m"
        elif color == "purple":
            return f"\033[35m{msg}\033[0m"
        elif color == "cyan":
            return f"\033[36m{msg}\033[0m"

    def init_settings(self):
        if not os.path.exists("./log.properties"):
            return
        with open("./log.properties", "r") as f:
            text = f.read()
            lines = text.split("\n")
            for line in lines:
                line = line.strip()
                if line.startswith("#"):
                    continue
                if line.startswith("mode"):
                    self.mode = line.split("=")[1].strip()
                elif line.startswith("format_time"):
                    time_format = line.split("=")[1].strip()
                    self.time_format = time_format
                elif line.startswith("output_to_file"):
                    flag = line.split("=")[1].strip()
                    self.output_to_file = True if flag == "true" else False
                elif line.startswith("dir_path"):
                    self.dir_path = line.split("=")[1].strip()
                elif line.startswith("file_max_size"):
                    size = line.split("=")[1].strip()
                    if size.endswith("KB"):
                        self.file_max_size = int(size[:-2])
                    elif size.endswith("MB"):
                        self.file_max_size = int(size[:-2]) * 1024
                    elif size.endswith("GB"):
                        self.file_max_size = int(size[:-2]) * 1024 * 1024
                elif line.startswith("file_archive"):
                    flag = line.split("=")[1].strip()
                    self.file_archive = True if flag == "true" else False
                elif line.startswith("rolling_cutting"):
                    flag = line.split("=")[1].strip()
                    self.rolling_cutting = True if flag == "true" else False
                elif line.startswith("clear_pre_output"):
                    flag = line.split("=")[1].strip()
                    self.clear_pre_output = True if flag == "true" else False
        if self.output_to_file and self.clear_pre_output and os.path.exists(self.dir_path):
            # 清楚之前的日志内容
            for file_name in os.listdir(self.dir_path):
                print(file_name)
                os.remove(f"{self.dir_path}/{file_name}")
        if self.output_to_file and not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)
        if self.output_to_file and self.file_archive and self.rolling_cutting:
            self.rolling_cutting_index = self.get_rolling_cutting_index()

    def get_rolling_cutting_index(self):
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        index = 1
        if os.listdir(self.dir_path):
            for file_name in os.listdir(self.dir_path):
                if file_name.find(today) != -1 and file_name.find("_") != -1:
                    i = int(file_name[:-4].rsplit("_")[1])
                    index = max(index, i)
            # os.path.getsize 单位为B
            if os.path.exists(f"{self.dir_path}/{today}_{index}.txt"):
                size = os.path.getsize(f"{self.dir_path}/{today}_{index}.txt")
                if size >= self.file_max_size * 1024:
                    index += 1
        return index


log = MyLog()
