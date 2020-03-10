#! /usr/bin/python3

import sys
import subprocess
import os
from os import path

main = sys.argv[1]
oldmain = sys.argv[2]
sha = sys.argv[3]

hlgit_path = path.realpath(sys.argv[0])
ld_cfg = path.join(path.dirname(hlgit_path), "ld.cfg")
folder = subprocess.check_output([ "git", "rev-parse", "--show-toplevel"]).decode("utf-8")[:-1] # strip \n from output
dirpath = os.getcwd()
relative = path.relpath(dirpath, folder)
folder_tmp = folder + "_tmp"
old_dirpath = folder_tmp + "/" + relative
oldmain_fullpath = old_dirpath + "/" + oldmain

print ("hlgit path: ", hlgit_path)
print ("ld.cfg path: ", ld_cfg)
print ("git root folder: ", folder)
print ("directory path: " + dirpath)
print ("relative path: " + relative)
print ("temporary git folder: ", folder_tmp)
print ("old directory path (tmp): " + old_dirpath)
print ("oldmain fullpath: " + oldmain_fullpath)

expanded_name = "expanded.tex"
expanded_tmp_name = "expanded_tmp.tex"
diff_name = "diff.tex"

expanded_tmp_fullname = path.join(folder_tmp, expanded_tmp_name)

latexpand_main = [ "latexpand", main ]
latexpand_oldmain = [ "latexpand", oldmain ]
latexdiffcmd = [ "latexdiff", expanded_tmp_fullname, expanded_name, '-c', ld_cfg ]

cpcmd = ["cp", "-R", folder, folder_tmp]
print ("\n\nCALLING: ", cpcmd)
subprocess.call(cpcmd)

expanded = open(expanded_name, "w")
expanded_tmp = open(expanded_tmp_fullname, "w")
diff = open(diff_name, "w")
latexmk_cmd = ["latexmk", "-pdf", diff_name]

print ("\n\nCALLING: ", latexpand_main)
subprocess.call(latexpand_main, stdout=expanded)
print ("\nCD TO ", old_dirpath)
os.chdir(old_dirpath)

subprocess.call(["git","reset","--hard", sha])
print ("\n\nCALLING: ", latexpand_oldmain)
subprocess.call(latexpand_oldmain, stdout=expanded_tmp)

print ("\nCD TO ", dirpath)

os.chdir(dirpath)


print ("\n\nCALLING: ", latexdiffcmd)
subprocess.call(latexdiffcmd, stdout=diff)

print ("\n\nCALLING: ", latexmk_cmd)
subprocess.call(latexmk_cmd)
