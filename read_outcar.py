"""
skript to extract different values from an OUTCAR file
"""

def read_tot_en(path_open,pos):
    with open(path_open,"r") as file:
        outcar = list(file)
    tot_en = []

    if finished_check(path_open) == True:
        for line in outcar:
            if "free  energy   TOTEN" in line:
                line_split = [ent for ent in line.split()]
                if pos == "first":
                    tot_en.append(float(line_split[4]))
                    break
                elif pos == "last":
                    tot_en = []
                    tot_en.append(float(line_split[4]))
                elif pos == "all":
                    tot_en.append(float(line_split[4]))
    else:
        print("Calculation did not finish")
        print(path_open)
        for line in outcar:
            if "free energy    TOTEN" in line:
                line_split = [ent for ent in line.split()]
                if pos == "first":
                    tot_en.append(float(line_split[4]))
                    break
                elif pos == "last":
                    tot_en = []
                    tot_en.append(float(line_split[4]))
                elif pos == "all":
                    tot_en.append(float(line_split[4]))
        print(tot_en)
    return tot_en




def finished_check(path_open):

    finished = False

    with open(path_open,"r") as file:
        outcar = list(file)
    i = 0
    for line in reversed(outcar):
        if "General timing and accounting informations for this job:" in line:
            finished = True
            break
        if i > 20:
            break
        i += 1

    return finished
