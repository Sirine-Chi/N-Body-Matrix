# N-Body Simulations

## General
Here are the physical simulation of N-body with start positions and velocities, in gravitational field. The space is 2-dimensional. Written on python with openCL for computing acceleration (matrix multiplication), as visualisator I use MatPlotLib library. Program settings are stored in Config.txt. Start conditions of the objects are in System.txt. You can run programm with Start.py, all computational functions are written in NBodyLib.py, all visual in Visualise.py. If you want to generate your own start configuration you are able to run Generator.py, it will write to System.txt new objects with parameters you can set.

## Archeticture
![ММС 10 2](https://github.com/Sirine-Chi/N-Body-Matrix/assets/71520044/8b96fb0b-b24b-458b-8729-2494c63aa1ed)




## Plans
Now I'm making the visualisation of gravitational potential field and 3-dimensional version. I'm planning to make on Open-CL version to improve performance.

## About config.txt
Here you can find a settings: Mode (Simulation, Progons, Field) – make 1 simulation/make some simulations with different start positions/show evolution of gravitational field, Force function(any type) – if you written correctly, sets function of the force, Method (Eiler, Adams) – what numerical method in use to solve ODE, End_time – how many model years will be simulated, Time_step – time interval in numerical methods, Time_direction (+1/-1) – to future/to past, Pulse_table – make table of full system pulse or no.

## About System.txt
In that file the data about the start positions and velocities are stored. Every line must look like this:
obj_(Earth, 1, [1.016725701, 0], [0, 6.174482536], 3, system, 'aqua', 224)
Where the first element id 

## Rights
You can use it as you want.
