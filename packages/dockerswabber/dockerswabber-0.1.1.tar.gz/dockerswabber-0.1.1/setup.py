"""Small CLI to automate management of Docker hub image tags."""

import os
import sys

from setuptools import find_packages, setup
from setuptools.command.install import install

from docker_swabber import __version__


dependencies = ['click', 'semantic_version']


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version."""

    description = 'Verify that the git tag matches our version.'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != 'v{0}'.format(__version__):
            info = 'Git tag: {0} does not match the version of this app: {1}'
            info = info.format(tag, __version__)
            sys.exit(info)


setup(
    name='dockerswabber',
    version=__version__,
    url='https://github.com/LongTailBio/python-docker-swabber',
    license='BSD',
    author='Benjamin Chrobot',
    author_email='benjamin.blair.chrobot@gmail.com',
    description='Small CLI to automate management of Docker hub image tags.',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'swabber = docker_swabber.cli:main',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    cmdclass={
        'verify': VerifyVersionCommand,
    },
)
