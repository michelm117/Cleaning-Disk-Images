import argparse
from dis import dis
import logging
import os
import shutil
import subprocess
import sys

from cairo import Path
from lxml import etree

from walkfile_parser import parse

# Software needed:
#   - disktype
# anonymizer
# out
#   - anonymizer
#   - reports_path
#   - diskimages_path
#   - files_path


def _make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--quiet", action="store_true",
                        help="Write only errors to log")
    parser.add_argument("--d", action="store_true",
                        help="dry run")
    parser.add_argument("source", help="Path to the disk images")
    parser.add_argument("destination", help="Output destination")

    return parser


def _configure_logging(args, destina_path) -> logging.Logger:
    Logger = logging.getLogger()
    log_file = os.path.join(destina_path, "anonymizer.log")

    if args.quiet:
        level = logging.ERROR
    else:
        level = logging.INFO
    Logger.setLevel(level)

    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)

    streamHandler = logging.StreamHandler(sys.stdout)
    streamHandler.setLevel(level)
    streamHandler.setFormatter(formatter)
    Logger.addHandler(streamHandler)

    fileHandler = logging.FileHandler(log_file)
    fileHandler.setLevel(level)
    fileHandler.setFormatter(formatter)
    Logger.addHandler(fileHandler)

    #logging.basicConfig(filename=log_file, level=level, format=log_format)
    return Logger


def init_destination(destina_path: Path, args):
    if os.path.exists(destina_path):
        enter = input(
            "Destination folder exists, content will be deleted. Continue? [Y/n]: ")

    if enter.upper() == 'N':
        print("No\n")
        exit()
    print("Yes\n")

    # TODO: Delete after release
    if not args.d:
        shutil.rmtree(destina_path)
    else:
        try:
            os.remove(os.path.join(destina_path, "anonymizer.log"))
            shutil.rmtree(os.path.join(destina_path, "reports"))
            shutil.rmtree(os.path.join(destina_path, "files"))
        except Exception as _e:
            pass

    reports_path = os.path.join(destina_path, "reports")
    diskimages_path = os.path.join(destina_path, "diskimages")
    files_path = os.path.join(destina_path, "files")

    if not args.d:
        for new_dir in destina_path, reports_path, diskimages_path, files_path:
            os.makedirs(new_dir)

    return reports_path, diskimages_path, files_path


def init_source(source_path: Path, Logger: logging.Logger):
    if not os.path.exists(source_path):
        Logger.error("Image does not exits")
        exit()

    if not os.path.isdir(source_path):
        Logger.error("Source path is not a folder.")
        exit()


def config_img_workspace(Logger, disk_image_name, disk_images_path,
                         source_dir, reports_path, files_path,
                         args):
    # Copy disk image and use the copy for processing
    Logger.info("Creating a copy of diskimage '%s'." % disk_image_name)
    disk_image_path = os.path.join(disk_images_path, disk_image_name)
    if not args.d:
        shutil.copyfile(os.path.join(source_dir, disk_image_name),
                        disk_image_path)

    # Create disk specif directories
    Logger.info("Creating diskimage specific subdirectories for '%s'." %
                disk_image_name)
    _reports_path = os.path.join(reports_path, disk_image_name)
    _files_path = os.path.join(files_path, disk_image_name)
    for new_dir in _reports_path, _files_path:
        os.makedirs(new_dir)
    return _reports_path, _files_path, disk_image_path


def main():
    parser = _make_parser()
    args = parser.parse_args()

    # Configure destination
    destina_path = os.path.abspath(args.destination)
    reports_path, diskimages_path, files_path = init_destination(
        destina_path, args)

    Logger = _configure_logging(args, destina_path)

    # Configure source
    source_dir = os.path.abspath(args.source)
    init_source(source_dir, Logger)

    for disk_image_name in os.listdir(source_dir):
        _reports_path, _files_path, disk_image_path = config_img_workspace(Logger, disk_image_name, diskimages_path,
                                                                           source_dir, reports_path, files_path,
                                                                           args)
        analyse_disk_image(Logger, disk_image_name, disk_image_path,
                           _reports_path, diskimages_path, _files_path)


def disktype(Logger, disk_image_name, disk_image_path, reports_path):
    """ Detect the content format of the disk image.

    Args:
        Logger (logging.Logger): Logger
        disk_image_name (string): The name of the disk image
        disk_image_path (path): The path of the disk image
        reports_path (path): The path where the disktype report should be saved

    Returns:
        string: content format of disk image.
    """
    Logger.info("Detecting the content format of '%s'." % disk_image_name)
    disktype = os.path.join(reports_path, "disktype.txt")

    # Run disktype on the disk image and save output to results_dir
    subprocess.call(
        "disktype '%s' > '%s'" % (disk_image_path, disktype), shell=True
    )

    # pull filesystem info from disktype.txt
    disk_fs = ""
    try:
        for line in open(disktype, "r"):
            if "file system" in line:
                disk_fs = line.strip()
    except:  # handle non-Unicode chars
        Logger.error("Can't read from %s." % disktype)
        exit()

    return disk_fs.lower()


def fiwalk(Logger: logging.Logger, disk_fs, disk_image_name,
           disk_image_path, reports_path):
    """ file and inode walk

    Args:
        Logger (logging.Logger): _description_
        disk_fs (_type_): _description_
        disk_image_name (_type_): _description_
        disk_image_path (_type_): _description_

    Raises:
        Exception: _description_
    """
    if not any(
        fs in disk_fs.lower()
        for fs in (
            "ntfs",
            "fat",
            "ext",
            "iso9660",
            "hfs+",
            "ufs",
            "raw",
            "swap",
            "yaffs2",
        )
    ):
        Logger.error("Filesystem is not supported.")
        raise Exception("Filesystem is not supported.")

    Logger.info("File and inode walk on '%s'." %
                disk_image_name)
    fiwalk_file = os.path.abspath(
        os.path.join(reports_path, "dfxml.xml"))
    try:
        subprocess.check_output(
            ["fiwalk", "-f", "-T", fiwalk_file, disk_image_path]
        )
    except subprocess.CalledProcessError as e:
        Logger.error("Fiwalk could not create DFXML for disk %s" %
                     (disk_image_name))
    return fiwalk_file


def analyse_disk_image(Logger, disk_image_name, disk_image_path,
                       reports_path, diskimages_path, files_path):
    disk_fs = disktype(Logger, disk_image_name, disk_image_path, reports_path)
    fiwalk_file = fiwalk(Logger,  disk_fs, disk_image_name,
                         disk_image_path, reports_path)
    filesystems = parse(fiwalk_file)
    for fs in filesystems:
        print("\n%s" % fs)
        print(fs.files.get(list(fs.files)[-1]))


if __name__ == "__main__":
    main()
