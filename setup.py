from setuptools import find_packages, setup


setup(
    # Package information:
    name='ao.shorturl',
    version='1.0.0',
    license='GNU GPL',
    url='http://github.com/aatiis/ao.shorturl',
    description='Reusable url shortener and lookup library.',
    long_description='%s\n\n%s'%(
        open('README.txt').read(),
        open('CHANGES.txt').read(),
    ),
    # Author information:
    author='Attila Olah',
    author_email='attilaolah@gmail.com',
    # Package settings:
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=True,
    tests_require=(
        'zope.testing',
    ),
    extras_require={
        'test': (
            'zope.testing'
        ),
        'docs': (
            'Sphinx',
            'z3c.recipe.sphinxdoc',
        ),
    },
    # Classifiers:
    classifiers=(
        'Development Status :: 4 - Beta',
        'Framework :: Buildout',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
    ),
)
