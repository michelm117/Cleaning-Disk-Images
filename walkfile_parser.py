import string

from filesystem import Filesystem
from filesystem_file import Filesystem_file


def parse(filepath: string) -> list[Filesystem]:
    with open(filepath) as file:
        nbr_fs = 0
        is_collecting_fs_info = False
        is_collecting_file_info = False
        all_file_systems: list[Filesystem] = []
        para = dict()
        for line in file:
            line = line.strip()

            # Start of filesystem info paragraph
            if "# fs start:" in line:
                nbr_fs += 1
                is_collecting_fs_info = True
                is_collecting_file_info = False
                continue

            # Inside of filesystem info paragraph
            elif is_collecting_fs_info and line != "":
                key, val = line.split(": ")
                para[key] = val
                continue

            # End of filesystem info paragraph
            elif is_collecting_fs_info and line == "":
                is_collecting_fs_info = False
                is_collecting_file_info = True
                fs = Filesystem(para.get('partition_offset'),
                                para.get('sector_size'),
                                para.get('block_size'),
                                para.get('ftype'),
                                para.get('ftype_str'),
                                para.get('block_count'),
                                para.get('first_block'),
                                para.get('last_block'))
                all_file_systems.append(fs)
                para = dict()
                continue

            if "end of volume" in line and is_collecting_file_info:
                is_collecting_file_info = False
                continue

            elif is_collecting_file_info and line != "":
                key, val = line.split(": ")
                para[key] = val
                continue

            elif is_collecting_file_info and line == "":
                fs_file = Filesystem_file(para.get('parent_inode'),
                                          para.get('filename'),
                                          para.get('partition'),
                                          para.get('file_id'),
                                          para.get('name_type'),
                                          para.get('filesize'),
                                          para.get('alloc'),
                                          para.get('used'),
                                          para.get('inode'),
                                          para.get('meta_type'),
                                          para.get('mode'),
                                          para.get('nlink'),
                                          para.get('uid'),
                                          para.get('gid'),
                                          para.get('md5'),
                                          para.get('sha1'),
                                          para.get('mtime'),
                                          para.get('mtime_txt'),
                                          para.get('ctime'),
                                          para.get('ctime_txt'),
                                          para.get('atime'),
                                          para.get('atime_txt'),
                                          para.get('crtime'),
                                          para.get('crtime_txt'),
                                          para.get('dtime'),
                                          para.get('dtime_txt'),
                                          para.get('libmagic')
                                          )

                all_file_systems[-1].add_file(fs_file)
                # print(fs_file)
                para = dict()
                continue

            elif "# clock: " in line:
                break

        return all_file_systems
