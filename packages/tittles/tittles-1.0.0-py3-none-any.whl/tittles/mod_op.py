""" tittles.mod_op 171217_1800
"""
import os

import mod
_t = mod.Mod("tittles")  # pylint: disable-msg=C0103

def mods_rld():
    """Reload modules"""
    _t.reload()


def wr_module(name, content):
    """Write module"""
    path_ = install_dir and os.path.join(install_dir, name) or name
    try:
        f_ = open(path_, 'wb')
        f_.write(content.encode())
        f_.close()
    except Exception as e_:
        raise t.ModuleRefreshError("Can't write to module '%s': %s" % (path_, e_))


def rm_module(name):
    """Remove module"""
    if os.path.isdir(name):
        raise _t.m.msg_exc("Unable to remove module '%s': is a directory" % (name, ), IsADirectoryError)
    try:
        os.remove(name)
    except:
        raise _t.m.msg_exc("Unable to remove module '%s'" % (name, ))


def __test():
    fname_ = "xxx001"
    rm_module(fname_)


if __name__ == "__main__":
    __test()
