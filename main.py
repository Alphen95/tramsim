import pygame as pg
import os
import json
import pathlib

#from player import Player
from tram import Tram

version = "0.4.6"
scale = 1
CURRENT_DIRECTORY = pathlib.Path(__file__).parent.resolve()
current_dir = CURRENT_DIRECTORY
MAPPING = [(8, -8), (7, -8), (8, -7), (6, -8), (7, -7), (8, -6), (5, -8), (6, -7), (7, -6), (8, -5), (4, -8), (5, -7), (6, -6), (7, -5), (8, -4), (3, -8), (4, -7), (5, -6), (6, -5), (7, -4), (8, -3), (2, -8), (3, -7), (4, -6), (5, -5), (6, -4), (7, -3), (8, -2), (1, -8), (2, -7), (3, -6), (4, -5), (5, -4), (6, -3), (7, -2), (8, -1), (0, -8), (1, -7), (2, -6), (3, -5), (4, -4), (5, -3), (6, -2), (7, -1), (8, 0), (-1, -8), (0, -7), (1, -6), (2, -5), (3, -4), (4, -3), (5, -2), (6, -1), (7, 0), (8, 1), (-2, -8), (-1, -7), (0, -6), (1, -5), (2, -4), (3, -3), (4, -2), (5, -1), (6, 0), (7, 1), (8, 2), (-3, -8), (-2, -7), (-1, -6), (0, -5), (1, -4), (2, -3), (3, -2), (4, -1), (5, 0), (6, 1), (7, 2), (8, 3), (-4, -8), (-3, -7), (-2, -6), (-1, -5), (0, -4), (1, -3), (2, -2), (3, -1), (4, 0), (5, 1), (6, 2), (7, 3), (8, 4), (-5, -8), (-4, -7), (-3, -6), (-2, -5), (-1, -4), (0, -3), (1, -2), (2, -1), (3, 0), (4, 1), (5, 2), (6, 3), (7, 4), (8, 5), (-6, -8), (-5, -7), (-4, -6), (-3, -5), (-2, -4), (-1, -3), (0, -2), (1, -1), (2, 0), (3, 1), (4, 2), (5, 3), (6, 4), (7, 5), (8, 6), (-7, -8), (-6, -7), (-5, -6), (-4, -5), (-3, -4), (-2, -3), (-1, -2), (0, -1), (1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (-8, -8), (-7, -7), (-6, -6), (-5, -5), (-4, -4), (-3, -3), (-2, -2), (-1, -1), (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (-8, -7), (-7, -6), (-6, -5), (-5, -4), (-4, -3), (-3, -2), (-2, -1), (-1, 0), (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (-8, -6), (-7, -5), (-6, -4), (-5, -3), (-4, -2), (-3, -1), (-2, 0), (-1, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 8), (-8, -5), (-7, -4), (-6, -3), (-5, -2), (-4, -1), (-3, 0), (-2, 1), (-1, 2), (0, 3), (1, 4), (2, 5), (3, 6), (4, 7), (5, 8), (-8, -4), (-7, -3), (-6, -2), (-5, -1), (-4, 0), (-3, 1), (-2, 2), (-1, 3), (0, 4), (1, 5), (2, 6), (3, 7), (4, 8), (-8, -3), (-7, -2), (-6, -1), (-5, 0), (-4, 1), (-3, 2), (-2, 3), (-1, 4), (0, 5), (1, 6), (2, 7), (3, 8), (-8, -2), (-7, -1), (-6, 0), (-5, 1), (-4, 2), (-3, 3), (-2, 4), (-1, 5), (0, 6), (1, 7), (2, 8), (-8, -1), (-7, 0), (-6, 1), (-5, 2), (-4, 3), (-3, 4), (-2, 5), (-1, 6), (0, 7), (1, 8), (-8, 0), (-7, 1), (-6, 2), (-5, 3), (-4, 4), (-3, 5), (-2, 6), (-1, 7), (0, 8), (-8, 1), (-7, 2), (-6, 3), (-5, 4), (-4, 5), (-3, 6), (-2, 7), (-1, 8), (-8, 2), (-7, 3), (-6, 4), (-5, 5), (-4, 6), (-3, 7), (-2, 8), (-8, 3), (-7, 4), (-6, 5), (-5, 6), (-4, 7), (-3, 8), (-8, 4), (-7, 5), (-6, 6), (-5, 7), (-4, 8), (-8, 5), (-7, 6), (-6, 7), (-5, 8), (-8, 6), (-7, 7), (-6, 8), (-8, 7), (-7, 8), (-8, 8)]

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
pg.display.set_caption(f"Alphen's Tramway Simulator v{version}")
font = pg.font.Font(os.path.join(CURRENT_DIRECTORY,"res","verdana.ttf"),20)


world = {}
track_switch_states = {}

#world = {(2,5):"house",(3,5):"house",(4,5):"house_widewindows",(5,5):"house",(6,5):"house"}
#world = {(-1, 2): 'track_straight_vertical', (-1, 1): 'track_straight_vertical', (-1, 0): 'track_straight_vertical', (-1, -1): 'track_straight_vertical', (-1, -2): 'track_straight_vertical', (-1, -3): 'track_straight_vertical', (0, -5): 'track_diagonal_a', (-1, -4): 'track_switch_1', (1, -6): 'track_diagonal_a', (2, -7): 'track_curve_5', (2, -8): 'track_curve_2', (0, -9): 'track_curve_8', (-1, -8): 'track_curve_1', (1, -9): 'track_curve_3', (-1, -7): 'track_straight_vertical', (-1, -5): 'track_straight_vertical', (-1, -6): 'track_straight_vertical', (-1, 3): 'track_switch_5', (-1, 4): 'track_straight_vertical', (-1, 5): 'track_straight_vertical', (-1, 6): 'track_straight_vertical', (-2, 5): 'track_straight_vertical', (-2, 4): 'track_curve_1', (-2, 6): 'track_curve_6', (-1, 7): 'track_switch_2', (-1, 8): 'track_straight_vertical', (-1, 9): 'track_straight_vertical', (-1, 10): 'track_straight_vertical', (-1, 11): 'track_straight_vertical', (-1, 12): 'track_straight_vertical', (-1, 13): 'track_straight_vertical', (-1, 14): 'track_straight_vertical', (-1, 15): 'track_straight_vertical', (-1, 16): 'track_curve_6', (0, 17): 'track_curve_7', (2, 17): 'track_straight_horizontal', (5, 17): 'track_straight_horizontal', (7, 17): 'track_straight_horizontal', (6, 17): 'track_straight_horizontal', (4, 17): 'track_straight_horizontal', (3, 17): 'track_straight_horizontal', (1, 17): 'track_straight_horizontal', (9, 16): 'track_diagonal_a', (10, 15): 'track_diagonal_a', (12, 14): 'track_curve_3', (11, 14): 'track_curve_8', (13, 15): 'track_curve_2', (13, 16): 'track_curve_5', (12, 17): 'track_curve_4', (11, 17): 'track_straight_horizontal', (9, 17): 'track_straight_horizontal', (10, 17): 'track_straight_horizontal', (8, 17): 'track_switch_4',(2,2):"house"}
#track_switch_states = {(-1, -4): False, (-1, 3): False, (-1, 7): False, (8, 17): False}

base_objects = []

game_state = "main"

trams = []
objects = []
player_pos = [0,0]
camera_pos = [0,0]
debug = 0
controlling_tram_id = -1

sprites = {}
tram_info = {}
new_controlled_tram = []
controlled_tram = []

toolkit = "base"
editing_tab = 0
tool = -1
tools = {}


trams_filenames = os.listdir(os.path.join(CURRENT_DIRECTORY,"trams"))
for tram_folder in trams_filenames:
    #try:
    folder_contents = os.listdir(os.path.join(CURRENT_DIRECTORY,"trams",tram_folder))
    if "tram.json" in folder_contents:
        with open(os.path.join(CURRENT_DIRECTORY,"trams",tram_folder,"tram.json")) as file:
            info = json.loads(file.read())
            key = info["system_name"]
            tram_info[key] = info
            sprites[info["graphical_properties"]["panel_texture_name"]] = pg.image.load(os.path.join(*([current_dir,"trams",tram_folder]+info["graphical_properties"]["panel_file_path"]))).convert_alpha()
            sprites[info["graphical_properties"]["km_handle_texture_name"]] = pg.image.load(os.path.join(*([current_dir,"trams",tram_folder]+info["graphical_properties"]["km_handle_path"]))).convert_alpha()

            base_sprite = pg.image.load(os.path.join(*([current_dir,"trams",tram_folder]+info["graphical_properties"]["panel_parts_path"]))).convert_alpha()
            for sprite_params in info["graphical_properties"]["panel_elements_sprites_loading_info"]:
                sprites[sprite_params["name"]] = base_sprite.subsurface(sprite_params["pos"][0],sprite_params["pos"][1],sprite_params["size"][0],sprite_params["size"][1])

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
packet_folders = os.listdir(os.path.join(CURRENT_DIRECTORY,"res"))
for packet_folder in packet_folders:
    #try:
    if os.path.isdir(os.path.join(CURRENT_DIRECTORY,"res",packet_folder)):
        folder_contents = os.listdir(os.path.join(CURRENT_DIRECTORY,"res",packet_folder))
        if "sprite_list.json" in folder_contents:
            with open(os.path.join(CURRENT_DIRECTORY,"res",packet_folder,"sprite_list.json")) as file:
                for sprites_filename in folder_contents:
                    if sprites_filename[-4:] == ".png":
                        temporary_sprites[sprites_filename[:-4]] = pg.image.load(os.path.join(CURRENT_DIRECTORY,"res",packet_folder,sprites_filename)).convert_alpha()
                sprite_list = json.loads(file.read())
                name = sprite_list["packet_name"]
                sprites[name] = {}
                tools[name] = sprite_list["editor_loadout"]

                for sprite_params in sprite_list["static"]:
                    base_sprite = temporary_sprites[sprite_params["file_name"]].subsurface(sprite_params["pos"][0],sprite_params["pos"][1],sprite_params["size"][0],sprite_params["size"][1])
                    if "ui_flag" in sprite_params and sprite_params["ui_flag"]:
                        sprites[sprite_params["name"]] = {}
                        sprites[sprite_params["name"]]["sprite"] = pg.transform.scale(
                            base_sprite,
                            (
                                sprite_params["size"][0]*4,
                                sprite_params["size"][1]*4
                            )
                        )
                        sprites[sprite_params["name"]]["offset"] = (sprite_params["offset"][0],sprite_params["offset"][1])
                    else:
                        sprites[name][sprite_params["name"]] = {}
                        sprites[name][sprite_params["name"]]["sprite"] = pg.transform.scale(
                            base_sprite,
                            (
                                sprite_params["size"][0]*4,
                                sprite_params["size"][1]*4
                            )
                        )
                        sprites[name][sprite_params["name"]]["offset"] = (sprite_params["offset"][0],sprite_params["offset"][1])

                for sprite_params in sprite_list["objects"]:
                    base_sprite = temporary_sprites[sprite_params["file_name"]].subsurface(sprite_params["x"],sprite_params["y"],sprite_params["w"],sprite_params["h"])
                    base_layers = []
                    sprites[name][sprite_params["name"]] = {}
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
                        sprites[name][sprite_params["name"]][rotation] = surface
                    sprites[name][sprite_params["name"]]["height"] = sprite_params["layer_amount"]*sprite_stack_factor-1

working = True

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
    
    pressed = pg.key.get_pressed()
    m_btn = pg.mouse.get_pressed()
    m_pos = pg.mouse.get_pos()
    m_block_pos = (int((m_pos[0]+camera_pos[0]-w/2)/(128*scale))-(1 if (m_pos[0]+camera_pos[0]-w/2) < 0 else 0),int((m_pos[1]+camera_pos[1]-h/2)/128)-(1 if (m_pos[1]+camera_pos[1]-h/2) < 0 else 0))


    objects = []
    objects+=base_objects

    for tram in trams:
        objects.append({"pos":tram.pos,"type":tram.type,"angle":tram.angle})

    if "playing" in game_state:
        controlled_tram = trams[controlling_tram_id] if controlling_tram_id != -1 else []

        speed = 1 if not pressed[pg.K_LSHIFT] else 4

        if controlling_tram_id == -1 or controlled_tram == []:
            if pressed[pg.K_DOWN]: 
                player_pos[1]+=speed*clock.get_fps()/60
            if pressed[pg.K_UP]: 
                player_pos[1]-=speed*clock.get_fps()/60
            if pressed[pg.K_LEFT]: 
                player_pos[0]-=speed*clock.get_fps()/60
            if pressed[pg.K_RIGHT]: 
                player_pos[0]+=speed*clock.get_fps()/60
            if pg.K_ESCAPE in keydowns:
                game_state = "main"
            if pg.K_s in keydowns:
                block_pos = (int((camera_pos[0]-(127 if camera_pos[0]< 0 else 0))/128),int((camera_pos[1]-(127 if camera_pos[1]< 0 else 0))/128))
                if block_pos in world:
                    tile = world[block_pos]
                    if tile[-4:] == "tst1":
                        trams.append(Tram([block_pos[0]*128+64,block_pos[1]*128+64],world,tram_info["ktm5m4"],track_switch_states))
                        trams[-1].angle = 180 if pressed[pg.K_LALT] else 0
                    if tile[-4:] == "tst0":
                        trams.append(Tram([block_pos[0]*128+64,block_pos[1]*128+64],world,tram_info["ktm5m4"],track_switch_states))
                        trams[-1].angle = 270 if pressed[pg.K_LALT] else 90

            if mouse_clicked:
                chose_tram = False
                for number, tram in enumerate(trams):
                    if m_pos[0]-w/2 > tram.pos[0]-camera_pos[0]-48 and m_pos[0]-w/2 < tram.pos[0]-camera_pos[0]+48 and m_pos[1]-h/2 > tram.pos[1]-camera_pos[1]-48 and m_pos[1]-h/2 < tram.pos[1]-camera_pos[1]+48:
                        controlling_tram_id = number
                        chose_tram = True
                        break

                if not chose_tram:
                    if m_btn[0] and m_block_pos in track_switch_states:
                        track_switch_states[m_block_pos] = not(track_switch_states[m_block_pos])
                        for tram in trams:
                            tram.track_switch_states = track_switch_states



        else:
            panel = sprites[controlled_tram.parameters["graphical_properties"]["panel_texture_name"]]
            panel_scale = controlled_tram.parameters["graphical_properties"]["panel_scale"]
            player_pos = [controlled_tram.pos[0],controlled_tram.pos[1]]
            if pressed[pg.K_ESCAPE]: 
                controlling_tram_id = -1

            if pg.K_DOWN in keydowns: 
                controlled_tram.km_pos -= 1 if controlled_tram.parameters["technical_properties"]["km_boundaries"][0] < controlled_tram.km_pos else 0
            if pg.K_UP in keydowns: 
                controlled_tram.km_pos += 1 if controlled_tram.parameters["technical_properties"]["km_boundaries"][1] > controlled_tram.km_pos else 0
            
            if m_pos[0] > w/2-panel.get_width()/2*panel_scale and m_pos[0] < w/2+panel.get_width()/2*panel_scale and m_pos[1] > h-panel.get_height()*panel_scale:
                for element in controlled_tram.driver_panel_element_states:
                    if controlled_tram.parameters["graphical_properties"]["panel_elements_information"][element]["type"] in controlled_tram.parameters["graphical_properties"]["clickable_ui_elements"]:
                        element_state = str(controlled_tram.driver_panel_element_states[element])
                        full_info = controlled_tram.parameters["graphical_properties"]["panel_elements_information"][element]
                        if (m_pos[0] > w/2+(-panel.get_width()/2+full_info["states"][element_state]["pos"][0])*panel_scale 
                            and m_pos[1] > h+(-panel.get_height()+full_info["states"][element_state]["pos"][1])*panel_scale 
                            and m_pos[0] < w/2+(-panel.get_width()/2+full_info["states"][element_state]["pos"][0]+full_info["states"][element_state]["collision_box"][0])*panel_scale and m_pos[1] < h+(-panel.get_height()+full_info["states"][element_state]["pos"][1]+full_info["states"][element_state]["collision_box"][1])*panel_scale):
                            if controlled_tram.parameters["graphical_properties"]["panel_elements_information"][element]["type"] == "switch" and mouse_clicked:  
                                controlled_tram.driver_panel_element_states[element] = "off" if controlled_tram.driver_panel_element_states[element] == "on" else "on"
                                controlled_tram.train_flags[full_info["controlling"]] = True if controlled_tram.driver_panel_element_states[element] == "on" else False
                            if full_info["type"] == "button":
                                if (m_btn[0] or m_btn[2]):
                                    controlled_tram.driver_panel_element_states[element] = "on"
                                    controlled_tram.train_flags[full_info["controlling"]] = True
                                else:
                                    controlled_tram.driver_panel_element_states[element] = "off"
                                    controlled_tram.train_flags[full_info["controlling"]] = False
                            if full_info["type"] == "switch_reverser" and mouse_clicked:
                                if m_btn[0] and controlled_tram.train_flags[full_info["controlling"]] < 1:
                                    controlled_tram.driver_panel_element_states[element] += 1
                                    controlled_tram.train_flags[full_info["controlling"]] += 1
                                    controlled_tram.driving_direction += 1
                                elif m_btn[2] and controlled_tram.train_flags[full_info["controlling"]] > -1:
                                    controlled_tram.driver_panel_element_states[element] -= 1
                                    controlled_tram.train_flags[full_info["controlling"]] -= 1
                                    controlled_tram.driving_direction -= 1
                        else:
                            if full_info["type"] == "button" and not(m_btn[0] or m_btn[2]):
                                controlled_tram.driver_panel_element_states[element] = "off"
                                controlled_tram.train_flags[full_info["controlling"]] = False
            else:
                block_pos = (int((m_pos[0]+camera_pos[0]-w/2)/128)-(1 if (m_pos[0]+camera_pos[0]-w/2) < 0 else 0),int((m_pos[1]+camera_pos[1]-h/2)/128)-(1 if (m_pos[1]+camera_pos[1]-h/2) < 0 else 0))
                if mouse_clicked and m_btn[0] and block_pos in track_switch_states:
                    track_switch_states[block_pos] = not(track_switch_states[block_pos])
                    for tram in trams:
                        tram.track_switch_states = track_switch_states


        if pg.K_d in keydowns: debug = (debug+1)%3

        camera_pos = [player_pos[0],player_pos[1]]

        new_controlled_tram = controlled_tram
        
        screen.fill((128,128,128))

        visible_objects = []

        for object in objects:
            if camera_pos[0]-8*128/scale <= object["pos"][0] <= camera_pos[0]+8*128/scale and camera_pos[1]-8*128/scale <= object["pos"][1] <= camera_pos[1]+8*128/scale:
                visible_objects.append(object)

        for x_coord, y_coord in MAPPING:
            tile_coordinates = (int((camera_pos[0]-(127 if camera_pos[0]<= 0 else 0))/128)+x_coord,int((camera_pos[1]-(127 if camera_pos[1]<= 0 else 0))/128)+y_coord)

            base_tile_blit_coords = (
                w/2+(x_coord*128*scale-int(camera_pos[0])%128*scale),
                h/2+(y_coord*128*scale-int(camera_pos[1])%128*scale)
            )
            centered_coords = (
                w/2+(x_coord*128*scale-int(camera_pos[0])%128*scale+64*scale),
                h/2+(y_coord*128*scale-int(camera_pos[1])%128*scale+64*scale)
            )

            if tile_coordinates in world:
                packet, sprite = world[tile_coordinates].split(":")
                size = sprites[packet][sprite]["sprite"].get_size()
                offset_horizontal = (x_coord*128-int(camera_pos[0])%128)
                offset_vertical = (y_coord*128-int(camera_pos[1])%128)
                tile_blit_coords = (
                    w/2+offset_horizontal+sprites[packet][sprite]["offset"][0]*4,
                    h/2+offset_vertical+sprites[packet][sprite]["offset"][1]*4
                )
                screen.blit(sprites[packet][sprite]["sprite"],tile_blit_coords)

                if tile_coordinates == m_block_pos and world[tile_coordinates][-4:-1] == "tsw":
                    if track_switch_states[m_block_pos]:
                        screen.blit(pg.transform.rotate(pg.transform.flip(sprites["ui_switch_alt"]["sprite"],int(world[tile_coordinates][-1])%2==1,False),(int(world[tile_coordinates][-1]))//2*-90),tile_blit_coords)
                    else:
                        size = sprites["ui_switch_normal"]["sprite"].get_size()
                        tile_blit_coords = (
                            w/2+offset_horizontal+sprites["ui_switch_normal"]["offset"][0]*4,
                            h/2+offset_vertical+sprites["ui_switch_normal"]["offset"][1]*4
                        )
                        if int(world[tile_coordinates][-1]) in [2,3,6,7]:screen.blit(sprites["ui_switch_normal"]["sprite"],tile_blit_coords)
                        else:screen.blit(pg.transform.rotate(sprites["ui_switch_normal"]["sprite"],90),tile_blit_coords)

            tile_blit_coords = (
                base_tile_blit_coords[0],
                base_tile_blit_coords[1]#+128*math.cos(math.radians(self.angle))-size[1]
            )

            if debug > 0:
                if debug > 1:
                    pg.draw.polygon(screen,(255,0,0),(
                        base_tile_blit_coords,
                        (base_tile_blit_coords[0]+128*scale,base_tile_blit_coords[1]),
                        (base_tile_blit_coords[0]+128*scale,base_tile_blit_coords[1]+128*scale),
                        (base_tile_blit_coords[0],base_tile_blit_coords[1]+128*scale),
                        ),2
                    )
                    pg.draw.rect(screen,(0,255,0),base_tile_blit_coords+(4,4),2)
                    pg.draw.rect(screen,(0,255,0),centered_coords+(4,4),2)
                    pos = font.render(f"{x_coord}:{y_coord}",True,(0,0,0))
                    screen.blit(pos,[centered_coords[0]-pos.get_width()/2,centered_coords[1]-pos.get_height()])
                    pos = font.render(f"{tile_coordinates[0]}:{tile_coordinates[1]}",True,(0,0,0))
                    screen.blit(pos,[centered_coords[0]-pos.get_width()/2,centered_coords[1]+pos.get_height()])
                #screen.blit(self.sprites["player_down"],(w/2-128*2+self.pos[0]-self.camera_pos[0],h/2-128*2+self.pos[1]-self.camera_pos[1]))


        for visible_object in sorted(visible_objects,key=lambda x:x["pos"][1]):
            object_blit_coords = (
                w/2+(visible_object["pos"][0]-camera_pos[0])*scale,
                h/2+(visible_object["pos"][1]-camera_pos[1])*scale
            )
            sprite_w,sprite_h = sprites[visible_object["type"]][(visible_object["angle"])//5*5%360].get_size()
            
            screen.blit(pg.transform.scale(sprites[visible_object["type"]][(0-visible_object["angle"])//5*5%360],(sprite_w*scale,sprite_h*scale)),(
                object_blit_coords[0]-sprite_w/2*scale,
                object_blit_coords[1]-(sprite_h-sprites[visible_object["type"]]["height"])/2*scale-sprites[visible_object["type"]]["height"]*scale
            ))
            if debug > 0:
                pg.draw.rect(screen,(0,255,0),object_blit_coords+(4,4),2)


        info_blit_list = []
        info_blit_list.append(font.render(version,True,(0,0,0)))
        if debug > 0:
            info_blit_list.append(font.render(f"tramcars: {len(trams)}",True,(0,0,0)))

        w,h = screen.get_size()
        if controlled_tram != []:
            panel_surface = pg.Surface(sprites[controlled_tram.parameters["graphical_properties"]["panel_texture_name"]].get_size())
            panel_surface.set_colorkey((0,0,0))

            panel = sprites[controlled_tram.parameters["graphical_properties"]["panel_texture_name"]]
            km_handle = sprites[controlled_tram.parameters["graphical_properties"]["km_handle_texture_name"]]
            panel_scale = controlled_tram.parameters["graphical_properties"]["panel_scale"]
            mapouts = controlled_tram.parameters["graphical_properties"]["km_handle_draw_mapouts"]

            panel_surface.blit(panel,(0,0))
            panel_surface.blit(
                km_handle,
                (
                    mapouts[str(controlled_tram.km_pos)]["pos"][0]-km_handle.get_width()/2, 
                    mapouts[str(controlled_tram.km_pos)]["pos"][1]-km_handle.get_height()/2,
                )
            )

            for element in controlled_tram.driver_panel_element_states:

                element_state = str(controlled_tram.driver_panel_element_states[element])
                panel_surface.blit(sprites[controlled_tram.parameters["graphical_properties"]["panel_elements_information"][element]["states"][element_state]["texture"]],
                    (controlled_tram.parameters["graphical_properties"]["panel_elements_information"][element]["states"][element_state]["pos"][0],
                    controlled_tram.parameters["graphical_properties"]["panel_elements_information"][element]["states"][element_state]["pos"][1]
                ))
            
            screen.blit(
                pg.transform.scale(panel_surface,
                    (
                        panel_surface.get_width()*panel_scale,
                        panel_surface.get_height()*panel_scale
                    )),
                (
                    w/2-panel.get_width()/2*panel_scale, 
                    h-panel.get_height()*panel_scale
                )
            )

            if debug > 0:
                info_blit_list.append(font.render(f"reverser: {controlled_tram.driving_direction}",True,(0,0,0)))
                info_blit_list.append(font.render(f"mover: {controlled_tram.movement_direction}",True,(0,0,0)))
                info_blit_list.append(font.render(f"velocity: {controlled_tram.velocity}",True,(0,0,0)))

        if debug > 0:
            info_blit_list.append(font.render(f"x:{player_pos[0]} y:{player_pos[1]}",True,(0,0,0)))
            pg.draw.rect(screen,(255,0,0),(w/2-4,h/2-4,8,8))
        info_blit_list.append(font.render("fps: "+str(int(clock.get_fps())), False, ((255 if clock.get_fps() < 45 else 0), (255 if clock.get_fps() > 15 else 0), 0)))
        for i, line in enumerate(info_blit_list):
            screen.blit(line, (0, 20*i))

    elif game_state == "editor":
        speed = 4 if pressed[pg.K_LSHIFT] else 1

        if pressed[pg.K_DOWN]: 
            camera_pos[1]+=speed*clock.get_fps()/60
        if pressed[pg.K_UP]: 
            camera_pos[1]-=speed*clock.get_fps()/60
        if pressed[pg.K_LEFT]: 
            camera_pos[0]-=speed*clock.get_fps()/60
        if pressed[pg.K_RIGHT]: 
            camera_pos[0]+=speed*clock.get_fps()/60
        if pressed[pg.K_ESCAPE]:
            game_state = "main"
        if pg.K_q in keydowns:
            print(world)
            print(track_switch_states)        
        
        m_pos = pg.mouse.get_pos()
        m_btn = pg.mouse.get_pressed()
        if pg.K_d in keydowns: debug = (debug+1)%3
        
        if mouse_clicked:
            if not(m_pos[0] > w/2-64*(len(tools[toolkit][editing_tab])+1) and m_pos[0] < w/2+64*(len(tools[toolkit][editing_tab])+1) and m_pos[1] > h-128): 
                block_pos = (int((m_pos[0]+camera_pos[0]-w/2)/128)-(1 if (m_pos[0]+camera_pos[0]-w/2) < 0 else 0),int((m_pos[1]+camera_pos[1]-h/2)/128)-(1 if (m_pos[1]+camera_pos[1]-h/2) < 0 else 0))
                if m_btn[0] and not m_btn[2] and tool != -1:
                    world[block_pos] = f"{toolkit}:{tools[toolkit][editing_tab][tool]}"
                    if tools[toolkit][editing_tab][tool][-4:-1] == "tsw":
                        track_switch_states[block_pos] = False
                elif m_btn[2] and not m_btn[0]:
                    if block_pos in world: 
                        world.pop(block_pos)
                    
                    if block_pos in track_switch_states:
                        track_switch_states.pop(block_pos)
            else:
                selected_item = int((m_pos[0]-w/2+64*(len(tools[toolkit][editing_tab])+1))//128)
                if selected_item < len(tools[toolkit][editing_tab]): 
                    if tool != selected_item:tool = selected_item
                    else: tool=-1
                else:
                    if m_pos[1] < h-64:editing_tab=(editing_tab-1)%len(tools[toolkit])
                    else:editing_tab=(editing_tab+1)%len(tools[toolkit])
            

        screen.fill((128,128,128))

        visible_objects = []

        for x_coord, y_coord in MAPPING:
            tile_coordinates = (int((camera_pos[0]-(127 if camera_pos[0]< 0 else 0))/128)+x_coord,int((camera_pos[1]-(127 if camera_pos[1]< 0 else 0))/128)+y_coord)

            base_tile_blit_coords = (
                w/2+(x_coord*128-int(camera_pos[0])%128),
                h/2+(y_coord*128-int(camera_pos[1])%128)
            )
            centered_coords = (
                w/2+(x_coord*128-int(camera_pos[0])%128+64),
                h/2+(y_coord*128-int(camera_pos[1])%128+64)
            )

            if tile_coordinates in world:
                packet, sprite = world[tile_coordinates].split(":")
                size = sprites[packet][sprite]["sprite"].get_size()
                offset_horizontal = (x_coord*128-int(camera_pos[0])%128)
                offset_vertical = (y_coord*128-int(camera_pos[1])%128)
                tile_blit_coords = (
                    w/2+offset_horizontal+sprites[packet][sprite]["offset"][0]*4,
                    h/2+offset_vertical+sprites[packet][sprite]["offset"][1]*4
                )
                screen.blit(sprites[packet][sprite]["sprite"],tile_blit_coords)
            tile_blit_coords = (
                base_tile_blit_coords[0],
                base_tile_blit_coords[1]#+128*math.cos(math.radians(self.angle))-size[1]
            )
            pg.draw.polygon(screen,(20,20,20),(
                base_tile_blit_coords,
                (base_tile_blit_coords[0]+128,base_tile_blit_coords[1]),
                (base_tile_blit_coords[0]+128,base_tile_blit_coords[1]+128),
                (base_tile_blit_coords[0],base_tile_blit_coords[1]+128),
                ),2
            )

            if debug > 0:
                if debug > 1:
                    pg.draw.rect(screen,(0,255,0),base_tile_blit_coords+(4,4),2)
                    pg.draw.rect(screen,(0,255,0),centered_coords+(4,4),2)
                    pos = font.render(f"{x_coord}:{y_coord}",True,(0,0,0))
                    screen.blit(pos,[centered_coords[0]-pos.get_width()/2,centered_coords[1]-pos.get_height()])
                    pos = font.render(f"{tile_coordinates[0]}:{tile_coordinates[1]}",True,(0,0,0))
                    screen.blit(pos,[centered_coords[0]-pos.get_width()/2,centered_coords[1]+pos.get_height()])
        
        length = len(tools[toolkit][editing_tab])+1
        pg.draw.rect(screen,(196,196,196),(w/2-64*length,h-128,128*length,128))
        for e,i in enumerate(tools[toolkit][editing_tab]):
            screen.blit(pg.transform.scale(sprites[toolkit][i]["sprite"],(128,128)),(w/2-64*length+e*128,h-128))
            pg.draw.rect(screen,(255,255,255) if e==tool else (32,32,32),(w/2-64*length+e*128,h-128,128,128),4)
        pg.draw.rect(screen,(32,32,32),(w/2+64*(length-2),h-128,128,64),4)
        pg.draw.rect(screen,(32,32,32),(w/2+64*(length-2),h-64,128,64),4)
        pg.draw.polygon(screen,(32,32,32),((w/2+64*(length-2)+64,h-128+16),(w/2+64*(length-2)+64+32,h-128+48),(w/2+64*(length-2)+64-32,h-128+48)))
        pg.draw.polygon(screen,(32,32,32),((w/2+64*(length-2)+64,h-16),(w/2+64*(length-2)+64+32,h-48),(w/2+64*(length-2)+64-32,h-48)))


    elif game_state == "main":
        screen.fill((128,128,128))
        w, h = screen.get_size()
        text = font.render(f"1 to play alone",True,(0,0,0))
        screen.blit(text,(w/2-text.get_width()/2,h/2-text.get_height()))
        text = font.render(f"2 to go to editor",True,(0,0,0))
        screen.blit(text,(w/2-text.get_width()/2,h/2+text.get_height()))

        if pg.K_1 in keydowns:
            game_state = "playing_singleplayer"
        if pg.K_2 in keydowns:
            game_state = "editor"

    pg.display.update()
    clock.tick(60)
    if not working:
        pg.quit()