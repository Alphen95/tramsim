import pygame as pg
import os
import json
import pathlib

#from player import Player
from tram import Tram

version = "0.4.5.1"
CURRENT_DIRECTORY = pathlib.Path(__file__).parent.resolve()
current_dir = CURRENT_DIRECTORY
MAPPING = [(8, -8), (7, -8), (8, -7), (6, -8), (7, -7), (8, -6), (5, -8), (6, -7), (7, -6), (8, -5), (4, -8), (5, -7), (6, -6), (7, -5), (8, -4), (3, -8), (4, -7), (5, -6), (6, -5), (7, -4), (8, -3), (2, -8), (3, -7), (4, -6), (5, -5), (6, -4), (7, -3), (8, -2), (1, -8), (2, -7), (3, -6), (4, -5), (5, -4), (6, -3), (7, -2), (8, -1), (0, -8), (1, -7), (2, -6), (3, -5), (4, -4), (5, -3), (6, -2), (7, -1), (8, 0), (-1, -8), (0, -7), (1, -6), (2, -5), (3, -4), (4, -3), (5, -2), (6, -1), (7, 0), (8, 1), (-2, -8), (-1, -7), (0, -6), (1, -5), (2, -4), (3, -3), (4, -2), (5, -1), (6, 0), (7, 1), (8, 2), (-3, -8), (-2, -7), (-1, -6), (0, -5), (1, -4), (2, -3), (3, -2), (4, -1), (5, 0), (6, 1), (7, 2), (8, 3), (-4, -8), (-3, -7), (-2, -6), (-1, -5), (0, -4), (1, -3), (2, -2), (3, -1), (4, 0), (5, 1), (6, 2), (7, 3), (8, 4), (-5, -8), (-4, -7), (-3, -6), (-2, -5), (-1, -4), (0, -3), (1, -2), (2, -1), (3, 0), (4, 1), (5, 2), (6, 3), (7, 4), (8, 5), (-6, -8), (-5, -7), (-4, -6), (-3, -5), (-2, -4), (-1, -3), (0, -2), (1, -1), (2, 0), (3, 1), (4, 2), (5, 3), (6, 4), (7, 5), (8, 6), (-7, -8), (-6, -7), (-5, -6), (-4, -5), (-3, -4), (-2, -3), (-1, -2), (0, -1), (1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (-8, -8), (-7, -7), (-6, -6), (-5, -5), (-4, -4), (-3, -3), (-2, -2), (-1, -1), (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (-8, -7), (-7, -6), (-6, -5), (-5, -4), (-4, -3), (-3, -2), (-2, -1), (-1, 0), (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (-8, -6), (-7, -5), (-6, -4), (-5, -3), (-4, -2), (-3, -1), (-2, 0), (-1, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 8), (-8, -5), (-7, -4), (-6, -3), (-5, -2), (-4, -1), (-3, 0), (-2, 1), (-1, 2), (0, 3), (1, 4), (2, 5), (3, 6), (4, 7), (5, 8), (-8, -4), (-7, -3), (-6, -2), (-5, -1), (-4, 0), (-3, 1), (-2, 2), (-1, 3), (0, 4), (1, 5), (2, 6), (3, 7), (4, 8), (-8, -3), (-7, -2), (-6, -1), (-5, 0), (-4, 1), (-3, 2), (-2, 3), (-1, 4), (0, 5), (1, 6), (2, 7), (3, 8), (-8, -2), (-7, -1), (-6, 0), (-5, 1), (-4, 2), (-3, 3), (-2, 4), (-1, 5), (0, 6), (1, 7), (2, 8), (-8, -1), (-7, 0), (-6, 1), (-5, 2), (-4, 3), (-3, 4), (-2, 5), (-1, 6), (0, 7), (1, 8), (-8, 0), (-7, 1), (-6, 2), (-5, 3), (-4, 4), (-3, 5), (-2, 6), (-1, 7), (0, 8), (-8, 1), (-7, 2), (-6, 3), (-5, 4), (-4, 5), (-3, 6), (-2, 7), (-1, 8), (-8, 2), (-7, 3), (-6, 4), (-5, 5), (-4, 6), (-3, 7), (-2, 8), (-8, 3), (-7, 4), (-6, 5), (-5, 6), (-4, 7), (-3, 8), (-8, 4), (-7, 5), (-6, 6), (-5, 7), (-4, 8), (-8, 5), (-7, 6), (-6, 7), (-5, 8), (-8, 6), (-7, 7), (-6, 8), (-8, 7), (-7, 8), (-8, 8)]

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
pg.display.set_caption(f"Alphen's Tramway Simulator v{version}")
font = pg.font.Font(os.path.join(CURRENT_DIRECTORY,"res","verdana.ttf"),20)

with open(os.path.join(CURRENT_DIRECTORY,"res","sprite_list.json")) as f:
    sprite_list = json.loads(f.read())

world = {}
track_switch_states = {}

#world = {(2,5):"house",(3,5):"house",(4,5):"house_widewindows",(5,5):"house",(6,5):"house"}


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

editing_tab = 0
tool = -1
tools = [
    ["track_straight_horizontal","track_straight_vertical","track_diagonal_a","track_diagonal_b"],
    ["track_curve_1","track_curve_2","track_curve_3","track_curve_4","track_curve_5","track_curve_6","track_curve_7","track_curve_8"],
    ["track_switch_1","track_switch_2","track_switch_3","track_switch_4","track_switch_5","track_switch_6","track_switch_7","track_switch_8"]
]


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

    #for rotation in range(0,360,15):
    rotation = 0
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
    m_block_pos = (int((m_pos[0]+camera_pos[0]-w/2)/128)-(1 if (m_pos[0]+camera_pos[0]-w/2) < 0 else 0),int((m_pos[1]+camera_pos[1]-h/2)/128)-(1 if (m_pos[1]+camera_pos[1]-h/2) < 0 else 0))


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
                    if tile == "track_straight_horizontal":
                        trams.append(Tram([block_pos[0]*128+64,block_pos[1]*128+64],world,tram_info["ktm5m4"],track_switch_states))
                        trams[-1].angle = 180 if pressed[pg.K_LALT] else 0
                    if tile == "track_straight_vertical":
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
            scale = controlled_tram.parameters["graphical_properties"]["panel_scale"]
            player_pos = [controlled_tram.pos[0],controlled_tram.pos[1]]
            if pressed[pg.K_ESCAPE]: 
                controlling_tram_id = -1

            if pg.K_DOWN in keydowns: 
                controlled_tram.km_pos -= 1 if controlled_tram.parameters["technical_properties"]["km_boundaries"][0] < controlled_tram.km_pos else 0
            if pg.K_UP in keydowns: 
                controlled_tram.km_pos += 1 if controlled_tram.parameters["technical_properties"]["km_boundaries"][1] > controlled_tram.km_pos else 0
            
            if m_pos[0] > w/2-panel.get_width()/2 and m_pos[0] < w/2+panel.get_width()/2 and m_pos[1] > h-panel.get_height():
                for element in controlled_tram.driver_panel_element_states:
                    if controlled_tram.parameters["graphical_properties"]["panel_elements_information"][element]["type"] in controlled_tram.parameters["graphical_properties"]["clickable_ui_elements"]:
                        element_state = str(controlled_tram.driver_panel_element_states[element])
                        full_info = controlled_tram.parameters["graphical_properties"]["panel_elements_information"][element]
                        if m_pos[0] > w/2-panel.get_width()/2+(full_info["states"][element_state]["pos"][0])*scale and m_pos[1] > h-panel.get_height()+(full_info["states"][element_state]["pos"][1])*scale and m_pos[0] < w/2-panel.get_width()/2+(full_info["states"][element_state]["pos"][0]+full_info["states"][element_state]["collision_box"][0])*scale and m_pos[1] < h-panel.get_height()+(full_info["states"][element_state]["pos"][1]+full_info["states"][element_state]["collision_box"][1])*scale:
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
            if camera_pos[0]-7*128 <= object["pos"][0] <= camera_pos[0]+7*128 and camera_pos[1]-7*128 <= object["pos"][1] <= camera_pos[1]+7*128:
                visible_objects.append(object)

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
                size = sprites[world[tile_coordinates]][0].get_size()
                offset_horizontal = (x_coord*128-int(camera_pos[0])%128+64)
                offset_vertical = (y_coord*128-int(camera_pos[1])%128+64)
                tile_blit_coords = (
                    w/2+offset_horizontal-size[0]/2,
                    h/2+offset_vertical-(size[1]-sprites[world[tile_coordinates]]["height"])/2-sprites[world[tile_coordinates]]["height"]
                )
                screen.blit(sprites[world[tile_coordinates]][0],tile_blit_coords)

                if tile_coordinates == m_block_pos and "switch" in world[tile_coordinates]:
                    if track_switch_states[m_block_pos]:
                        screen.blit(pg.transform.rotate(pg.transform.flip(sprites["ui_switch_alt"][0],int(world[tile_coordinates][-1])%2==0,False),(int(world[tile_coordinates][-1])-1)//2*-90),tile_blit_coords)
                    else:
                        size = sprites["ui_switch_normal"][0].get_size()
                        tile_blit_coords = (
                            w/2+offset_horizontal-size[0]/2,
                            h/2+offset_vertical-(size[1]-sprites[world[tile_coordinates]]["height"])/2-sprites[world[tile_coordinates]]["height"]
                        )
                        if int(world[tile_coordinates][-1]) in [3,4,7,8]:screen.blit(sprites["ui_switch_normal"][0],tile_blit_coords)
                        else:screen.blit(pg.transform.rotate(sprites["ui_switch_normal"][0],90),tile_blit_coords)

            tile_blit_coords = (
                base_tile_blit_coords[0],
                base_tile_blit_coords[1]#+128*math.cos(math.radians(self.angle))-size[1]
            )

            if debug > 0:
                if debug > 1:
                    pg.draw.polygon(screen,(255,0,0),(
                        base_tile_blit_coords,
                        (base_tile_blit_coords[0]+128,base_tile_blit_coords[1]),
                        (base_tile_blit_coords[0]+128,base_tile_blit_coords[1]+128),
                        (base_tile_blit_coords[0],base_tile_blit_coords[1]+128),
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
                w/2+(visible_object["pos"][0]-camera_pos[0]),
                h/2+(visible_object["pos"][1]-camera_pos[1])
            )
            sprite_w,sprite_h = sprites[visible_object["type"]][(visible_object["angle"])//5*5%360].get_size()
            
            screen.blit(sprites[visible_object["type"]][(0-visible_object["angle"])//5*5%360],(
                object_blit_coords[0]-sprite_w/2,
                object_blit_coords[1]-(sprite_h-sprites[visible_object["type"]]["height"])/2-sprites[visible_object["type"]]["height"]
            ))
            if debug > 0:
                pg.draw.rect(screen,(0,255,0),object_blit_coords+(4,4),2)


        info_blit_list = []
        info_blit_list.append(font.render(version,True,(0,0,0)))
        if debug > 0:
            info_blit_list.append(font.render(f"tramcars: {len(trams)}",True,(0,0,0)))

        w,h = screen.get_size()
        if controlled_tram != []:
            panel = sprites[controlled_tram.parameters["graphical_properties"]["panel_texture_name"]]
            km_handle = sprites[controlled_tram.parameters["graphical_properties"]["km_handle_texture_name"]]
            scale = controlled_tram.parameters["graphical_properties"]["panel_scale"]
            mapouts = controlled_tram.parameters["graphical_properties"]["km_handle_draw_mapouts"]

            screen.blit(panel,(w/2-panel.get_width()/2, h-panel.get_height()))
            screen.blit(km_handle,(w/2-panel.get_width()/2-km_handle.get_width()/2+mapouts[str(controlled_tram.km_pos)]["pos"][0]*scale, h-panel.get_height()-km_handle.get_height()/2+mapouts[str(controlled_tram.km_pos)]["pos"][1]*scale))

            for element in controlled_tram.driver_panel_element_states:

                element_state = str(controlled_tram.driver_panel_element_states[element])
                screen.blit(sprites[controlled_tram.parameters["graphical_properties"]["panel_elements_information"][element]["states"][element_state]["texture"]],(w/2-panel.get_width()/2+controlled_tram.parameters["graphical_properties"]["panel_elements_information"][element]["states"][element_state]["pos"][0]*scale,h-panel.get_height()+controlled_tram.parameters["graphical_properties"]["panel_elements_information"][element]["states"][element_state]["pos"][1]*scale))
            
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
            if not(m_pos[0] > w/2-64*(len(tools[editing_tab])+1) and m_pos[0] < w/2+64*(len(tools[editing_tab])+1) and m_pos[1] > h-128): 
                block_pos = (int((m_pos[0]+camera_pos[0]-w/2)/128)-(1 if (m_pos[0]+camera_pos[0]-w/2) < 0 else 0),int((m_pos[1]+camera_pos[1]-h/2)/128)-(1 if (m_pos[1]+camera_pos[1]-h/2) < 0 else 0))
                if m_btn[0] and not m_btn[2] and tool != -1:
                    world[block_pos] = tools[editing_tab][tool]
                    if "switch" in tools[editing_tab][tool]:
                        track_switch_states[block_pos] = False
                elif m_btn[2] and not m_btn[0]:
                    if block_pos in world: 
                        world.pop(block_pos)
                    
                    if block_pos in track_switch_states:
                        track_switch_states.pop(block_pos)
            else:
                selected_item = int((m_pos[0]-w/2+64*(len(tools[editing_tab])+1))//128)
                if selected_item < len(tools[editing_tab]): 
                    if tool != selected_item:tool = selected_item
                    else: tool=-1
                else:
                    if m_pos[1] < h-64:editing_tab=(editing_tab-1)%len(tools)
                    else:editing_tab=(editing_tab+1)%len(tools)
            

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
                size = sprites[world[tile_coordinates]][0].get_size()
                offset_horizontal = (x_coord*128-int(camera_pos[0])%128+64)
                offset_vertical = (y_coord*128-int(camera_pos[1])%128+64)
                tile_blit_coords = (
                    w/2+offset_horizontal-size[0]/2,
                    h/2+offset_vertical-(size[1]-sprites[world[tile_coordinates]]["height"])/2-sprites[world[tile_coordinates]]["height"]
                )
                screen.blit(sprites[world[tile_coordinates]][0],tile_blit_coords)
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
        
        length = len(tools[editing_tab])+1
        pg.draw.rect(screen,(196,196,196),(w/2-64*length,h-128,128*length,128))
        for e,i in enumerate(tools[editing_tab]):
            screen.blit(pg.transform.scale(sprites[i][0],(128,128)),(w/2-64*length+e*128,h-128))
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