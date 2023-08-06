from setuptools import setup
import io

setup(
    name='bw2calc',
    version="1.7.3",
    packages=["bw2calc"],
    author="Chris Mutel",
    author_email="cmutel@gmail.com",
    license=io.open('LICENSE.txt', encoding='utf-8').read(),
    url="https://bitbucket.org/cmutel/brightway2-calc",
    install_requires=[
        "eight",
        "numpy",
        "scipy",
        "stats_arrays",
    ],
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)
