from setuptools import setup, Extension

extensions = [Extension("libvpp",
                        ["vpp/vpp.c"],
                        include_dirs=['vpv'],
                        depends=["vpp/vpp.h"])]


# from https://stackoverflow.com/a/38525461
from distutils.command.install_lib import install_lib as _install_lib
import os
import re
def batch_rename(src, dst, src_dir_fd=None, dst_dir_fd=None):
    '''Same as os.rename, but returns the renaming result.'''
    os.rename(src, dst,
              src_dir_fd=src_dir_fd,
              dst_dir_fd=dst_dir_fd)
    return dst

class _CommandInstall(_install_lib):
    def __init__(self, *args, **kwargs):
        _install_lib.__init__(self, *args, **kwargs)

    def install(self):
        # let the distutils' install_lib do the hard work
        outfiles = _install_lib.install(self)
        # batch rename the outfiles:
        # for each file, match string between
        # second last and last dot and trim it
        matcher = re.compile('\.([^.]+)\.so$')
        return [batch_rename(file, re.sub(matcher, '.so', file))
                for file in outfiles]


setup(name="vpp",
      version='2.3.2-5',
      author="Jérémy Anger",
      author_email="angerj.dev@gmain.com",
      description="Python wrapper to vpp",
      url='https://github.com/kidanger/vpp',
      classifiers=[
          "Operating System :: OS Independent",
      ],
      py_modules=['vpp'],
      ext_modules=extensions,
      cmdclass={
          'install_lib': _CommandInstall,
      },
      )

