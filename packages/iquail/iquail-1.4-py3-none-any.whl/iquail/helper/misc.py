import atexit
import os
import shutil
import sys
import copy
import ctypes
import platform
import tempfile

OS_LINUX = platform.system() == 'Linux'
OS_WINDOWS = platform.system() == 'Windows'


def cache_result(func):
    """ Decorator to save the return value of a function
    Function will be only run once.
    WARNING:
    - The cached return value will be copied with copy.copy
    - Only shallow copy, not deep copy
    - Use this if you know what you are doing!
    """
    cache_attr = "___cache_result"

    def wrapper(self, *args, **kwargs):
        if not hasattr(self, cache_attr):
            setattr(self, cache_attr, {})
        cache = getattr(self, cache_attr)
        if func.__name__ not in cache:
            cache[func.__name__] = func(self, *args, **kwargs)
        return copy.copy(cache[func.__name__])

    return wrapper


def get_module_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def get_script():
    return os.path.realpath(sys.argv[0])


def get_script_name():
    return os.path.basename(get_script())


def get_script_path():
    return os.path.dirname(get_script())


def running_from_script():
    """check if being run from script
    and not builded in standalone binary"""
    if getattr(sys, 'frozen', False):
        return False
    return True


def _delete_atexit(path_to_delete):
    """On windows we can't remove binaries being run.
    This function will remove a file or folder at exit
    to be able to delete itself
    """
    assert os.path.isdir(path_to_delete)

    def _delete_from_tmp():
        tmpdir = tempfile.mkdtemp()
        newscript = shutil.copy2(get_script(), tmpdir)
        args = (newscript, "--quail_rm", path_to_delete)
        if running_from_script():
            os.execl(sys.executable, sys.executable, *args)
        else:
            os.execl(newscript, *args)

    atexit.register(_delete_from_tmp)


def self_remove_directory(directory):
    """Remove directory but if we are running from a compiled binary
    it will remove the directory only when exiting.
    This function was made for windows, because we can't remove ourself on windows
    """
    if running_from_script():
        shutil.rmtree(directory)
    else:
        _delete_atexit(directory)


def rerun_as_admin():
    if OS_LINUX:
        # os.system('pkexec %s %s' % (get_script_path(),
        # ' '.join(sys.argv[1:])))
        raise NotImplementedError
    elif OS_WINDOWS:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            ctypes.windll.shell32.ShellExecuteW(None,
                                                'runas',
                                                sys.executable,
                                                ' '.join(sys.argv),
                                                None, 1)
    exit(0)


def move_folder_content(src, dest, ignore_errors=False):
    """Move folder content to another folder"""
    for f in os.listdir(src):
        # print("moved %s >> %s" % (os.path.join(src, f), dest))
        try:
            shutil.move(os.path.join(src, f), dest)
        except:
            if not ignore_errors:
                raise


def safe_remove_folder_content(src):
    """Remove folder content
    If an error happens while removing
    the content will be untouched
    """
    tmp_dir = tempfile.mkdtemp()
    try:
        move_folder_content(src, tmp_dir)
    except Exception:
        # rollback move on exception
        move_folder_content(tmp_dir, src, ignore_errors=True)
        raise
    finally:
        # TODO chmod -R +w ?
        shutil.rmtree(tmp_dir)
