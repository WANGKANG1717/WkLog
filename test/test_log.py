from WkLog import log


class test:
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
    # config = Config()
    # config.readConfig()
    # print(config.getConfig())
    # config.saveConfig()
    # print(Config.locals())
    # log = MyLog()
    # log.config.level = DEBUG
    # log.config.level = INFO
    # log.config.level = WARN
    # log.config.level = WARNING
    # log.config.level = ERROR
    # log.config.level = FATAL
    # log.config.level = CRITICAL
    # log.config.time_format = "%Y-%m-%d %H:%M:%S.%f"
    # log.config.output_location = 1
    # print(log.config.getConfig())
    # log.config.slient = True
    # log.critical("critical")
    # log.fatal("fatal")
    # log.error("error")
    # log.warn("warn")
    # log.warning("warning")
    # log.info("info")
    # log.debug("debug")
    for i in range(10000):
        test().test1()
        test2()
