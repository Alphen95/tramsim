import os
import json
import threading
import socket
import time
import pygame as pg

MAX_CLIENTS = 10
clients = []
objects = []
send_objects = []
running = True

port =8008 #int(input("Port>"))

server_socket = socket.socket()
try:
    server_socket.bind(("", port))
    print("[LOG]", "Successfully installed port for socket")
except Exception as exc:
    print("[ERROR]", "Failed to install port for socket")
    print("[EXCEPTION]", exc)
    input("Press enter to terminate the server...")
    exit()
server_socket.listen(1)


class Client:
    def __init__(self,socket,id):
        self.socket = socket
        self.nickname = nickname
        self.pos = [0,0]
        self.angle = 0
        self.running = True
        self.thread = threading.Thread(target=self.cycle)
        self.thread.start()

    def cycle(self):
        global clients,objects

        while self.running: 
            received = ""
            while True:
                received += self.socket.recv(8192).decode("utf-8")
                if not received:
                    self.running = False
                    break
                if received[-1] == "=":
                    received = received[:-1]
                    break
            received = json.loads(received)

            self.pos = received["pos"]
            self.angle = received["angle"]
            send_objects = []
            for object in objects:
                send_objects.append({"type":object.type,"pos":object.pos,"angle":object.angle})
            for object in clients:
                if object != self:
                    send_objects.append({"type":"player","pos":object.pos,"angle":object.angle})

            self.socket.send((json.dumps(send_objects)+"=").encode())

class Object:
    def __init__(self,pos,obj_type):
        self.pos = pos
        self.type = obj_type
        self.velocity = [0,0]
        self.acceleration = [0,0]
        self.angle = 0
        self.exists = True
    
    def cycle(self):
        while self.exists:
            self.pos = [round(self.pos[0]+self.velocity[0],3),round(self.pos[1]+self.velocity[1],3)]
            self.velocity = [round(self.acceleration[0]+self.velocity[0],3),round(self.acceleration[1]+self.velocity[1],3)]
            time.sleep(1/60)

def cycle():
    global clients,objects,running,send_objects
    
    while running:
        send_objects = []
        removal_list = []

        for pos, client in enumerate(clients):
            if not client.running or not client.thread.is_alive():
                removal_list.append(pos)
        
        for pos in reversed(removal_list):
            print(f"[INFO] dropping player {clients[pos].nickname}")
            clients.pop(pos)


global_thread = threading.Thread(target=cycle)
global_thread.start()

while running:
    connection, address = server_socket.accept()
    try:
        nickname = connection.recv(8192).decode("utf-8")
        if len(clients) < MAX_CLIENTS:
            reply = "CONNECTION_SUCCESSFUL"
            reply = reply
            connection.send((reply + "=").encode())
            print("[INFO]", "{} has connected".format(nickname))
            clients.append(Client(connection, nickname))
        else:
            reply = "SERVER_FULL"
            reply = reply
            connection.send((reply + "=").encode())
            print("[INFO]", "{} tried to connect; not enough space on the server".format(nickname))
            
    except Exception as exc:
        print("[ERROR]", "An unexpected error occured while client was connecting")
        print("[EXCEPTION]", exc)
        continue