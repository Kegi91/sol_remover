import numpy as np
import subprocess as subp

def read_n_split(f):
    return f.readline().split()

def skip_lines(f, i):
    for i in range(i):
        next(f)

def tail(f):
    return subp.getoutput('tail -1 ' + f) + "\n"

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
    f = open("input.dat", 'r')
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
    params.append(split[1])

    skip_lines(f,2)
    split = read_n_split(f)
    params.append(float(split[0]))
    params.append(float(split[1]))

    f.close()
    return params

def change_mol_number(output_file, removed_lines):
    f_in = open("temp_out","r")
    f_out = open(output_file, "w")

    # Handling the first two lines of the .gro file ------------------
    f_out.write(f_in.readline())
    f_out.write("%d\n"%(int(f_in.readline().split()[0])-removed_lines))
    #  ---------------------------------------------------------------

    for line in f_in:
        f_out.write(line)

    f_in.close()
    f_out.close()

    subp.run(["rm", "temp_out"])

def find_min_n_max(input_file, lipid_name):
    f_in = open(input_file, 'r')
    skip_lines(f_in,2)
    first_meet = True

    while True:
        try:
            resname, atom, z, line = read_gro_line(f_in)
        except ValueError:
            break

        if resname == lipid_name:
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

def find_center(input_file, res_name, atom_name):
    f = open(input_file, 'r')
    skip_lines(f,2)

    z_sum = 0
    z_numb = 0

    while True:
        try:
            res, atom, z, line = read_gro_line(f)
        except ValueError:
            break

        if res == res_name and atom == atom_name:
            z_sum += z
            z_numb += 1

    f.close()
    return z_sum/z_numb

def leaflets(input_file, lipid_name, lim_atom):
    f = open(input_file, "r")
    skip_lines(f,2)

    upper_zsum = 0
    upper_num = 0
    lower_zsum = 0
    lower_num = 0

    center = find_center(input_file, lipid_name, lim_atom)

    while True:
        try:
            res, atom, z, line = read_gro_line(f)
        except ValueError:
            break

        if res == lipid_name and atom == lim_atom:
            if z > center:
                upper_zsum += z
                upper_num += 1
            else:
                lower_zsum += z
                lower_num += 1

    f.close()
    return lower_zsum/lower_num, upper_zsum/upper_num

def remove_lims(input_file, output_file, zmin, zmax, res_name, res_size):
    f = open(input_file, "r")
    out = open("temp_out", "w")

    out.write(f.readline())
    out.write(f.readline())

    removed_lines = 0

    while True:
        try:
            resname, atom, z, line = read_gro_line(f)
        except ValueError:
            break

        if resname == res_name:
            if z < zmax and z > zmin and atom == "OW":
                skip_lines(f,res_size-1)
                removed_lines += res_size
                continue

        out.write(line)

    out.write(tail(input_file))

    f.close()
    out.close()

    change_mol_number(output_file, removed_lines)

    print(
    "Removed: %d molecules = %d atoms"%(removed_lines/res_size, removed_lines)
    )

def remove(
    input_file, output_file, res_name, res_size, lipid_name, lim_atom,
    adjust_low, adjust_high
):

    lower, upper = leaflets(input_file, lipid_name, lim_atom)
    lower += adjust_low
    upper -= adjust_high

    remove_lims(input_file, output_file, lower, upper, res_name, res_size)

def read_n_remove():
    remove(*read_params())
