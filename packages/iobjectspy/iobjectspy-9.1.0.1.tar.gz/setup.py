from setuptools import setup

import sys
import platform

plat_bit = platform.architecture()[0]

major = sys.version_info.major
minor = sys.version_info.minor
micro = sys.version_info.micro

package_dir = {}

if major == 3 and minor == 5:
    if micro > 2:
        if plat_bit == '32bit':
            package_dir = {'iobjectspy': 'iobjectspy/iobjectspy-py35_32/iobjectspy'}
        else:
            package_dir = {'iobjectspy': 'iobjectspy/iobjectspy-py35_64/iobjectspy'}
    else:
        if plat_bit == '32bit':
            package_dir = {'iobjectspy': 'iobjectspy/iobjectspy-py352_32/iobjectspy'}
        else:
            package_dir = {'iobjectspy': 'iobjectspy/iobjectspy-py352_64/iobjectspy'}
elif major == 3 and minor == 6:
    if micro < 6:
        if plat_bit == '32bit':
            package_dir = {'iobjectspy': 'iobjectspy/iobjectspy-py36_32/iobjectspy'}
        else:
            package_dir = {'iobjectspy': 'iobjectspy/iobjectspy-py36_64/iobjectspy'}
    else:
        if plat_bit == '32bit':
            package_dir = {'iobjectspy': 'iobjectspy/iobjectspy-py366_32/iobjectspy'}
        else:
            package_dir = {'iobjectspy': 'iobjectspy/iobjectspy-py366_64/iobjectspy'}
elif major == 3 and minor == 7:
    if plat_bit == '32bit':
        package_dir = {'iobjectspy': 'iobjectspy/iobjectspy-py37_32/iobjectspy'}
    else:
        package_dir = {'iobjectspy': 'iobjectspy/iobjectspy-py37_64/iobjectspy'}
else:
    raise RuntimeError('Unsupported python version : %d.%d ' % (major, minor))

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='iobjectspy',
    version='9.1.0.1',
    packages=['iobjectspy'],
    url='http://iobjectspy.supermap.io',
    license='SuperMap',
    description='SuperMap iObjects Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'py4j>=0.10.7'
    ],
    package_data={'iobjectspy': ['*.*', 'ai/*', '_jsuperpy/*', '_jsuperpy/jars/*.jar', '_jsuperpy/data/*']},
    package_dir=package_dir,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
    ]
)
