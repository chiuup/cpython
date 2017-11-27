"""Package minimal python into epython.zip
"""

import os
import zipfile
import argparse


def package_epython():
    """Package minimal python into epython.zip
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='conf', default='Release')
    parser.add_argument('-p', dest='platf', default='Win32')
    args = parser.parse_args()

    if args.platf == 'x64':
        arch = 'x64'
        if os.path.exists('./amd64'):
            target = 'amd64'
        else:
            target = 'x86_amd64'
    else:
        target = 'Win32'
        arch = 'x86'

    if args.conf == 'Debug':
        debug = True
    else:
        debug = False
    # Packaging dev-lib
    if debug:
        zfname = 'epython36-dev_%s_d.zip' % arch
    else:
        zfname = 'epython36-dev_%s.zip' % arch

    includes = '../Include'
    abs_includes = os.path.abspath(includes)
    libs = './%s' % target
    abs_libs = os.path.abspath(libs)

    libs_included = ('_asyncio', '_bz2', '_ctypes', '_decimal', '_elementtree', '_hashlib',
                     '_lzma', '_msi', '_multiprocessing', '_overlapped', '_socket',
                     '_sqlite3', '_ssl', 'pyexpat', 'select', 'unicodedata',
                     'winsound', 'python', 'python3', 'python36', 'pythonw', 'sqlite3')

    filename_included = []

    for filename in libs_included:
        if debug:
            lib_name = '%s_d.lib'
            pdb_name = '%s_d.pdb'
        else:
            lib_name = '%s.lib'
            pdb_name = '%s.pdb'
        if filename != 'python' and filename != 'pythonw':
            filename_included.append(lib_name % filename)
        filename_included.append(pdb_name % filename)

    with zipfile.ZipFile(zfname, "w", zipfile.ZIP_DEFLATED) as zfile:
        for root, _, files in os.walk(includes):
            for filename in files:
                absname = os.path.abspath(os.path.join(root, filename))
                arcname = os.path.join('include', absname[len(abs_includes)+1:])
                zfile.write(absname, arcname)

        for filename in filename_included:
            absname = os.path.abspath(os.path.join(libs, filename))
            arcname = os.path.join('libs', absname[len(abs_libs)+1:])
            zfile.write(absname, arcname)

    # Packaging runtime
    if debug:
        zfname = 'epython36_%s_d.zip' % arch
    else:
        zfname = 'epython36_%s.zip' % arch

    runtimes_included = ('_asyncio%s.pyd', '_bz2%s.pyd', '_ctypes%s.pyd', '_decimal%s.pyd',
                         '_elementtree%s.pyd', '_hashlib%s.pyd', '_lzma%s.pyd', '_msi%s.pyd',
                         '_multiprocessing%s.pyd', '_overlapped%s.pyd', '_socket%s.pyd',
                         '_sqlite3%s.pyd', '_ssl%s.pyd', 'pyexpat%s.pyd', 'select%s.pyd',
                         'unicodedata%s.pyd', 'winsound%s.pyd', 'python%s.exe', 'python3%s.dll',
                         'python36%s.dll', 'pythonw%s.exe', 'sqlite3%s.dll')
    runtimes_included = [filename % ('_d' if debug else '') for filename in runtimes_included]

    if debug:
        rt_libs = 'python36_%s_d.zip' % arch
    else:
        rt_libs = 'python36_%s.zip' % arch

    with zipfile.ZipFile(zfname, "w", zipfile.ZIP_DEFLATED) as zfile:
        for filename in runtimes_included:
            absname = os.path.abspath(os.path.join(libs, filename))
            zfile.write(absname, filename)

        zfile.write(os.path.abspath(rt_libs), rt_libs)

if __name__ == '__main__':
    package_epython()
