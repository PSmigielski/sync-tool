import socket
import tqdm
import os
# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
syncdir="/home/poligon/sync/"
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
while True:   
    client_socket, address = s.accept() 
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    dirname = os.path.split(os.path.dirname(filename))[-1];
    hasDir = os.path.isdir(syncdir+dirname)
    if hasDir == False:
        os.mkdir(syncdir+dirname)
    filename = os.path.basename(filename)
    filesize = int(str(filesize))
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="KB", unit_scale=True, unit_divisor=1024)
    with open(syncdir+dirname+"/"+filename, "wb") as f:
        while True:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:    
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))
    client_socket.close()
