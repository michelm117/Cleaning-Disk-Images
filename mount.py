import difflib
import re
import subprocess
import os


def get_os_type(mount_source):
    tune2fs = subprocess.check_output("sudo tune2fs -l %s" %
                                      mount_source, shell=True).decode("utf-8")
    for line in tune2fs.split('\n'):
        if 'Filesystem OS type' in line:
            info = re.sub(' +', '', line).split(':')[1]
            return info
    return None


image = "out/diskimages/ubuntu_os.img"

output = subprocess.check_output(
    "fdisk -l %s" % image, shell=True).decode("utf-8")
lines = output.lower().split("\n")
relevant_lines = []
for i, line in enumerate(lines):
    if "device" in line.lower() and "boot" in line.lower() and "start" in line.lower():
        relevant_lines = lines[i:]

indices = [i for i, s in enumerate(relevant_lines) if 'linux' in s]

subprocess.check_output(
    "sudo losetup -f -P %s" % image, shell=True)
output = subprocess.check_output(
    "sudo losetup -l", shell=True).decode("utf-8")

loop_device = output.split("\n")[-2].split()[0]
ls_cmd = "sudo ls -l %s*" % loop_device
output = subprocess.check_output(ls_cmd, shell=True).decode("utf-8")

for device in indices:
    mount_source = output.split("\n")[device].split()[-1]
    mount_target = mount_source.split("/")[-1]
    mount_target = os.path.join("mnt", mount_target)
    os.makedirs(mount_target)
    subprocess.check_output(
        "sudo mount %s %s" % (mount_source, mount_target), shell=True)

    os_type = get_os_type(mount_source)
    print(os_type)
    # umount and detach loop device
    subprocess.check_output("sudo umount %s" % mount_source, shell=True)
    subprocess.check_output("sudo losetup -d %s" % loop_device, shell=True)
    os.rmdir(mount_target)
