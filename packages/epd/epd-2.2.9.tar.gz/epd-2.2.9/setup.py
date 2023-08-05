# -*- coding: utf-8 -*-
from distutils.core import setup, Extension

#import distutils.log
#distutils.log.set_verbosity(distutils.log.DEBUG) # Set DEBUG level

c_convert = Extension('c_convert',
                    sources = ['epdconvert/src/lz.c',
                               'epdconvert/src/epdconvert.c',
                               'epdconvert/src/Compression.c',
                               'epdconvert/src/Type0.c',
                               'epdconvert/src/Type2.c',
                               'epdconvert/src/Invert.c'],
                    include_dirs=['epdconvert/include/',],
                    language='c',
                    extra_compile_args = ["-std=c99"],
                  )



setup (name = 'epd',
       version = '2.2.9',
       author="Paweł Musiał, MpicoSys",
       url="https://www.mpicosys.com/",
       author_email='pawel.musial@mpicosys.com',
       description = 'EPD library for MpicoSys Timing Controllers (TC/TCM)',
       ext_modules = [c_convert,],
       packages = ['epd','epd.tcm','epd.convert'],
       requires = ['Pillow',]
       )