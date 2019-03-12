import os

class check_daplication:
    def __init__(self, image_file_path):
        self.image_file_path = image_file_path

    # 指定されたパスの中のファイル名リストを返す(ディレクトリが存在すれば警告をだす) 
    def get_file_list(self):
        file_name_list = []
        for filename in os.listdir(image_file_path):
            if os.path.isfile(os.path.join(image_file_path, filename)):
                file.append(filename)
            else :
                print("Warning:There is a directory in"+ image_file_path)

        self.file_list = file_name_list
        return self.file_list

    def 

    