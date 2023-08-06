import os

import sys


def flatten_fs_tree(the_tree, start_path=""):
    """ Return complete flatten dictionary representing files with it's "contents" or whatever is there
        Assumes that a directory is represented as a dictionary, and files are whatever else.
    """

    def _flatten_tree(obj, current_path):
        if isinstance(obj, dict):
            for element_name, element in obj.items():
                for item in _flatten_tree(element, os.path.join(current_path, element_name)):
                    yield item
        else:
            yield current_path, obj

    return dict(_flatten_tree(the_tree, start_path))


def is_byte_string(val):
    """Return True if `val` is a bytes-like object, False for a unicode
    string. Taken from pyfakefs. """
    if sys.version_info[0] > 2:
        return not hasattr(val, 'encode')
    return isinstance(val, str)


class RealFS(object):
    """ pyfakefs mock adapter. It's supposed to be used to perform real file system operations
    via fakefs interface. """

    @staticmethod
    def create_dir(path_):
        os.makedirs(path_, exist_ok=True)

    @classmethod
    def create_file(cls, file_path, contents=None, st_size=None, encoding=None):
        cls.create_dir(os.path.dirname(file_path))
        mode = ('wb' if encoding is not None or is_byte_string(contents) else 'w')

        if encoding is not None and contents is not None:
            contents = contents.encode(encoding)

        if st_size is not None:
            if contents is None:
                contents = "\x00" * st_size
            else:
                raise ValueError("Cannot use both contents and st_size argument at the same call.")

        cls._write_file(contents, file_path, mode)
        os.chmod(file_path, 0o666)

    @classmethod
    def _write_file(cls, contents, file_path, mode):
        with open(file_path, mode) as f:
            f.write(contents)
