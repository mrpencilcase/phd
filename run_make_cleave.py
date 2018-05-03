from  make_cleave_fkt import make_cleave_calc

path_dir = "/home/lukas/Documents/dft/upload/CrN_TiN/cleave/001/af/"
cleave_planes = [4, 5, 6, 7, 8]
cleave_dist = cleave_dist = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.8, 1,
                             1.5, 2, 2.5, 3, 4, 5, 7, 10]
cleave_direction = "c"
print(path_dir)
make_cleave_calc(path_dir, cleave_planes, cleave_dist, cleave_direction)