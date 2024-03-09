import math
import time
import threading

class Tram():
    def __init__(self,pos,world,parameters):
        self.km_pos = 0
        self.rk_pos = 0
        self.energies = {
            "engine":0,
            "roll_friction":0,
            "magnet_brake":0,
            "electro_brake":0
        }
        self.train_flags = {
            "doors_r":False,
            "doors_l":False,
            "magnet_brake_active":False,
            "magnet_brake_activation":False,
            "switching_states":False,
            "batteries":False,
            "max_rk":False,
            "ring":False,
            "km":0,
            "reverser":0,
            "speedometer_left":0,
            "speedometer_right":0
        }
        self.driving_direction = 0
        self.movement_direction = 0

        self.parameters = parameters
        self.pos = pos
        self.type = parameters["system_name"]
        self.velocity = 0
        self.angle = 0
        self.last_block_pos = []
        
        self.driver_panel_element_states = {}
        for control_name in parameters["graphical_properties"]["panel_elements_information"]:
            self.driver_panel_element_states[control_name] = parameters["graphical_properties"]["panel_elements_information"][control_name]["default_state"]
        
        self.exists = True
        self.thread = threading.Thread(target=self.cycle,args=[world],daemon=True)
        self.thread.start()
    
    def cycle(self,world):
        roll_friction = 0.05
        slip_friction = 0.2
        free_fall_acceleration = 9.86

        mass = self.parameters["technical_properties"]["mass"]
        radius = self.parameters["technical_properties"]["wheel_radius"]
        magnet_brake_force = self.parameters["technical_properties"]["magnet_brake_force"]
        km_mapouts = self.parameters["technical_properties"]["km_mapouts"]
        rk_mapouts = self.parameters["technical_properties"]["rk_mapouts"]
        resistance = self.parameters["technical_properties"]["engine_resistance"]
        voltage = 0


        self.last_block_pos =(int((self.pos[0]-(127 if self.pos[0]< 0 else 0))/128),int((self.pos[1]-(127 if self.pos[1]< 0 else 0))/128))
        while self.exists:
            #logic block
            if self.train_flags["batteries"]:
                if km_mapouts[str(self.km_pos)]["type"]=="neutral":
                    timer = 0
                    self.rk_pos = 0

                    energy_kinetic = mass*self.velocity*self.velocity/2
                    engine_power = 0
                    roll_friction_power = roll_friction*mass*free_fall_acceleration*self.velocity/120/radius/8
                    if self.train_flags["magnet_brake_activation"]:
                        rail_magnet_brake_power = (magnet_brake_force*slip_friction*self.velocity*4/120)
                        self.train_flags["magnet_brake_active"] = True
                    else:
                        self.train_flags["magnet_brake_active"] = False
                        rail_magnet_brake_power = 0
                    ballast_resistance_power = 0
                elif km_mapouts[str(self.km_pos)]["type"]=="acceleration":
                    if self.driving_direction != 0:
                        if self.rk_pos < km_mapouts[str(self.km_pos)]["rheostat_positions"][0]:
                            self.rk_pos = km_mapouts[str(self.km_pos)]["rheostat_positions"][0]
                        elif self.rk_pos > km_mapouts[str(self.km_pos)]["rheostat_positions"][-1]:
                            self.rk_pos = km_mapouts[str(self.km_pos)]["rheostat_positions"][-1]
                        
                        if self.rk_pos != km_mapouts[str(self.km_pos)]["rheostat_positions"][-1]:
                            if timer == 0:
                                index = km_mapouts[str(self.km_pos)]["rheostat_positions"].index(self.rk_pos)
                                self.rk_pos = km_mapouts[str(self.km_pos)]["rheostat_positions"][index+1]
                                timer = km_mapouts[str(self.km_pos)]["change_time"]

                    
                    voltage = rk_mapouts[str(self.rk_pos)]["voltage"]
                    #split_amt = 4 if rheostat_positions_mapout[rheostat_position]["connection_type"]

                    energy_kinetic = mass*self.velocity*self.velocity/2
                    engine_power = ((20*voltage*voltage)/120/resistance)*(self.driving_direction/self.movement_direction if self.movement_direction != 0 else 0)
                    roll_friction_power = roll_friction*mass*free_fall_acceleration*self.velocity/120/radius/8
                    rail_magnet_brake_power = 0
                    ballast_resistance_power = 0
                    self.train_flags["magnet_brake_active"] = False
                elif km_mapouts[str(self.km_pos)]["type"]=="deceleration":
                    ballast_resistance = km_mapouts[str(self.km_pos)]["brake_resistance"]

                    energy_kinetic = mass*self.velocity*self.velocity/2
                    engine_power = 0
                    roll_friction_power = roll_friction*mass*free_fall_acceleration*self.velocity/120/radius/8
                    if ("magnet_brake" in km_mapouts[str(self.km_pos)] and km_mapouts[str(self.km_pos)]["magnet_brake"]) or self.train_flags["magnet_brake_activation"]:
                        rail_magnet_brake_power = (magnet_brake_force*slip_friction*self.velocity*4/120)
                        self.train_flags["magnet_brake_active"] = True
                    else:
                        self.train_flags["magnet_brake_active"] = False
                        rail_magnet_brake_power = 0
                    ballast_resistance_power = 2*resistance*self.velocity*roll_friction*mass*free_fall_acceleration*self.velocity/120/radius/ballast_resistance
            else:
                timer = 0
                self.rk_pos = 0
                energy_kinetic = mass*self.velocity*self.velocity/2
                roll_friction_power = roll_friction*mass*free_fall_acceleration*self.velocity/120/radius/8
                engine_power = 0
                self.train_flags["magnet_brake_active"] = False
                rail_magnet_brake_power = 0
                ballast_resistance_power = 0
            
            energy_kinetic = round(complex(energy_kinetic).real,2)
            self.energies["engine"] = round(complex(engine_power).real,2)
            self.energies["roll_friction"] = round(complex(roll_friction_power).real,2)
            self.energies["magnet_brake"] = round(complex(rail_magnet_brake_power).real,2)
            self.energies["electro_brake"] = round(complex(ballast_resistance_power).real,2)


            if timer != 0: self.train_flags["switching_states"] = True
            else: self.train_flags["switching_states"] = False

            if self.rk_pos == self.parameters["technical_properties"]["km_boundaries"][1]: self.train_flags["max_rk"] = True
            else: self.train_flags["max_rk"] = False

            self.train_flags["km"] = self.km_pos

            new_velocity = (2*(energy_kinetic+engine_power-roll_friction_power-rail_magnet_brake_power-ballast_resistance_power)/mass)**0.5

            self.velocity = round(complex(new_velocity).real,6)
            if self.velocity == 0: self.movement_direction = self.driving_direction

            if timer > 0: timer -=1

            self.train_flags["speedometer_left"] = int(self.velocity*3.6)//10%10
            self.train_flags["speedometer_right"] = int(self.velocity*3.6)%10

            #movement block
            self.block_pos = (int((self.pos[0]-(127 if self.pos[0]< 0 else 0))/128),int((self.pos[1]-(127 if self.pos[1]< 0 else 0))/128))
            if self.block_pos in world and "track" in world[self.block_pos]:
                if world[self.block_pos] == "track_straight_horizontal":
                    if self.angle == 0 or self.angle == 180:
                        if self.pos[1] > self.block_pos[1]*128+64:
                            self.pos[1] -= 0.2
                        if self.pos[1] < self.block_pos[1]*128+64:
                            self.pos[1] += 0.2
                elif world[self.block_pos] == "track_straight_vertical":
                    if self.angle == 90 or self.angle == 270:
                        if self.pos[0] > self.block_pos[0]*128+64:
                            self.pos[0] -= 0.2
                        if self.pos[0] < self.block_pos[0]*128+64:
                            self.pos[0] += 0.2
                elif world[self.block_pos] == "track_curve_3":
                    
                    diff = self.pos[0]-self.block_pos[0]*128
                    if diff <= 16:
                        self.angle = 0 if self.angle >= 0 and self.angle <= 90 else 180
                    elif diff < 48:
                        self.angle = 15 if self.angle >= 0 and self.angle <= 90 else 195
                    elif diff < 96:
                        self.angle = 30 if self.angle >= 0 and self.angle <= 90 else 210
                    else:
                        self.angle = 45 if self.angle >= 0 and self.angle <= 90 else 225
                elif world[self.block_pos] == "track_curve_2":
                    diff = self.pos[1]-self.block_pos[1]*128
                    if diff >= 112:
                        self.angle = 90 if self.angle >= 0 and self.angle <= 90 else 270
                    elif diff > 80:
                        self.angle = 75 if self.angle >= 0 and self.angle <= 90 else 255
                    elif diff > 32:
                        self.angle = 60 if self.angle >= 0 and self.angle <= 90 else 240
                    else:
                        self.angle = 45 if self.angle >= 0 and self.angle <= 90 else 225
                elif world[self.block_pos] == "track_curve_5":
                    diff = self.pos[1]-self.block_pos[1]*128
                    if diff <= 16: 
                        self.angle = 90 if self.angle >= 90 and self.angle <= 180 else 270
                    elif diff < 48:
                        self.angle = 105 if self.angle >= 90 and self.angle <= 180 else 285
                    elif diff < 96:
                        self.angle = 120 if self.angle >= 90 and self.angle <= 180 else 300
                    else:
                        self.angle = 135 if self.angle >= 90 and self.angle <= 180 else 315
                elif world[self.block_pos] == "track_curve_4":
                    diff = self.pos[0]-self.block_pos[0]*128
                    if diff <= 16: 
                        self.angle = 180 if self.angle >= 90 and self.angle <= 180 else 0
                    elif diff < 48:
                        self.angle = 165 if self.angle >= 90 and self.angle <= 180 else 345
                    elif diff < 96:
                        self.angle = 150 if self.angle >= 90 and self.angle <= 180 else 330
                    else:
                        self.angle = 135 if self.angle >= 90 and self.angle <= 180 else 315
                elif world[self.block_pos] == "track_curve_7":
                    diff = self.pos[0]-self.block_pos[0]*128
                    if diff >= 112:
                        self.angle = 180 if self.angle >= 180 and self.angle <= 270 else 0
                    elif diff > 80:
                        self.angle = 195 if self.angle >= 180 and self.angle <= 270 else 15
                    elif diff > 32:
                        self.angle = 210 if self.angle >= 180 and self.angle <= 270 else 30
                    else:
                        self.angle = 225 if self.angle >= 180 and self.angle <= 270 else 45
                elif world[self.block_pos] == "track_curve_6":
                    diff = self.pos[1]-self.block_pos[1]*128
                    if diff <= 16:
                        self.angle = 270 if self.angle >= 180 and self.angle <= 270 else 90
                    elif diff < 48:
                        self.angle = 255 if self.angle >= 180 and self.angle <= 270 else 75
                    elif diff < 96:
                        self.angle = 240 if self.angle >= 180 and self.angle <= 270 else 60
                    else:
                        self.angle = 225 if self.angle >= 180 and self.angle <= 270 else 45
                elif world[self.block_pos] == "track_curve_1":
                    diff = self.pos[1]-self.block_pos[1]*128
                    if diff >= 112:
                        self.angle = 270 if self.angle >= 270 and self.angle <= 360 else 90
                    elif diff > 80:
                        self.angle = 285 if self.angle >= 270 and self.angle <= 360 else 105
                    elif diff > 32:
                        self.angle = 300 if self.angle >= 270 and self.angle <= 360 else 120
                    else:
                        self.angle = 315 if self.angle >= 270 and self.angle <= 360 else 135
                elif world[self.block_pos] == "track_curve_8":
                    diff = self.pos[0]-self.block_pos[0]*128
                    if diff >= 112:
                        self.angle = 360 if self.angle >= 270 and self.angle <= 360 or self.angle == 0 else 180
                    elif diff > 80:
                        self.angle = 345 if self.angle >= 270 and self.angle <= 360 or self.angle == 0 else 165
                    elif diff > 32:
                        self.angle = 330 if self.angle >= 270 and self.angle <= 360 or self.angle == 0 else 150
                    else:
                        self.angle = 315 if self.angle >= 270 and self.angle <= 360 or self.angle == 0 else 135
            self.last_block_pos = () + self.block_pos
            self.angle = self.angle%360
            self.pos[0]+=round(self.velocity*math.cos(math.radians(self.angle))*0.25*self.movement_direction,2)
            self.pos[1]+=round(self.velocity*math.sin(math.radians(self.angle))*0.25*self.movement_direction,2)

            for element in self.driver_panel_element_states:
                if self.parameters["graphical_properties"]["panel_elements_information"][element]["type"] == "lamp":
                    self.driver_panel_element_states[element] = str(self.train_flags[self.parameters["graphical_properties"]["panel_elements_information"][element]["condition_flag"]])
                
            time.sleep(1/120)