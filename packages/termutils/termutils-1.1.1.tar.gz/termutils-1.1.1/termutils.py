from subprocess import call
import platform
import sys
import time
import socket
from requests import get

# Get platform for clear func
platform = platform.system()

r_version = "1.1.1"


def clear():

    # Check platform
    if platform == "Windows":
        # Call clear based on OS, cls for windows
        call(["cls"], shell=True)

    else:
        # else is clear
        call(["clear"], shell=True)

# Slow print
def sprint(text, rate="MISSING"):
    # Iterate over every letter
    for c in text:
        # Write the letter
        sys.stdout.write(c)
        # Flush the buffer
        sys.stdout.flush()

        # Check if rate of print doesn't exist
        if rate == "MISSING":
            time.sleep(0.05)

            # if it does, change the delay between letters
        else:
            time.sleep(rate)

    print("\n")


def reverse(text):
    # output the string in reverse with slices
    return text[::-1]


def mock(text):
    meme = ""
    z = True

    # Iterate over each character in the string
    for char in text:
        if z:
            # make each odd character lowercase
            meme += char.lower()

        else:
            # make each even character capital
            meme += char.upper()
        # ignore if it is a space

        if char != ' ':
            z = not z
            print(z)
    # Output the result
    return meme


# Prints local loopback address
def localIP():
    try:
        # Use socket to get the hostname
        hostname = socket.gethostname()
        # get the ip from the hostname
        loIP = socket.gethostbyname(hostname)

    except Exception as e:
        # If there is any errors, print an error message with the exception
        print("Unable to get Hostname and IP: {}".format(e))

    # Return the result
    return loIP


def externalIP():
    # using get from requests, grab the data from ipify
    return get('https://api.ipify.org').text

def version():
    # Output the version var
    print(r_version)

