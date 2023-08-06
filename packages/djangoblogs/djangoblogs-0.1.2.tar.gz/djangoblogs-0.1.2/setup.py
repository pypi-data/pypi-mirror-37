from setuptools import setup, find_packages
from blogs import __version__

def readfile(filename):
    return open(filename, 'r').read()

print(__version__)
long_description = readfile('README.md')

setup(
    version=__version__,
    name='djangoblogs',
    description='Django blogging with medium style editor',
    long_description=long_description,
    url='https://github.com/arjunsinghy96/django-blogs',
    author='Arjun Singh Yadav',
    author_email='arjunsinghy96@gmail.com',
    license='MIT',
    keywords='django blogs medium blog',
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        ],
    packages=find_packages(exclude=['blogs.tests', 'config']),
    install_requires=[
        'django>=2.0'
    ]
    )
