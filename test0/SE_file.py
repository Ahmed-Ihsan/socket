import socket
from threading import Thread
from time import sleep

SIZE = 1024
FORMAT = "utf-8"

def listen_for_client_file(PORT =4455,IP ='127.0.0.1'):
    ADDR = (IP, PORT )
    print("[STARTING] Server is starting.")
    """ Staring a TCP socket. """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """ Bind the IP and PORT to the server. """
    server.bind(ADDR)
    """ Server is listening, i.e., server is now waiting for the client to connected. """
    server.listen()
    print("[LISTENING] Server is listening.")

    while True:
        """ Server has accepted the connection from the client. """
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")
        """ Receiving the filename from the client. """
        type_dta = conn.recv(SIZE).decode(FORMAT)
        print(f'data type : {type (type_dta)}')
        conn.send("".encode(FORMAT))
        if type_dta == 'file':
            """ Receiving the filename from the client. """
            filename = conn.recv(SIZE).decode(FORMAT)
            print(f"[RECV] Receiving the filename.")
            file = open(filename, "w")
            conn.send("Filename received.".encode(FORMAT))
            """ Receiving the file data from the client. """
            data = conn.recv(SIZE).decode(FORMAT)
            print(f"[RECV] Receiving the file data.")
            file.write(data)
            conn.send("File data received".encode(FORMAT))
            """ Closing the file. """
            file.close()
            """ Closing the connection from the client. """
            conn.close()
            print(f"[DISCONNECTED] {addr} disconnected.")
        else:
            text = conn.recv(SIZE).decode(FORMAT)
            conn.send("".encode(FORMAT))
            print(text)
            conn.close()

def send_data(PORT=4455,IP ='127.0.0.1', path = 'None.txt',text = 'None',type_data = 'text'):
    ADDR = (IP, PORT)
    """ Staring a TCP socket. """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """ Connecting to the server. """
    client.connect(ADDR)
    if type_data == 'file':
        client.send('file'.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER]: {msg}")
        """ Opening and reading the file data. """
        file = open(path, "r")
        data = file.read()
        """ Sending the filename to the server. """
        client.send("yt.txt".encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER]: {msg}")
        """ Sending the file data to the server. """
        client.send(data.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER]: {msg}")
        """ Closing the file. """
        file.close()
        """ Closing the connection from the server. """
        client.close()
    else:
        client.send('text'.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER]: {msg}")
        print(type(text))
        client.send(text.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER]: {msg}")
        client.close()

if __name__ == "__main__":
    t = Thread(target=listen_for_client_file)
    t.start()
    sleep(2)
    while 1:
        in_key = input('Enter text or -file : ')
        if '-' in in_key and 'file' in in_key:
            path = input('Enter path file ')
            send_data(path = path,type_data ='file')
        elif 'text' in in_key :
            text = input('Enter text : ')
            send_data(text=text)
        sleep(10)
