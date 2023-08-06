from setuptools import setup, find_packages
import lifelib

lifelib.reset_tree()

setup(
    name='python-lifelib',
    version=lifelib.__version__,
    description='Algorithms for manipulating and simulating patterns in cellular automata',
    author='Adam P. Goucher',
    author_email='goucher@dpmms.cam.ac.uk',
    url='https://gitlab.com/apgoucher/lifelib',
    license='MIT',
    packages=['lifelib'],
    test_suite='lifelib.tests',
    include_package_data=True,
    zip_safe=False,
    install_requires=['numpy'],
    extras_require={'notebook': ['jupyter']},
    classifiers = [
        'Development Status :: 4 - Beta',

        # MIT licence as always:
        'License :: OSI Approved :: MIT License',

        # Since we require gcc or clang to compile:
        'Operating System :: POSIX',
        'Programming Language :: C++',

        # Lifelib is compatible with Python 2 and 3, and has been tested on:
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ])
