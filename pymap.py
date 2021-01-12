from threading import Thread, Lock
import socket
import concurrent.futures
from time import time
from sys import argv

if len(argv) != 3:
	print("USAGE: ")
	print("[IP] [STARTPORT-ENDPORT]")
	exit(1)

ports = argv[2].split('-')
ip = socket.gethostbyname(argv[1])

ts = time()

def scan(ip, port):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.settimeout(6)
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

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
	for port in range(int(ports[0]), int(ports[1]) + 1):
		executor.submit(scan, ip, port)

td = time() - ts

print("Done in in " + str(td) + " sec.")
