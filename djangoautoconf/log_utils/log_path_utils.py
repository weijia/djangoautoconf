import os

from ufs_tools.folder_tool import ensure_dir


def get_log_file_path(folder, log_file_name, ext=".log"):
    log_folder_relative_path = os.path.join('logs', folder)
    log_filename = '%s%s' % (log_file_name, ext)
    current_dir = os.path.join(os.getcwd())
    folder_log_full_path = os.path.join(current_dir, log_folder_relative_path)
    log_full_path = os.path.join(folder_log_full_path, log_filename)
    ensure_dir(folder_log_full_path)
    return log_full_path
