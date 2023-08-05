from setuptools import setup

setup(
    name='bdcli',
    packages=['bdcli'],
    version='0.4.2',
    description='Python based command-line interface for Brown Dog services',
    long_description='This command-line interface written using the Brown Dog Python Library helps you to convert '
                     'files between different formats and extract metadata from files. Details about using this client '
                     'can be found here: '
                     'https://opensource.ncsa.illinois.edu/bitbucket/projects/BD/repos/bdcli/browse/README.md. '
                     'For more information about Brown Dog and its services, please visit '
                     'https://browndog.ncsa.illinois.edu/',
    author='Kenton McHenry',
    author_email='mchenry@illinois.edu',
    url='https://browndog.ncsa.illinois.edu/',
    download_url='https://opensource.ncsa.illinois.edu/bitbucket/projects/BD/repos/bdcli',
    keywords=['Brown Dog, BD-CLI, BDCLI'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
    ],
    entry_points={
        'console_scripts': [
            'bd=bdcli:main',
        ]
    },
    install_requires=['browndog==0.5.0', 'python-docker-machine==0.2.2'],
    zip_safe=False,
    include_package_data=True
)
