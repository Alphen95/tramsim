import pygame as pg
import threading
import os
import json
import pathlib
import time

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
font = pg.font.SysFont("Arial",32)

pole_pairs = 2
winding_conductors_amt = 10
magnetic_flow = 1
branches_amount = 5
anchor_resistance = 0.25

current_energy = 0
flywheel_mass = 4687
flywheel_radius = 0.355
anchor_voltage = 0
pi = 3.1415
rpm = 0
angle = 0

mode = "neutral"
braking_resistance = 1
net_voltage = 0
transmissional_number = 7.143

torque = 0

working = True

max_km = 8
min_km = 0
current_km = 0

velocity_chart = [-1]*360*5

mapouts = {
    "8":{"mode":"accel","voltage":275},
    "7":{"mode":"accel","voltage":250},
    "6":{"mode":"accel","voltage":225},
    "5":{"mode":"accel","voltage":200},
    "4":{"mode":"accel","voltage":175},
    "3":{"mode":"accel","voltage":150},
    "2":{"mode":"accel","voltage":100},
    "1":{"mode":"accel","voltage":50},
    "0":{"mode":"neutral"}
}

w,h = screen.get_size()

def engine_cycle():
    global pole_pairs, winding_conductors_amt, magnetic_flow, branches_amount, anchor_resistance, current_energy, flywheel_mass, flywheel_radius, anchor_voltage, pi, rpm,braking_resistance, net_voltage, torque, working, mapouts, current_km, transmissional_number

    while working:
        mode = mapouts[str(current_km)]["mode"]

        if mode == "accel":

            net_voltage = mapouts[str(current_km)]["voltage"]
            anchor_voltage = net_voltage
            torque = pole_pairs * winding_conductors_amt * (anchor_voltage - pole_pairs * winding_conductors_amt * rpm * transmissional_number * magnetic_flow / 60 / branches_amount) * magnetic_flow / 2 / pi / branches_amount / anchor_resistance
            
            roll_friction_power = 0.05*flywheel_mass*9.81*rpm*2*pi/60/120/2
            current_energy += torque*transmissional_number-roll_friction_power

            rpm = flywheel_radius * (current_energy / flywheel_mass)**0.5 / pi * 60
        
        time.sleep(1/960)

wheel = pg.Surface((64,64))
pg.draw.circle(wheel,(20,20,20),(32,32),32)
pg.draw.circle(wheel,(100,100,100),(32,32),28)
pg.draw.line(wheel,(230,230,230),(32,4),(32,32),4)
wheel.set_colorkey((0,0,0))

engine_thread = threading.Thread(target=engine_cycle,daemon=True)
engine_thread.start()

while working:
    m_btn_down = False

    screen.fill((128,128,128))
    keydowns = []
    for evt in pg.event.get():
        if evt.type == pg.QUIT:
            working = False
        elif evt.type == pg.KEYDOWN:
            if evt.key == pg.K_UP and max_km > current_km:
                current_km +=1
            elif evt.key == pg.K_DOWN and min_km < current_km:
                current_km -= 1

        elif evt.type == pg.MOUSEBUTTONDOWN:
            m_btn_down = True
        
    m_pos = pg.mouse.get_pos()
    m_btn = pg.mouse.get_pressed()

    keys = pg.key.get_pressed()

    texts = [
        "fps: "+str(int(clock.get_fps())),
        f"энергия: {current_energy} Дж",
        f"оборотов в минуту: {rpm}",
        f"оборотов в минуту на двигателе: {rpm*transmissional_number}",
        f"угловая скорость: {rpm*2*pi/60} рад/с",
        f"угловая скорость вала двигателя: {rpm*2*pi/60*transmissional_number} рад/с",
        f"линейная скорость: {round(rpm*2*pi/60*flywheel_radius*3.6,2)} км/ч",
        f"напряжение в цепи: {net_voltage} В",
    ]

    for pos, line in enumerate(texts):
        screen.blit(font.render(line,True,(0,0,0)), (0, 20+40*pos))

    try:angle += rpm*2*pi/60/float(clock.get_fps())*57.2958
    except:pass
    angle %= 360

    rotated_wheel = pg.transform.rotate(wheel,angle)
    screen.blit(rotated_wheel,(w/2-rotated_wheel.get_width()/2,h/2-rotated_wheel.get_height()/2))

    pg.draw.line(screen,(0,0,0),(w/4*3-2,h/4+2),(w/4*3-2,h/4-200))
    pg.draw.line(screen,(0,0,0),(w/4*3-2,h/4+2),(w/4*3+360,h/4+2))
    pg.draw.line(screen,(0,0,0),(w/4*3-2,h/4-40),(w/4*3+360,h/4-40))
    pg.draw.line(screen,(0,0,0),(w/4*3-2,h/4-80),(w/4*3+360,h/4-80))
    pg.draw.line(screen,(0,0,0),(w/4*3-2,h/4-120),(w/4*3+360,h/4-120))
    pg.draw.line(screen,(0,0,0),(w/4*3-2,h/4-160),(w/4*3+360,h/4-160))

    for pos, point in enumerate(velocity_chart):
        if point > -1 and pos%5==0:
            screen.set_at((int(w/4*3+pos//5),int(h/4-point*2)),(255,0,0))


    velocity_chart.append(round(rpm*2*pi/60*flywheel_radius*3.6,2))
    if len(velocity_chart) > 360*5: velocity_chart = velocity_chart[1:]

    pg.display.update()
    clock.tick(60)

    if not working:
        pg.quit()