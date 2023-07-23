from setuptools import setup

setup(
    name='pygame_layout',
    version='1.0.0',
    author='Arthur Le Floch',
    author_email='alf.github@gmail.com',
    description='Pygame Layout',
    long_description='Pygame Layout',
    url='https://github.com/ArthurLeFloch/PygameLayout',
    packages=[''],
    package_dir={'': 'src'},
    install_requires=[
        'pygame',
        'pygame-ui-controls',
        'lxml'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
