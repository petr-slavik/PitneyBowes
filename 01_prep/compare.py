###############################################################################
# This script will compate files in 00_new and 01_old folders and will create #
# 03_comp folder containing diff files + new files from 00_new folder. Then   #
# it will create 04_flat folder containing flat stricture which will be used  #
# for TMS. The script will create also kopiruj.bat batch file and will upload #
# it to Trados project folder 15_TS2017 where it will help to reconstruct     #
# folder structure during Exporting files. ExportFiles.cmd file will generate #
# files for all languages to "_GeneratedFilesFlat" folder, will reconstruct   #
# folder structure using kopiruj.bat script and upload these files to         #
# \50_toClient\Generated Files\%lang% folder - ready for delivery             #
###############################################################################

from filecmp import dircmp
from shutil import copy, copytree
import os

def print_diff_files(dcmp):
     for name in dcmp.diff_files:
         print("diff_file %s found in %s and %s" % (name, dcmp.left,dcmp.right))
         src = os.path.join(dcmp.left,name)
         dst_comp = os.path.dirname(os.path.join("03_comp", src[8:]))
         dst_flat = "04_flat"
         if not os.path.exists(dst_comp):
             os.makedirs(dst_comp)
         copy(src, dst_comp)
         copy(src, dst_flat)
     for sub_dcmp in dcmp.subdirs.values():
         print_diff_files(sub_dcmp)


def print_left_side_only(dcmp):
     for name in dcmp.left_only:
         print("NEW_file %s found in %s" % (name, dcmp.left))
         src = os.path.join(dcmp.left,name)
         dst_comp = os.path.dirname(os.path.join("03_comp\\" + src[8:]))
         dst_flat = "04_flat"
         if not os.path.exists(dst_comp):
             os.makedirs(dst_comp)
         copy(src, dst_comp)
         copy(src, dst_flat)
     for sub_dcmp in dcmp.subdirs.values():
         print_left_side_only(sub_dcmp)


def copy_diff_structure_to_temp():
    copytree("03_comp", "..\\15_TS2017\\temp")
    os.chdir("..\\15_TS2017")
    print("Created temp folder structure in 15_TS2017")
    for root, directory, files in os.walk("temp"):
        for f in files:
            os.remove(os.path.join(root,f))

def create_kopiruj_bat_file():
    print("Creating of kopiruj.bat file and moving it to 15_TS2017")
    with open("kopiruj.bat", "x") as batak:
        for root, directory, files in os.walk("03_comp"):
            for f in files:
                if len(root[8:]) == 0:
                    print(f"copy {f} temp")
                    batak.write(f"copy {f} temp\n")
                else:
                    print(rf"copy {f} temp\{root[8:]}")
                    batak.write(f"copy {f} temp\\{root[8:]}\n")
    os.rename("kopiruj.bat", "..\\15_TS2017\\kopiruj.bat")




os.mkdir("04_flat")
dcmp = dircmp('00_new', '01_old')

print("LIST OF DIFF FILES")
print_diff_files(dcmp)
print("\n\nLIST OF NEW FILES")
print_left_side_only(dcmp)
print("\n\n")
create_kopiruj_bat_file()
print("\n\n")
copy_diff_structure_to_temp()
