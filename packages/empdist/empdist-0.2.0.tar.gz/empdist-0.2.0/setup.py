import setuptools

VER = '0.2.0'
AUTHOR = 'Dylan Skola'

print('*' * 80)
print('* {:<76} *'.format('Empirical Distribution {} by {}'.format(VER, AUTHOR)))
print('*' * 80)
print()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='empdist',
                 version=VER,
                 description='Python class and helper functions for modeling and manipulating empirical distributions ',
                 long_description=long_description,
                 url='https://github.com/phageghost/empirical-distribution',
                 author=AUTHOR,
                 author_email='empdist@phageghost.net',
                 license='MIT',
                 packages=['empdist'],
                 install_requires=['numpy', 'scipy>=0.19'],
                 zip_safe=False,
                 classifiers=(
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                 ),
                 )
