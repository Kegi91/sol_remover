from sol_remover import read_n_remove, remove, remove_lims

# Read the input from input.dat
read_n_remove()

# Specify the input by yourself. Funny limits used to show the behaviour
remove(
    "../input/system_solv.gro",
    "../output/remove_example.gro",
    "SOL",
    3,
    "DPPC",
    1,
    3
)

remove_lims(
    "../input/system_solv.gro",
    "../output/lims_example.gro",
    3,
    7,
    "SOL",
    3
)
