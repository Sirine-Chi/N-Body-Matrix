# N-Body Simulations

## General
Here are the physical simulation of N-body with start positions and velocities, in gravitational field. In First November realise the space is 2-dimensional. Written on python with object-based programming ideas, as visualisator I use MatPlotLib livrary. Start configuration, masses and everything about objects are written in Config.txt. You can run programm with Start.py, all computational functions are written in NBodyLib.py, all visual in Visualise.py.

## Plans
Now I'm making the visualisation of gravitational potential field and 3-dimensional version. I'm planning to make on Open-CL version to improve performance.

## About config.txt
Here you can find a settings: Mode (Simulation, Progons, Field) – make 1 simulation/make some simulations with different start positions/show evolution of gravitational field, Force function(any type) – if you written correctly, sets function of the force, Method (Eiler, Adams) – what numerical method in use to solve ODE, End_time – how many model years will be simulated, Time_step – time interval in numerical methods, Time_direction (+1/-1) – to future/to past, Pulse_table – make table of full system pulse or no.

## Rights
You can use it as you want.