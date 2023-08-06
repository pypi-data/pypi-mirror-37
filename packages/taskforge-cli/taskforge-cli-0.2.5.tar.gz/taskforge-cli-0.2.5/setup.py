"""A task management tool that integrates with 3rd party services."""

from setuptools import find_packages, setup

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='taskforge-cli',
    version='0.2.5',
    url='https://github.com/chasinglogic/taskforge',
    license='AGPL-3.0',
    author='Mathew Robinson',
    author_email='chasinglogic@gmail.com',
    description='A task management library and tool that integrates'
    ' with 3rd party services',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['docopt', 'toml'],
    extras_require={'mongo': ['pymongo==3.7.1']},
    entry_points={
        'console_scripts': [
            'task = task_forge.cli:main',
        ],
        'task_forge.lists': [
            'mongodb = task_forge.lists.mongo',
            'sqlite = task_forge.lists.sqlite',
        ],
    },
    classifiers=[
        # As from https://pypi.org/classifiers/
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ])
