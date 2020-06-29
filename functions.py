import math
import numpy as np
import matplotlib.pyplot as plt

def plot_function(x_vals: list, y_vals: list, plt_xlbl: str, plt_ylbl: str, plt_name: str, plt_size: tuple=(16, 8), plt_path: str='img/'):

    plt.figure(figsize=plt_size)
    plt.xlabel(plt_xlbl)
    plt.ylabel(plt_ylbl)
    plt.title(plt_name)
    plt.plot(x_vals, y_vals)
    plt.grid(True)
    plt.savefig(plt_path + plt_name + '.png')

class Particle:

    """
    Particle class, defining initial x and y position, velocity, angle and mass
    Default units: [Velocity: m/s, Angle: deg, Position: m, Mass: kg]
    
    """

    def __init__(self, initial_y_pos: float, initial_vel: float, initial_ang: float, m: float, vel_dtype='m/s', ang_dtype='deg', pos_dtype='m'):

        self.initial_y_pos = initial_y_pos
        self.initial_vel = initial_vel
        self.initial_ang = initial_ang
        self.m = m
        self.pos_y = 0
        self.y_pos_max = 0
        self.touchdown_time = None

    def calculate_initial_momentum(self):

        self.p = (self.m * self.initial_vel * math.cos(math.radians(self.initial_ang)), self.m * self.initial_vel * math.sin(math.radians(self.initial_ang)))
    
    def velocity_comps(self, velocity, angle):
        
        return (velocity * math.cos(math.radians(angle)), velocity * math.sin(math.radians(angle)))

    def calculate_force_gravity(self, acceleration: float):

        return self.m * acceleration
    
    def current_pos_y(self, time: float, acceleration: float):

        velocity_y = self.velocity_comps(self.initial_vel, self.initial_ang)[1]
        self.y_pos = self.initial_y_pos + velocity_y * time + 0.5 * acceleration * (time ** 2)

        return self.y_pos

    def current_kinetic_energy(self, time: float, acceleration: float):

        velocity_y = self.velocity_comps(self.initial_vel, self.initial_ang)[1] + acceleration * time
        velocity_x = self.velocity_comps(self.initial_vel, self.initial_ang)[0]
        kinetic_energy = 0.5 * self.m * math.sqrt(velocity_y ** 2 + velocity_x ** 2)

        return kinetic_energy

    def current_potential_energy(self, time: float, acceleration: float):

        y_pos = self.current_pos_y(time, acceleration)
        potential_energy = self.m * acceleration * y_pos

        return potential_energy
    
    def time_at_touchdown(self, y_pos_final: float, acceleration: float):

        self.touchdown_time = np.amax(np.roots([acceleration * 0.5, self.velocity_comps(self.initial_vel, self.initial_ang)[1], self.initial_y_pos - y_pos_final]))
    
    def calculate_y_max(self, acceleration: float):

        self.y_pos_max = -self.velocity_comps(self.initial_vel, self.initial_ang)[1] ** 2 / (2 * acceleration)

        return self.y_pos_max

    def projectile_path_generator(self, acceleration: float, initial_time: float, final_time: float, step_count: int=0, conditional_stop: bool=False, y_stop_pos: float=0):

        if step_count == 0:
            step_count = round((final_time - initial_time)) * 50
        if step_count < 0:
            step_count = abs(step_count)

        time_array = np.linspace(initial_time, final_time, step_count)
        pos_x_array = self.velocity_comps(self.initial_vel, self.initial_ang)[0] * time_array
        pos_y_array = np.zeros(len(time_array))

        for i in range(len(time_array)):

            pos_y_array[i] = self.current_pos_y(time_array[i], acceleration) 

            if conditional_stop:
                self.time_at_touchdown(y_stop_pos, acceleration)
                if (self.touchdown_time - time_array[i]) < 0.01:
                    pos_y_array[i:] = y_stop_pos

                    break
    
        projectile_path = [time_array, pos_x_array, pos_y_array]
            
        return projectile_path
