"""Package minimal python into epython.zip
"""

import os
import zipfile

def main():
    """Pack everything
    """
    with zipfile.ZipFile('./epython/epython36.zip', 'w', zipfile.ZIP_DEFLATED) as zfile:
        pack_include(zfile)
        pack_by_arch_conf(zfile, 'x64', 'Release')
        pack_by_arch_conf(zfile, 'x64', 'Debug')
        pack_by_arch_conf(zfile, 'x86', 'Release')
        pack_by_arch_conf(zfile, 'x86', 'Debug')


def pack_include(zfile):
    """Pack includes
    """
    includes = '../Include'
    abs_includes = os.path.abspath(includes)
    for root, _, files in os.walk(includes):
        for filename in files:
            absname = os.path.abspath(os.path.join(root, filename))
            arcname = os.path.join('epython/include', absname[len(abs_includes)+1:])
            zfile.write(absname, arcname)
    zfile.write(os.path.join(os.path.abspath('../PC'), 'pyconfig.h'), 'epython/include/pyconfig.h')


def pack_by_arch_conf(zfile, arch, conf):
    """Package minimal python into epython.zip
    """
    if arch == 'x64':
        if os.path.exists('./amd64'):
            target = 'amd64'
        else:
            target = 'x86_amd64'
    else:
        target = 'Win32'
        arch = 'x86'

    if conf == 'Debug':
        debug = True
    else:
        debug = False
    prefix = 'epython/%s/%s/' % (arch, conf)
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

    for filename in filename_included:
        absname = os.path.abspath(os.path.join(libs, filename))
        arcname = os.path.join(os.path.join(prefix, 'libs'), absname[len(abs_libs)+1:])
        zfile.write(absname, arcname)

    if debug:
        rt_libs = 'python36_%s_d.zip' % arch
    else:
        rt_libs = 'python36_%s.zip' % arch

    zfile.write(os.path.abspath(os.path.join('./epython', rt_libs)),
                os.path.join(prefix, 'python36.zip'))

    dlls_included = ('_asyncio%s.pyd', '_bz2%s.pyd', '_ctypes%s.pyd', '_decimal%s.pyd',
                     '_elementtree%s.pyd', '_hashlib%s.pyd', '_lzma%s.pyd', '_msi%s.pyd',
                     '_multiprocessing%s.pyd', '_overlapped%s.pyd', '_socket%s.pyd',
                     '_sqlite3%s.pyd', '_ssl%s.pyd', 'pyexpat%s.pyd', 'select%s.pyd',
                     'unicodedata%s.pyd', 'winsound%s.pyd', 'sqlite3%s.dll')
    others_included = ('python%s.exe', 'python3%s.dll', 'python36%s.dll', 'pythonw%s.exe')
    dlls_included = [filename % ('_d' if debug else '') for filename in dlls_included]
    others_included = [filename % ('_d' if debug else '') for filename in others_included]


    for filename in dlls_included:
        absname = os.path.abspath(os.path.join(libs, filename))
        zfile.write(absname, os.path.join(os.path.join(prefix, 'DLLs'), filename))

    for filename in others_included:
        absname = os.path.abspath(os.path.join(libs, filename))
        zfile.write(absname, os.path.join(prefix, filename))


if __name__ == '__main__':
    main()
