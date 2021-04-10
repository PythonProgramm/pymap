from threading import Thread, Lock
import socket
import concurrent.futures
from time import time
from sys import argv

ports = [20, 21, 22, 23, 25, 53, 65, 67, 68, 69, 88, 80, 110, 123, 135, 137, 138, 139, 143, 161, 162, 389, 443, 445, 500, 993, 995, 1433, 1433, 8080, 8088, 8443, 1494, 2512, 2513, 2598, 2869, 3389, 4500, 2222, 2020, 2022]
version = "2.0"


if "-v" in argv or "--version" in argv:
    print("pymap version: " + str(version))
    exit(0)

if len(argv) < 3:
	print("USAGE: ")
	print("""pymap [OPTIONS] [IP]
              -sU | use UDP scan.
              -sT | use TCP scan.
              -sV | try to find the versions of ports.
    -v, --version | print version of pymap.""")
	exit(1)

if "-sT" in argv and "-sU" in argv:
    print("You can only use -sU or -sT!\nQUITTING!")
    exit(1)

if "-sT" in argv:
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
elif "-sU" in argv:
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
else:
    print("Please use -sT or -sU\nQUITTING!")
    exit(-1)

ip = socket.gethostbyname(argv[-1])

ts = time()

def scan(ip, port, soc):
    soc.settimeout(2)
    res = soc.connect_ex((ip, port))
    if res == 0:
        print("Port " + str(port) + " OPEN []")

def scanVersion(ip, port, soc):
    soc.settimeout(2)
    res = soc.connect_ex((ip, port))

    if res == 0:
        banner = ""
        if port == 80:
            soc.send(b'GET / HTML/1.1 \r\n')

        try:
            banner = soc.recv(1024)
            banner = banner.decode("UTF-8", errors='replace')

            if port == 80:
                tmp = banner.split('\n')
                for line in tmp:
                    if line.strip().lower().startswith("server"):
                        banner = line.strip()

        except:
            pass

        print("Port " + str(port) + ' OPEN [' + banner.rstrip() + "]")

if "-sV" in argv:
    scanV = True
else:
    scanV = False

if "-sT" in argv:
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if scanV:

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            for port in ports:
                executor.submit(scanVersion, ip, port, soc)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            for port in ports:
                executor.submit(scan, ip, port, soc)
elif "-sU" in argv:
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if scanV:

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            for port in ports:
                executor.submit(scanVersion, ip, port, soc)

    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            for port in ports:
                executor.submit(scan, ip, port, soc)
else:
    print("Please use -sT or -sU\nQUITTING!")
    exit(-1)



td = time() - ts

print("Done in in " + str(td) + " sec.")
