import re

filepath = "out/diskimages/ubuntu_os.img"
try:
    with open(filepath, "rb") as f:
        byte = f.read(512)
        i = 0
        while byte:
            # Do stuff with byte.
            i += 1
            byte = f.read(512)
            st = byte.decode('latin-1')
            if "geheim" in st.lower():
                print(st)
                print("Blockcount:", i)
                print("Block:", i * 512)
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

except IOError:
    print('Error While Opening the file!')
