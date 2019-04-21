#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys
import os
import glob
import os.path

#ファイル名のリネーム

def listdir_nohidden(path):
    retnum = 0
    for f in os.listdir(path):
        if not f.startswith('.'):
            retnum = retnum + 1
        else:
            retnum = retnum + 0
    return retnum

if __name__ == '__main__':
    glasses_original_dir_pass = '/Users/shimadatakuyume/iCloud_pi/icloud_photos/glasses/glasses_original/'
    glasses_original_dir_filenum = listdir_nohidden(glasses_original_dir_pass)
    missing_number = 0
    change_counter = 0
    loop_counter = 0
    while True:
        hit_list = glob.glob(glasses_original_dir_pass + str(loop_counter+1) +'.*')
        if hit_list == []:
            missing_number = missing_number+1
        elif not len(hit_list) == 1:
            print('error')
            sys.exit
        else:
            root, ext = os.path.splitext(hit_list[0])
            os.rename(hit_list[0], glasses_original_dir_pass+str(loop_counter+1-missing_number)+ext)
            change_counter = change_counter + 1

        if change_counter == glasses_original_dir_filenum:
            break
        
        loop_counter = loop_counter+1

    if missing_number == 0:
        print ('no change')
    else:
        print (str(missing_number) +' change')