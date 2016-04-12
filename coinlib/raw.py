import os
import shutil
import tarfile
import zipfile
from os.path import join, exists, split

from coinlib.util import get_package_cache_folder_path, download_package, copy_dir


def just_unpack(archive_path, unpack_dir):
    path, filename = split(archive_path)
    if filename.endswith('.tar.gz') or filename.endswith('.tar.bz2'):
        tarfile.open(archive_path).extractall(unpack_dir)
    if filename.endswith('.zip'):
        with zipfile.ZipFile(archive_path, "r") as z:
            z.extractall(unpack_dir)


def unpack_raw(archive_path, download_dir, sub_folder):

    unpack_dir = download_dir
    if sub_folder is not None:
        unpack_dir = join(download_dir, sub_folder)
    just_unpack(archive_path, unpack_dir)

    sub_dirs = os.listdir(download_dir)
    if len(sub_dirs) != 1:
        raise Exception('Package {0} is expected to contain one folder inside {1}'.format(archive_path, download_dir))
    subdir = sub_dirs[0]

    package_dir = join(download_dir, subdir)
    return package_dir


def install_raw_package(cache_folder, url_or_path, ignore_cache, destination, sub_folder):
    package_path = url_or_path
    download_dir = get_package_cache_folder_path(cache_folder, sub_folder)
    if not exists(url_or_path):
        package_path = download_package(download_dir, url_or_path, ignore_cache)
    print("Package file: %s" % package_path)

    unpack_dir = unpack_raw(package_path, download_dir, sub_folder)
    print("Unpacked to: %s" % unpack_dir)

    copy_dir(unpack_dir, destination)
    print("Copied to: %s" % destination)
