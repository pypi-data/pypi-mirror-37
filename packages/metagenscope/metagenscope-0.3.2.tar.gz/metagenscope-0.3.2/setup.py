"""
MetaGenScope-CLI is used to upload data sets to the MetaGenScope web platform.
"""

from setuptools import find_packages, setup
from setuptools.command.install import install

from metagenscope_cli import __version__


dependencies = [
    'click',
    'requests',
    'configparser',
    'pandas',
    'datasuper==0.9.0',
]


dependency_links = [
    'git+https://github.com/dcdanko/DataSuper.git@develop#egg=datasuper-0.9.0',
]


def readme():
    """Print long description."""
    with open('README.md') as readme_file:
        return readme_file.read()


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
    name='metagenscope',
    version=__version__,
    url='https://github.com/bchrobot/python-metagenscope',
    license='MIT',
    author='Benjamin Chrobot',
    author_email='benjamin.chrobot@alum.mit.edu',
    description='MetaGenScope-CLI is used to upload data sets to the MetaGenScope web platform.',
    long_description=readme(),
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    dependency_links=dependency_links,
    entry_points={
        'console_scripts': [
            'metagenscope = metagenscope_cli.cli:main',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    cmdclass={
        'verify': VerifyVersionCommand,
    },
)
