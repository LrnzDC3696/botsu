import os


def get_all_files(directory):
    """Gets all the files in a directory.

    Args:
      directory: The directory to get the files from.

    Returns:
      A list of all the files in the directory.
    """
    files = []
    for file in os.listdir(directory):
        path = os.path.join(directory, file)
        if os.path.isfile(path):
            files.append(path)

    return sorted(files)


TG_BACKUP_DIR = "/home/lrnzdc/Codes/telegram-backup-parser/backups/ChatExport_2023-02-27/"
USEFULL_DIR = [
    "photos",
    #     "round_video_messages",
    #     "video_files",
    #     "voice_messages",
]

files_ = {}
for dir_ in USEFULL_DIR:
    files = get_all_files(TG_BACKUP_DIR + dir_ + "/")
    files_2 = []

    for filesss in files:
        if filesss.endswith("thumb.jpg"):
            continue
        files_2.append(files)

    files_[dir_] = files_2
#     print(files)
#     print()
