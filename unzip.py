import os
import json
import zipfile


def get_beatmaps_file_names(path=None):
    """Returns beatmap's file names without .zip extensions."""
    files_list = os.listdir(path)
    return [f[:-4] for f in files_list if f[-4:] == '.zip' and len(f) == 44]


def extract_files(file_list):
    for file in file_list:
        # if directory doesn't exist - extract all files
        if not os.path.isdir(f"{file}"):
            with zipfile.ZipFile(f"{file}.zip", 'r') as zip:
                zip.extractall(f"{file}/")


def get_song_name(file):
    with open(f"{file}/info.dat", "r") as info:
        info_dict = json.load(info)
        name = info_dict.get('_songName', 'Unknown_author')
        author = info_dict.get('_songAuthorName', 'Unknown_name')
        return f"{author} - {name}"


def clean_song_name(song_name):
    """Removes forbiden characters from song name"""
    invalid_chars = '<>:;[]\"/\\|?*'
    for character in invalid_chars:
        song_name = song_name.replace(character, '')
    return song_name


def rename_new_folders(file_list):
    for path in file_list:
        new_name = get_song_name(path)
        clean_name = clean_song_name(new_name)
        os.rename(path, clean_name)  # Can throw an exception


def remove_zip_files(file_list):
    for file in file_list:
        os.remove(f"{file}.zip")


def main():
    new_files = get_beatmaps_file_names()
    extract_files(new_files)
    rename_new_folders(new_files)
    remove_zip_files(new_files)


if __name__ == '__main__':
    main()
