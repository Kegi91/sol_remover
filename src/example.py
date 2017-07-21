from sol_remover import *

# Read the input from input.dat
read_n_remove()

# Specify the input by yourself. Funny limits used to show the behaviour
remove(
    "../input/system_solv.gro",
    "../output/remove_example.gro",
    "SOL",
    "OW",
    3,
    "POPC",
    "P",
    1,
    1
)

remove_lims(
    "../input/system_solv.gro",
    "../output/lims_example.gro",
    3,
    7,
    "SOL",
    "OW",
    3
)
