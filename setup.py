import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
LICENSE = open(os.path.join(os.path.dirname(__file__), 'LICENSE.txt')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-sortable-listview',
    version='0.30',
    packages=['sortable_listview'],
    include_package_data=True,
    license=LICENSE,
    description='An extension of django\'s ListView that provides sorting',
    long_description=README,
    url='https://github.com/aptivate/django-sortable-listview',
    author='Sarah Bird',
    author_email='sarah@aptivate.org',
    install_requires=['django>=1.4'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    test_suite='tests.runtests.runtests',
    tests_require=['Django', 'mock']
)
