from setuptools import setup, find_packages, Extension

setup_options = dict(
    name='marte',
    version='0.0.0',
    description='pymars',
    # long_description=long_description,
    author='Qin Xuye',
    author_email='qin@qinxuye.me',
    maintainer='Qin Xuye',
    maintainer_email='qin@qinxuye.me',
    license='Apache License 2.0',
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries',
    ],
    packages=find_packages(exclude=('*.tests.*', '*.tests')),
    include_package_data=True,
)
setup(**setup_options)

