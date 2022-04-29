class Filesystem_file:
    def __init__(self, parent_inode, filename, partition,
                 file_id, name_type, filesize,
                 alloc, used, inode, meta_type, mode,
                 nlink, uid, gid, md5, sha1,
                 mtime, mtime_txt,
                 ctime, ctime_txt,
                 atime, atime_txt,
                 crtime, crtime_txt,
                 dtime, dtime_txt,
                 libmagic
                 ) -> None:
        self.parent_inode: str = parent_inode
        self.filename: str = filename
        self.partition: str = partition
        self.id: str = file_id
        self.name_type: str = name_type
        self.filesize: str = filesize
        self.alloc: str = alloc
        self.used: str = used
        self.inode: str = inode
        self.meta_type: str = meta_type
        self.mode: str = mode
        self.nlink: str = nlink
        self.uid: str = uid
        self.gid: str = gid
        self.md5: str = md5
        self.sha1: str = sha1
        self.mtime: str = mtime
        self.mtime_txt: str = mtime_txt
        self.ctime: str = ctime
        self.ctime_txt: str = ctime_txt
        self.atime: str = atime
        self.atime_txt: str = atime_txt
        self.crtime: str = crtime
        self.crtime_txt: str = crtime_txt
        self.dtime: str = dtime
        self.dtime_txt: str = dtime_txt,
        self.libmagic: str = libmagic

    def __str__(self) -> str:
        st = "parent_inode: {0}\nfilename: {1}\npartition: {2}\nid: {3}\nname_type: {4}\nfilesize: {5}\nalloc: {6}\nused: {7}\ninode: {8}\nmeta_type: {9}\nmode: {10}\nnlink: {11}\nuid: {12}\ngid: {13}\nmd5: {14}\nsha1: {15}\nmtime: {16}\nmtime_txt: {17}\nctime: {18}\nctime_txt: {19}\natime: {20}\natime_txt: {21}\ncrtime: {22}\ncrtime_txt: {23}\nmtime: {24}\ndtime_txt: {25}".format(
            self.parent_inode,
            self.filename,
            self.partition,
            self.id,
            self.name_type,
            self.filesize,
            self.alloc,
            self.used,
            self.inode,
            self.meta_type,
            self.mode,
            self.nlink,
            self.uid,
            self.gid,
            self.md5,
            self.sha1,
            self.mtime,
            self.mtime_txt,
            self.ctime,
            self.ctime_txt,
            self.atime,
            self.atime_txt,
            self.crtime,
            self.crtime_txt,
            self.dtime,
            self.dtime_txt,
            self.libmagic
        )
        return st
