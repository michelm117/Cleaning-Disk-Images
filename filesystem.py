from filesystem_file import Filesystem_file


class Filesystem:
    def __init__(self, partition_offset, sector_size,
                 block_size, ftype,
                 ftype_str, block_count,
                 first_block, last_block) -> None:
        self.partition_offset = partition_offset
        self.sector_size = sector_size
        self.block_size = block_size
        self.ftype = ftype
        self.ftype_str = ftype_str
        self.block_count = block_count
        self.first_block = first_block
        self.last_block = last_block
        self.files = {}

    def add_file(self, file: Filesystem_file) -> None:
        self.files[file.inode] = file

    def __str__(self) -> str:
        files_st = ""
        for key, val in self.files.items():
            files_st = files_st + "%s: %s\n\t" % (key, val)
        st = "partition_offset: %s\nsector_size: %s\nblock_size: %s\nftype: %s\nftype_str: %s\nblock_count: %s\nfirst_block: %s\nlast_block: %s\nfiles: %s" % (
            self.partition_offset,
            self.sector_size,
            self.block_size,
            self.ftype,
            self.ftype_str,
            self.block_count,
            self.first_block,
            self.last_block,
            len(self.files))
        return st
