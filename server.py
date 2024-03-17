import os
import json
import threading
import socket
import time
import pygame as pg
import pathlib

from tram import Tram

MAX_CLIENTS = 10
clients = []
objects = []
trams = []
send_objects = []
running = True

world = {}
#world = {(2,5):"house",(3,5):"house",(4,5):"house_widewindows",(5,5):"house",(6,5):"house"}
world[(0,0)] = "track_straight_horizontal"
world[(0,6)] = "track_straight_horizontal"
world[(-3,3)] = "track_straight_vertical"
world[(3,3)] = "track_straight_vertical"
world[(-2,1)] = "track_diagonal_a"
world[(2,1)] = "track_diagonal_b"
world[(-2,5)] = "track_diagonal_b"
world[(2,5)] = "track_diagonal_a"
world[(-1,0)] = "track_curve_8"
world[(1,0)] = "track_curve_3"
world[(-1,6)] = "track_curve_7"
world[(1,6)] = "track_curve_4"
world[(-3,2)] = "track_curve_1"
world[(3,2)] = "track_curve_2"
world[(-3,4)] = "track_curve_6"
world[(3,4)] = "track_curve_5" 

world[(8,0)] = "track_curve_3"
world[(9,1)] = "track_curve_2"

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

tram_info = {}
CURRENT_DIRECTORY = pathlib.Path(__file__).parent.resolve()

trams_filenames = os.listdir(os.path.join(CURRENT_DIRECTORY,"trams"))
for tram_folder in trams_filenames:
    #try:
    folder_contents = os.listdir(os.path.join(CURRENT_DIRECTORY,"trams",tram_folder))
    if "tram.json" in folder_contents:
        with open(os.path.join(CURRENT_DIRECTORY,"trams",tram_folder,"tram.json")) as file:
            info = json.loads(file.read())
            key = info["system_name"]
            tram_info[key] = info

class Client:
    def __init__(self,socket,id):
        self.socket = socket
        self.nickname = nickname
        self.pos = [0,0]
        self.angle = 0
        self.running = True
        self.controlling = -1
        self.thread = threading.Thread(target=self.cycle)
        self.thread.start()

    def cycle(self):
        global clients,objects, trams

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
            self.controlling = received["controlling"]
            received_tram = received["tram"]

            if self.controlling != -1 and received_tram != []:
                trams[self.controlling] = received_tram

            send = {"objects":[],"tram":None}
            for object in objects:
                send["objects"].append({"type":object.type,"pos":object.pos,"angle":object.angle})

            for tram in trams:
                send["objects"].append({"type":tram.type,"pos":tram.pos,"angle":tram.angle})

            for object in clients:
                if object != self:
                    send["objects"].append({"type":"player","pos":object.pos,"angle":object.angle})
            
            if self.controlling != -1:
                send["tram"]= trams[self.controlling]

            print(send)

            self.socket.send((json.dumps(send)+"=").encode())

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
    global clients,objects,running,send_objects,trams
    
    while running:
        send_objects = []
        removal_list = []

        for pos, client in enumerate(clients):
            if not client.running or not client.thread.is_alive():
                removal_list.append(pos)
        
        for pos in reversed(removal_list):
            print(f"[INFO] dropping player {clients[pos].nickname}")
            clients.pop(pos)

trams.append(Tram([64,64],world,tram_info["ktm5m4"]))

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