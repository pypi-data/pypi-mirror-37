import os
import six
from CheKnife.errors import ParameterError


def mktree(abs_path):
    if not abs_path:
        raise ParameterError("No valid path suplied to mktree: {}".format(abs_path))
    if not os.path.isdir(abs_path):
        try:
            if six.PY3:
                os.makedirs(abs_path, exist_ok=True)
            elif six.PY2:
                os.makedirs(abs_path)

        except IOError:
            raise PermissionError('Error creating directory: {} Check user permissions'.format(abs_path))
    return True


def split_path(file_path):
    path, filename = os.path.split(file_path)
    filename, file_extension = os.path.splitext(filename)
    return {'path': path, 'filename': filename, 'extension': file_extension, 'type': file_extension.replace('.', '')}


def mv(from_path, to_path):
    os.rename(from_path, to_path)
