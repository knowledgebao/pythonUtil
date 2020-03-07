# -*- coding: UTF-8 -*-
import os
import logging
def logmsg(*args):
    # 创建存放日志的绝对目录
    def Create_dirs():
        application_path = os.getcwd()  # 获取当前目录
        L = []
        for root, dirs, files in os.walk(application_path):
            for dir in dirs:
                L.append(dir)
        logging.info("pwd is %s"%L)
        logdir = "logs"

        if logdir not in L:
            temp = application_path + os.sep + logdir
            os.mkdir(temp)

        else:
            temp = application_path + os.sep + logdir
        return temp

    abspath = Create_dirs()
    # 第一步，创建一个logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG) # Log等级总开关的最低级,开关级别从低到高是debug，info,warning,error,critical,低于设定级别的不被打印，高于的都可以打印

    # 创建控制台打印的handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)  # 输出log等级的开关,只打印错误消息
    # 创建一个handler，用于写入日志文件
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
    logname = 'my.log'
    logfile = abspath + os.sep + logname
    print(logfile)
    fh = logging.FileHandler(logfile, mode='a')
    fh.setLevel(logging.WARNING)# 输出到file的log等级的开关

    # 第三步，定义handler的输出格式
    fh_formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    ch_formatter = logging.Formatter("%(asctime)s - [line:%(lineno)d] - %(levelname)s: %(message)s")

    ch.setFormatter(ch_formatter)  # ch绑定输出格式
    fh.setFormatter(fh_formatter)#fh绑定输出格式

    logger.addHandler(ch)
    logger.addHandler(fh)#logger绑定文件
    return logger
logger = logmsg()
if __name__=="__main__":
    logger.warning('hao')