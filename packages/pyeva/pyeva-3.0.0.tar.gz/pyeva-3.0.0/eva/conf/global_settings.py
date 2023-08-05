# Default Eva settings. Override these with settings in the module
MODELS_MODULE = "codebase.models"
MANAGEMENT_MODULE = 'codebase.management'

####################
# CORE             #
####################

DEBUG = False

# 数据库：默认使用 sqlite 内存型数据库
DB_URI = "sqlite://"

SERVICE_NAME = 'microservice'
SERVICE_VERSION = '1.0'

PAGE_SIZE = 10
