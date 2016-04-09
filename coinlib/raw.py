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

    temp_dir = download_dir

    unpack_dir = temp_dir
    if sub_folder is not None:
        unpack_dir = join(temp_dir, sub_folder)
    just_unpack(archive_path, unpack_dir)

    sub_dirs = os.listdir(temp_dir)
    if len(sub_dirs) != 1:
        raise Exception('Package %s is expected to contain one folder inside' % archive_path)
    subdir = sub_dirs[0]

    package_dir = join(temp_dir, subdir)
    return package_dir


def install_raw_package(cache_dir, cache_folder, url_or_path, ignore_cache, destination, sub_folder):
    package_path = url_or_path
    download_dir = get_package_cache_folder_path(cache_dir, cache_folder)
    if not exists(url_or_path):
        package_path = download_package(download_dir, url_or_path, ignore_cache)
    print("Package file: %s" % package_path)

    unpack_dir = unpack_raw(package_path, download_dir, sub_folder)
    print("Unpacked to: %s" % unpack_dir)

    install_to = destination
    copy_dir(unpack_dir, install_to)
    print("Copied to: %s" % install_to)

    shutil.rmtree(unpack_dir, ignore_errors=True)
    print("Cleaned unpack dir: %s" % unpack_dir)
