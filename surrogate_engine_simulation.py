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
winding_conductors_amt = 8
magnetic_flow = 0.9
branches_amount = 2
anchor_resistance = 7.5

current_energy = 0
total_mass = 4687*4
flywheel_mass = 600*4
engine_amt = 4
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

max_km = 4
min_km = -4
current_km = 0

velocity_chart = [-1]*360*5

rk_mapouts = {
    "-1":{"voltage":25,"min_angular":0},
    "0":{"voltage":50,"min_angular":0.05},
    "1":{"voltage":75,"min_angular":0.3},
    "2":{"voltage":100,"min_angular":2},
    "3":{"voltage":150,"min_angular":6},
    "4":{"voltage":200,"min_angular":10},
    "5":{"voltage":250,"min_angular":15},
    "6":{"voltage":350,"min_angular":25},
    "7":{"voltage":450,"min_angular":35},
    "8":{"voltage":550,"min_angular":45},
}

mapouts = {
    "4":{"mode":"accel","rk_pos":[-1,0,1,2,3,4,5,6,7,8],"min_change_time":60},
    "3":{"mode":"accel","rk_pos":[-1,0,1,2,3,4,5,6,7],"min_change_time":60},
    "2":{"mode":"accel","rk_pos":[-1,0,1,2,3,4,5],"min_change_time":60},
    "1":{"mode":"accel","rk_pos":[-1,0,1,2,3],"min_change_time":60},
    "0":{"mode":"neutral"},
    "-1":{"mode":"decel","resistance":1500},
    "-2":{"mode":"decel","resistance":750},
    "-3":{"mode":"decel","resistance":400},
    "-4":{"mode":"decel","resistance":150},
}
'''
mapouts = {
    "9":{"mode":"accel","voltage":550,"resistance":2},
    "8":{"mode":"accel","voltage":450,"resistance":2},
    "7":{"mode":"accel","voltage":350,"resistance":2},
    "6":{"mode":"accel","voltage":250,"resistance":2},
    "5":{"mode":"accel","voltage":200,"resistance":2},
    "4":{"mode":"accel","voltage":150,"resistance":2},
    "3":{"mode":"accel","voltage":100,"resistance":2},
    "2":{"mode":"accel","voltage":50,"resistance":2},
    "1":{"mode":"accel","voltage":25,"resistance":2},
    "0":{"mode":"neutral"},
    "-1":{"mode":"decel","resistance":1500},
    "-2":{"mode":"decel","resistance":750},
    "-3":{"mode":"decel","resistance":400},
    "-4":{"mode":"decel","resistance":150},
}
'''
w,h = screen.get_size()

class Engine():
    def __init__(self,pole_pairs, winding_conductors_amt, magnetic_flow, branches_amount, anchor_resistance, current_energy, flywheel_mass, flywheel_radius, anchor_voltage,braking_resistance, mapouts, engine_amt, transmissional_number, total_mass,rk_mapouts):
        self.angular_velocity = 0
        self.current_energy = 0
        self.current_km = 0
        self.electromotive_force = 0
        self.working = True
        self.current_rk = 0
        self.velocity_array = [-1]*360*5
        self.accel = 0
        self.timer = 0
        engine_thread = threading.Thread(target=self.engine_cycle,daemon=True,args=[pole_pairs, winding_conductors_amt, magnetic_flow, branches_amount, anchor_resistance, flywheel_mass, flywheel_radius, anchor_voltage,braking_resistance, mapouts, engine_amt, transmissional_number, total_mass,rk_mapouts])
        engine_thread.start()
    

    def engine_cycle(self, pole_pairs, winding_conductors_amt, magnetic_flow, branches_amount, anchor_resistance, flywheel_mass, flywheel_radius, anchor_voltage,braking_resistance, mapouts, engine_amt, transmissional_number, total_mass,rk_mapouts):
        pi = 3.1415
        net_voltage = 0
        
        while self.working:
            mode = mapouts[str(self.current_km)]["mode"]
            engine_power = 0
            brake_work = 0
            cps = 120
            self.electromotive_force = pole_pairs * winding_conductors_amt * self.angular_velocity * transmissional_number * magnetic_flow / 2 / pi / branches_amount

            if mode == "accel":

                net_voltage = rk_mapouts[str(self.current_rk)]["voltage"]
                anchor_voltage = net_voltage
                anchor_current = (anchor_voltage - self.electromotive_force) / (anchor_resistance)
                engine_power = anchor_current*anchor_voltage*(1 if anchor_current > 0 else 0)
                if self.current_rk < mapouts[str(self.current_km)]["rk_pos"][-1] and self.timer == 0:
                    index = mapouts[str(self.current_km)]["rk_pos"].index(self.current_rk)
                    if self.angular_velocity >= rk_mapouts[str(mapouts[str(self.current_km)]["rk_pos"][index+1])]["min_angular"]:
                        self.current_rk = mapouts[str(self.current_km)]["rk_pos"][index+1]
                        self.timer = mapouts[str(self.current_km)]["min_change_time"]
                elif self.current_rk > mapouts[str(self.current_km)]["rk_pos"][-1]: self.current_rk = mapouts[str(self.current_km)]["rk_pos"][-1]

            else:
                self.current_rk = int(min(list(rk_mapouts.keys())))
                self.timer = 0
                if mode == "decel":
                    brake_work = self.electromotive_force*self.electromotive_force/mapouts[str(self.current_km)]["resistance"]
            
                
            roll_friction_power = 0.03*flywheel_mass*9.81*self.angular_velocity/120
            self.current_energy += engine_power*transmissional_number*0.95*engine_amt/120-roll_friction_power-brake_work
            old_velocity = self.angular_velocity
            self.angular_velocity =  2 * (2*self.current_energy / (0.5*flywheel_mass+total_mass))**0.5 /flywheel_radius
            self.accel = complex((self.angular_velocity-old_velocity)*120).real
            self.current_energy = complex(self.current_energy).real
            self.angular_velocity = complex(self.angular_velocity).real
            self.velocity_array.append(round(self.angular_velocity*flywheel_radius*3.6,2))
            if len(self.velocity_array) > 360*5: self.velocity_array = self.velocity_array[1:]
            if self.timer > 0: self.timer -=1

            time.sleep(1/cps)

wheel = pg.Surface((64,64))
pg.draw.circle(wheel,(20,20,20),(32,32),32)
pg.draw.circle(wheel,(100,100,100),(32,32),28)
pg.draw.line(wheel,(230,230,230),(32,4),(32,32),4)
wheel.set_colorkey((0,0,0))

engines = []
for i in range(1):
    engines.append(Engine(pole_pairs,winding_conductors_amt+2*i,magnetic_flow,branches_amount,anchor_resistance,0,flywheel_mass,flywheel_radius,0,0,mapouts,engine_amt,transmissional_number,total_mass,rk_mapouts))

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
                for engine in engines:
                    engine.current_km = current_km
            elif evt.key == pg.K_DOWN and min_km < current_km:
                current_km -=1
                for engine in engines:
                    engine.current_km = current_km
            elif evt.key == pg.K_8:
                current_km = 8
                for engine in engines:
                    engine.current_km = current_km

        elif evt.type == pg.MOUSEBUTTONDOWN:
            m_btn_down = True
        
    m_pos = pg.mouse.get_pos()
    m_btn = pg.mouse.get_pressed()

    keys = pg.key.get_pressed()
    texts = [
        "fps: "+str(int(clock.get_fps())),
        "позиция км: "+str(current_km),
        #f"энергия: {round(current_energy,2)} Дж",
        #f"оборотов в минуту: {round(rpm,2)}",
        #f"оборотов в минуту на двигателе: {round(rpm*transmissional_number,2)}",
        #f"угловая скорость: {rpm*2*pi/60} рад/с",
        #f"угловая скорость вала двигателя: {rpm*2*pi/60*transmissional_number} рад/с",
        #f"линейная скорость: {round(rpm*2*pi/60*flywheel_radius*3.6,2)} км/ч",
        #f"напряжение в цепи: {net_voltage} В",
    ]

    for pos, line in enumerate(texts):
        screen.blit(font.render(line,True,(0,0,0)), (0, 20+40*pos))
    
    try:angle += rpm*2*pi/60/float(clock.get_fps())*57.2958
    except:pass
    angle %= 360

    rotated_wheel = pg.transform.rotate(wheel,angle)
    screen.blit(rotated_wheel,(w/2-rotated_wheel.get_width()/2,h/2-rotated_wheel.get_height()/2))

    for i in range(1,len(engines)+1):
        pg.draw.line(screen,(0,0,0),(w/4*3-2,h/(len(engines)+1)*i+2),(w/4*3-2,h/(len(engines)+1)*i-200))
        pg.draw.line(screen,(0,0,0),(w/4*3-2,h/(len(engines)+1)*i+2),(w/4*3+360,h/(len(engines)+1)*i+2))
        pg.draw.line(screen,(0,0,0),(w/4*3-2,h/(len(engines)+1)*i-40),(w/4*3+360,h/(len(engines)+1)*i-40))
        pg.draw.line(screen,(0,0,0),(w/4*3-2,h/(len(engines)+1)*i-80),(w/4*3+360,h/(len(engines)+1)*i-80))
        pg.draw.line(screen,(0,0,0),(w/4*3-2,h/(len(engines)+1)*i-120),(w/4*3+360,h/(len(engines)+1)*i-120))
        pg.draw.line(screen,(0,0,0),(w/4*3-2,h/(len(engines)+1)*i-160),(w/4*3+360,h/(len(engines)+1)*i-160))
        screen.blit(font.render(f"{round(engines[i-1].current_rk,2)} - рк поз",True,(0,0,0)), (w/4*3-200, h/(len(engines)+1)*i-180))
        screen.blit(font.render(f"{round(engines[i-1].angular_velocity*flywheel_radius*3.6,2)} км/ч",True,(0,0,0)), (w/4*3-200, h/(len(engines)+1)*i-140))
        screen.blit(font.render(f"{round(engines[i-1].current_energy,2)} Дж",True,(0,0,0)), (w/4*3-200, h/(len(engines)+1)*i-100))
        screen.blit(font.render(f"{round(engines[i-1].electromotive_force,2)} В",True,(0,0,0)), (w/4*3-200, h/(len(engines)+1)*i-60))
        screen.blit(font.render(f"{round(engines[i-1].accel*2*pi/60*flywheel_radius,2)} м/с^2",True,(0,0,0)), (w/4*3-200, h/(len(engines)+1)*i-20))

        for pos, point in enumerate(engines[i-1].velocity_array):
            if point > -1 and pos%5==0:
                screen.set_at((int(w/4*3+pos//5),int(h/(len(engines)+1)*i-point*2)),(255,0,0))
        


    velocity_chart.append(round(rpm*2*pi/60*flywheel_radius*3.6,2))
    if len(velocity_chart) > 360*5: velocity_chart = velocity_chart[1:]

    pg.display.update()
    clock.tick(60)

    if not working:
        pg.quit()