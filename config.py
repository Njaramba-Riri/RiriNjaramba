class Config(object):
    pass

class DevConfig(object):
    SECRET_KEY = '`\xbc\x95\x9cEC`I\xd7b\x9fu\xcb\x0b\xa5w%\xc2/\xd4B\xa8\xc6U'
    CACHE_TYPE = 'simple'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://Riri:$Shadowalker1@localhost:3306/portifolio'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_ECHO = True

class ProdConfig(object):
    SECRET_KEY = '\x8e`\x9a0\xfc_\x89B;?q\x05"\x8duA\xd6\xc1gm\x8a-t\xdb'