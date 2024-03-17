import pygame as pg
import os
import json
import pathlib

pg.init()
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)


print("Alphen's Tram Simulator spritestack render dumping program")
tram_folder = input("Enter name of folder with tram json to get renders of>")
current_dir = pathlib.Path(__file__).parent.resolve()

folder_contents = os.listdir(os.path.join(current_dir,"trams",tram_folder))
if "tram.json" in folder_contents:
    print("Located json file in specified folder!")
    with open(os.path.join(current_dir,"trams",tram_folder,"tram.json")) as file:
        info = json.loads(file.read())

        sprite_params = info["graphical_properties"]["texture_parameters"]

        base_sprite = pg.image.load(os.path.join(*([current_dir,"trams",tram_folder]+info["graphical_properties"]["texture_path"]))).convert_alpha()
        base_layers = []
        for i in range(sprite_params["layer_amount"]):
            y_pos = sprite_params["h_layer"]*i if not ("reversed" in sprite_params and sprite_params["reversed"]) else sprite_params["h_layer"]*(sprite_params["layer_amount"]-1-i)
            base_layers.append(pg.transform.scale(base_sprite.subsurface(0,y_pos,sprite_params["w_layer"],sprite_params["h_layer"]),(sprite_params["w_layer"]*4,sprite_params["h_layer"]*4)))

        sprite_stack_factor = 3

        if not os.path.exists(os.path.join(current_dir,"renders")):
            os.makedirs(os.path.join(current_dir,"renders"))

        for rotation in range(0,360,15):
            w, h = pg.transform.rotate(base_layers[0],rotation).get_size()

            surface = pg.Surface((w,h+sprite_params["layer_amount"]*sprite_stack_factor-1))
            surface.set_colorkey((0,0,0))

            for i in range(sprite_params["layer_amount"]*sprite_stack_factor):
                pos = (0,surface.get_height()-i-h)
                surface.blit(pg.transform.rotate(base_layers[int(i/sprite_stack_factor)],rotation),pos)
                pg.image.save(surface,os.path.join(current_dir,"renders",f"{info['system_name']}_{rotation}.png"))

pg.quit()