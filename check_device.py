#!/usr/bin/env python
#-*- coding:utf-8 -*-
from pyicloud import PyiCloudService
from getpass import getpass

#以下は接続するicloudのアカウントとパスワードを記載します。
iCloudAccount = getpass('Enter your icloud Account: ')
iCloudPassword = getpass('Enter your icloud Password: ')
api = PyiCloudService(iCloudAccount, iCloudPassword)

def get_oauth():
    auth = api.devices
    return auth

if __name__ == '__main__':
    auth=get_oauth()
    print('\n')
    print(auth)