import zipfile
import os
import shutil

class FileInfo:
    def __init__(self, path):
        self.target_file_path = path
        self.unzip_file_path = ""
        self.ooxml_file_flag = False
        self.ooxml_file_type = "" # {xl | ppt | word}
        self.temp_path = ""

        if FileInfo.check_pk_zip_signature(self.target_file_path) == True:
            self.temp_path = os.path.dirname(self.target_file_path) + "\\" + "temp"
            os.makedirs(self.temp_path, exist_ok=True)

            self.unzip_file_path = self.temp_path + "\\" + "sample" + os.path.basename(self.target_file_path)
            os.mkdir(self.unzip_file_path)

            if FileInfo.unzip_file(self.target_file_path, self.unzip_file_path):

                if FileInfo.check_ooxml_file(self.unzip_file_path):
                    self.ooxml_file_flag = True
                    content_file = open(self.unzip_file_path + "\\" + "[Content_Types].xml","r")
                    content_data = content_file.read()
                    content_file.close()
                    if content_data.find("xl") != -1:
                        self.ooxml_file_type = "xl"
                    elif content_data.find("word") != -1:
                        self.ooxml_file_type = "word"
                    elif content_data.find("ppt") != -1:
                        self.ooxml_file_type = "ppt"
                    else:
                        self.ooxml_file_type = "another"

    def delete_unzip_file(self):
        """ delete unziped file package and directory

        Args:

        Return:
        """
        shutil.rmtree(self.unzip_file_path)

    @staticmethod
    def check_pk_zip_signature(path):
        """ check the file has PKZIP signature
        Args:
            path (string) : file path to check
        Return:
            bool : if file has PKZIP signature return True, else return False
            None : if function raise exception return None
        """
        try:
            f = open(path,"rb")
            file_data = f.read(4)
            f.close()
            if file_data != b"\x50\x4B\x03\x04":
                return False
            else:
                return True
        except:
            return None

    @staticmethod
    def unzip_file(target_path, extract_path):
        """ unzip target file to extract_path
        Args:
            target_path (string)  : file path to unzip
            extract_path (string) : unziped result will be placed this path
        Return:
            bool : if function succeed return True else return False
        """
        try:
            target_handle = zipfile.ZipFile(target_path)
            target_handle.extractall(extract_path)
            return True
        except:
            return False

    @staticmethod
    def check_ooxml_file(path):
        """ check the file is OOXML file
        Args:
            path (string) : path to unziped file to check
        Return:
            bool : if file is OOXML file return True, else return False
        """
        return os.path.isfile(path + "\\" + "[Content_Types].xml")

sample = [FileInfo("C:\\Users\\forgo\\Desktop\\testtt\\abcd" + str(i) + ".zip") for i in range(1,4)]
for i in sample:
    print(i.ooxml_file_type)
    i.delete_unzip_file()
shutil.rmtree(sample[0].temp_path)