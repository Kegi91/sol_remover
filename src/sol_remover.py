import numpy as np
import os

def read_n_split(f):
    return f.readline().split()

def skip_lines(f, i):
    for i in range(i):
        next(f)

def read_gro_line(f_in):
    l = f_in.readline()
    if l == '' or len(l)<45:
        return ''

    # res_num = int(l[0:5])
    # a_number = int(l[15:20])
    # x = float(l[20:28])
    # y = float(l[28:36])

    res_name = l[5:10].strip()
    a_name = l[10:15].strip()
    z = float(l[36:44])

    return res_name, a_name, z, l

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
    f_in = open("temp_out","r")
    f_out = open(output_file, "w")

    for line in f_in:
        split = line.split()

        if len(split) == 1: # TODO
            f_out.write(str(int(split[0])-removed_lines)+"\n")
            continue
        else:
            f_out.write(line)

    f_in.close()
    f_out.close()

    os.system("rm temp_out")

def find_min_n_max(input_file, lipid_name):
    f_in = open(input_file, 'r')
    skip_lines(f_in,2)
    first_meet = True

    while True:
        try:
            resname, atom, z, line = read_gro_line(f_in)
        except ValueError:
            break

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
    out = open("temp_out", "w")
    skip_lines(f,2)

    removed_lines = 0

    while True:
        try:
            resname, atom, z, line = read_gro_line(f)
        except ValueError:
            break

        if resname.find(res_name) != -1:
            if z < zmax and z > zmin and atom.find("OW") != -1:
                skip_lines(f,res_size-1)
                removed_lines += res_size
                continue

        out.write(line)

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
