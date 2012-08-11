from setuptools import setup, find_packages

version = '0.1'

long_description = (
    open('README.txt').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(
    name='netexpe.pdf',
    version=version,
    description="Tools for the creation of pdf with reportlab",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
      "Programming Language :: Python",
      ],
    keywords='',
    author='',
    author_email='',
    url='http://svn.plone.org/svn/collective/',
    license='gpl',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['netexpe'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'reportlab==2.5',
        'pyPdf==1.13',
        'css==0.1',
    ],
    extras_require=dict(
        tests=[
            'unittest2',
        ]),
    entry_points="""
    # -*- Entry points: -*-
    """,
    )
