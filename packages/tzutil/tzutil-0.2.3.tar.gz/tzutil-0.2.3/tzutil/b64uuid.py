from os import urandom
from base64 import urlsafe_b64encode


def b64uuid():
    return urlsafe_b64encode(urandom(16)).decode('utf-8').rstrip('=')


if __name__ == '__main__':
    import time
    while True:
        print(b64uuid())
        time.sleep(.5)
