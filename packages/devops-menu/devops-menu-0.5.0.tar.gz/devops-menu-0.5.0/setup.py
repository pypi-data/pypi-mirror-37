import sys
import os
from setuptools import setup, find_packages

SRC_DIR = 'src'



PREFIX = '/usr/share/devops-menu'


with open('requirements.txt') as f:
    required = f.read().splitlines()

def readme():
    with open('README.rst') as f:
        return f.read()


def get_version():
    sys.path[:0] = [SRC_DIR]
    return __import__('devops_menu').__version__

if "VIRTUAL_ENV" in os.environ:
        # could be a virtual environment
        virtual = os.environ['VIRTUAL_ENV']




if ('virtual' in vars() or 'virtual' in globals()) and len(virtual)>0:

    PREFIX = str(virtual)+str(PREFIX)

    if not os.path.exists(str(virtual)+'/usr/share/'):
            os.makedirs(str(virtual)+'/usr/share/')

    if os.path.exists('/usr/share/devops-menu'):
        for root, dirs, files in os.walk(str(virtual)+'/usr/share/devops-menu', topdown=False):
                for name in files:
                        os.remove(os.path.join(root, name))
                for name in dirs:
                        os.rmdir(os.path.join(root, name))

else:

    if os.path.exists('/usr/share/devops-menu'):
        for root, dirs, files in os.walk('/usr/share/devops-menu', topdown=False):
                for name in files:
                        os.remove(os.path.join(root, name))
                for name in dirs:
                        os.rmdir(os.path.join(root, name))


setup(
    name='devops-menu',
    version='0.5.0',
    author='Will Rubel',
    maintainer='Will Rubel',
    maintainer_email='willrubel@gmail.com',
    description='Menu system for Managing AWS Accounts',
    long_description=readme(),
    author_email='willrubel@gmail.com',
    license='Apache 2.0 License',
    keywords='AWS CLI AWSCLI Boto Boto3',
    install_requires=required,
    tests_require=[
        'mock == 1.0.1',  # lock version for older version of setuptools
    ] + (['unittest2'] if sys.version_info < (2, 7) else []),
    package_dir={'': SRC_DIR},
    packages=find_packages(SRC_DIR),
    include_package_data=True,
    test_suite='tests',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Systems Administration'
    ],
    entry_points="""
    [console_scripts]
    devops-menu = devops_menu.devops_menu:main
    """,
    data_files =    [
            (PREFIX, ['datafiles/devops-menu.yml']),
            (PREFIX+'/scripts', ['datafiles/scripts/test.py'])

    ]
)
