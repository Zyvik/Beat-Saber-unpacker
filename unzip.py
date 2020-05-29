from os import listdir, remove, rename
import zipfile
import json


def get_zip_files_list(path=None):
    """Gets file names without .zip extensions"""
    files_list = listdir(path)
    return [f[:-4] for f in files_list if f[-4:] == '.zip']


def extract_files(file_list):
    for file in file_list:
        with zipfile.ZipFile(f"{file}.zip", 'r') as zip:
            zip.extractall(f"{file}/")


def get_song_name(file):
    with open(f"{file}/info.dat", "r") as info:
        info_dict = json.load(info)
        name = info_dict.get('_songName')
        author = info_dict.get('_songAuthorName')
        return f"{author} - {name}"


def rename_new_folders(file_list):
    for path in file_list:
        new_name = get_song_name(path)
        rename(path, new_name)


def remove_zip_files(file_list):
    for file in file_list:
        remove(f"{file}.zip")


def main():
    new_files = get_zip_files_list()
    extract_files(new_files)
    rename_new_folders(new_files)
    remove_zip_files(new_files)


main()
