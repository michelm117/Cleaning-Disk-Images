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
        self.parent_inode = parent_inode
        self.filename = filename
        self.partition = partition
        self.id = file_id
        self.name_type = name_type
        self.filesize = filesize
        self.alloc = alloc
        self.used = used
        self.inode = inode
        self.meta_type = meta_type
        self.mode = mode
        self.nlink = nlink
        self.uid = uid
        self.gid = gid
        self.md5 = md5
        self.sha1 = sha1
        self.mtime = mtime
        self.mtime_txt = mtime_txt
        self.ctime = ctime
        self.ctime_txt = ctime_txt
        self.atime = atime
        self.atime_txt = atime_txt
        self.crtime = crtime
        self.crtime_txt = crtime_txt
        self.dtime = dtime
        self.dtime_txt = dtime_txt,
        self.libmagic = libmagic

    def __str__(self) -> str:
        st = "parent_inode: %s\nfilename: %s\npartition: %s\nid: %s\nname_type: %s\nfilesize: %s\nalloc: %s\nused: %s\ninode: %s\nmeta_type: %s\nmode: %s\nnlink: %s\nuid: %s\ngid: %s\nmd5: %s\nsha1: %s\nmtime: %s\nmtime_txt: %s\nctime: %s\nctime_txt: %s\natime: %s\natime_txt: %s\ncrtime: %s\ncrtime_txt: %s\nmtime: %s\ndtime_txt: %s" % (
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
