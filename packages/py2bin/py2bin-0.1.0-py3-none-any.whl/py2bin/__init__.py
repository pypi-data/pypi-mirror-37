"""py2bin - Python script file transform into binary file.
Usage:
 py2bin [options] pyc <file>
 py2bin [options] pyd <file> [<flags>...]

Commands:
 pyc                Transform to pyc
 pyd                Transform to pyd

Options:
 -f                 Overwrite old file.

Arguments:
 <file>             Source file or directory.
 <flags>        The flags for gcc compiler.

Examples:
 py2bin pyc a.py
 py2bin pyd a.py -I../include -L../libs -llibrary
"""

import os
import sys
import py_compile
import subprocess

from docopt import docopt


class PyToBin(object):
    def __init__(self, src, cflags, is_pyd, is_overwrite):
        self._base_prefix = sys.base_prefix
        self._include_path = os.path.join(self._base_prefix, 'include')
        self._libs_path = os.path.join(self._base_prefix, 'libs')
        self._lib_name = 'python{}{}'.format(sys.version_info[0], sys.version_info[1])

        self._src = src
        self._cflags = cflags
        self._is_pyd = is_pyd
        self._is_overwrite = is_overwrite
        self._compile()

    def _compile(self):
        if os.path.isfile(self._src):
            if self._is_pyd:
                self.__pyd_compile(self._src, self._cflags)
            else:
                self.__pyc_compile(self._src)

        elif os.path.isdir(self._src):
            for root, dirs, files in os.walk(self._src):
                for file in files:
                    file = os.path.join(root, file)
                    if self._is_pyd:
                        self.__pyd_compile(file, self._cflags)
                    else:
                        self.__pyc_compile(file)
        else:
            raise FileNotFoundError('[-]{}'.format(self._src))

    def __pyc_compile(self, src_path):
        if src_path.endswith('.py'):
            out = "{}c".format(src_path)
            if os.path.isfile(out) and not self._is_overwrite:
                print('[*]File exists, skip: {}'.format(out))
            else:
                py_compile.compile(src_path, out)

    def __pyd_compile(self, src, flags):
        src_name = os.path.splitext(src)[0]

        if not (src.endswith('.py') or src.endswith('.pyx')):
            return

        # *.pyx
        if src.endswith('.py') and os.path.isfile('{}.pyx'.format(src_name)):
            return

        # cython
        src_c = '{}.c'.format(src_name)
        if os.path.isfile(src_c) and not self._is_overwrite:
            print('[*]File exists, skip: {}'.format(src_c))
        else:
            cmd = 'cython "{}" -o "{}"'.format(src, src_c)
            print('[*]Run: {}'.format(cmd))
            if subprocess.call(cmd):
                raise Exception('[-]Cython error.')

        # gcc
        out = '{}.pyd'.format(src_name)
        if os.path.isfile(out) and not self._is_overwrite:
            print('[*]File exists, skip: {}'.format(out))
        else:
            cmd = 'gcc "{}" -o "{}"'.format(src_c, out)
            cmd = '{} -I"{}" -L"{}" -l{}'.format(cmd, self._include_path, self._libs_path, self._lib_name)
            if flags:
                cmd = '{} {}'.format(cmd, ' '.join(flags))
            cmd = '{} -s -shared'.format(cmd)

            print('[*]Run: {}'.format(cmd))

            if subprocess.call(cmd):
                raise Exception('[-]gcc error.')


def main():
    args = docopt(__doc__, options_first=True)

    # print(args)
    src = args['<file>']
    cflags = args['<flags>']

    PyToBin(src, cflags, args['pyd'], args['-f'])


if __name__ == '__main__':
    main()
