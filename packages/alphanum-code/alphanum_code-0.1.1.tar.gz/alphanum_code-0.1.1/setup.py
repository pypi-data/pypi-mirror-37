from setuptools import setup, find_packages

pkg_name = "alphanum_code"
version = open("%s/VERSION" % pkg_name).read().strip()
download_url = 'https://github.com/ylaizet/%s/archive/%s.tar.gz' % (pkg_name, version)


setup(
    name = pkg_name,
    packages=find_packages(),
    version = version,
    description = 'AlphaNumeric unique consecutive code generator.',
    long_description=open('README.rst').read(),
    author = "Yec'han Laizet",
    author_email = 'y.laizet@bordeaux.unicancer.fr',
    url = 'https://github.com/ylaizet/%s' % pkg_name,
    download_url = download_url,
    include_package_data=True,
    license = "MIT",
    install_requires=[
        'SQLAlchemy'
    ],
    keywords = ['code', 'generator'],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ]
)
