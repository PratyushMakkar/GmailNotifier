import os
from time import time, sleep

from notification import InitiatePushNotification

if __name__ == '__main__':
    while True:
        InitiatePushNotification()
        sleep(60- time() % 60)
       

