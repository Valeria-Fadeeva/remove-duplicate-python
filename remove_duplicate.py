#!/usr/bin/env python3


import os
import sys
import zlib


def crc32(filename):
    try:
        if os.path.getsize(filename) == 0:
            raise Exception('Zero size')
        with open(filename, 'rb') as fhandle:
            hash_ = 0
            while True:
                file_string = fhandle.read(65536)
                if not file_string:
                    break
                hash_ = zlib.crc32(file_string, hash_)
            return "%08X" % (hash_ & 0xFFFFFFFF)
    except:
        return "ERROR"


def get_file_list(root_dir):
    file_list = []
    for folder, folders, files in os.walk(root_dir, followlinks=False):
        for file in files:
            #print(os.path.join(folder, file))
            filename = os.path.join(folder, file)
            crc = crc32(filename)
            print(crc, filename)
            file_list.append([filename.replace(root_dir, ''), crc])

    return file_list


def get_duplicate(file_list_1, file_list_2):
    list_duplicate = []
    for element in file_list_1:
        if element in file_list_2:
            print('Finded duplicate', element)
            list_duplicate.append(element)

    return list_duplicate


def remove_duplicate(list_duplicate, root_dir_2):
    for i in list_duplicate:
        f = os.path.join(os.path.abspath(root_dir_2), i[0].replace(os.sep, '', 1))
        print('Remove duplicate', f)
        os.remove(f)


#def remove_empty_folders(root_dir_2):
    #folders = list(os.walk(root_dir_2))[1:]
    #for folder in folders:
        #if not folder[2]:
            #print('Delete empty folder', folder[0])
            #os.rmdir(folder[0])

# https://stackoverflow.com/questions/22001216/scan-files-recursively-and-delete-empty-directories-in-python
def remove_empty_folders(root_dir_2):
    index = 0

    for root, dirs, files in os.walk(root_dir_2):
        for dir in dirs:
            newDir = os.path.join(root, dir)
            index += 1
            print(str(index), "--->", newDir)

            try:
                os.removedirs(newDir)
                print("Delete empty folder", newDir)
            except:
                print("Directory not empty. Skip", newDir)


if __name__ == "__main__":
    root_dir_1 = sys.argv[1]  # новая папка
    root_dir_2 = sys.argv[2]  # старая папка (дубликаты для удаления)

    for directory in [root_dir_1, root_dir_2]:
        if not os.path.isdir(directory):
            raise ValueError("Not a directory: " + directory)

    if root_dir_1 == '/' or root_dir_2 == '/':
        raise ValueError("Root directory: " + directory)

    file_list_1 = get_file_list(root_dir_1)
    file_list_2 = get_file_list(root_dir_2)

    list_duplicate = get_duplicate(file_list_1, file_list_2)

    answer = input("Remove duplicate? Y/n ")
    if answer.lower() == 'y':
        remove_duplicate(list_duplicate, root_dir_2)
    else:
        exit(0)

    answer = input("Remove empty folders? Y/n ")
    if answer.lower() == 'y':
        remove_empty_folders(root_dir_2)
    else:
        exit(0)
