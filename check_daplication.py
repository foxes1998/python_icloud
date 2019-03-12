import os
import numpy as np
import cv2 as cv

class check_daplication:
    def __init__(self, image_dir_path):
        self.image_dir_path = image_dir_path

    # 指定されたパスの中のファイル名リストを返す(ディレクトリが存在すれば警告をだす) 
    def get_file_list(self):
        file_name_list = []
        for filename in os.listdir(image_dir_path):
            if os.path.isfile(os.path.join(image_dir_path, filename)):
                file.append(filename)
            else :
                print("Warning:There is a directory in"+ image_dir_path)

        self.file_list = file_name_list
        return self.file_list

    # 2つの画像ファイルパスを受け取ってakaze特徴量を元に特徴点マッチングを行い、特徴点が閾値以上で一致した数を返す
    def get_akaze_feature_value(self, image_file_path_1, image_file_path_2):
        self.image_file_path_1 = image_file_path_1
        self.image_file_path_2 = image_file_path_2
        img1 = cv2.imread(self.image_file_path_1,0)
        img2 = cv2.imread(self.image_file_path_2,0)
        #特徴抽出機の生成
        detector = cv2.AKAZE_create()
        #kpは特徴的な点の位置 destは特徴を現すベクトル
        kp1, des1 = detector.detectAndCompute(img1, None)
        kp2, des2 = detector.detectAndCompute(img2, None)
        #特徴点の比較機
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1,des2, k=2)
        #割合試験を適用
        good = []
        match_param = 0.2
        for m,n in matches:
            if m.distance < match_param*n.distance:
                good.append([m])
        return len(good)