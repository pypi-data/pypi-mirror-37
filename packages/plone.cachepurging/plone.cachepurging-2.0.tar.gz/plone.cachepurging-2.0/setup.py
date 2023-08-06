from setuptools import setup, find_packages

version = '2.0'

setup(
    name="plone.cachepurging",
    version=version,
    description="Cache purging support for Zope 2 applications",
    long_description=(
        open("README.rst").read() + "\n" + open("CHANGES.rst").read()
    ),
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="plone cache purge",
    author="Plone Foundation",
    author_email="plone-developers@lists.sourceforge.net",
    url="https://pypi.org/project/plone.cachepurging",
    license="GPL version 2",
    packages=find_packages(),
    namespace_packages=["plone"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "five.globalrequest",
        "plone.registry",
        "requests",
        "six",
        "z3c.caching",
        "zope.annotation",
        "zope.component",
        "zope.event",
        "zope.i18nmessageid",
        "zope.interface",
        "zope.lifecycleevent",
        "zope.schema",
        "zope.testing",
        "Zope2",
    ],
    extras_require={"test": ["plone.app.testing"]},
)
