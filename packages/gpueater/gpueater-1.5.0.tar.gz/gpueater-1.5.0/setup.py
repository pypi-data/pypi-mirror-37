from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))

version = '1.5.0'

install_requires = [
    'requests'
]


setup(name='gpueater',
    version=version,
    description="GPUEater API console for python.",
    long_description="See https://github.com/aieater/gpueater_python",
    classifiers=(
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ),
    keywords='gpu gpueater deeplearning eater cloud',
    author='Pegara, Inc.',
    author_email='info@pegara.com',
    url='https://github.com/aieater/gpueater_python',
    license='MIT',
    packages=['gpueater'],
    zip_safe=False,
    install_requires=install_requires,
    entry_points={}
)
