"""
skript to extract different values from an OUTCAR file
"""

def read_tot_en(path_open,pos):
    with open(path_open,"r") as file:
        outcar = list(file)
    tot_en = []
    for line in outcar:
        if "free  energy   TOTEN" in line:
            line_split = [ent for ent in line.split()]
            if pos == "first":
                tot_en = float(line_split[4])
                break
            elif pos == "last":
                tot_en = float(line_split[4])
            elif pos == "all":
                tot_en.append(float(line_split[4]))
    return tot_en
