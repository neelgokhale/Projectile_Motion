from functions import Particle, plot_function

if __name__ == "__main__":
        
    P = Particle(0, 45, 30, 10)
    g = -9.81

    y_stop = P.calculate_y_max(g)
    print(y_stop)
    
    path = P.projectile_path_generator(g, 0, 10, conditional_stop=True, y_stop_pos=y_stop)
    file_name = 'projectile_path1'

    plot_function(path[1], path[2], 'd_x(t)', 'd_y(t)', file_name)

    print(path[2])