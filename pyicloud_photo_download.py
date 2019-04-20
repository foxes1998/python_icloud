#!/usr/bin/env python
#-*- coding:utf-8 -*-
from pyicloud import PyiCloudService
from getpass import getpass
import sys
import glob
import os.path

import check_daplication as CD

#以下は接続するicloudのアカウントとパスワードを記載します。
iCloudAccount = getpass('Enter your icloud Account: ')
iCloudPassword = getpass('Enter your icloud Password: ')
api = PyiCloudService(iCloudAccount, iCloudPassword)

#ここから2段認証を実施する。
if api.requires_2sa:
    import click
    print ("Two-factor authentication required. Your trusted devices are: ")

    devices = api.trusted_devices
    for i, device in enumerate(devices):
        print ("  %s: %s" % (i, device.get('deviceName',
            "SMS to %s" % device.get('phoneNumber'))))

    device = click.prompt('Which device would you like to use?', default=0)
    device = devices[device]
    if not api.send_verification_code(device):
        print ("Failed to send verification code")
        sys.exit(1)

    code = click.prompt('Please enter validation code')
    if not api.validate_verification_code(device, code):
        print ("Failed to verify verification code")
        sys.exit(1)

def get_oauth():
    # デバイスナンバーは、icloudに登録しているデバイスに応じて数が異なる。
    auth = api.devices[5].location()
    return auth

def listdir_nohidden(path):
    retnum = 0
    for f in os.listdir(path):
        if not f.startswith('.'):
            retnum = retnum + 1
        else:
            retnum = retnum + 0
    return retnum

if __name__ == '__main__':
    # デバイスナンバー表示
    print(api.devices)

    # GPS 位置取得
    """
    auth = str(get_oauth())
    s=auth.find('longitude')
    e=auth.find(u'positionType')
    s1=auth.find(u'latitude')
    e1=auth.find(u'isOld')
    lng1 =float(auth[s+12:s+12+10])
    lat1 =float(auth[s1+11:s1+11+10])
    print('%3.14f,%3.14f'%(lng1,lat1))
    """

    # 写真の glasses 取得
    # オリジナルのメガネ画像保存先パス
    glasses_original_dir_pass = '/Users/shimadatakuyume/iCloud_pi/icloud_photos/glasses/glasses_original/'
    glasses_original_dir_filenum = listdir_nohidden(glasses_original_dir_pass)
    # インスタンスに画像が保存されているパスを与える
    ins_check_daplication = CD.check_daplication(glasses_original_dir_pass)
    # 重複チェックリスト
    all_daplication_pair = []
    # glasses_original_dir_filenum = len(glasses_original_dir_files)
    print('glasses_original_dir_filenum:'+ str(glasses_original_dir_filenum))
    icloud_glasses_photo_number = len(api.photos.albums['glasses'])
    print('icloud_glasses_photo_number:'+ str(icloud_glasses_photo_number))
    photo_number = icloud_glasses_photo_number
    if glasses_original_dir_filenum != icloud_glasses_photo_number:
        if glasses_original_dir_filenum > icloud_glasses_photo_number:
            print ('There may be errors in '+glasses_original_dir_pass)
        else :
            for photo in api.photos.albums['glasses']:
                print (photo, photo.filename)
                download = photo.download()
                print ('dounloaded...')
                root, ext = os.path.splitext(photo.filename)
                with open('/Users/shimadatakuyume/iCloud_pi/icloud_photos/glasses/glasses_original/'+ str(photo_number) + str(ext), 'wb') as opened_file:
                    opened_file.write(download.raw.read())
                print ('written...')
                photo_number = photo_number - 1
                if photo_number == glasses_original_dir_filenum:
                    break

            for index_num in range(icloud_glasses_photo_number, glasses_original_dir_filenum, -1):
                #print ('daplication loop')
                l_index_file_name = glob.glob('/Users/shimadatakuyume/iCloud_pi/icloud_photos/glasses/glasses_original/'+str(index_num)+'.*')
                s_index_file_name = str(l_index_file_name[0])
                #print (s_index_file_name)
                dap_pair = ins_check_daplication.check_daplication_for_single_file(s_index_file_name)
                if dap_pair != []:
                    print('There is daplication file(s)')
                    print(dap_pair)
                    all_daplication_pair.append(dap_pair)

        if all_daplication_pair != []:
            print('There is daplication file(s)')
            print(all_daplication_pair)
        else:
            print('no daplication')
                
    else:
        print('no update')

    # 画像の重複チェック
    print('Run Daplication check?(y/n)')
    daplication_select = input('y/n? >> ')

    if daplication_select == 'y':
        daplication_pair = ins_check_daplication.find_daplication_with_Brute_force_search()
        if daplication_pair == []:
            print ('no daplication')
        else :
            print('There is daplication file(s)')
            print(daplication_pair)
    else :
        pass
    