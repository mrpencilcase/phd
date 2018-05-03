"""
Script that delets all files contained in the delete_file list in all subfolders
of the given directory
"""

import os

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


def clear_folder(root_path, delete_custom = []):
    delete_basic =  ["EIGENVAL","CHG", "CHGCAR","IBZJPT", "OSZICAR", "PCDAT",
                     "WAVECAR", "PROCAR", "XDATCAR","IBZKPT"]
    delete_count = 0

    size_start = get_size(root_path)

    if delete_custom == []:
        delete_list = delete_basic
    else:
        delete_list = delete_custom

    for subdir, dirs, files in os.walk(root_path):
        print(subdir)
        for file in files:
            if file in delete_list:
                os.remove(os.path.join(subdir,file))
                delete_count += 1

    size_end = get_size(root_path)
    print("\n")
    print("Number of deleted files: {}".format(delete_count))
    print("Freed disk space: {} mb".format((size_start-size_end)/1000000))

def main():
    path = "/home/lukas/Documents/work/dft/vasp_results/"
    clear_folder(path)

if __name__ =="__main__":
    main()
