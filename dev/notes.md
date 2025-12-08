# NOTES

## Ideas on func import

Function format idea:
`isacting, f = G * m1 * m2 * (r1 - r2) / scal(r1 - r2)**3`

### Idea 0

Hardcode functions

### idea 1

in csv we have columns
__"force1 (to, from)"__, __"force2 (to, from)"__

and values like __11__, __01__
in fomat is force acting to the body, and is acting from the body

then we have forces written in code, and we must link __forceN__ with some `def force(): id = N`

### Idea 2

Write function as __string for parsing__ instead of `forceN` in CSV table column header

    ++ all force stuff in one place

    -- 2-files input

### Idea 3

Link `forceN` with something in `config.file`

Something – string value for parsing

    ++ Straight-forward linking by the string name `forceN`

    -- Parsing function:

        - pseudo lang
        - documentation
        - linking varaibles problems

## Synthesis

- Store functions in `config`
- Parse them to make code functions
- Link them to CSV columns data, have acting-map for all functions
- All functions in 2 processors

## Some Usage Connventions

    - Unit system: earth-mass, astro-unit, earth-years
    - knowledge about numerical methods

## Submodules

- math
- mydatatypes
- linear algebra
- cli
- parsing config
- generating data
- parsing data
- visualisation
- string parsing for functions
- numerical methods

ex of syntax highlighting
```python
def main():
    pass
```
## Particles storing thoughts

### Idea 1 
TOML:
```toml
["Bodies"]
"Sun" = {"Mass" = 332840, "R (polar)" = [0.0, 0.0, 0.0], "V (polar)" = [0.0, 0.0, 0.0], "Color" = "yellow", "force_1 (to, from)" = "1, 0", "force_2 (to, from)" = "0, 0", "force_3 (to, from)" = "0, 0", "force_4 (to, from)" = "0, 0"}
"Earth" = {"Mass" = 1, "R (polar)" = [1.496e+11, 0.0, 0.0], "V (polar)" = [0.0, 2.978e+4, 0.0], "Color" = "blue", "force_1 (to, from)" = "0, 1", "force_2 (to, from)" = "0, 0", "force_3 (to, from)" = "0, 0", "force_4 (to, from)" = "0, 0"}
```

or

CSV:
```csv
"Name: str", "Mass: float", "R (polar): list of float", "V (polar): list of float", "Color: hex", "force_1 (to, from)", "force_2 (to, from)", "force_3 (to, from)", "force_4 (to, from)"
Sun, 332840, 0.0 0.0 0.0, 0.0 0.0 0.0, yellow, 11, 00, 00, 00
```

## Progress bar

with tqdm loop evaluation took
67.28305245900992

without took
62.24328733400034

## Config

Does cofig even linked to simulator now?

## Visualisation

How to speed up the VIS??

**Drawing not all of the frames**

Make a natural factor like 

*1 of N frames is drawn*
