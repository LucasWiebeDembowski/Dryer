import socket

def recvMsg(sock, delim):
    full_msg = ''
    while delim not in full_msg:
        msg = sock.recv(1048)
        if len(msg) <= 0:
            break
        full_msg += msg.decode("utf-8")
    return full_msg

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.bind(("192.168.100.107", 4321)) # Specify client port... should be unnecessary.
#s.connect((socket.gethostname(), 1234))
# s.connect(("192.168.193.135", 1234))
# s.connect(("192.168.1.42", 1234))
# s.connect(("192.168.100.105", 1234)) # My desktop
client.connect(("192.168.1.106", 1234)) # Spot

usrIn = ""
response = recvMsg(client, '\n')
print("Server message: " + response)
while True:
    usrIn = input("") + "\n"
    if usrIn != "\n":
        # Windows kills the connection if you send an empty string 3 times in a row.
        client.send(str.encode(usrIn))
        response = recvMsg(client, '\n')
        print("Server message: " + response)
    if "quit" in usrIn:
        break

print("Quitting.")
client.close()
