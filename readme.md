前言：
由于实战经验变得丰富很多，深感日志的重要性，并且学习了解到springboot的日志使用方法
于是决定自己实现一个简单的日志类，实现能够满足日常使用的基本功能

目前实现的功能有如下：
1. 日志格式：
    1. 时间和日期 yyyy-MM-dd HH:mm:ss.SSS
    2. 日志级别：ERROR、WARN、INFO、DEBUG
    3. 消息分隔符：---
    4. 类名和函数名
    5. 消息
2. 文件输出
3. 文件归档和滚动切割
4. 使用properties来进行自定义化配置
    可配置的功能有：
        日志模式，日志路径，日期时间格式，文件归档，滚动切割，滚动切割文件大小，清空输出
5. 整体实现思路是，我希望引入log类后，整个程序运行期间，只有一个实例
    log类可以自动获取调用类和调用函数，并按照规定的数据格式输出日志


一些重要的其他信息：
● 日志级别：由低到高：DEBUG, INFO, WARN, ERROR
  ○ 只会打印指定级别及以上级别的日志
  ○ DEBUG：开发调试细节日志
  ○ INFO：关键、感兴趣信息日志
  ○ WARN：警告但不是错误的信息日志，比如：版本过时
  ○ ERROR：业务错误日志，比如出现各种异常

归档：每天的日志单独存到一个文档中。
切割：每个文件10MB，超过大小切割成另外一个文件。

静默模式：不显示类名和方法名

使用示例：

from WkLog import log

class Test:
    def test2(self):
        log.Debug("debug")
        log.Info("info")
        log.Warn("warn")
        log.Error("error")


def test1():
    log.Debug("debug")
    log.Info("info")
    log.Warn("warn")
    log.Error("error")


if __name__ == "__main__":
    test1()
    Test().test2()
    log.SLIENT = True
    Test().test2()
    log.SLIENT = False
