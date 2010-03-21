import os

from setuptools import find_packages, setup


setup(
    # Package information:
    name='ao.shorturl',
    version='1.1.6',
    license='GNU GPL',
    url='http://github.com/aatiis/ao.shorturl',
    description='Reusable url shortener and lookup library.',
    long_description=\
        open('README.txt').read() + \
        open(os.path.join('src', 'ao', 'shorturl', 'shorturl.txt')).read() + \
        open(os.path.join('src', 'ao', 'shorturl', 'django.txt')).read() + \
        open('TODO.txt').read() + \
        open('CHANGES.txt').read(),
    # Author information:
    author='Attila Olah',
    author_email='attilaolah@gmail.com',
    # Package settings:
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=('ao',),
    include_package_data=True,
    zip_safe=True,
    tests_require=(
        'zope.component',
        'zope.interface',
        'zope.testing',
    ),
    extras_require={
        'test': (
            'zope.component',
            'zope.interface',
            'zope.testing',
        ),
        'docs': (
            'Sphinx',
            'z3c.recipe.sphinxdoc',
        ),
    },
    # Classifiers:
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Buildout',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
    ],
)
