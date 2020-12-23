from dryermonitor import *

import socket
import sys
from threading import Thread

serverRunning = True
dryerTh = None
dryer = Dryer()

def recvMsg(conn, delim):
    global stopped
    full_msg = ''
    while serverRunning:
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
    global serverRunning
    global dryerTh
    global dryer
    # conn.send(str.encode("Welcome to the Python server. Type something and press enter.\n"))
    while serverRunning: # This loop also stops if the client process terminates.
        data = recvMsg(conn, '\n')
        if not data or "quit" == data:
            break
        elif "killserver" == data:
            print(f"Client {addr[1]} has killed this server.")
            serverRunning = False
        elif "start" == data:
            if dryer and not dryerTh:
                print("Starting")
                dryerTh = Thread(target=dryer.run_dryermonitor)
                dryerTh.start()
        elif "stop" == data:
            if dryerTh:
                print("Stopping")
                dryer.stopDryerLoop()
                dryerTh.join()
                dryerTh = None
        elif "list" == data:
            if dryer:
                monitorStatus = (not dryer.dryerMonitorRunning()) * "NOT " + "running"
                dryerStatus = "Unknown"
                dryerRuntime = "Unknown"
                dryerStopped = (dryer.getDryerStopped() * "STOPPED")
                dryerLastRuntime = dryer.getLastRuntime()
                # print(f"dryerStopped: {dryerStopped}")
                if dryer.dryerMonitorRunning():
                    dryerStatus = ((not dryer.getDryerRunning()) * "NOT " + "running")
                    dryerRuntime = dryer.getRuntimeSec()

                conn.send(str.encode(
                    f"{monitorStatus},{dryerStatus},{dryerRuntime},{dryerStopped},{dryerLastRuntime}\n"))
        else:
            print(f"Client {addr[1]} command: " + data)
            reply = "Unimplemented server command: " + data + "\n"
            conn.send(str.encode(reply))
    print(f"Client {addr[1]} has disconnected.")
    conn.close()

###################################################################################################

dryerTh = Thread(target=dryer.run_dryermonitor)
dryerTh.start()

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s.bind((socket.gethostname(), 1234))
# s.bind(("192.168.193.135", 1234))
# s.bind(("192.168.1.42", 1234))
# tcpServer.bind(("192.168.100.105", 1234)) # My desktop
tcpServer.bind(("192.168.100.107", 1234)) # Spot
tcpServer.settimeout(0.2) # timeout for listening
# tcpServer.listen(5)

threads = []
while serverRunning:
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
    print("Joining client")
    clientTh.join()

if dryerTh:
    print("Joining dryerTh")
    dryer.stopDryerLoop()
    dryerTh.join()

print("Exiting Server.")
