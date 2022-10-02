from time import sleep
import tqdm
import socket
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
host = "192.168.1.120"
port = 5001

dirs = ["/home/pawelsmigielski/projekty/sync-tool/pliki/", "/home/pawelsmigielski/projekty/sync-tool/pliki2/"]
for dir in dirs:
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    for file in files:
        s = socket.socket()
        s.connect((host, port))
        filesize = os.path.getsize(dir+file)
        s.send(f"{dir+file}{SEPARATOR}{filesize}".encode())
        progress = tqdm.tqdm(range(filesize), f"Sending {dir+file}", unit="KB", unit_scale=True, unit_divisor=1024)
        with open(dir+file, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                s.sendall(bytes_read)
                progress.update(len(bytes_read))
        sleep(5)
        s.close()