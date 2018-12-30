#!/usr/bin/env python3
# Into The Breach saves backuper/restorer
#
# MAYBE: do not save again the same save (calc files hashes)
# TODO: remove external dependency (on pick)
# TODO: add save name dialogue (save save's meta info like date)
# TODO: config file/env vars support (where to save saves & etc)
# TODO: do not override settings by default
import argparse
import datetime as dt
import os
import pathlib
import shutil
import sys

# external dependency
from pick import pick

# TODO: pass cmd args
homedir = os.environ['HOME']

game_save_dir = "Library/Application Support/IntoTheBreach"
game_save_dir = os.path.join(homedir, game_save_dir)

save_baks_dir = "Documents/GameSaves/IntoTheBreach"
save_baks_dir = os.path.join(homedir, save_baks_dir)

#/20181208_1

def copy_subdirs(srcdir, dstdir):
    src = os.listdir(srcdir)
    os.mkdir(dstdir)
    for f in src:
        src = os.path.join(srcdir, f)
        # dst = dstdir
        dst = os.path.join(dstdir, f)
        print("{} -> {}".format(src, dst))
        if os.path.isfile(src):
            # print("copy {} {}".format(src, dst))
            shutil.copy(src, dstdir)
        else:
            # print("copy -r {} {}".format(src, dst))
            shutil.copytree(src, dst)


def backup_cmd(args):
    dtime = dt.datetime.now()
    dtime_bak_subdir = dtime.strftime("%Y%m%d_%H%M")
    print("new backup:", dtime_bak_subdir)
    # return
    src = game_save_dir
    dst = os.path.join(save_baks_dir, dtime_bak_subdir)
    # print("{} -> {}".format(src, dst))
    # TODO: check is dst dir exists
    copy_subdirs(src, dst)

def _get_saves():
    return sorted([
        f for f in os.listdir(save_baks_dir)
        if os.path.isdir(os.path.join(save_baks_dir, f))
    ], key=str.lower, reverse=True)

def restore_cmd(args):
    saves = _get_saves()
    print("{}: {}".format(save_baks_dir, saves))
    option, index = pick(["<< quit >>"] + saves, "available-saves")
    if index == 0:
        return

    restore_dir = os.path.join(save_baks_dir, option)
    print("restore save from dir:", restore_dir)
    orig_bak_dir = game_save_dir + ".bak"

    # print(f"shutil.rmtree({orig_bak_dir})", )
    # print(f"shutil.move({game_save_dir}, {orig_bak_dir})")
    shutil.rmtree(orig_bak_dir, ignore_errors=True)
    shutil.move(game_save_dir, orig_bak_dir)
    try:
        # print(f"copy_subdirs({restore_dir}, {game_save_dir})")
        copy_subdirs(restore_dir, game_save_dir)
    except Exception as ex:
        print("failed to restore save dir")
        print(ex)
        print("try to restore removed original save")
        print(f"shutil.rmtree({game_save_dir})")
        print(f"shutil.move({orig_bak_dir}, {game_save_dir})")
        shutil.rmtree(game_save_dir, ignore_errors=True)
        shutil.move(orig_bak_dir, game_save_dir)

def list_cmd(args):
    saves = _get_saves()
    print(f"Saves in {game_save_dir}:")
    for s in saves:
        print(s)



def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    parser_backup = subparsers.add_parser(
        "save",
        help="Save current ITB progress")
    parser_backup.set_defaults(func=backup_cmd)
    parser_restore = subparsers.add_parser(
        "load",
        help="Restore ITB save")
    parser_restore.set_defaults(func=restore_cmd)
    parser_list = subparsers.add_parser(
        "show",
        help="Show ITB saves")
    parser_list.set_defaults(func=list_cmd)
    args = parser.parse_args()
    args.func(args)

main()

# https://docs.python.org/3/library/datetime.html
# https://docs.python.org/3/library/argparse.html
