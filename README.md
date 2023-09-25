# N-Body Simulations

## General

Here is the physical simulation of the N-body problem with start positions and velocities, in a gravitational field. The space is 2-dimensional. Written in Python with OpenCL for computing acceleration (matrix multiplication), the MatPlotLib library is used as the visualization tool.
Program settings are stored in Config.yaml. The start conditions of the objects are in the systems_data folder in CSV tables. You can run the program by running the Start.py file, all computational functions are written in NBodyLib.py, and all the visual tools in Visualise.py. If you want to generate your own start configuration you are able to run Generator.py, it will write to table.csv new objects with random distribution parameters you can set.

## Installation

Download the source code as a zip archive or clone the project using the Git CLI.

Python 3 must be installed on your device.

### Linux and MacOS:

In your project directory that contains "nbody":

- create Python virtual environment (in the project directory folder open the terminal and run `python -m venv venv`)
- activate virtual environment (run `source venv/bin/activate`)
- install requirements.txt. (run `pip install -r requirements.txt`)

### Windows

In your project directory that contains "nbody":

- create Python virtual environment (in the project directory folder open the terminal and run `python -m venv venv`)
- activate virtual environment (run `.\venv\Scripts\activate`)
- install the dependencies (run `pip install -r requirements.txt`)

If all dependencies have been installed successfully, the application is ready to use. If you have troubles with venv, you can manually install all the libraries from requirements.txt to your global python, but **this way is not recommended**.

## Archeticture

...Reloading...

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

This software is distributed under the MIT license.
