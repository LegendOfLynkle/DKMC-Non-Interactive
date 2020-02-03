# Don't Kill My Cat (DKMC)
This is a Non Interactive fork of the original Don't Kill My Cat by Mr-Un1k0d3r. The only changes that have been made are a refactor to be make the program not object oriented and operate only on command line arguments as opposed to an interactive menu.

Don't kill my cat is a tool that generates obfuscated shellcode that is stored inside of polyglot images. The image is 100% valid and also 100% valid shellcode. The idea is to avoid sandbox analysis since it's a simple "legit" image. For now the tool rely on PowerShell the execute the final shellcode payload.

Why it's called don't kill my cat? Since I suck at finding names for tools, I decided to rely on the fact that the default BMP image is a cat to name the tool. 

Presentation on how it works internally can be found here: https://github.com/Mr-Un1k0d3r/DKMC/blob/master/DKMC%20presentation%202017.pdf

# Basic Flow
* Generate shellcode (meterpreter / Beacon)
* Embed the obfuscated shellcode inside the image
* PowerShell download the image and execute the image as shellcode
* Get your shell

# Installation

```
$ git clone https://github.com/Mr-Un1k0d3r/DKMC 
$ cd DKMC
```

# Usage
Launching DKMC
```
$ python2 dkmc.py -s SHELLCODE -o OUTPUT -p POWERSHELL -u URL -i IMAGE
```
OR
```
$ ./dkmc.py -s SHELLCODE -o OUTPUT -p POWERSHELL -u URL -i IMAGE
```

The final step requires you to run the PowerShell oneliner on the victim system.

## Optional Aguments
Some arguments are optional and have defaults. These optional arguments with 
default values are as follows:

|Option|Default Value|
|:----:|:----:|
|-o/--output|out.bmp|
|-p/--powershell|exploit.ps|
|-i/--image|sample/default.bmp|

# Credit
Mr.Un1k0d3r RingZer0 Team 2016
