
#-*- coding:utf-8 -*-
import os
import re
import numpy as np
import cv2 as cv
import time
import random

from tqdm import tqdm
from natsort import natsorted
from multiprocessing import Pool

class check_daplication:
    def __init__(self, image_dir_path):
        self.image_dir_path = image_dir_path

    # 指定されたパスの中のファイル名リストを返す(ディレクトリが存在すれば警告をだす) 
    def get_file_list(self):
        file_name_list = []
        for filename in os.listdir(self.image_dir_path):
            if re.match('\.', filename):
                print('.hoge file exist')
            elif os.path.isfile(os.path.join(self.image_dir_path, filename)):
                file_name_list.append(filename)
            else :
                print("Warning:There is a directory in"+ self.image_dir_path)

        self.file_list = file_name_list
        return self.file_list

    # 2つの画像ファイルパスを受け取ってakaze特徴量を元に特徴点マッチングを行い、特徴点が閾値以上で一致した数を返す
    def get_akaze_feature_value(self, image_file_path_1, image_file_path_2):
        self.image_file_path_1 = image_file_path_1
        self.image_file_path_2 = image_file_path_2
        try:
            img1 = cv.imread(self.image_file_path_1,0)
            #cv.imwrite('1.jpg', img1)
        except:
            print ('faild to loade'+ self.image_file_path_1)
        try:
            img2 = cv.imread(self.image_file_path_2,0)
            #cv.imwrite(str(random.random())+'2.jpg', img2)
        except:
            print ('faild to loade'+ self.image_file_path_2)
        #速度向上のためのリサイズ
        resize_width = 300
        img_height_1, img_width_1 = img1.shape[:2]
        img_height_2, img_width_2 = img2.shape[:2]
        resize_height1 = (resize_width / img_width_1) * img_height_1
        resize_height2 = (resize_width / img_width_2) * img_height_2
        img1 = cv.resize(img1,(int(resize_width),int(resize_height1)))
        img2 = cv.resize(img2,(int(resize_width),int(resize_height2)))
        #特徴抽出機の生成
        detector = cv.AKAZE_create()
        #kpは特徴的な点の位置 destは特徴を現すベクトル
        kp1, des1 = detector.detectAndCompute(img1, None)
        kp2, des2 = detector.detectAndCompute(img2, None)
        #特徴点の比較機
        bf = cv.BFMatcher()
        matches = bf.knnMatch(des1,des2, k=2)
        #割合試験を適用
        good = []
        match_param = 0.1
        for m,n in matches:
            if m.distance < match_param*n.distance:
                good.append([m])
        return len(good)

    # 全画像を総当たりでakaze特徴を求めて重複していると思われる画像のファイル名の組みを返す
    def find_daplication_with_Brute_force_search(self):
        daplication_pair = []
        all_file_list = natsorted(check_daplication.get_file_list(self))
        for i in all_file_list:
            print('for '+ i +' File')
            for j in tqdm(all_file_list):
                if i == j or all_file_list.index(i) > all_file_list.index(j):
                    pass
                else:
                    akaze_match_num = check_daplication.get_akaze_feature_value(self, self.image_dir_path + i, self.image_dir_path + j)
                    #print(self.image_dir_path + i +", "+ self.image_dir_path + j +" Match Number:"+ str(akaze_match_num))
                    if akaze_match_num > 0:
                        daplication_pair.append([self.image_dir_path + i, self.image_dir_path + j, akaze_match_num])

        return daplication_pair
                    
    def check_daplication_for_single_file(self, single_file_path):
        daplication_file = []
        self.single_file_path = single_file_path
        all_file_list = natsorted(check_daplication.get_file_list(self))
        for i in tqdm(all_file_list):
            if (self.single_file_path != self.image_dir_path+i) :
                akaze_match_num = check_daplication.get_akaze_feature_value(self, self.single_file_path, self.image_dir_path + i)
            # print(single_file_path+ ", "+ self.image_dir_path + i +" Match Number:"+ str(akaze_match_num))
                if akaze_match_num > 0:
                    daplication_file.append([single_file_path, self.image_dir_path+i, akaze_match_num])
        
        return daplication_file