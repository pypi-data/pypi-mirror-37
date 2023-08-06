from subprocess import call
import platform
import sys
import time
import socket
from requests import get
import types

platform = platform.system()

version = "1.0"

def getClear():
    if platform == "Windows":
        clearCMD = "cls"
    else:
        clearCMD = "clear"
    return clearCMD


clearCMD = getClear()


def clear():
    if platform == "Windows":
        call(["cls"], shell=True)
    else:
        call(["clear"], shell=True)


def slowPrint(text, rate="MISSING"):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        if rate == "MISSING":
            time.sleep(0.05)
        else:
            time.sleep(rate)

def revPrint(text):
    print(text[::-1])


def mock(text):
    meme = ""
    z = True
    for char in text:
        if z:
            meme += char.lower()
        else:
            meme += char.upper()
        if char != ' ':
            z = not z
    print(meme)

def pagedPrint(text, confirmation):
    input(confirmation)
    print(text)

# Prints local loopback address
def localIP():
    try:
        hostname = socket.gethostname()
        loIP = socket.gethostbyname(hostname)
    except:
        print("Unable to get Hostname and IP")

    return loIP


def externalIP():
    return get('https://api.ipify.org').text

def version():
    print(version)

def getImports():
    for name, val in globals().items():
        if isinstance(val, types.ModuleType):
            yield str(val.__name__)

def imports():
    print(list(getImports()))
