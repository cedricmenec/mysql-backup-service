import os

class Configuration(object):
    DEBUG = True
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
#    SERVER_NAME = '0.0.0.0:5000'

    MYSQL_CMD = '/usr/bin/mysql'
    MYSQLDUMP_CMD = '/usr/bin/mysqldump'