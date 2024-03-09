import pygame as pg
import os
import socket
import threading
import random
import json
import pathlib

from player import Player
from tram import Tram

version = "0.3.1"
CURRENT_DIRECTORY = pathlib.Path(__file__).parent.resolve()
current_dir = CURRENT_DIRECTORY

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
pg.display.set_caption(f"Alphen's Tramway Simulator v{version}")
font = pg.font.Font(os.path.join(CURRENT_DIRECTORY,"res","verdana.ttf"),32)

with open(os.path.join(CURRENT_DIRECTORY,"res","sprite_list.json")) as f:
    sprite_list = json.loads(f.read())

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

base_objects = [{"type":"player","pos":(128,128),"angle":30}]

state = "playing_singleplayer"
running = True
send_data = []
username = str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))
ip = "localhost"
port = 8008

trams = []
objects = []
player_pos = [0,0]
camera_pos = [0,0]

def thread():
    global running, objects, send_data, client_socket, state, player

    while running:
        send_data = {"pos":player.pos,"angle":player.angle,"required_tram":player.controlling_tram}
        client_socket.send((json.dumps(send_data) + "=").encode())
        
        received = ""
        while True:
            received += client_socket.recv(8192).decode("utf-8")
            if not received:
                running = False
                state = "disconnected"
            if received[-1] == "=":
                received = received[:-1]
                break
        received = json.loads(received)
        objects = received
        send_data = []

sprites = {}
tram_info = {}

trams_filenames = os.listdir(os.path.join(CURRENT_DIRECTORY,"trams"))
for tram_folder in trams_filenames:
    #try:
    folder_contents = os.listdir(os.path.join(CURRENT_DIRECTORY,"trams",tram_folder))
    if "tram.json" in folder_contents:
        with open(os.path.join(CURRENT_DIRECTORY,"trams",tram_folder,"tram.json")) as file:
            info = json.loads(file.read())
            key = info["system_name"]
            tram_info[key] = info
            panel = pg.image.load(os.path.join(*([current_dir,"trams",tram_folder]+info["graphical_properties"]["panel_file_path"]))).convert_alpha()
            sprites[info["graphical_properties"]["panel_texture_name"]] = pg.transform.scale(panel,(panel.get_width()*info["graphical_properties"]["panel_scale"],panel.get_height()*info["graphical_properties"]["panel_scale"]))
            km_handle = pg.image.load(os.path.join(*([current_dir,"trams",tram_folder]+info["graphical_properties"]["km_handle_path"]))).convert_alpha()
            sprites[info["graphical_properties"]["km_handle_texture_name"]] = pg.transform.scale(km_handle,(km_handle.get_width()*info["graphical_properties"]["km_handle_scale"],km_handle.get_height()*info["graphical_properties"]["km_handle_scale"]))

            base_sprite = pg.image.load(os.path.join(*([current_dir,"trams",tram_folder]+info["graphical_properties"]["panel_parts_path"]))).convert_alpha()
            for sprite_params in info["graphical_properties"]["panel_elements_sprites_loading_info"]:
                sprites[sprite_params["name"]] = pg.transform.scale(base_sprite.subsurface(sprite_params["pos"][0],sprite_params["pos"][1],sprite_params["size"][0],sprite_params["size"][1]),(sprite_params["size"][0]*sprite_params["scale"],sprite_params["size"][1]*sprite_params["scale"]))

            sprite_params = info["graphical_properties"]["texture_parameters"]

            base_sprite = pg.image.load(os.path.join(*([current_dir,"trams",tram_folder]+info["graphical_properties"]["texture_path"]))).convert_alpha()
            base_layers = []
            sprites[sprite_params["name"]] = {}
            for i in range(sprite_params["layer_amount"]):
                y_pos = sprite_params["h_layer"]*i if not ("reversed" in sprite_params and sprite_params["reversed"]) else sprite_params["h_layer"]*(sprite_params["layer_amount"]-1-i)
                base_layers.append(pg.transform.scale(base_sprite.subsurface(0,y_pos,sprite_params["w_layer"],sprite_params["h_layer"]),(sprite_params["w_layer"]*4,sprite_params["h_layer"]*4)))

            sprite_stack_factor = 3

            for rotation in range(0,360,15):
                w, h = pg.transform.rotate(base_layers[0],rotation).get_size()

                surface = pg.Surface((w,h+sprite_params["layer_amount"]*sprite_stack_factor-1))
                surface.set_colorkey((0,0,0))

                for i in range(sprite_params["layer_amount"]*sprite_stack_factor):
                    pos = (0,surface.get_height()-i-h)
                    surface.blit(pg.transform.rotate(base_layers[int(i/sprite_stack_factor)],rotation),pos)
                sprites[sprite_params["name"]][rotation] = surface
            sprites[sprite_params["name"]]["height"] = sprite_params["layer_amount"]*sprite_stack_factor-1

    #except:
    #    print("skipped loading from", tram_folder)


temporary_sprites = {}
sprites_filenames = os.listdir(os.path.join(CURRENT_DIRECTORY,"res"))
for sprites_filename in sprites_filenames:
    if sprites_filename[-4:] == ".png":temporary_sprites[sprites_filename[:-4]] = pg.image.load(os.path.join(current_dir,"res",sprites_filename)).convert_alpha()

for sprite_params in sprite_list["static"]:
    base_sprite = temporary_sprites[sprite_params["file_name"]].subsurface(sprite_params["x"],sprite_params["y"],sprite_params["w"],sprite_params["h"])
    base_layers = []
    sprites[sprite_params["name"]] = {}
    for i in range(sprite_params["layer_amount"]):
        y_pos = sprite_params["h_layer"]*i if not ("reversed" in sprite_params and sprite_params["reversed"]) else sprite_params["h_layer"]*(sprite_params["layer_amount"]-1-i)
        base_layers.append(pg.transform.scale(base_sprite.subsurface(0,y_pos,sprite_params["w_layer"],sprite_params["h_layer"]),(sprite_params["w_layer"]*4,sprite_params["h_layer"]*4)))

    if sprite_params["w"] != 16:
        sprite_stack_factor = 3
    else:
        sprite_stack_factor = 6

    for rotation in range(0,360,15):
        w, h = pg.transform.rotate(base_layers[0],rotation).get_size()

        surface = pg.Surface((w,h+sprite_params["layer_amount"]*sprite_stack_factor-1))
        surface.set_colorkey((0,0,0))

        for i in range(sprite_params["layer_amount"]*sprite_stack_factor):
            pos = (0,surface.get_height()-i-h)
            surface.blit(pg.transform.rotate(base_layers[int(i/sprite_stack_factor)],rotation),pos)
        sprites[sprite_params["name"]][rotation] = surface
    sprites[sprite_params["name"]]["height"] = sprite_params["layer_amount"]*sprite_stack_factor-1

for sprite_params in sprite_list["objects"]:
    base_sprite = temporary_sprites[sprite_params["file_name"]].subsurface(sprite_params["x"],sprite_params["y"],sprite_params["w"],sprite_params["h"])
    base_layers = []
    sprites[sprite_params["name"]] = {}
    for i in range(sprite_params["layer_amount"]):
        y_pos = sprite_params["h_layer"]*i if not ("reversed" in sprite_params and sprite_params["reversed"]) else sprite_params["h_layer"]*(sprite_params["layer_amount"]-1-i)
        base_layers.append(pg.transform.scale(base_sprite.subsurface(0,y_pos,sprite_params["w_layer"],sprite_params["h_layer"]),(sprite_params["w_layer"]*4,sprite_params["h_layer"]*4)))

    if sprite_params["w"] != 16:
        sprite_stack_factor = 3
    else:
        sprite_stack_factor = 6

    for rotation in range(0,360,15):
        w, h = pg.transform.rotate(base_layers[0],rotation).get_size()

        surface = pg.Surface((w,h+sprite_params["layer_amount"]*sprite_stack_factor-1))
        surface.set_colorkey((0,0,0))

        for i in range(sprite_params["layer_amount"]*sprite_stack_factor):
            pos = (0,surface.get_height()-i-h)
            surface.blit(pg.transform.rotate(base_layers[int(i/sprite_stack_factor)],rotation),pos)
        sprites[sprite_params["name"]][rotation] = surface
    sprites[sprite_params["name"]]["height"] = sprite_params["layer_amount"]*sprite_stack_factor-1

working = True
trams.append(Tram([64,64],world,tram_info["ktm5m4"]))

player = Player(f"v{version}",sprites)
player.controlling_tram = 0

while working:
    keydowns = []
    mouse_clicked = False
    for evt in pg.event.get():
        if evt.type == pg.QUIT:
            working = False
        if evt.type == pg.KEYDOWN:
            keydowns.append(evt.key)
        if evt.type == pg.MOUSEBUTTONDOWN:
            mouse_clicked = True
        

    if state == "playing_singleplayer":
        objects = []
        objects+=base_objects

        for tram in trams:
            objects.append({"pos":tram.pos,"type":tram.type,"angle":tram.angle})

    if "playing" in state:
        if state=="playing_singleplayer":
            controlled_tram = trams[player.controlling_tram] if player.controlling_tram != -1 else []
        new_controlled_tram = player.update(screen,world,pg.key.get_pressed(),keydowns,pg.mouse.get_pos(),pg.mouse.get_pressed(),mouse_clicked,controlled_tram)
        if state=="playing_singleplayer":
            if player.controlling_tram != -1:trams[player.controlling_tram] = new_controlled_tram
        player.draw(screen,objects,clock,controlled_tram,tram_info)
    elif state == "main":
        screen.fill((128,128,128))
        w, h = screen.get_size()
        text = font.render(f"1 to play alone",True,(0,0,0))
        screen.blit(text,(w/2-text.get_width()/2,h/2-text.get_height()))
        #text = font.render(f"хуй тебе, а не мультиплеер",True,(0,0,0))
        #screen.blit(text,(w/2-text.get_width()/2,h/2+text.get_height()))

        if pg.K_1 in keydowns:
            state = "playing_singleplayer"
        #elif pg.K_2 in keydowns:
        #    state = "connect"
    '''
    elif state == "disconnected":
        screen.fill((128,128,128))
        w, h = screen.get_size()
        text = font.render(f"disconnected",True,(0,0,0))
        screen.blit(text,(w/2-text.get_width()/2,h/2-text.get_height()))
        text = font.render(f"press any key to go back to main menu",True,(0,0,0))
        screen.blit(text,(w/2-text.get_width()/2,h/2+text.get_height()))
        if keydowns:
            state = "main"
    elif state == "connect_failed":
        screen.fill((128,128,128))
        w, h = screen.get_size()
        text = font.render(f"connect failed",True,(0,0,0))
        screen.blit(text,(w/2-text.get_width()/2,h/2-text.get_height()))
        text = font.render(f"press any key to go back to main menu",True,(0,0,0))
        screen.blit(text,(w/2-text.get_width()/2,h/2+text.get_height()))
        if keydowns:
            state = "main"
    elif state == "connected":
        screen.fill((128,128,128))
        w, h = screen.get_size()
        text = font.render(f"connected",True,(0,0,0))
        screen.blit(text,(w/2-text.get_width()/2,h/2-text.get_height()))
        text = font.render(f"yippie",True,(0,0,0))
        screen.blit(text,(w/2-text.get_width()/2,h/2+text.get_height()))
    elif state == "connect":
        screen.fill((128,128,128))
        w, h = screen.get_size()
        text = font.render(f"Connecting to {ip+str(port)}...",True,(0,0,0))
        screen.blit(text,(w/2-text.get_width()/2,h/2-text.get_height()/2))
        pg.display.update()
        
        try:
            client_socket = socket.socket()
            client_socket.connect((ip, int(port)))
            client_socket.settimeout(5)
            client_socket.send(bytes(f"player{username}","utf=8"))
            received = ""
            while True:
                received += client_socket.recv(8192).decode("utf-8")
                if not received:
                    break
                if received[-1] == "=":
                    received = received[:-1]
                    break
            if not received or received == "SERVER_FULL":
                state = "connect_failed"
            elif received == "CONNECTION_SUCCESSFUL":
                socket_thread = threading.Thread(target=thread,daemon=True)
                socket_thread.start()
                state = "playing_multiplayer"
        except:
            state = "connect_failed"
    '''

    pg.display.update()
    clock.tick(60)
    if not working:
        pg.quit()