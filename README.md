# N-Body Simulations

## General
Here are the physical simulation of N-body problem with start positions and velocities, in gravitational field. The space is 2-dimensional. Written on python with openCL for computing acceleration (matrix multiplication), as visualisator I use MatPlotLib library.

Program settings are stored in Config.yaml. Start conditions of the objects are in systems_data folder in CSV tables. You can run programm with Start.py, all computational functions are written in NBodyLib.py, all visual in Visualise.py. If you want to generate your own start configuration you are able to run Generator.py, it will write to table.csv new objects with random distribution parameters you can set.

## Installation
Download source code as zip or clone with git.

You must be sure that you have python language on your device.
Install pip and virtualenv libraries to your global python (run in termianl `python get-pip.py`, and after `pip install virtualenv`).

In your project directory that contains "nbody",
- create python virtual enviroment (in project directory folder open terminal and run `virtualenv venv`, if troubles - google it)
- activate virtual enviroment (unix: run `source venv/bin/activate`, windows: run `source venv\Scripts\activate`)
- install requirements.txt. (run `pip install -r requirements.txt`)
If all have been installed correct, you are ready to use. If you have troubles with venv, you can manualy install all the libraries from requirements.txt to your global python, but I don't recommend this.

## Archeticture
![ММС 10 2](https://github.com/Sirine-Chi/N-Body-Matrix/assets/71520044/8b96fb0b-b24b-458b-8729-2494c63aa1ed)




## Plans
Now I'm making the visualisation of gravitational potential field and 3-dimensional version.
Also I'm working on c++ version, you can check [that repository](https://github.com/Sirine-Chi/n-body-simulations).

## About config.yaml
Here you can find a settings:
- `Mode` (Simulation, Progons, Field) – make 1 simulation/make some simulations with different start positions/show evolution of gravitational field,
- `Force function`(any type) – if you written correctly, sets function of the force,
- `Method` (Eiler, Adams) – what numerical method in use to solve ODE,
- `End_time` – how many model years will be simulated,
- `Time_step` – time interval in numerical methods,
- `Time_direction` (+1/-1) – to future/to past,
- `Pulse_table` – make table of full system pulse or no.

## About table.csv
In that file the data about the start positions and velocities is stored. Every line must look like this:
`dynamic,Earth,1,1.016725701,0,0,6.174482536,aqua,224`

Except of the header: Type,Name,Mass,R x,R y,V x, Vy, Color, Angle (Deg).
In table's rows first is a type of object (dynamical/analytic), second is it's unique name, third is it's mass, forth and fifth is X and Y coordinates, sixth and seventh is X and Y velocity components, eight is color, ninth is angle in degrees, measured to left side from X axis.

## Copyright
MIT License, open source.
