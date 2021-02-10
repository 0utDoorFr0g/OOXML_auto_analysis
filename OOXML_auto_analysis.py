import zipfile
import os
import shutil

def check_ooxml_file(path):
    """ check the file is OOXML file
    Args:
        path (string) : path to file to check
    Return:
        bool : if file is OOXML file return True, else return False
        None : if function raise exception return False
    """

    f = open(path,'rb')
    check_file_data = f.read()
    f.close()

    if check_file_data[:4] != b"\x50\x4B\x03\x04":
        return False

    check_file = zipfile.ZipFile(path)

    temp_directory = os.path.dirname(path) + "\\" + "temp"

    try:
         os.makedirs(temp_directory)
    except OSError:
        return None

    check_file.extractall(temp_directory)

    content_file = temp_directory + "\\" + "[Content_Types].xml"

    if os.path.isfile(content_file) == False:
        return False

    shutil.rmtree(temp_directory) 
    
    return True

print(check_ooxml_file(r"C:\Users\forgo\Desktop\testtt\abcd.zip"))