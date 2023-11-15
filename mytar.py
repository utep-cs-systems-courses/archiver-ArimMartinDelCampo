#importing modules
import sys
import os
import struct


#specifyin header size in bytes
MAGIC = b"mytar" 
HDR_SIZE = 16 
NAME_SIZE = 12 


def pack_string(s, n):
    
    return struct.pack(f"{n}s", s.encode())

def unpack_string(b):
    
    return struct.unpack(f"{len(b)}s", b)[0].decode().rstrip("\x00")

def create_archive(files, output):
    
    output.write(MAGIC) 
    for file in files:
        name = os.path.basename(file) 
        size = os.path.getsize(file) 
        output.write(pack_string(name, NAME_SIZE)) 
        output.write(struct.pack("I", size)) 
        with open(file, "rb") as f:
            output.write(f.read()) 

def extract_archive(input, directory):
    
    magic = input.read(len(MAGIC)) 
    if magic != MAGIC:
        print("Invalid archive format")
        return
    while True:
        name = unpack_string(input.read(NAME_SIZE))
        if not name:
            break 
        size = struct.unpack("I", input.read(4))[0] 
        content = input.read(size) 
        path = os.path.join(directory, name) 
        with open(path, "wb") as f:
            f.write(content) 

#here i defined the main fucntion
def main():
    if len(sys.argv) < 3:
        print("Type to the terminal like this mytar.py c|x files|directory")
        return
    mode = sys.argv[1] 
    if mode == "c":
        files = sys.argv[2:] 
        create_archive(files, sys.stdout.buffer) 
    elif mode == "x":
        directory = sys.argv[2] 
        extract_archive(sys.stdin.buffer, directory) 
    else:
        print("Invalid mode")

# main function
if __name__ == "__main__":
    main()
