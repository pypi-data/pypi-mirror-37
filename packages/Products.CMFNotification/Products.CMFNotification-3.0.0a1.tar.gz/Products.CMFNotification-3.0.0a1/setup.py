import os
from setuptools import find_packages
from setuptools import setup

version = '3.0.0a1'
description = open('README.rst').read().strip()
long_description = '\n\n'.join((
    open(os.path.join(
        'Products',
        'CMFNotification',
        'README.txt',
    )).read().strip(),
    open(os.path.join("CHANGES.rst")).read().strip(),
))

setup(
    name='Products.CMFNotification',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=(
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Development Status :: 5 - Production/Stable',
        'Framework :: Plone',
        'Framework :: Plone :: 5.0',
        'Framework :: Plone :: 5.1',
    ),
    keywords='CMFNotification plone notification e-mail',
    author='Pilot Systems',
    author_email='ploneorg@pilotsystems.net',
    url='http://plone.org/products/cmfnotification',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,
    install_requires=(
        'setuptools',
        'Plone >= 5.0',
    ),
    extras_require={
        'test': [
            'Products.PloneTestCase',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
