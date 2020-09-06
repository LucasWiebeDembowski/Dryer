import socket
import sys
from threading import Thread

stopped = False
def recvMsg(conn, delim):
    global stopped
    full_msg = ''
    while not stopped:
        try:
            msg = conn.recv(1)
        except socket.timeout:
            pass
        else:
            if not msg:
                break
            decodedMsg = msg.decode("utf-8")
            if not decodedMsg or len(decodedMsg) <= 0:
                break
            if decodedMsg == delim:
                break
            full_msg += decodedMsg
    return full_msg

def client_thread(conn, addr):
    global stopped
    conn.send(str.encode("Welcome to the Python server. Type something and press enter.\n"))
    while not stopped:
        data = recvMsg(conn, '\n')
        if not data:
            break
        if "quit" == data:
            print(f"Client {addr[1]} has disconnected.")
            break;
        elif "killserver" == data:
            print(f"Client {addr[1]} has killed this server.")
            stopped = True
        reply = "Python response: You sent: " + data + "\n"
        print(f"Client {addr[1]} command: " + data)
        conn.send(str.encode(reply))
    conn.close()

###################################################################################################

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s.bind((socket.gethostname(), 1234))
# s.bind(("192.168.193.135", 1234))
# s.bind(("192.168.1.42", 1234))
# tcpServer.bind(("192.168.100.105", 1234)) # My desktop
tcpServer.bind(("192.168.100.107", 51415)) # Spot
tcpServer.settimeout(0.2) # timeout for listening
# tcpServer.listen(5)

threads = []
while not stopped:
    try:
        tcpServer.listen(1) 
        (conn, (ip, port)) = tcpServer.accept() 
    except socket.timeout:
        pass
    except:
        raise
    else:
        print("Connected with client at " + ip + " on port " + str(port))
        conn.settimeout(0.2)
        clientTh = Thread(target=client_thread, args=(conn, (ip, port), ))
        clientTh.start()
        threads.append(clientTh)

tcpServer.close()
for clientTh in threads:
    clientTh.join()
    
print("Exiting Server.")
