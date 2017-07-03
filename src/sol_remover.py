import numpy as np
import os

def read_n_split(f):
    return f.readline().split()

def skip_lines(f, i):
    for i in range(i):
        next(f)

def read_params():
    f = open("../input/input.dat", 'r')
    params = []

    skip_lines(f,1)
    split = read_n_split(f)
    params.append(split[0])
    params.append(split[1])

    skip_lines(f,2)
    split = read_n_split(f)
    params.append(split[0])
    params.append(int(split[1]))

    skip_lines(f,2)
    split = read_n_split(f)
    params.append(split[0])

    skip_lines(f,2)
    split = read_n_split(f)
    params.append(float(split[0]))
    params.append(float(split[1]))

    f.close()
    return params

def change_mol_number(output_file, removed_lines):

    f_in = open("../output/temp_out","r")
    f_out = open(output_file, "w")

    for line in f_in:
        split = line.split()

        if len(split) == 1:
            f_out.write(str(int(split[0])-removed_lines)+"\n")
            continue
        else:
            f_out.write(line)

    f_in.close()
    f_out.close()

    os.system("rm ../output/temp_out")

def find_min_n_max(input_file, lipid_name):

    f_in = open(input_file, 'r')
    first_meet = True

    for line in f_in:
        split = line.split()
        items = len(split)

        if items not in [5,6]:
            continue

        resname = split[0]
        z = float(split[-1])

        if resname.find(lipid_name) != -1:
            if first_meet:
                minim = z
                maxim = z
                first_meet = False
            else:
                if z < minim:
                    minim = z
                elif z > maxim:
                    maxim = z

    return minim, maxim

def remove_lims(input_file, output_file, zmin, zmax, res_name, res_size):

    f = open(input_file, "r")
    out = open("../output/temp_out", "w")

    line = f.readline()
    split = line.split()
    removed_lines = 0

    while line != "":
        items = len(split)

        if items not in [5,6]:
            out.write(line)
            line = f.readline()
            split = line.split()
            continue

        resname = split[0]
        atom = split[1]
        z = float(split[-1])

        if resname.find(res_name) != -1:
            if z < zmax and z > zmin and atom.find("OW") != -1:
                skip_lines(f,res_size-1)
                line = f.readline()
                split = line.split()
                removed_lines += res_size
                continue

        out.write(line)
        line = f.readline()
        split = line.split()

    f.close()
    out.close()

    change_mol_number(output_file, removed_lines)

    print("Removed: %d molecules = %d atoms"%(removed_lines/res_size, removed_lines))

def remove(
    input_file, output_file, res_name, res_size, lipid_name,
    adjust_low, adjust_high
):

    minim, maxim = find_min_n_max(input_file, lipid_name)
    minim += adjust_low
    maxim -= adjust_high

    remove_lims(input_file, output_file, minim, maxim, "SOL", 3)

def read_n_remove():
    p = read_params()
    remove(p[0],p[1],p[2],p[3],p[4],p[5],p[6])
