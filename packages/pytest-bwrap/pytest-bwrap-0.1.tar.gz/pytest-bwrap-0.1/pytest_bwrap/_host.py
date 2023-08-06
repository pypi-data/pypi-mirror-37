import pathlib


def has_lib64():
    usr_lib64 = pathlib.Path('/usr/lib64')

    return usr_lib64.is_dir()


def has_merged_usr():
    bin = pathlib.Path('/bin')
    usr_bin = pathlib.Path('/usr/bin')

    return bin.resolve() == usr_bin
