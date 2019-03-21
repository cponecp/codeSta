import hashlib
from settings import DevConfig

m = hashlib.md5(DevConfig.SALT)


def md5(arg):
    arg = str(arg)
    m.update(bytes(arg, encoding='utf8'))
    return m.hexdigest()


if __name__ == '__main__':
    print(md5('123'))
