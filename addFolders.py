import os
import shutil
def folder_creation_helpe(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(folder_name," Folder created")
    else:
        print(folder_name," Folder already exists")


def delete_folder(folder_name):
    for filename in os.listdir(folder_name):
        file_path = os.path.join(folder_name, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


