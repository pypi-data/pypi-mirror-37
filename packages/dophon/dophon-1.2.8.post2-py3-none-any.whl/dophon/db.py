from dophon import logger
from dophon import pre_boot

logger.inject_logger(globals())

print(pre_boot.modules_list)

if __name__ in pre_boot.modules_list:
    try:
        __import__(__name__)
        logger.info('该模块( %s )还没安装,请配置module.xml文件安装' % (__name__))
    except Exception as e:
        print(e)

mysql = object
orm = object
