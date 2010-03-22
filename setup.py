import os

from setuptools import find_packages, setup


setup(
    # Package information:
    name='ao.shorturl',
    version='1.1.7',
    license='GNU GPL',
    url='http://github.com/aatiis/ao.shorturl',
    description='Reusable url shortener and lookup library.',
    long_description=\
        open('README.rst').read() + \
        open(os.path.join('src', 'ao', 'shorturl', 'shorturl.rst')).read() + \
        open(os.path.join('src', 'ao', 'shorturl', 'django.rst')).read() + \
        open(os.path.join('src', 'ao', 'shorturl', 'appengine.rst')).read() + \
        open('TODO.rst').read() + \
        open('CHANGES.rst').read(),
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
        'minimock',
        'zope.component',
        'zope.interface',
        'zope.testing',
    ),
    extras_require={
        'test': (
            'minimock',
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
