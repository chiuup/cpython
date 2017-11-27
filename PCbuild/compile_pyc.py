"""Compile and create an embeddable python36.zip
"""

import os
import zipfile
import argparse


def compile_pyc():
    """Compile and create an embeddable python36.zip
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='conf', default='Release')
    parser.add_argument('-p', dest='platf', default='Win32')
    args = parser.parse_args()
    if args.platf == 'x64':
        target = 'x64'
    else:
        target = 'x86'

    if not os.path.exists('./epython'):
        os.mkdir('epython')

    if args.conf == 'Debug':
        zfname = './epython/python36_%s_d.zip' % target
    else:
        zfname = './epython/python36_%s.zip' % target
    src = '../Lib'
    abs_src = os.path.abspath(src)
    excluded = ('__pycache__', 'ensurepip', 'idlelib', 'pydoc_data',
                'test', 'tests', 'tkinter', 'turtledemo', 'venv')

    with zipfile.ZipFile(zfname, "w", zipfile.ZIP_DEFLATED) as zfile:
        for root, dirs, files in os.walk(src):
            dirs[:] = [d for d in dirs if d not in excluded]
            for filename in files:
                if filename.endswith('.py') or filename.endswith('.exe'):
                    continue
                absname = os.path.abspath(os.path.join(root, filename))
                arcname = absname[len(abs_src) + 1:]
                zfile.write(absname, arcname)

if __name__ == '__main__':
    compile_pyc()
