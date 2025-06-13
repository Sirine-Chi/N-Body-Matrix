# Installation

## For Pros

Recommended python 3.11.11 with venv

## Step-by-step Guide

1. Clone project from GitHub to your PC
2. Open in terminal [N-Body-Matrix](../N-Body-Matrix/) folder
3. Create local [Virtual Enviroment](https://docs.python.org/3/library/venv.html)
    1. Be sure you have pyhton and pip, else – install python
    2. Be sure you have virtualenv lib, else – install
        mac: `pip install virtualenv`
    3. Create Venv _(be sure you're in the [N-Body-Matrix](../N-Body-Matrix/) folder)_

        mac: `python<version> -m venv <virtual-environment-name>`

        mac-example (recommended): `python3.11.11 -m venv venv`
    4. Activate Venv

        mac: `source venv/bin/activate`
4. Install [requirements](/requirements.txt)

    mac: `pip install -r requirements.txt`
5. Check them:

    mac: `pip list`

## Config

Configs are in [TOML format](https://toml.io/en/). Here's the basic [config](nbody/config.toml) example.

Somehow parse data from [NASA's SPICE system](https://naif.jpl.nasa.gov/naif/spiceconcept.html)

## Obj Initialisation

- list of arguments
- dict of arguments

gen -> dict of args
then init iterates through the dicts, and creating an oblects from 

let's try to read system.toml, and see what happans
