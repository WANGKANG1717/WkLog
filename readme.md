# WkLog使用文档

## 前言：
这是一个使用python实现的日志模块，简单好用，功能齐全，可以满足日常开发中的日志需求。


## 功能概述：
###  日志输出模式：
1. 控制台输出
   - 输出到控制台
2. 文件输出：
   - 输出到文件，可以设置是否按日期归档，是否按大小切割，是否清空之前的输出文件等
3. 同时输出到控制台和文件
   - 可以针对控制台和文件分别进行设置

###  日志输出格式：
1. 时间和日期 日志级别 消息分隔符 类名 函数名: 消息
   - 时间和日期 yyyy-MM-dd HH:mm:ss.SSS
   - 日志级别：ERROR、WARN、INFO、DEBUG
   - 消息分隔符：---
   - 类名和函数名
   - 消息
   
   示例：
    ```
    2024-07-27 18:04:32 DEBUG    --- class=test, method=test1: 消息内容
    ```
2. 彩色输出：
   - 可以设置是否彩色输出，彩色输出可以让日志更加美观，更容易区分不同级别的日志

3. 静默模式：不显示类名和方法名，只输出消息内容。
    
    示例：
    ```
    2024-07-27 18:24:42 WARNING  --- 消息内容
    ```
###  文件输出
1. 当输出模式为文件模式时，可以选择是否可开启文件归档和滚动切割功能
2. 文件归档：
   - 可以按照设定的时间粒度（比如某一天），将日志自动归档到某个文件中，避免将日志堆积到一个文件中
3. 滚动切割：
   - 当单个日志文件超过一定大小时，可以自动切割成新的文件，防止单个日志文件过大


### 日志级别
1. 可以设置日志的输出级别，只输出高于或等于指定级别的日志。
2. 日志级别：由低到高：DEBUG, INFO, WARNING / WARN, ERROR, FATAL / CRITICAL
3. 日志级别：
   - DEBUG：开发调试细节日志
   - INFO：关键、感兴趣信息日志
   - WARN / WARNING：警告但不是错误的信息日志，比如：版本过时
   - ERROR：业务错误日志，比如出现各种异常
   - FATAL / CRITICAL：严重错误日志，比如：系统崩溃

### 参数介绍
| 参数名                        | 类型 | 说明                                               | 默认值               |
| ----------------------------- | ---- | -------------------------------------------------- | -------------------- |
| level                         | str  | 日志输出级别：Debug, Info, Warning... 不区分大小写 | DEBUG                |
| format_time                   | str  | 时间格式，如 %Y-%m-%d %H:%M:%S                     | %Y-%m-%d %H:%M:%S.%f |
| output_location               | int  | 控制输出位置 0:终端 1:文件 2:文件和终端            | 0                    |
| log_dir                       | str  | 日志文件存放目录                                   | ./logs               |
| log_file_name                 | str  | 日志文件名称                                       | log.txt              |
| color                         | bool | 是否彩色输出                                       | true                 |
| slient                        | bool | 是否静默模式,开启后不输出调用者的类名和函数名      | false                |
| file_archive                  | bool | 是否开启日志文件归档                               | false                |
| file_archive_format           | str  | 日志文件归档格式，如 %Y-%m-%d                      | %Y-%m-%d             |
| rolling_cutting               | bool | 是否开启日志滚动切割                               | false                |
| rolling_cutting_file_max_size | int  | 日志文件最大大小，单位kb                           | 1024                 |
| rolling_cutting_start_index   | int  | 日志文件切割起始序号                               | 1                    |
| clear_pre_output              | bool | 是否清空之前的日志输出                             | false                |

### 功能说明
1. 当输出模式为控制台输出时，日志会输出到终端，并根据日志级别显示不同的颜色。同时参数中与文件输出相关的参数将不会生效
2. 当输出模式为文件输出时，日志会输出到文件中，并根据参数配置进行日志文件归档和滚动切割。
   1. 开启了文件归档，未开启滚动切割，日志将按照`file_archive_format`规定的粒度输出到指定文件中
      - 注意，输出路径为：`./{log_dir}/{file_archive_format}.txt`
   2. 开启了文件归档，同时开启了滚动切割，日志将按照`file_archive_format`和`rolling_cutting_file_max_size`规定的粒度输出到指定文件中，当单个日志文件超过`rolling_cutting_file_max_size`时，日志将自动切割，同时`rolling_cutting_start_index`序号将递增， 新的日志将输出到新的文件中。
        - 注意，输出路径为：`./{log_dir}/{file_archive_format}_{rolling_cutting_start_index}.txt`
   3. 未开启文件归档，开启了滚动切割，此时滚动切割将不会生效。输出的日志文件的路径为`./{log_dir}/{log_file_name}.txt`。

## 配置文件示例：

./config.ini
``` ini
# 日志配置
[wklog]
level = Debug
time_format = %Y-%m-%d %H:%M:%S
output_location = 0
log_dir = ./log
log_file_name = log.txt
color = true
slient = false
file_archive = true
file_archive_format = %Y-%m-%d
rolling_cutting = true
rolling_cutting_file_max_size = 1024
rolling_cutting_start_index = 1
clear_pre_output = false
```

## 使用示例：

#### 单例模式
```python
from WkLog import log


class Test:
   def test1(self):
      log.critical("critical")
      log.fatal("fatal")
      log.error("error")
      log.warn("warn")
      log.warning("warning")
      log.info("info")
      log.debug("debug")


def test2():
   log.critical("critical")
   log.fatal("fatal")
   log.error("error")
   log.warn("warn")
   log.warning("warning")
   log.info("info")
   log.debug("debug")


if __name__ == "__main__":
   Test().test1()
   test2()

```

#### 非单例模式
```python
from WkLog import WkLog

log = WkLog()

if __name__ == "__main__":
   Test().test1()
   test2()
```

#### 注意：
   - 无论是单例模式还是非单例模式，WkLog在初始化的时候都会去尝试读取配置文件(./config.ini)，并根据配置文件中的参数进行初始化。
   - 如果你设置了参数但是没有生效，可以检查一下当前路径下是否有配置文件
