import os, subprocess, socket, errno
from threading import Thread

_SERVER = '0.0.0.0'
_PORT = 8989
_LOG_FILE = ""

def conn(client, addr):
    global _LOG_FILE
    try:
        client.send("CYBERGHOST V2.1 :  Python Command Processor \r\n>>")

        while True:
            try:
                data = client.recv(1024)
                if data is None:
                    break
        
                command = "python -c \'" +  data.strip() + "\'"
        
                response = subprocess.check_output(command, shell=True).strip()
                log = str(addr[0]) + " " + str(addr[1]) + " " + command + "\t" + " ".join(response.split()) + "\n"

		print(log),
		_LOG_FILE.write(log)

                client.send(">>" + str(response) + "\n>>")
            except subprocess.CalledProcessError as ex:
		#print(ex)
                client.close()
                break
            except IOError as ex:
		#print(ex)
                if ex.errno == errno.EPIPE or ex.errno == errno.ECONNRESET:
                    break
                pass
    except Exception as ex:
	#print(ex)
        client.close()

def main():
    print("[+] Starting CYBERGHOST V2.1 Server")
    global _LOG_FILE
    _LOG_FILE = open('/etc/vulnserver/vuln.log', 'a+')
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
